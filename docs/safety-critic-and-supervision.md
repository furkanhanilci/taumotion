# Learned Safety & Performance Critic — yöntem, veri, kayıplar, kabul şartları

**Güncel yayın: v1.3.1.** [Entegrasyon sözleşmesi](integration-contract-v1.3.1.md) bu belgedeki nominal ufuk, veri kapsamı ve sürüm uyumluluğunu kesinleştirir; tüm yöntemler korunur.


## Neden yeni bir critic?

Geometrik risk hesapları (minimum TTC, hedef ilerleme, şerit ihlali, eğrilik, jerk, MPC proxy) hata yapan aktör tahminlerinden veya eksik sensör görüşünden etkilenir. Tek sabit maliyet ağırlığı her şehir/senaryoda doğru sıralama üretmeyebilir. Bu nedenle **M10-C** olarak küçük, çok başlıklı güvenlik ve performans eleştirmeni eklenir. Başlangıçta fiziksel özellikleri kullanır; ayrı deneylerde **görünürlük**, **kanıt durumu**, **zamansal CoT** ve **kontrol uygulanabilirliği** katılır. Ana M10 ve M11 modülleri aynı kalır.

## Girdi ve çıktı

**Girdi:** `CandidateSet` (K×40×pose), candidate valid mask, route/ego ve sahne özellikleri, propagated actor forecasts + observation age/uncertainty-kind, grounding claim mask, previous NMPC tracking/solver feedback (yalnız geçmiş). Yalnız eğitimde bulunan oracle future/action results **asla** online girdi değildir.

**Çıktı (`SafetyScoreBundle`):** bir `candidate_id` için `p_no_collision`, `p_drivable_area`, `p_ttc_within_bound`, `p_direction_compliance`, `progress_estimate`, `comfort_estimate`, `control_feasibility_estimate`, `confidence/uncertainty`, `label_source`, `valid_mask`, `calibration_version`, `observation_timestamp` ve isteğe bağlı ranking skorları. Her risk başlığının çıktı türü, alt veri ayrımı ve kalibrasyon durumu ayrı saklanmalıdır; her sayıya otomatik olasılık denmez.

## Mimari önerisi

Fiziksel özellikler için küçük MLP; K aday karşılaştırması için paylaşılan aday kodlayıcı ve tercihen attention. İlk aşama **critic-only**: yalnız frozen aday cache üzerinde eğitim. Daha sonra küçük politikaya feature olarak bağlanır. Native pretrained scoring head, başka planlayıcının latentlerine doğrudan takılmaz; kod yapısı, skor taksonomisi ve ranking fikri yeniden kullanılır.

## Etiketler ve kayıplar

Güvenlik hedefleri sınıf/olay; ilerleme/konfor regresyon; aday karşılaştırması pairwise/listwise ranking olabilir. Aday bazlı `unsafe_high_score` hataları ayrıca izlenir. Temel alternatif:

`L = λs L_safety + λp L_progress_comfort + λr L_pairwise_rank + λcal L_calibration`.

Eğitimde oracle ground truth kullanımı yalnız label maker tarafındadır. NAVSIM sahnesinden elde edilen pseudo-simulation etiketiyle CARLA closed-loop episode sonucu eşit şey değildir; `label_protocol` ve `label_horizon_s` olmadan harmanlanmaz. Tek kaydedilmiş gelecek, farklı eylemin sonucunu doğrudan vermez; alternatiflerin skoru gerekiyorsa simulator rollout yapılır.

## Ölçümler ve ablation

1. Critic'siz heuristic / yalnız fiziksel scorer / supervised multihead scorer / +grounding / +visibility / +CoT / +MPC proxy / full.
2. ROC/PR ve class prevalence; Brier/ECE ve calibration curve (per-head); actor/occlusion/dataset grupları; `false-safe-at-threshold`, incorrect top-1 selection, unsafe-high-score ve oracle gap.
3. Aynı frozen candidate set, aynı örnek sayısı/split/compute; trained critic / policy parametre sayısı ve GPU maliyeti ayrı.
4. Eğitim sırası: `human/expert observation` -> `candidate collection` -> `source-pinned labels` -> `critic-only` -> `calibration` -> `RL feature integration` -> `closed-loop evaluation`.
5. Yol kenarı, geçiş hakkı ve zorlu TTC senaryoları ayrı risk grupları olarak raporlanır. Test setinden curriculum'a veri sızıntısı yoktur.

## FPD-Drive yöntemsel ilişki ve lisans

Öğrenilmiş çok başlıklı scoring, yanlış sıralama/score correction ve future-privileged multi-target distillation fikri için dış kaynak [FPD-Drive](https://github.com/CountNemoChan/FPD-Drive) incelenmiştir. Resmî inference, scorer, ranking ve DDIM refiner kodları vardır; **öğretmen model eğitimi kaynakta yayımlanmadığından** doğrudan hazır modül değildir. Repo Apache-2.0; bağımlılıkların/weight'lerin ayrı koşulları ve attribution kontrol edilir. Mimari çizimde jenerik ad, yöntem/kod kaynağında gerçek atıf bulunur.

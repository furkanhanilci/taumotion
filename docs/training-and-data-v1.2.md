# Çevrim dışı eğitim, görünürlük ve çoklu hedefli denetim

**Güncel yayın: v1.3.1.** [Entegrasyon sözleşmesi](integration-contract-v1.3.1.md) bu belgedeki nominal ufuk, veri kapsamı ve sürüm uyumluluğunu kesinleştirir; tüm yöntemler korunur.


## Neden uzman sürüş?

CARLA'daki güçlü bir uzman sensör öğreneninden daha fazla dünya bilgisine sahip olabilir. Bu, imitation learning için iki risk yaratır: (i) öğrencinin görmediği aktör nedeniyle expert'ın frenini nedensel olarak açıklayamaması, (ii) tek kayıtlı expert hareketinin tek doğru hedef sayılması. V1.2 bu sorunları **görünürlük etiketleri** ve **multi-target valid action set** ile ele alır. Her iki yöntem ilk aşamada yalnız eğitim/data ürünü olarak çalışır.

## Veri sözleşmesi

`ExpertEpisode`: route/seed/map/town/scenario identifiers, sensor rig, ego state, expert action, actor map (teacher-only), observation times, episode outcomes. `VisibilityEvidence`: actor ID, visible pixel counts across cameras, lidar points if permitted, occlusion_state, geometry confidence, time, offline_or_runtime_source. `TeacherTargetSet`: K adet potansiyel hareket, validity mask, quality/safety label vector, evaluation protocol, hindsight/rollout flag ve counterfactual scenario id. `TrainingSample`: **only** causal observation features + supervised targets with strict allowlist.

## Üretim akışı

1. Frozen planner-A/B, gerekirse ayrı strong baseline, uygun kayıtlı sahnelerde Native→Canonical adayları üretir; cache key model revision, source seed, history, preprocess, coordinates ve 4s/0.1s sözleşmesini içerir.
2. CARLA expert farklı route/seed/weather/occlusion senaryolarında sürüş gerçekleştirir; recorded `normal_view` ve uygun `perturbed_view` ayrı tutulur.
3. Instance segmentation + depth + varsa LiDAR'dan aktör görünürlüğü/örtülme offline etiketlenir. Teacher'ın görebildiği ve öğrenci sensörün göremediği fark açık tutulur; `UNKNOWN` otomatik `ABSENT` değildir.
4. Çoklu hedef yörüngeler, planlayıcı adayları ve/veya simülatör rollout'larıyla oluşturulur. Gelecek bilgi, only `label_builder` içinde kullanılır. Aynı log geleceğiyle farklı yol seçimlerinin sonucu uydurulmaz.
5. Grounding label'leri, SafetyScoreBundle training labels, candidate ranking labels ve temporal CoT labels oluşturulur. Her hedef `protocol/version/privilege` metadata'sı taşır.
6. *Critic-only* eğitim; risk calibration; supervised/listwise ranker; küçük PPO+residual curriculum. CVaR ancak episode hacmi ve maliyet kestirim kararlılığı yeterliyse uygulanır.
7. Closed-loop CARLA ile test; orijinal baselines native kontrolüyle ve aynı-sensör rule+NMPC ile ayrı. NAVSIM pseudo-open-loop, CARLA gerçek closed-loop ve KITScenes imitation accuracy birbirine karıştırılmaz.

## Eğitim kaynakları ve kullanım sınırları

Dış [LEAD](https://github.com/kesai-labs/lead) deposundaki CARLA expert, `occlusion.py`, `forecast_kernels.py`, `speed_planning.py`, `path_planning.py`, log reader ve dataset/cache fingerprint örnekleri veri ve expert mekanizmasını somutlaştırır. `main` (2026 yeni modular dataset/checkpoint) ve `cvpr2026` paper reproduction **birbiriyle uyumsuz** veri/checkpoint aileleridir. LEAD `main` kodu MIT; dataset ve ağırlık kullanım koşulları ayrıca incelenmeli. Expert ayrıcalıklı sim state kullanabilir; bu bilgi tau policy online girişine alınmaz. Dış code reuse tezde açık atıf, upstream license/NOTICE ile yapılır.

## Eğitim ölçekleme ve 2× A5000

LEAD'in büyük veri kümesinin tamamını başlangıçta indirmiyoruz. Pilot kontrollü route/scenario subset, verimli sensor recording ve fingerprint cache ile başlanır. Large teacher inference offline/serial çalıştırılabilir, iki 24GB GPU tek 48GB GPU değildir. Cache stale tespitinde sessizce eski etiket kullanmak yerine hata verilir. Runtime profilleri P0/P1/P2/P3 için farklı model residency ve ölçülmüş VRAM planları hazırlanır.

## Sızıntı/başarı reddi şartları

- Inference observation'da CARLA privileged actor state, geleceğe ait ground truth, future collision outcomes veya oracle risk score bulunursa **run INVALID**.
- Same benchmark test route'unun eğitimde yeniden kullanımı ayrı data-leak kontrolü ve bağımsız held-out split gerektirir.
- Policy label `teacher_generated` ise çevrim içi oracle gibi sunulmaz.
- Kayıtlı expert ile farklı karşı-olgusal eylemin gerçekleşmeyen outcome'u biliniyormuş gibi kaydedilmez.
- Varyantlar arası aynı eksenlerde compute/route/seed/observation privilege karşılaştırma matrisi bulunmadan üstünlük iddiası yoktur.

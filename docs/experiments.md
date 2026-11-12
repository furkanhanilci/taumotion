# Deney planı: korunmuş kapsam ve eklenen kontroller
## 1. Araştırma soruları
RQ1: A ve B aynı toplam K ve hesap bütçesinde birbirini tamamlıyor mu?
RQ2: Öğrenilmiş seçici, aynı aday kümesindeki heuristic/supervised/bandit seçiciden iyi mi?
RQ3: Yapılandırılmış ve çok ufuklu reasoning karar ve sürüşe katkı sağlıyor mu?
RQ4: Bağımsız kanıt ve kalibrasyon yanlış semantiğin zararını azaltıyor mu?
RQ5: CVaR yaklaşımı ortalama ödüle göre kuyruk maliyetini azaltıyor mu; ilerleme bedeli nedir?
RQ6: Kontrol uygulanabilirliği ve NMPC geri beslemesi kapalı döngüyü iyileştiriyor mu?
RQ7: NAVSIM kazanımları CARLA'ya ve farklı koşullara aktarılıyor mu?
RQ8: Qwen3.8 semantik görevinde Qwen3.5'e göre hesap maliyetine değer mi?
RQ9: Küçük horizon student hangi koşullarda teacher'a göre yararlı doğruluk/gecikme dengesi sunuyor?

Bunlar önceki RQ1–RQ9'un korunmuş karşılığıdır. İlk tez formunun S1–S3 ve insan değerlendirmesi aşağıda açıkça eklenmiştir. H1–H3 hipotezdir, elde edilmiş sonuç değildir.

## 2. Ön kayıt ve birincil sonuçlar
Her platform kendi metriğiyle değerlendirilir. NAVSIM v1.1: PDMS; v2.1.2: bu sürümün resmi EPDMS; CARLA Bench2Drive 0.0.4: Driving Score. Kritik güvenlik sonucu CARLA collision/km ve rota bazında collision-free completion olarak önceden kaydedilir. İlerleme/blocked rate birlikte verilir; durup kalmak güvenli başarı sayılmaz.

Confirmatory ana karşılaştırma C8 ile C6'dır: aynı iki üretici/aday bütçesi, aynı algı, aynı NMPC ve aynı supervisor. RQ2 için C8'in semantic/risk farkları kontrol edilerek learned-vs-heuristic alt eşlemesi yapılır. C8–C4/C5 tam sistem farkı ikincildir. Etki büyüklüğü ve güven aralığı raporlanır; keşifsel alt gruplar açık işaretlenir.

Sürüm, test rotası, hava/seed, checkpoint, quantization ve budget test başlamadan kilitlenir. Published tablolar yalnız bağlamdır; REPRODUCED kendi çalıştırılan sonuçtur; PROPOSED henüz ölçülmemiştir. Başka makalenin skoru kendi sonuç hücresine kopyalanmaz.

## 3. Korunan deney aileleri
| ID | Tasarım ve gerekli kontroller | Ana çıktı |
|---|---|---|
| E1 | Resmi loader/evaluator tekrar üretimi; NAVSIM iki sürümü ayrı; KITScenes ve CARLA adapter smoke tests | Resmi örnek uyumu, manifest ve sensor privilege |
| E2 | A:K, B:K, A:K/2+B:K/2; K=2/6/12; eşit hesap bütçesi ayrı; oracle yalnız değerlendirmede | minADE/FDE, çeşitlilik, A-only/B-only-win, both-fail, oracle gap, zaman |
| E3 | Aynı candidate cache: heuristic, supervised ranker, contextual bandit; CARLA PPO; GRU/attention ayrı ablasyon | Seçim skoru, kapalı döngü performans, eşit eğitim/kapasite maliyeti |
| E4 | No-semantic, text-only, structured single/multi-horizon, shuffled horizon, missing actor, contradictory/zeroed reasoning | Semantik katkı, hata hassasiyeti, inference maliyeti |
| E5 | Grounding yok, self-confidence, bağımsız algı, train-only oracle, calibrated gating | Claim P/R, Brier/ECE, unsupported rate, kötü semantiğin sürüş etkisi |
| E6 | Mean PPO, sabit bounded penalty, PPO-Lagrangian mean-cost, CVaR uyarlaması; ortak fallback | CVaR ve tail sayısı, collision, near-miss, progress/stall |
| E7 | No, speed-only, lateral-only, bounded joint residual; aynı adaylar | Δtraj, jerk, curvature, hata iyileşme/kötüleşme, shield override |
| E8 | Kinematik MPC vs dinamik NMPC; ufuk/dt/warmstart, hard/soft sınır, belirsizlik, düşük hız; MPC-aware top-N=1/3/6 search | Tracking RMSE, P50/P95/P99, fail/slack/saturation, realtime factor |
| E9 | Town/route/weather/traffic/occlusion/noise/dropout/ego error/friction; native Robust profili ayrı | OOD alt grup, worst-decile, gecikme ve sensör kırılganlığı |
| E10 | Sabit aday/kanıt/state ile semantik müdahale; ayrı paired environment müdahalesi | Seçim/residual/referans/komut etkisi, doğru yön, faithfulness |
| E11 | Qwen3.5 vs 3.8; FP/INT4 yalnız desteklenirse; teacher vs student | Görev doğruluğu, grounding, P95/P99, VRAM, kararlılık |
| E12 | Cache, parallel/sequential, P0/P1/P2/P3; gerçek gecikme enjeksiyonu | GPU-s/scene, kaynak ve güvenlik Pareto, decision age |
| E13 | İlk form S1/S2: görsel-only/visual+language; piksel özelliği/BEV/nesne tablosu | Aynı küçük policy kapasitesinde temsil ve dil katkısı |
| E14 | İlk form S3: aynı örnek/hesap bütçesinde tek geçiş, çeşitlendirme, yinelemeli failure toplama | Veri sürümü bazlı kapalı döngü ve OOD değişimi |
| E15 | AlpaSim/NuRec keşifsel aktarım; hazır uygun sahne/araç varlıklarıyla bridge | Girdi/çıktı uyumu, sim farkları, kanıtlanan ve erişilemeyen kısımlar |

E4'te dış semantik kanalının kapatılması üreticilerin iç dil kullanımını kaldırmaz. E13 bu nedenle iki alt katmandır: sabit üreticilerde selector temsili; desteklenen yerel kiplerde üretici visual/direct vs reasoning. Bir model yerel visual-only kip sunmuyorsa bu karşılaştırmanın desteklenmediği açık yazılır; rastgele latent sıfırlama eşdeğer baseline sayılmaz.

E15 bütün KITScenes sahnelerinin hazır NuRec rekonstrüksiyonuna sahip olduğu varsayımını içermez. Hazır varlık yoksa keşif raporu ve somut format adaptörü teslim edilir; diğer benchmarkların yerine geçirilmez.

## 4. İnsan değerlendirmesi E10-H
İlk tez formundaki kullanıcı çalışması teknik XAI testlerinden ayrı korunur. Aynı sürüş kesitleri açıklamasız, serbest kısa metin, yapılandırılmış/kanıt bağlantılı açıklama koşullarında gösterilir. Sıra karşı dengelenir; katılımcı aynı kesitin cevabını öğrenerek avantaj kazanmamalıdır. Doğru ve yanlış karar örnekleri dengeli seçilir.

Ölçümler: karar/tehlike anlama doğruluğu; cevap süresi; yanlış karara güvenme oranı; doğru karara uygun güven; öznel okunabilirlik. Araştırmacının ürettiği açıklamalar bağımsız anotatörle doğrulanır. Katılımcı sayısı pilot etki/varyansa göre belirlenir; örneğin 24–40 katılımcı bir planlama aralığıdır, güç hesabının yerine geçmez. Kurumun insan katılımcı prosedürü ve onamı veri toplamadan uygulanır; bu belge katılımcı toplamaya başlamaz.

## 5. Baseline matrisi
| ID | Yöntem | Ortam / kontrol | Raporlama notu |
|---|---|---|---|
| N0 | Constant Velocity | NAVSIM resmi | Hazır tabansal referans |
| N1 | EgoStatusMLP | NAVSIM resmi | Ego shortcut kontrolü |
| N2 | TransFuser | Uyumlu NAVSIM checkpoint | Etkin sensör girdisi kaydedilir |
| N3 | Tek flow üretici A | NAVSIM resmi | Native ve ortak 4 s ayrı |
| N4 | Tek diffusion üretici B | NAVSIM resmi | K ve sampler maliyeti |
| N5 | İkili heuristic | NAVSIM resmi | Algı/risk hesap maliyeti dahil |
| N6 | İkili learned selector | NAVSIM resmi | Supervised/bandit ayrı |
| N7 | N6 + structured CoT | NAVSIM resmi | Aynı aday kümesi |
| N8 | N7 + evidence + risk | NAVSIM resmi | Risk politikası eğitim kaynağı CARLA/uygun train düzeni |
| N9 | AutoE2E BEV+GRU | KITScenes yerel | Native girdi/ufuk; hazır kod baseline'ı |
| C0 | BasicAgent | CARLA native kontrol | Privileged tam sistem |
| C1 | BehaviorAgent | CARLA native kontrol | Privileged tam sistem |
| C2 | Traffic Manager | CARLA native kontrol | Privileged tam sistem |
| C3 | Klasik rota/engel planlayıcı | Ortak NMPC/shield | İzinli aynı algı; oracle actor yok |
| C4 | Tek A | Ortak NMPC/shield | Aynı K/hesap bütçesi tabloları |
| C5 | Tek B | Ortak NMPC/shield | Aynı koşullar |
| C6 | İkili heuristic | Ortak NMPC/shield | Ana karşılaştırma |
| C7 | İkili RL + static CoT | Ortak NMPC/shield | Ufuk/gating katkısının kontrolü |
| C8 | Tam τMOTION | Ortak NMPC/shield | Ana sistem |
| C9 | SimLingo | Önce native CARLA | Uyarlanabilirse ortak NMPC ek tablo |
| C10 | UniAD yerel planner | Önce native CARLA | Algı backend'inin planlama katkısı kıyası |

Hazır klasik rota/engel planner için mevcut CARLA navigation waypoint/route hesapları tekrar kullanılır; actor/world oracle sorguları kaldırılıp M02 girdisiyle değiştirilir. Bu artık native BasicAgent skoru değildir; C3 adaptörlü baseline'dır. Oracle erişimini kaldırmanın kod ve performans etkisi kaydedilir.

Her sonuç tablosunda sensor_rig, effective_inputs, map_privilege, controller, shield, horizon, K, compute_budget, checkpoint ve source_type bulunur. Baseline girdi farkları yalnız dipnotta kaybolmaz.

## 6. Metrikler ve istatistik
Sürüş: resmi score/success/completion; collision/km; red-light; offroad; blocked; TTC/near-miss. Plan: ADE/FDE@1/2/3/4 ortak ufuk; doğal 5 s modeller için ayrı @5; diversity ve oracle gap. Kontrol: lateral/yaw/speed RMSE, saturation, jerk, solver status/slack/deadline. Semantik: claim P/R, unsupported, Brier/ECE, intervention sensitivity ve doğru yön. Hesap: end-to-end P50/P95/P99, GPU-s/scene, VRAM peak, decision age; enerji ölçülebiliyorsa kullanılan ölçüm sınırıyla birlikte.

Bağımsız örnek birimi frame değil scene/route ailesidir. Aynı route'un tekrarları birlikte cluster bootstrap edilir. Eğitim seed'leri ile değerlendirme trafik seed'leri ayrı eksenlerdir. Küçük politika için hedef beş eğitim seed'i; önce üç seed pilot, genişleme sonradan seçilmiş en iyi seed'e dayanmadan yapılır. Resmi tam Bench2Drive seti ana testtir; geliştirme alt kümesi test sonucu yerine sunulmaz.

Ana ön kayıtlı kıyaslar için Holm düzeltmesi; çok sayıdaki keşifsel alt grup için FDR veya açık keşifsel etiket. Güven aralıkları, mutlak/bağıl etki ve örnek sayısı birlikte verilir. Sıfır gözlenen çarpışma sıfır gerçek risk demek değildir; olay sayısı ve maruziyetle uygun üst sınır raporlanır. Pratik anlamlı etki eşiği pilot sonrası test açılmadan yazılır; şu anda sonuç veya güç hesabı uydurulmaz.

## 7. XAI ve supervisor katkı ayrımı
Her run en az şu beş izi tutar: aday havuzu, seçilen ham aday, residual sonrası öneri, supervisor kabul referansı, gerçek araç kontrolü. Açıklama müdahalesi seçimi değiştirse bile shield aynı komutu üretebilir; bu durumda semantic-policy sensitivity var, executed-control etkisi yoktur.

Supervisor kritik kazancı sağlıyorsa bunu seçicinin öğrenilmiş başarısı diye yazmamak için override rate, veto nedeni, fallback süresi ve ham öneri maliyeti gösterilir. Shield-off karşılaştırması yalnız simülasyon araştırma koşuludur; ana adil tablo bütün yöntemlerde aynı shield kullanır.

## 8. Saklama ve tez çıktıları
Her run: config, source/weight hashes, split/route manifest, training seed, traffic seed, metric version, episodes, decisions, control, latency, resources, failure cases ve yeniden çalıştırma komutu. Her tablo otomatik olarak bu izden üretilir; el ile seçilmiş başarı örnekleri ana sonucu belirlemez.

Önceki T01–T12 planı korunur: model özellikleri; yöntem sınıfları; NAVSIM v1; NAVSIM v2; KITScenes; CARLA; semantik/seçim; risk; XAI; NMPC; kaynak maliyeti; Qwen sürümü. T13 görsel temsil/veri döngüsü ve T14 insan değerlendirmesi eklenir. Grafikler: oracle gap, learning curves, reliability, failure heatmap, paired CF, control time series, risk/latency Pareto.


## 9. v1.1 ek deneyleri
E16: AoI/olay farkındalıklı scheduling, native geçmiş, worker co-load ve kanıt taşıma.
E17: Tüm kontrol yolu zaman bütçesi, M22 deadline/hang/late-result deneyi; uniform/nonuniform ufuk ve SQP_RTI/AS-RTI kıyası.
E18: Sensör ve hesap karşılaştırma sınıfları; saf mimari etkisinin tanımlanabilirlik sınırı.

Bunlar E1–E15 ve E10-H kapsamını koruyan derinleştirmelerdir. Ayrıntılar [pilot-protocol.md](pilot-protocol.md) ve [evidence-policy.md](evidence-policy.md) içindedir. Bütün ana kontrollü baseline’larda M22 aynı biçimde uygulanır.

## v1.2 addendum — current specification supersedes applicable v1.1 text

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

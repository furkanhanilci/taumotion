# τMOTION — Nihai Araştırma Mimarisi / Final Architecture Specification

**Dokümantasyon sürümü: 1.3.1 · 12 Kasım 2026**  
**Mimari tasarım temeli: v1.2 sabit, 24 ana modül (M00–M23), 54 bağımlılık kaydı (52 farklı yönlü modül çifti).**  
**Akademik tanım: Explainable, Risk-Aware Hybrid End-to-End Autonomous Driving Framework.**

Bu belge τMOTION'ın *mimari referans tanımıdır*: Hangi problemi neden çözdüğümüzü, algoritmaları, eğitim ve sürüşte izin verilen verileri, her modülün girdisi/çıktısını, mimari sınırları ve bilimsel katkı tezlerini tek bir yerde açıklar. **Kullanıcının güncel önceliği mimarinin tanım olarak eksiksiz olmasıdır; çalışma zamanı entegrasyonu veya benchmark çalıştırılması bu tasarımın tamamlanma önkoşulu değildir.** Bu açıklama, test yapılmış olduğu anlamına gelmez.

**Dondurulmuş tasarım kararı:** Yeni konuşmalarda tartışılan hazır model veya yöntemlerin güçlü yönleri önceden tanımlanmışsa yeni ana modül oluşturulmaz. M05 zamansal reasoning, M11 GRU+evidence-gated coupling, M18 intervention XAI, M20 hafif BEV+GRU baseline zaten kapsamda. Mevcut M07/M08 çift üreticinin yanına üçüncü aktif planlayıcıyı zorunlu olarak eklemiyoruz. Üçüncü hafif planner yalnız opsiyonel karşılaştırma ve uygunluk halinde aday kaynağıdır.

**Onaylı logo:** `assets/brand/TAUMOTION_APPROVED_FINAL_LOGO_2026-11-12.png` dosyası, LiDAR içermeyen araç silüeti ile büyük τ işaretini birleşik biçimde taşıyan, kullanıcının son onayladığı raster görseldir. **Dosya byte-for-byte korunur.** Eski mor referans ve diğer vektör denemeleri tarihsel varlık olarak kalır; yeni görselin vektörel olduğu iddia edilmez.

## I. Bilimsel problem, konumlandırma ve sınırlar

τMOTION, kamera + ego hareketi + izin verilen navigasyon bilgisinden hareket adayları üreten öğrenilmiş planlayıcılarla; yapılandırılmış ve doğrulanabilir semantik muhakemeyi, risk tahminini, hibrit eylem uzaylı RL'yi ve fiziksel NMPC kontrolünü birleştiren **hibrit uçtan uca sürüş mimarisidir**. Görüntüden motor komutuna uzanan tüm sistem kapsanır; ancak tek sinir ağı olarak uçtan uca diferansiyellenebilir/eğitilebilir değildir. Bu nedenle *monolithic E2E* veya *fully end-to-end trainable* denmez.

Araştırmanın cevaplamak istediği sorular: (i) VLM'nin yazdığı gerekçe sahneye dayalı ve güncel mi? (ii) Söz konusu gerekçe gerçek seçimi etkiliyor mu? (iii) Birbirinden farklı iki dondurulmuş hareket üreticisinin adayları tamamlayıcı mı? (iv) Öğrenilmiş çok başlıklı safety/performance critic yanlış güvenli aday sıralamasını azaltabiliyor mu? (v) Öğrenilmiş seçim + sınırlı residual fiziksel NMPC altında daha iyi ve daha az riskli hareket üretiyor mu? (vi) Bunlar ayrıcalıklı gelecek bilgisini politika girdisine sızdırmadan yapılabiliyor mu? (vii) ağır modeller asenkronken 20 Hz kontrol çevrimi veri eskimesi/deadline yönünden nasıl korunur?

**Nihai özgünlük hipotezi**, yeni bir görsel backbone keşfetmek veya bütün temel planlayıcıları yeniden eğitmek değildir. Kanıt güvenilirliğine bağlı seçim, öğrenilmiş güvenlik eleştirmeni, risk duyarlı aday/residual RL, kontrol uygulanabilirliği geri beslemesi ve açıklamanın gerçek karar üzerindeki etkisini ölçen karşı-olgusal yöntemleri bütünleştirmektir. Her biri ablation gerektiren araştırma hipotezidir; mimariye yazılması başarının ölçüldüğü anlamına gelmez.

## II. Tek araç sürüş adımının tam çevrim içi akışı

**M00→M01 (veri yetkisi ve senkronizasyon).** Kamera görüntüleri, ego konum/yönelim/hız/ivme, direksiyon durumu, sensör zaman damgaları, kalibrasyon ve rota girdileri `SceneEnvelope` olarak birleştirilir. M00 veri kaynağının sensör-temelli inference için izinli mi yoksa yalnızca öğretmen/ödül etiketinde kullanılabilir mi olduğunu tutar. Aynı fiziksel sahne, M07/M08 gibi planlayıcıların kendi çözünürlük, kamera dizilimi, geçmiş ve koordinat beklentisine uygun ayrı preprocessing adaptörleriyle beslenir. Simülatörün diğer aktörler için bildiği oracle gelecek konumları politika durumuna eklenmez.

**M02 ve M23 (bağımsız fiziksel kanıt ve tazelik).** Ayrı algı servisi 3B aktörler, BEV/occupancy, drivable area, şerit/geometri, mümkünse trafik ışığı ve multimodal hareket tahminleri üretir. Son gerçek gözlemin `observed_at` zamanı ve confidence/uncertainty saklanır. M23 farklı hızda gelen bilgiyi karar zamanına kısa süreli kinematik/filtreleme ile taşır; türetilmiş konumu yeni gözlem diye etiketlemez. Görünmeme `UNKNOWN`, kanıtla çelişme `CONTRADICTED` değildir. Geçerli tahmin ufku aşıldığında `STALE` uygulanır.

**M03→M04→M05→M06 (semantik ve kanıt).** Büyük görsel-dil modeli çevredeki aktör, etkileşim, sürüş kuralı ve muhtemel tehlikeleri metinle açıklar; bir doğrudan direksiyon komutu üretmez. M04 `actor/relation/hazard/cause/action/rule/horizon` alanlarında yapılandırılmış iddialara dönüştürür. M05 `now,+1,+2,+3,+4s` için risk ve taktik niyet özellikleri üretir; offline VLM öğretmeninden eğitilebilecek küçük horizon student ana hesaplama optimizasyonudur. M06 iddiaları M02/M23 bağımsız kanıtları, görünürlük ve yaş bilgisiyle ilişkilendirir: `SUPPORTED`, `CONTRADICTED`, `UNKNOWN`, `CONFLICT`, `STALE`. Kalibre güven ve maskeleme M11'e aktarılır. **Bir dil modelinin kendi metni kendi doğrulaması sayılmaz.**

**M07 ve M08 (iki dondurulmuş güçlü hareket üretici).** Planlayıcı A görsel-dil / flow-matching yaklaşımıyla yaklaşık native 5s/0.1s, B diffusion yaklaşımıyla yaklaşık native 4s/0.5s yörüngeler verir; bunlar ilgili checkpoint/protokol konfigürasyonlarıdır. Temel deneyde iki modellerin ağırlıkları dondurulur. M09 başlangıç `K=3+3=6` adayı aynı başlangıç zamanı, araç frame'i ve 4s/0.1s değerlendirme grid'ine getirir. Interpolasyon yeni fiziksel forecast değildir. K=2/6/12 ve eşit hesaplama bütçesi karşılaştırmaları saklanır. Her adayın native yol noktaları, sampler seed, rig, generation_id ve validity mask'i bulunur.

**M10 (fiziksel aday özellikleri + learned multihead critic).** Önce aktör tahminleriyle çarpışmasızlık, drivable area, TTC, ilerleme, yön uygunluğu, hız/ivme/jerk, eğrilik, planlayıcı ayrışması, kanıt yaşı ve ucuz MPC feasibility proxy çıkarılır. Ardından küçük öğrenilmiş safety/performance critic `trajectory+scene+grounded evidence+control` özelliklerinden ayrı başlıklarda NC/DAC/TTC/DDC/progress/comfort/control-feasibility tahmini üretir. Bazı başlıklar kalibre olasılık, bazıları regresyon/skor olabilir: hepsini yapay olarak aynı olasılık diye yorumlamayız. Critic'in eğitimi `per-head supervised loss + ranking correction + calibration` temellidir. **Bu critic ile PPO value veya episode CVaR critic farklı işlevlerdir.** Öğrenilmiş puan fiziksel güvenlik denetiminin yerine geçmez.

**M11→M12 (risk duyarlı hibrit karar ve bounded residual).** Candidate Attention altı adayı bağlam içinde karşılaştırır; GRU kısa süreli karar sürekliliğini tutar. M05/M06 semantik katkısı görsel/aday temsiline `z_out=z_base+α g(evidence,age) P(z_reason)` ile eklenebilir; gate başlangıçta sıfıra yakın olur ve yalnız küçük politika içinde eğitilir, dondurulmuş büyük planner iç katmanına müdahale edilmez. PPO politikası ayrık aday indeksi `j` ve seçilene koşullu sekiz sürekli değer `Δv[4],Δd[4]` üretir. Başlangıç sınırları |Δv|≤2m/s, |Δd|≤0.5m; smooth interpolasyon 4s boyunca dağıtılır. Bunlar tasarım başlangıçlarıdır, her sahne için güvenlik sertifikası değildir. Eğitimde hibrit log-prob, action masking, recurrent state ve supervisor override ayrı izlenir.

**M13→M14→M22→M15 (öneri güvenliği ve fiziksel yürütme).** M13 güncel yol/aktör kısıtları, hız-eğrilik ve başlangıç durumu bakımından öneriyi kabul eder veya gerekçeli fallback üretir. M14 dinamik bisiklet modelinde `[X,Y,ψ,vx,vy,r,δ,a]` durumları ve `[δdot,jerk]` kontrolleriyle acados/CasADi tarzı Dynamic NMPC'yi kullanır. Nominal planlama ufku 4s/40×0.1s, hedef kontrol tick'i 20Hz (50ms). Solver status/slack/tracking hatası da çıkıştır. M22 bağımsız generation_id, deadline, snapshot ve veri yaşına göre geç komutu reddeder. **M15 tek araç komut yazıcısıdır**: direksiyon/gaz/fren adaptörü; RL doğrudan CAN komutu yazmaz. Bu ayrım güvenlik iddiasından çok uygulama sözleşmesidir; sistemin formal sertifikalı olduğu anlamına gelmez.

**M16/M17/M18 (zamanlama, karar izi, XAI).** Büyük VLM/perception/planner'lar farklı hızlarda asenkron çalışabilir; 20Hz yalnız nihai kontrol hedefidir. Her aşamanın scene timestamp'i, age-of-information, candidate set generation, kabul/override, gerçek kontrol ve gerçek ego hareketi M17 DecisionTrace'e kaydolur. M18 aynı sahne için `supported→unknown`, tek horizon token sıfırlama, reasoning shuffle ile **metin müdahalesi**, CARLA'da kontrollü aktör kaldırma/değiştirmeyle **dünya müdahalesi** testlerini ayrı tutar. Bir karar gerekçesinin okunaklı olması nedensel doğruluk kanıtı değildir.

**M19/M20/M21 (araştırma çevrimi).** M19 NAVSIM v1 PDMS, NAVSIM v2 EPDMS, Bench2Drive DS/SR, KITScenes ADE/FDE ve latency/VRAM/TTC/konforu protokol-seed-sensör ayrıcalığıyla değerlendirir. M20 native güçlü VLA, güçlü ayrıcalıklı uzman, AutoE2E 79.9M BEV+GRU, native klasik Autoware ve aynı-algı classical rule+NMPC baseline'larını ayırır. M21 train-only uzman kayıtları, visibility/occlusion etiketleri, future-privileged multi-target öğretmen yörüngeleri, iyi/kötü örnekler, scenario/domain transfer verisini sürümleyerek critic/selection eğitimine verir. Öğretmenin geleceği görmesi, öğrenciye çıkarımda gelecek ground truth erişimi vermez.

**Asenkron ufuk düzeltmesi:** 4s nominal ufuktur. Gecikme sonrası her kararın ortak geçerli ufku kısalır; padding tahmin sayılmaz. [v1.3.1 zaman ve veri sözleşmesi](integration-contract-v1.3.1.md) belirleyicidir.

## III. Girdi–çıktı sözleşmeleri ve görev ayrımı

Ana işleme sözleşmeleri şunlardır: `SourceManifest → SceneEnvelope → ActorEvidence/ForecastEvidence + ClaimSet/TemporalReasoning → GroundedClaim → NativeTrajectorySet(A,B) → CandidateSet → CandidateFeatureBundle/SafetyScoreBundle → PolicyProposal(j,8D residual) → AcceptedReference → ControlResult → GateDecision → steering/throttle/brake → DecisionTrace`. Bu yalnız **mantıksal bağımlılıktır**; VLM/algı/planner kolları paraleldir, tüm düğümler tek zincirde senkron 50 ms çalışmaz.

`TeacherTargetSet`, future observations, privileged actor truth, offline visibility GT, episode outcomes, calibration labels ve oracle scoring yalnız M00/M21 eğitim-denetim tarafına aittir. Runtime `PolicyObservation` içinde bulunamaz. `CandidateSet` için ortak `t0`, `0.1..4.0s` zaman noktaları, orijinal native çözünürlük, source planner, output validity, kaynak gözlem zamanı zorunludur. `GroundedClaim` için actor match, destek durumu, confidence, evidence age saklanır. `GateDecision` için accepted, reject/fallback reason, generation ve valid-until kontrol edilir.

Önemli ayrımlar: *unsafe action önerildi* ile *unsafe eylem uygulandı* ayrı raporlanır. Öğrenilmiş critic puanı, bağımsız safety supervisor'ın sert kısıtı değildir. Aynı şekilde dense horizon student, dil modelinin iç düşünce zincirini kesin temsil ediyor iddiası taşımamalıdır.

## IV. Eğitim, aktarım ve hesaplama tasarımı

**Aşama A — Dataset ve expert:** CARLA uzman sürüşü, tek ve çoklu aktör senaryoları, normal/perturbed view, kamera/ego/rota eşleme; farklı gizlilik/izin etiketleri. Simülatörde görülen ama kameraya kapalı aktörler için offline görünürlük truth üretilir. Bağımsız sensor-estimated görünürlük runtime'da ayrı tutulur.

**Aşama B — Multi-target:** Aynı sahnedeki farklı güvenli rotaların uygunluğu, insan/uzman kayıtları, candidate trajectories ve gerekli kontrollü rollout ile incelenir. Kayıtlı tek gelecek tüm karşı-olgusal adayların doğru sonucunu garanti etmez; teacher geleceği görebilir ama öğrencinin çevrim içi input'u göremez. Native sampler score ile valid rollout etiketleri karıştırılmaz.

**Aşama C — Semantik:** Büyük VLM offline öğretmen olarak yapılandırılmış claim ve ufuk etiketlerini üretir; küçük student M02'nin sensör-temelli zaman serisi ve ego/rota özelliklerinden bunları taklit edebilir. Öğretmene ait future GT label çıkarımda student'a aktarılmaz. Large VLM online ancak daha yavaş ve event-triggered kullanılabilir.

**Aşama D — Critic:** Fiziksel aday/scene/grounded evidence özelliklerinden NC/DAC/TTC/DDC/progress/comfort/control feasibility başlıkları supervised + ranking + calibration hedefleriyle öğrenilir. Data split, scene leakage ve out-of-domain calibration tutarlı tutulur.

**Aşama E — Policy:** Başlangıç heuristic/oracle-gap → supervised ranker/BC → CARLA gerçek kapalı döngü PPO; ayrık aday seçimi ve koşullu sınırlı residual ayrı logp ile optimize edilir. CVaR α=0.9/0.95 episode tail cost ve risk budget ile ele alınır; NAVSIM offline ranker'ı kapalı döngü PPO diye adlandırılmaz. Sınırlı 2×RTX A5000 24GB'lık workstation'da büyük model co-load/unload, caching ve farklı profiller değerlendirilir; 24+24GB otomatik birleşik 48GB değildir.

**Aşama F — Modeller ve kontrol:** Ağır hareket üreticileri ana tezde frozen. Dynamic NMPC için araç parametreleri ve kontrol kısıtları ayrı konfigüre edilir; solver'ın gerçek zamanlı başarısı bir hipotezdir. P0 senkron referans, P1 asenkron, P2 küçük reasoning student, P3 koşullu heavy model gibi çalışma profilleri bulunur.

## V. Model ve teknik seçimlerin mimarideki gerçek durumu

| Yöntem | Mevcut konum | Karar |
|---|---|---|
| Temporal BEV / bağımsız algı | M02 | Zaten tanımlı; AutoE2E'nin tüm backbone'u birebir buraya taşınmış denemez |
| Yapılandırılmış reasoning taxonomy | M04 | Zaten tanımlı |
| 0–4s horizon-aware reasoning head | M05 | Zaten tanımlı |
| Büyük öğretmen → küçük student | M05/M21 | Zaten tanımlı |
| Zero-initialized reasoning coupling | M11 | Zaten tanımlı; küçük karar politikasında, frozen planner içinde değil |
| Candidate Attention + GRU | M11 | Zaten tanımlı |
| Reasoning faithfulness interventions | M18 | Zaten tanımlı |
| AutoE2E hafif BEV+GRU | M20 | **Güçlü baseline**; üçüncü zorunlu online planner değil |
| Klasik Autoware Universe | M20 | Native ve same-evidence+NMPC baseline iki ayrı koşul |
| AutoE2E model benchmark | M19/M20 | KITScenes ve gerekirse native başka senaryolar |
| Öğrenilmiş multihead safety critic | M10 | v1.2'de eklendi, özgün critic eğitimi hipotezi |
| Görünürlük / teacher-only future | M00/M02/M06/M21 | v1.2'de eklendi; inferenceta future GT yok |
| Bounded 8D residual + Dynamic NMPC | M12/M14 | Korunan ana kontrol mimarisi |
| Üçüncü ağır planner / bridge refiner | M20 | Opsiyonel challenger; zorunlu omurga değil |

Yöntem/model adlarının gerekliliği teknik doküman ve atıflarda korunur, **bilimsel mimari şema kutularında özel model/kuruluş isimleri kullanılmaz**. Veriden öğrenilen hazır E2E hareket üreticilerine rağmen bütün sistem monolitik olmadığından **Hybrid End-to-End Autonomous Driving Framework** adını kullanıyoruz.

## VI. Benchmark, başarı potansiyeli ve epistemik durum

Aşağıdaki skorlar τMOTION için *kullanıcının istediği nokta beklentileri* olup gerçek deney sonucu değildir; confidence interval değillerdir. Rekabetçi güçlü sistemlerin yayımlanmış sonuçları ayrı protokollerde olabilir. Özellikle NAVSIM v1 PDMS ile NAVSIM v2 EPDMS karıştırılmaz, KITScenes eski 202-keyframe ile corrected canonical 11.035-keyframe sonuçları tek sıraya sokulmaz.

| Benchmark | τMOTION v1.2 ana nokta beklentisi | Koşullu olası aralık | İddialı iyi senaryo |
|---|---:|---:|---:|
| NAVSIM v1 PDMS (yüksek iyi) | 92.5 | 91.5–93.5 | 94–95 |
| NAVSIM v2 navhard EPDMS | 53 | 48–58 | 59–62 |
| Bench2Drive Driving Score | 82 | 75–85 | 88–92 |
| Bench2Drive Success Rate | 60% | 50–65% | 70–80% |
| KITScenes 3s ADE (düşük iyi) | 0.60 m | 0.55–0.70 m | 0.48–0.55 m |
| KITScenes 3s FDE (düşük iyi) | 1.55 m | 1.35–1.85 m | 1.15–1.35 m |

**Hedef ile beklenti ayrı:** Şimdiye dek raporlanmış güçlü planner için KITScenes 202 örnekte 0.565 ADE/1.397 FDE kaydı bulunduğundan, yeni güçlü **stretch target** `ADE≤0.565, FDE≤1.397` olarak ifade edilir. Bu yeni hedef, ana tahminin 0.60/1.55'ten otomatik ölçümle yükseldiği anlamına gelmez. Risk-aware seçim insan kaydından daha temkinli yörünge seçerek ADE'yi artırabilir; güvenlik ve hata metriği ayrı tutulur.

**Rakipler:** NAVSIM v1 yayımlanmış PDM-Closed 89.1, Qwen-Drive RL 90.7, ReCogDrive RL 90.8, HiPro-AD 92.6, FPD-Drive 94.88, FPD-Drive-Pro 95.57. NAVSIM v2 FPD 54.75, FPD-Pro 58.07. Bench2Drive v0.0.4 LEAD 95.59 DS/87.28% SR, SimLingo 86.55/70.45%, Drive-π0 69.71/45.91%; ayrı protokolde BridgeDrive 96.34±0.55/89.25±0.50. KITScenes eski 202 örnekte Qwen 0.565/1.397, AutoE2E fine-tuned 0.744/1.98; AutoE2E canonical 11.035 0.7556/2.0504. Bunlar bilimsel kıyas bağlamını sağlar, τMOTION sonucunu temsil etmez.

**Autoware kapsamı:** Klasik Autoware Universe için ortak NAVSIM/Bench2Drive yayını olmadığı için sayı uydurulmaz. Bunun yerine (1) native classical stack, (2) ortak algı ve ortak NMPC kullanan rule-based planlayıcı, (3) Autoware AutoE2E/temporal BEV+GRU karşılaştırması, (4) Autoware'in uygun olduğunda yeni learned planner modu ayrı koşullar olarak tanımlanır. Klasik Autoware ile τMOTION'ın başarısı sensör ve harita eşitliği kurularak yorumlanır. Kurallı ve iyi haritalanmış sahnelerde klasik stack daha iyi olabilir; karmaşık niyet/belirsizlik ve multi-candidate risk seçimi τMOTION'ın araştırma avantajı adayıdır.

## VII. Bir örnek kavşak olayının giriş–çıkış izleme senaryosu

Araç kavşağa 35 km/sa civarında yaklaşırken sağdan başka araç gelir ve yaya geçidinde görüşü kısmen kapalı bir yaya bulunur. M01 sensör ve ego hareketini ortak zamana getirir; M02 sağdan gelen aracı algılar ve yayanın görünürlük belirsizliğini ayrı tutar. M23 eski aktör konumunu zamanla taşırken yeni bir ölçüm olduğunu iddia etmez. M03 yol verme ve muhtemel yaya riskini açıklar; M04/M05 bunları actor–hazard–cause–action + 0–4s zaman ufuklarına çevirir; M06 aktör iddialarını fiziksel kanıtla destekler/UNKNOWN işaretler. M07/M08 farklı hız ve yanal hareket içeren altı aday üretir; M09 4s grid'de birleştirir. M10 physics features + learned critic üretir. M11 bağlam ve geçmişe göre bir adayı seçer, M12 dört hız/dört yanal knot ile küçük düzeltme yapar. M13 güncel yol/dinamik kısıtları kontrol eder; M14 NMPC direksiyon ve hız kontrolünü optimize eder. M22 gecikmiş/sahneye ait olmayan komutları reddeder; M15 yalnız geçerli komutu yazabilir. M17 bütün ham/önerilen/kabul/gerçek sonucu loglar; M18 semantik yaya özelliği müdahalesiyle gerçek dünya yaya senaryo müdahalesini karıştırmadan faithfulness test eder. Karar nihai değil; yeni gözlemle kapalı çevrim tekrarlanır.

## VIII. Mimari karar kilidi ve ileriye yönelik önerilerin yorumu

1. Bu doküman v1.2'de kararlaştırılmış 24 modüllü **nihai tasarım kapsamını korur**. v1.3 yeni çalışma zamanı modülü eklemez, bağlantı grafiğini değiştirmez.
2. Test/benchmark çalıştırılmış olması, kullanıcının istediği nihai mimari tanımının şartı değildir; tasarım dokümanları tamamlanabilir. Ancak yayımlanmış skor ve tahmin açıkça ayrı yazılır.
3. Hazır araştırmadan yöntem uyarlama ile hazır kod/weight'i doğrudan kopyalama aynı şey değildir. Kod ve checkpoint lisansları, branş/commit ve veri izinleri ayrı tutulur.
4. AutoE2E'nin M04/M05/M11/M18/M20 ve M16/M21'e yararlı yöntemleri *daha önce* tanımlanmıştır. Bu bileşenleri tekrar yeni eklemiş gibi sunmak yanlıştır.
5. Klasik Autoware, üçüncü zorunlu planlayıcı değildir; ayrı native ve same-information baseline olmalıdır.
6. Logo için en son kullanıcı onayı geçerlidir: araç silüeti ve mor/cyan τ, **araba üstünde LiDAR yok**. Orijinal raster değişmez. Eski mor logo onaylı güncel logo değil, arşiv varlığıdır.
7. Kaynak/model isimleri teknik raporda atıf olarak yer alabilir, figürün fonksiyon bloklarında jenerik bilimsel terimler kullanılır.
8. Genellikle algoritmaların kendilerini geliştirmekten çok, modüllerin girdi/çıktı sözleşmeleri ve gerekçeleri tez için yeterli spesifikasyondur; ileriki runtime sonuçları ayrı sürümlenecektir.


## v1.3.1 yayın öncesi gözden geçirme

[İnceleme raporu](prepublication-review-v1.3.1.md) ve [entegrasyon düzeltmeleri](integration-contract-v1.3.1.md), eski sürümlerdeki çelişen alanların yerini alır. Topoloji ve yöntem kapsamı korunur. Sayısal beklentiler kullanıcı tarafından saklanması istenen planlama varsayımlarıdır; bunları üreten kalibre edilmiş bir tahmin modeli veya τMOTION ölçümü yoktur.

## IX. M00–M23: her modülün bağımsız görev, girdi/çıktı ve hata sözleşmesi

Aşağıdaki 24 madde `specs/components.json` ile **doğrudan eşleşir**. Önceki ayrıntılı Türkçe `docs/components.md` ve `docs/interfaces.md` dosyaları tamamlayıcı teknik referanstır. Burada herhangi bir modülün gerekliliği veya input-output kapsamı atlanmaz.


### M00 — Kaynak ve veri ayrıcalığı kaydı

**Neden var:** Gelecek etiketlerinin veya simulator oracle bilgisinin politikaya sızmasını önler.

**Girdi:** Girdi dosyaları, sürümler, izinli sensör listesi

**Çıktı:** Çalışma manifesti ve izinli gözlem görünümü

**Hazır yöntem:** Hazır manifest ve benchmark veri yükleyicileri

**Kaynak:** NAVSIM, Bench2Drive, KITScenes

**Köprü:** Veri allowlist adaptörü; train/eval/inference süreç ayrımı

**Öğrenme:** Yok

**Hata davranışı:** İzin dışı alanı reddet; run başlatma.

**Kabul kanıtı:** Konfigürasyon ile çalışan hash'ler eşleşir; test future alanı politika sınırını geçemez.

**Deneyler:** E1

### M01 — Sahne eşzamanlama ve koordinatlar

**Neden var:** Aynı sahne iddiasını gerçek zamansal ve geometrik eşlemeye dönüştürür.

**Girdi:** Kamera geçmişi, ego, kalibrasyon, rota

**Çıktı:** SceneEnvelope; t0 ego çerçevesi; veri yaşı

**Hazır yöntem:** CARLA sensör ajanı ve hazır model preprocessing

**Kaynak:** Bench2DriveZoo/team_code/uniad_b2d_agent.py; Qwen docs/data.md; ReCogDrive features

**Köprü:** İki modelin farklı sensör ihtiyaçlarına adaptör; CARLA y-sağ → ortak y-sol

**Öğrenme:** Yok

**Hata davranışı:** Eksik kamera geçerlilik maskesi; kritik ego/kalibrasyon yoksa durma profili.

**Kabul kanıtı:** İleri/sol dönüş/geri dönüş sentetik dönüşümleri ve özgün preprocessing eşdeğerliği.

**Deneyler:** E1,E9

### M02 — Bağımsız görsel kanıt ve tahmin

**Neden var:** VLM iddialarını farklı model kaynağıyla sorgular; risk hesabına görsel dayanak sağlar.

**Girdi:** SceneEnvelope; geçmiş görüntüler; izinli rota geometrisi

**Çıktı:** ActorEvidence, MapEvidence, ForecastEvidence, VisibilityEvidence(sensor_estimated), native observed_at

**Hazır yöntem:** Hazır BEV, track, map, motion, occupancy; ROI ışık sınıflandırma

**Kaynak:** Bench2DriveZoo UniAD-Tiny 0.0.4; OpenDriveLab/UniAD; Autoware traffic_light_classifier

**Köprü:** Ara çıktılar silinmeden return_evidence kancası; ışık-şerit eşleme; backend dönüşümü

**Öğrenme:** Önce mevcut ağırlıklar; gerekiyorsa ayrı alan uyarlama deneyi

**Hata davranışı:** Kayıp aktörü yok sayma; bilinmeyen/eskimiş işaretle, ihtiyatlı sınırlar uygula.

**Kabul kanıtı:** Aktör kimliği devamlılığı; ışık rengi ayrı doğrulanır; alan bazlı kalibrasyon.

**Deneyler:** E5,E9,E13

**Korunan v1.2 eklemesi:** VisibilityEvidence: camera instance-pixel/occlusion offline labels; runtime requires independent sensor estimate and uncertainty; no CARLA actor-truth leak.

### M03 — Semantik VLM servisi

**Neden var:** Görsel bağlamı dilsel kural, niyet ve tehlike ilişkisine taşır; özgün tez S1.

**Girdi:** Görüntü, ego/rota özeti, izinli talimat

**Çıktı:** Karardan önce üretilmiş kısa açıklama, yapılandırılmış etiket adayları

**Hazır yöntem:** Mevcut multimodal inference, tokenizer ve vision preprocessing

**Kaynak:** Qwen/Qwen-Drive-1.0-4B root VLM; Qwen/Qwen3.8-27B comparison

**Köprü:** Sürüm kontrollü prompt; JSON/etiket dönüşümü; exact-request cache

**Öğrenme:** Ana büyük modeller güncellenmez

**Hata davranışı:** Gecikme/parse hatası semantik maskeyi kapatır; görsel aday hattı sürer.

**Kabul kanıtı:** Aynı istem/veriyle sürüm kıyası; yanlış öncül ve eksik nesne testleri.

**Deneyler:** E4,E11

### M04 — Yapılandırılmış CoT ve taksonomi

**Neden var:** Serbest metni tekrarlanabilir ve müdahale edilebilir politika girdisi yapar.

**Girdi:** VLM çıktısı, kanonik aktör tablosu

**Çıktı:** İddia listesi: ilişki, tehlike, neden, boylamsal/yatay/taktik eylem, kural

**Hazır yöntem:** AutoE2E reasoning taxonomy ve mevcut teacher veri işleme; offline teacher_client/prompt_builder/parquet_writer

**Kaynak:** auto_e2e/Model/model_components/reasoning/reasoning_taxonomy.py

**Köprü:** Etiketler doğrudan alınır; actor_id ve evidence_ref alanları eklenir

**Öğrenme:** Parser öğrenmez; teacher etiketleri eğitim verisidir

**Hata davranışı:** Uydurulan actor_id reddedilir; unknown etiketi kullanılır.

**Kabul kanıtı:** Taksonomi versiyonu ve bilinmeyen etiket davranışı; açıklama biçimi ile doğruluk ayrı.

**Deneyler:** E4,E5,E10

### M05 — Ufka bağlı reasoning ve küçük öğrenci

**Neden var:** Şimdiki tehlike ile gelecekteki ihtimali ayırır; teacher maliyetini deneysel azaltır.

**Girdi:** Görsel özellik, ego, teacher etiketleri veya geçmiş öğrenci temsili

**Çıktı:** 0/1/2/3/4 s semantik temsiller ve ham confidence

**Hazır yöntem:** Hazır horizon reasoning head; teacher etiket hattı

**Kaynak:** auto_e2e/Model/model_components/reasoning/horizon_reasoning_head.py

**Köprü:** Girdi projeksiyonları; student distillation ve label maskeleri

**Öğrenme:** Küçük başlık ve öğrenci öğrenilir

**Hata davranışı:** Öğrenci düşük güvenli ufku unknown döndürür; teacher çağrısı profil kuralına bağlı.

**Kabul kanıtı:** Ufuk karıştırma; teacher/student hata ve gecikmesi; confidence kalibrasyonu.

**Deneyler:** E4,E11,E12

### M06 — İddia eşleme ve güven kalibrasyonu

**Neden var:** Yanlış metnin eyleme aşırı etkisini azaltır; tek güven skoru yerine neyin bilinmediğini açıklar.

**Girdi:** ClaimSet, ActorEvidence, ufuk ve yaş

**Çıktı:** GroundedClaim + evidence age + visibility state + confidence/calibration version

**Hazır yöntem:** Hazır nesne geometrisi; sıcaklık ölçekleme/kalibrasyon yöntemleri

**Kaynak:** UniAD evidence + calibration reference

**Köprü:** Actor association; tür bazlı claim testleri; doğrulama setinde kalibrasyon

**Öğrenme:** Az parametreli kalibratör; büyük ağ yok

**Hata davranışı:** Eşleme belirsizliği unknown; destek yokluğu otomatik false değildir.

**Kabul kanıtı:** Negatif/pozitif/çelişkili örneklerde P/R, Brier, ECE ve grup hataları.

**Deneyler:** E5

**Korunan v1.2 eklemesi:** Grounding supports visibility/occlusion states; UNKNOWN ≠ absent; SUPPORT/CONTRADICTED/STALE and per-head calibration.

### M07 — Flow-matching aday üreticisi A

**Neden var:** İlk güçlü plan önerisi kaynağı; alternatif üretim mekanizması.

**Girdi:** Yerel kamera/ego geçmişi; modelin kendi prompt/latent sözleşmesi

**Çıktı:** NativeTrajectorySet A; 5 s yerel çıktı

**Hazır yöntem:** Mevcut VLM + flow plan expert + resmi ağırlıklar

**Kaynak:** QwenLM/Qwen-Drive-1.0; Qwen/Qwen-Drive-1.0-4B/planner-rl reasoning mode

**Köprü:** Seed kontrollü K üretimi; hafıza bütçesi; ham çıktı dışa aktarımı

**Öğrenme:** Ana tezde ağırlık güncellenmez

**Hata davranışı:** NaN/eksik/tazelik hatası adayı invalid yapar; sessiz yeniden isimlendirme yok.

**Kabul kanıtı:** Tek aday native forward eşdeğerliği; çok aday seed çeşitliliği ve süre.

**Deneyler:** E2,E3,E4

### M08 — Diffusion aday üreticisi B

**Neden var:** A'nın hatalarına alternatif üretici sağlar; faydası E2'de sınanır.

**Girdi:** Yerel ön kamera/ego; native backbone özellikleri

**Çıktı:** NativeTrajectorySet B; 4 s, 0.5 s yerel aralık

**Hazır yöntem:** Mevcut backbone, diffusion planner ve pretrained checkpoint

**Kaynak:** xiaomi-research/recogdrive; recogdrive_agent.py, recogdrive_features.py, recogdrive_diffusion_planner.py; ReCogDrive-VLM-2B + ReCogDrive-2B-RL

**Köprü:** Online feature/cache modu düzeltmesi; K batch; device ve belleğe alınmış görüntü adaptörü

**Öğrenme:** Ana tezde ağırlık güncellenmez

**Hata davranışı:** Geçersiz feature/cache modu run başlangıcında hata verir.

**Kabul kanıtı:** Varsayılan cache bayrakları kontrolü; tekli/batch çıktıları aynı seed ile eşdeğer.

**Deneyler:** E2,E3

### M09 — Yörünge sözleşmesi ve yeniden örnekleme

**Neden var:** Adayları fiziksel olarak aynı soruya cevap verir hale getirir.

**Girdi:** A/B native noktaları ve gerçek örnek zamanları

**Çıktı:** Ortak 4 s, 0.1 s, ego x-ileri y-sol adaylar

**Hazır yöntem:** Hazır SE(2) ve benchmark trajectory biçimleri

**Kaynak:** NAVSIM trajectory + yerel model çıktıları

**Köprü:** Heading unwrap; süreye göre enterpolasyon; native metadata korunması

**Öğrenme:** Yok

**Hata davranışı:** Ufuk yetersizse aday reddi; tahmin dışına uzatma yapılmaz.

**Kabul kanıtı:** Düz/sol/sağ örnekleri; hızın zamanda türevi; 4 s kapsam denetimi.

**Deneyler:** E1,E2,E7

### M10 — Fiziksel aday özellikleri ve öğrenilmiş güvenlik eleştirmeni

**Neden var:** Politikanın neyi seçtiğini gözlenebilir sayılarla bağlar; tüm adaylarda pahalı tam çözümü zorunlu kılmaz. Çok başlıklı öğrenilmiş critic yanlış-güvenli sıralamayı azaltma hipotezini sınar; PPO value ve CVaR cost ağı değildir.

**Girdi:** CandidateSet + ego/route/actor forecast + age + visibility + groundedCoT + past NMPC feedback

**Çıktı:** PhysicalCandidateFeatures + SafetyScoreBundle (probabilities/regressions/uncertainty; per-head masks)

**Hazır yöntem:** Hazır geometri, benchmark feature yardımcıları, kısa acados rollout; FPD-Drive checkpoint-native scorer/ranking kod yapısı; küçük critic için yeni trainer

**Kaynak:** UniAD forecasts; acados model; NAVSIM yalnız izinli geometrik parçalar; FPD-Drive multihead scoring and ranking (method/code reference only; native weights not transferable); own trainer required

**Köprü:** Özellik hesapları ve valid maskeleri; yalnız seçilen için tam NMPC; MPC-aware top-N=1/3/6 optional search experiment

**Öğrenme:** Small critic multihead + ranking + calibration, initially physical-only, then visibility/groundedCoT/control ablations

**Hata davranışı:** Tahmin ufku dışındaki risk unknown; proxy garantili feasibility sayılmaz.

**Kabul kanıtı:** Proxy/full solver uyuşmazlığı; oracle future kullanılmadığının kontrolü.; heldout Brier/ECE, false-safe-rate, candidate ranking regret, latency/VRAM, no future label leakage

**Deneyler:** E2,E3,E6,E8

**Korunan v1.2 eklemesi:** NEW trainable subcomponent M10-C Learned Safety and Performance Critic (NC,DAC,TTC,DDC,EP,comfort,MPC feasibility), calibrated head types, false-safe ranking; physical features retained.

### M11 — Risk ve kanıt koşullu öğrenilmiş seçici

**Neden var:** Hazır üreticilerin hangi durumda daha uygun olduğunu öğrenir.

**Girdi:** Candidate features + SafetyScoreBundle + GroundedClaim/visibility/age + prior control only

**Çıktı:** Aday dağılımı, seçilen j, value ve risk value; recurrent state

**Hazır yöntem:** TorchRL PPO/collectors; AutoE2E gating fikri; GRU/attention blokları

**Kaynak:** pytorch/rl, pytorch/tensordict; auto_e2e reasoning_coupling.py

**Köprü:** Küçük aday attention + GRU; gated semantic fusion; hibrit log-prob arayüzü

**Öğrenme:** Seçici/value/gate eğitilir

**Hata davranışı:** Tüm adaylar maskeli ise özel STOP dalı; boş categorical çalıştırılmaz.

**Kabul kanıtı:** Aday permütasyonu; mask log-prob; recurrent reset; eşit kapasite ablasyonları.

**Deneyler:** E3,E4,E5,E6; E19,E20,E23

**Korunan v1.2 eklemesi:** RL policy consumes separate physical features AND calibrated SafetyScoreBundle, plus semantic validity; learned M10 safety critic is not the PPO value critic.

### M12 — Sınırlı residual düzeltme

**Neden var:** Seçimle yetinmeyen yerel iyileştirme; büyük planlayıcıyı yeniden eğitmez.

**Girdi:** Seçilen aday, politika bağlamı

**Çıktı:** Hız/yatay ofset knotları ve düzeltilmiş yörünge

**Hazır yöntem:** Mevcut dağılım/optimizasyon araçları; residual RL yöntemi

**Kaynak:** Torch distributions/TensorDict; residual RL reference

**Köprü:** Aday koşullu Gaussian → tanh sınırı; pürüzsüz eğri ve başlangıç sürekliliği

**Öğrenme:** Küçük residual head eğitilir

**Hata davranışı:** Sınır/curvature ihlalinde no-residual veya güvenli denetçi kararı.

**Kabul kanıtı:** No/speed/lateral/joint kıyası; Jacobian logp; önce/sonra risk ve konfor.

**Deneyler:** E7,E8

**Korunan v1.2 eklemesi:** Retain 8D: 4 speed Δv knots + 4 lateral Δd knots; DDIM refiner is optional comparison, not merged default.

### M13 — Uygulanabilirlik denetçisi ve geri dönüş

**Neden var:** Kötü öneri ve kontrol hatasını araç komutundan önce yönetir.

**Girdi:** Düzeltilmiş öneri, dinamik engel tahmini ve veri yaşı

**Çıktı:** Kabul edilmiş referans veya denetimli yavaşlama; override reason

**Hazır yöntem:** Aynı araç sınırları; NMPC yardımcı çözümü; hazır çarpışma geometrisi

**Kaynak:** acados model + CARLA geometrisi

**Köprü:** Ortak shield; retry kuralları; slack/timeout ve eylem kaydı

**Öğrenme:** Yok

**Hata davranışı:** Önce uygulanabilir son referansın kalan kısmı; uygun değilse frenleme profili.

**Kabul kanıtı:** Bütün ana baseline'larda aynı shield; ham politika ile müdahale katkısı ayrı.

**Deneyler:** E6,E7,E8

### M14 — Dinamik NMPC

**Neden var:** Referansın fiziksel takip edilebilirliği; kullanıcı NMPC gereksinimi.

**Girdi:** Kabul edilmiş yol/hız, ego, engel modları, fizik sınırları

**Çıktı:** NMPC komutu ve status/slack; M22 üzerinden M15

**Hazır yöntem:** acados/CasADi OCP iskeleti, SQP_RTI/HPIPM, kod üretimi

**Kaynak:** acados/examples/acados_python/race_cars/acados_settings.py

**Köprü:** Araç model parametreleri, düşük hız geçişi, OCP cost/constraints

**Öğrenme:** Ağ eğitimi yok; sistem tanılama/parametre ayarı var

**Hata davranışı:** Çözücü başarısızlığı M13'e; NaN/timeout komutu uygulanmaz.

**Kabul kanıtı:** Model/aktüatör kalibrasyonu; izleme RMSE; P99 süre ve deadline ihlali. Kontrol bütçesi içinde solver/IPC/guardian ayrımı; AS-RTI/nonuniform pilot.

**Deneyler:** E8

### M15 — Araç komut adaptörü

**Neden var:** NMPC'nin SI birimlerini simulator komutlarına bağlar.

**Girdi:** M22 tarafından yetkilendirilmiş normal/fallback komutu; ego hızı ve aktüatör kalibrasyonu

**Çıktı:** Normalize steer/throttle/brake ve actuator trace

**Hazır yöntem:** CARLA VehicleControl arayüzü

**Kaynak:** CARLA 0.9.15

**Köprü:** Direksiyon işareti/limitleri; ivme-komut haritası; jerk limitli takip

**Öğrenme:** Kalibrasyon tablosu; yeni ana PID yok

**Hata davranışı:** Throttle/brake çatışmasını engelle; limit ve command age uygula.

**Kabul kanıtı:** Düz hız, dönüş, fren, sıfır hız ve yokuş testleri.

**Deneyler:** E8,E9

### M16 — Zamanlayıcı ve tazelik yönetimi

**Neden var:** Uyumsuz ortamları ve pahalı hesapları yönetir; gerçek zaman iddiasını ölçülebilir yapar.

**Girdi:** Worker request/response, wall/sim clocks, bütçe

**Çıktı:** Deadline/age, iptal/reuse kararı, P0–P3 profil izi

**Hazır yöntem:** Mevcut süreç/IPC, model worker ve simulator clock; AutoE2E speed_benchmark measurement harness adapted to workers

**Kaynak:** Python multiprocessing/shared_memory + CARLA sync

**Köprü:** Model bazlı worker; exact-key cache; gecikmiş adayın yeniden çerçevelenmesi; AoI + olay/deadline önceliği; bir bekleyen istek; VLM ağırlık servis paylaşımı

**Öğrenme:** P3 çağrı politikası ayrı deney olabilir

**Hata davranışı:** Stale çıktıyı sıfır gecikmeli gibi kullanma; geçerli fallback.

**Kabul kanıtı:** 200 ms/500 ms enjeksiyon; saat ayrımı; worker çökmesi ve bellek ölçümü.

**Deneyler:** E9,E12

### M17 — İz, sürüm ve tekrar üretim

**Neden var:** Sonuçların hangi model ve müdahaleden geldiğini gösterir.

**Girdi:** Bütün ara kararlar, sim/duvar zamanları, ağırlık ve veri sürümleri

**Çıktı:** Episode/decision/control traces ve deney manifesti

**Hazır yöntem:** Resmi benchmark logları + mevcut Python/Parquet/JSON araçları

**Kaynak:** Benchmark run manifestleri; model commitleri

**Köprü:** Hash bağlantıları, packet lineage, ham/uygulanan ayrımı

**Öğrenme:** Yok

**Hata davranışı:** Eksik kritik iz run'ı incomplete işaretler; skor yine saklanır.

**Kabul kanıtı:** Tek kararın sensörden komuta tüm zinciri; checkpoint/preprocess hash eşleme.

**Deneyler:** E1–E15

**Korunan v1.2 eklemesi:** Versioned expert, teacher, candidate and critic caches; fingerprint includes rig, preprocess, model, split, label protocol and calibration version.

### M18 — Karşıolgusal ve insan odaklı XAI

**Neden var:** Güzel görünen açıklama ile karar üzerinde doğru etkisi olan açıklamayı ayırır.

**Girdi:** Sabit candidate/evidence/state snapshot; eşlenmiş sahneler

**Çıktı:** Metin→seçim/düzeltme→komut etkisi; doğru yön; insan anlama puanı

**Hazır yöntem:** AutoE2E faithfulness müdahale iskeleti; CARLA senaryo araçları

**Kaynak:** auto_e2e/Model/evaluation/faithfulness.py; Bench2Drive scenarios

**Köprü:** Hafıza/RNG snapshot restore; kontrollü metin ve ortam müdahaleleri

**Öğrenme:** Değerlendirme; yeni açıklama modeli zorunlu değil

**Hata davranışı:** Tek sahne değişimiyle saf metin nedenselliği iddia edilmez.

**Kabul kanıtı:** Beklenen yönü kör anotasyon; correctness ve sensitivity ayrı; insan güven kalibrasyonu.

**Deneyler:** E10,E10-H

### M19 — Benchmark ve istatistik

**Neden var:** İddiaları adil ve tekrarlanabilir karşılaştırmaya çevirir.

**Girdi:** Kilitlemiş split, rota/seed, run çıktıları

**Çıktı:** Sürüm ayrı skor tabloları, CI, tail ve kaynak maliyeti

**Hazır yöntem:** Resmi metrik/eval entrypoint; cluster bootstrap

**Kaynak:** NAVSIM v1.1/v2.1.2; Bench2Drive 0.0.4; Robust; KITScenes

**Köprü:** Birleşik sonuç şeması; frame yerine scene/route kümeleri

**Öğrenme:** Yok

**Hata davranışı:** Kısmi/başarısız koşu açık raporlanır; cherry-pick yok.

**Kabul kanıtı:** Resmi örnek uyumu, veri ayrımı, çoklu kıyas kontrolü.

**Deneyler:** E1–E15

### M20 — Hazır baseline uyumluluk katmanı

**Neden var:** Kazancın güçlü baselinelara ve kontrol farkına göre yorumlanmasını sağlar.

**Girdi:** Her baseline'ın yerel girdisi veya ortak gözlem sözleşmesi

**Çıktı:** Yerel tam sistem ve ortak NMPC plan sonuçları

**Hazır yöntem:** CV/EgoStatus/TransFuser/AutoE2E/SimLingo ve klasik ajanlar; AutoE2E control_rollout acceleration/curvature integration

**Kaynak:** NAVSIM; auto_e2e; simlingo; CARLA agents

**Köprü:** Sadece çıktı adaptörü; ayrı privilege/sensor/control sütunları

**Öğrenme:** Hazır checkpoint varsa kullan; zorunlu küçük baseline eğitimini kaydet

**Hata davranışı:** Uyumsuz checkpoint için sonuç uydurma; uyarlama kalemini açık tut.

**Kabul kanıtı:** N0–N9 ve C0–C8 korunur; native ve standardized skor ayrılır.

**Deneyler:** E1,E3,E8; E21,E22,E24

**Korunan v1.2 eklemesi:** Add expert native privileged baseline, same-evidence rule+NMPC, strong independent FPD-Drive-Pro benchmark, optional diffusion-bridge baseline; all sensor/privilege/benchmark version differences logged.

### M21 — Alan aktarımı ve veri döngüsü

**Neden var:** İlk tez veri çeşitliliği sorusunu ve platformlar arası genellemeyi korur.

**Girdi:** Bölünmüş veri/senaryo; train failure örnekleri

**Çıktı:** ExpertEpisode, VisibilityEvidence(offline), TeacherTargetSet, cache fingerprints, held-out split manifests

**Hazır yöntem:** Hazır dataset loaders, scenario generation ve AlpaSim altyapısı; AutoE2E alpasim_driver plugin/parser/calibration export

**Kaynak:** KITScenes; NAVSIM; Bench2Drive-Robust; NVlabs/alpasim; LEAD data/expert/occlusion workflow; FPD-Drive future-policy distillation *idea*; BridgeDrive optional training comparison

**Köprü:** Rig/route adapters; DAgger-benzeri küçük politika veri toplama; keşifsel AlpaSim bridge

**Öğrenme:** Küçük politika/öğrenci; büyük üreticiler ana protokolde sabit

**Hata davranışı:** Test senaryosunu curriculum'e katma; uyumsuz rig'i missing olarak kaydet.

**Kabul kanıtı:** Her tur veri lineage; aynı bütçede çeşitlilik kıyası; sim backend ayrı rapor.

**Deneyler:** E9,E13,E14,E15; E20,E21,E22

**Korunan v1.2 eklemesi:** Offline expert episode generation, normal/perturbed sensor views, privileged teacher and visibility labels, multi-target valid-action labels; online student cannot see oracle future.

### M22 — Bağımsız deadline guardian ve komut kapısı

**Neden var:** Solver veya model beklediğinde araç komut hattının da beklemesini önler; 50 ms bütün kontrol yoluna aittir.

**Girdi:** NMPC sonuçları, generation/deadline, ego ve kanıt yaşı, worker heartbeat

**Çıktı:** Zamanında kabul edilen komut veya kayıtlı fallback kararı; M15 tek yazıcı

**Hazır yöntem:** CARLA komut arayüzü; Autoware command-gate/heartbeat tasarım kalıbı; ROS backend seçilirse hazır node

**Kaynak:** CARLA 0.9.15; Autoware vehicle_cmd_gate resmi belge; native CARLA için yeni ince köprü

**Köprü:** Blocking solver çağrısından ayrı process; late-result rejection, epoch kontrolü, sınırlı recovery

**Öğrenme:** Yok

**Hata davranışı:** Geçerli kalan kontrol dizisi koşullu kullanılabilir; aksi halde kalibre durma profili. Güvenli durma garantisi değildir.

**Kabul kanıtı:** Worker hang/late/wrong-epoch altında zamanında komut; normal/fallback katkısı ayrı; hard-real-time kanıtı iddia edilmez.

**Deneyler:** E8,E9,E16,E17

### M23 — Zaman farkındalıklı kanıt taşıma

**Neden var:** Ağır algı ile 20 Hz kontrol arasındaki zaman farkını açık modeller; yeni gözlem üretmiş gibi davranmaz.

**Girdi:** M02 aktör izi, konum/hız, doğal tahmin modları, zaman ve kalibrasyon

**Çıktı:** Güncel zamana taşınmış kanıt; original capture time, prediction flag, yaş ve belirsizlik

**Hazır yöntem:** UniAD native forecast zamanları; FilterPy Kalman predict/update

**Kaynak:** rlabbe/filterpy 1.4.5 / 582885dd9e01c2784a5786b02fb527b46f090370

**Köprü:** Değişken dt F/Q; kalibre P veya uncalibrated error envelope; stale/unknown yönetimi

**Öğrenme:** Kalibrasyon parametreleri; yeni büyük model yok

**Hata davranışı:** Yeni aktör keşfedemez; ışık durumunu tahminle taze göstermez; süre sınırında degraded/fallback.

**Kabul kanıtı:** Zaman taşıma ve tazelik alanları; predict-only koşulda observation time değişmez; coverage/error ölçülür.

**Deneyler:** E5,E9,E16


## X. Kaynaklar, arayüzler ve referans şemaları

- Mevcut 54 bağlantı `specs/architecture_edges.json` içinde tutulur; v1.3 güncellemesi bu listeyi değiştirmez.
- Ayrıntılı paket tipleri `docs/interfaces.md` ve `docs/interfaces-v1.2-addendum.md`; zaman sözleşmesi `docs/runtime-contract.md`.
- Kritik güvenlik eleştirmeni `docs/safety-critic-and-supervision.md`; uzman, çoklu hedef ve görünürlük denetimi `docs/training-and-data-v1.2.md`.
- Matematiksel RL/CVaR/NMPC temelleri `docs/methods.md`; denemeler `docs/experiments.md` ve `docs/experiments-v1.2-addendum.md`.
- Kaynak kodların gerçek adları/branch/commit bilgileri `docs/reuse-register-v1.2.md` ve `specs/source_pins.json`.
- Türkçe/İngilizce 8 düzenlenebilir ana figür `assets/diagrams/v1_2/` içinde. Mimari bloklarında harici araştırma proje isimleri yazılmaz.
- Son kararlar `docs/revisions-v1.3.md`, `history/` ve `docs/benchmark-expectations-v1.3.md` içinde kronolojik kaydedilir.

**Kapsam özeti:** Tek belge, temel bilimsel gerekçe + sürüş akışı + çevrim dışı eğitim + 24 modülün tüm sözleşmeleri + AutoE2E/Autoware yerleşimleri + adlandırma + tahminler + marka kararı içerir. Bu bir yöntem tasarım belgesidir; ölçülmemiş performansı gerçekleşmiş gibi sunmaz.

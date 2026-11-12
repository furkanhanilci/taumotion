# Bileşen kataloğu — 24 bileşen

Architecture Specification v1.3.1. Etkin alanlar v1.2 genişlemelerini içerir. Runtime: NOT_RUN.

## M00 — Kaynak ve veri ayrıcalığı kaydı

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

## M01 — Sahne eşzamanlama ve koordinatlar

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

## M02 — Bağımsız görsel kanıt ve tahmin

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

## M03 — Semantik VLM servisi

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

## M04 — Yapılandırılmış CoT ve taksonomi

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

## M05 — Ufka bağlı reasoning ve küçük öğrenci

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

## M06 — İddia eşleme ve güven kalibrasyonu

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

## M07 — Flow-matching aday üreticisi A

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

## M08 — Diffusion aday üreticisi B

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

## M09 — Yörünge sözleşmesi ve yeniden örnekleme

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

## M10 — Fiziksel aday özellikleri ve öğrenilmiş güvenlik eleştirmeni

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

## M11 — Risk ve kanıt koşullu öğrenilmiş seçici

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

## M12 — Sınırlı residual düzeltme

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

## M13 — Uygulanabilirlik denetçisi ve geri dönüş

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

## M14 — Dinamik NMPC

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

## M15 — Araç komut adaptörü

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

## M16 — Zamanlayıcı ve tazelik yönetimi

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

## M17 — İz, sürüm ve tekrar üretim

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

## M18 — Karşıolgusal ve insan odaklı XAI

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

## M19 — Benchmark ve istatistik

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

## M20 — Hazır baseline uyumluluk katmanı

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

## M21 — Alan aktarımı ve veri döngüsü

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

## M22 — Bağımsız deadline guardian ve komut kapısı

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

## M23 — Zaman farkındalıklı kanıt taşıma

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


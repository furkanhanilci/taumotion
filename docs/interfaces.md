# Ortak sözleşmeler ve entegrasyon köprüleri — v1.1

**Güncel yayın: v1.3.1.** [Entegrasyon sözleşmesi](integration-contract-v1.3.1.md) bu belgedeki nominal ufuk, veri kapsamı ve sürüm uyumluluğunu kesinleştirir; tüm yöntemler korunur.

M00–M21 sözleşmeleri korunur. Ek M22/M23 ve zaman kuralları [runtime-contract.md](runtime-contract.md) içinde tanımlanır.
## 1. Sözleşme ilkesi
Modellerin iç katmanlarını birbirine bağlamak yerine sürümlü veri paketleri kullanılır. Büyük tensorler paylaşımlı bellekte; metadata JSON/MessagePack biçiminde taşınabilir. Bir worker'ın Python nesnesi başka ortamda pickle ile açılmaz. Her worker kendi bağımlılıklarını ve CUDA bağlamını taşır.

Ortak zarf alanları: schema_version, packet_id, episode_id, scene_id, frame_id, t_capture_sim_s, t_submit_wall_ns, t_finish_wall_ns, source_id, checkpoint_sha256, preprocess_sha256, input_packet_ids, privilege, valid_mask, native_frame. Eğitime ait etiket paketleri farklı süreç ve depoda tutulur. İnference alanları allowlist ile seçilir; yalnız yasak alan isimlerini silmek yeterli değildir.

Süreler SI birimleridir: metre, saniye, radyan, m/s. Ortak ego çerçevesi x ileri, y sol, z yukarı, pozitif yaw sola dönüştür. CARLA'nın y ekseni/heading işareti model kütüphanesine göre açıkça çevrilir. Kamera extrinsic'i ve ego/global dönüşümü ayrı tutulur. Simülasyon zamanı, fiziksel gecikme ve duvar zamanı üç ayrı niceliktir.

## 2. Paket türleri
| Paket | Zorunlu içerik | Geçerlilik koşulu | Tüketici |
|---|---|---|---|
| SceneEnvelope | Kamera kimliği ve görüntü referansı; her kare zamanı; intrinsics/extrinsics; ego geçmişi; izinli rota | İstenen geçmiş ve kalibrasyon; eksikler açık | M02,M03,M07,M08 |
| ActorEvidence | track_id; sınıf; kutu/konum; kaynak frame; skor; görünürlük; association confidence | Tahmin ile gözlem ayrılır; kalibrasyon sürümü | M06,M10,M13 |
| ForecastEvidence | track_id; mode_id; olasılık; doğal örnek zamanları; konumlar; uncertainty_kind | Olasılık toplamı ve zamanlar; kovaryans bilinmiyorsa null | M06,M10,M14 |
| ClaimSet | claim_id; actor_ref; relation/hazard/cause/action/rule; horizon_s; source_text_span | Bilinmeyen aktör/etiket maskeli; karar öncesi üretilmiş | M06,M11,M18 |
| GroundedClaim | claim_id; status; support_score; evidence_refs; age; forecast_flag | UNKNOWN ile false ayrılır; kalibrasyon id'si | M11,M18 |
| NativeTrajectorySet | planner_id; candidate_id; seed; native_times; x/y/yaw; native_frame | NaN yok, zamanlar artan, checkpoint kayıtlı | M09 |
| CandidateSet | t=0.1…4.0 s için 40 pose; source_times; source_resolution; valid mask; native_ref | Aynı t0 ve çerçeve; yerel kapsama dışı uzatma yok | M10–M12 |
| PolicyProposal | seçilen j; pre-squash residual; bounded residual; logp; hidden_state_id; behavior_version | Train'de örneklenen eylem aynen kaydedilir | M13,learner |
| AcceptedReference | kabul edilen yörünge; override flag/reason; parent_proposal | Ham önerinin izi kaybolmaz; remaining horizon yeterli | M14 |
| ControlResult | komut, solver status, slack, izleme hatası, generation, deadline, actuator saturation | M22 kabul etmeden M15'e uygulanmaz | M22,M11,M17 |
| PropagatedEvidence | original_capture_time, propagated_to, native_forecast_ref, uncertainty_kind | Taşıma kaynak gözlem zamanını değiştirmez | M06,M10,M13,M14,M22 |
| GateDecision | episode/generation, accepted_command, fallback_reason, selected_at, valid_until | Tek yazıcı M15; geç/yanlış generation reddi | M15,M17 |
| DecisionTrace | bütün packet id'leri, candidate mask, ham/residual/kabul/uygulanan iz | Tek episode/clock lineage; veri ayrıcalığı sütunu | M18,M19 |

Bu belge sözleşme spesifikasyonudur. components.json ve örnek paket tam bir üretim JSON Schema veya sürüş API uygulaması değildir.

## 3. Köprü kataloğu ve kabul testleri
**B01 — Sensör rig adaptörü (M01):** resmi model preprocessing fonksiyonlarını çağırır. Aynı fiziksel rig sağlamak modellerin aynı etkin girdiyi kullandığı anlamına gelmez. A'nın üç kamera geçmişi ile B'nin tek kamera tüketimi ayrı metadata'da görünür. Eksik görüntüyü siyah doldurma yalnız açık missing-camera deneyi olabilir; normal örnek gibi sayılmaz. Kabul: kaynak pipeline ile tensor eşdeğerliği ve renk/ölçek/kırpma kontrolü.

**B02 — Online feature adaptörü (M08):** ReCogDrive'ın dosya/cache odaklı özellik akışını çevrimiçi görüntü ve açık cihaz seçimiyle çalıştırır. İncelenen varsayılan cache bayrakları, backbone'un hangi koşulda kurulduğu ile birlikte kontrol edilmelidir. Kabul: tek kayıt dosyadan ve bellekten işlendiğinde aynı özellik/çıktı toleransı; cache açık/kapalı ve cold-start testleri.

**B03 — K aday üretimi (M07,M08):** görüntü/backbone hesaplarını mümkün olduğunda bir kez yapar; latent/embedding kopyalarını bağımsız seed'lerle örnekler. Örnekleyici adımları modelin kendi implementation'ında kalır. Kabul: K=1 native eşdeğerliği, K batch/loop kıyası, aynı seed tekrar üretimi ve gerçek GPU-saniye ölçümü.

**B04 — Kanıt dışa aktarımı (M02):** UniAD forward_test içinde ara çıktılar temizlenmeden ihtiyaç duyulan track/map/motion/occupancy değerleri ayrılır. Yeni parametre eklenmez; ana modelin sonuçları değiştirilmez. Etkinleştirilebilir return_evidence bayrağı ve detach edilmiş tensorler kullanılır. Kabul: bayrak kapalı/açık yerel planlama ve algı çıktıları eşit; bellek maliyeti ölçülü. Modelin planlama çıktısı ana havuza eklenmez.

**B05 — Işık kuralı (M02,M06):** hazır ROI sınıflandırıcısının renk/unknown çıktısını kanonik light_id ve ilgili şerit/stopline ile birleştirir. HSV hazır referans; mevcut CNN dalı karşılaştırmadır. Kabul: kırmızı/sarı/yeşil, arkadan görülen ışık ve kavşaktaki ilgisiz ışık testleri. Algılanan lambanın doğru şeride ait olmaması false grounding üretmemeli.

**B06 — İddia-kanıt (M04–M06):** metnin aktör referansını konumsal/görsel eşlemeyle track_id'ye taşır. Nesne yokluğu ancak yeterli kapsama ve görünürlükte çelişki olabilir. Gelecekte geçiş yapacak aktör iddiası için forecast uyumluluğu kullanılır, kesin doğruluk etiketi üretilmez. Kabul: çelişen ve örtülen nesnelerin farklı statü alması.

**B07 — Yörünge ve residual (M09,M12):** native noktalar saklanır; heading unwrap edilir; başlangıç t=0 ego durumu olarak eklenebilir fakat tahmin diye sayılmaz. Ortak grid enterpolasyonunda kendiliğinden yeni viraj/ivme üretilmemesi kontrol edilir. Düzeltme knotları aynı referans eğrisine uygulanır. Kabul: düz/daire/sert fren örnekleri, hız/ivme/jerk sınırları ve koordinat roundtrip.

**B08 — Hibrit politika (M11,M12):** TorchRL veri toplama ve PPO kaybını tekrar kullanır. Seçilmiş aday koşullu residual dağılımı eklenir; kategorik ve sürekli log-olasılıkları tek eylem için toplanır. Hazır bağımsız dağılım bileşimi, koşullu modelin yerine otomatik geçmez. Kabul: logp/entropy şekilleri, maskeler, tanh Jacobian ve recurrent episode reset.

**B09 — NMPC ve aktüatör (M13–M15):** acados OCP kurulumunu mevcut araç modeli ve ortak referansla bağlar. Benchmark'ın yerel PID'si ana hattın içine gizlenmez. Fiziksel ivme/direksiyon modelinden normalize CARLA komutlarına kalibre edilmiş dönüşüm vardır. Kabul: doygunluk, brake/throttle ayrımı ve dur-kalk izleme.

**B10 — Saat ve cache (M16):** anahtar; model/weight/preprocess/prompt/sampling sürümü, tüm input hash'leri, scene/frame ve RNG seed içerir. Offline kayıt cache'i farklı online sahnede kullanılamaz. Kabul: tek kamera veya prompt değişince miss; gecikmiş eski sonuç yeni request'i ezemez.

**B11 — XAI müdahalesi (M18):** adaylar, kanıt, recurrent state, RNG ve solver warmstart snapshot'ı kaydedilir. Tek kanal değiştirilir; eşlenmiş koşu sonrası bütün state geri yüklenir. Kabul: no-op müdahalesinde deterministik eşdeğerlik; etki ve doğru davranış yönünün ayrı raporu.

**B12 — Benchmark/alan (M19–M21):** resmi değerlendiricinin giriş/çıkış adaptörü; veri/rota/seed split ve privilege etiketleri. NAVSIM değerlendirme ground truth'u learner etiketi üretebilir fakat inference özelliğine geri akmaz. Kabul: resmi örnek skor ve test seti sızıntı kontrolü.

## 4. Gecikmiş çıktının kullanımı
Geçmiş t0 anında üretilen planın noktaları güncel ego çerçevesine SE(2) dönüşümüyle taşınır; geçmiş zaman dilimi atılır. Böylece yalnız koordinat ve zaman düzeltilmiş olur. Aktörlerin niyet değişikliği veya yeni engel bu işlemle düzelmez; güncel kanıtla yeniden uygulanabilirlik kontrolü gerekir.

Önerilen başlangıç sınırları: semantik için 0.5 s, aday için 0.5 s azami yaş; kalan referans ufku en az 2 s. Bunlar güvenli olduğu kanıtlanmış sabitler değildir; E9/E12 içinde taranacak tasarım değerleridir. Tazelik operasyonel saatle hesaplanır. P0'ın bekletilen simülasyonunda duvar gecikmesi yine kaydedilir; P1/P2 değerlendirmesinde gecikme simülasyona açıkça enjekte edilir.

## 5. Ortam ayrıştırması
İlave hazır köprüler: AutoE2E control_rollout, N9'un ivme/eğrilik çıktısını kendi native dinamiğiyle yörüngeye çevirir; ana dinamik NMPC'nin yerine kullanılmaz. AutoE2E alpasim_driver içindeki parser, calibration export ve BaseTrajectoryModel giriş noktası E15 için başlangıç adaptörüdür. τMOTION'a gereken değişiklik bu giriş/çıkış sözleşmesini iki üretici ve seçici servisine yönlendirmektir.

AutoE2E öğretmen istemindeki clip_horizons gelecekteki kareleri içerebilir. Bu yalnız eğitim hedefi üretiminde kullanılır. Çevrimiçi M03 servisi geçmiş/şimdiki karelerle çalışan ayrı causal request kullanır; training teacher_client doğrudan araca taşınmaz. Öğrencinin geleceğe ilişkin hedef etiketi görmesi ile inference sırasında gelecek görüntüyü görmesi ayrılır.

AutoE2E speed_benchmark ölçüm iskeleti worker'lara uyarlanır. Dummy tek-model forward süresi, bütün sistem latency'sinin yerine yazılmaz. PyTorch allocated/reserved değerleri allocator belleğidir; toplam süreç/GPU tüketimi ayrıca NVML ile ölçülür. GPU zamanlaması synchronize/event kurallarıyla, IPC ve kuyruk bekleme duvar saatiyle kaydedilir.

env-perception: B2DZoo'nun eski Python/MMCV dünyası. env-planner-a ve env-planner-b: her modelin resmi ortamı. env-policy: TorchRL'nin uyumlu modern Python/PyTorch sürümü. env-control: acados generated solver. env-eval-v1 ve env-eval-v2: NAVSIM sürümleri ayrı.

Bunlar altı GPU gerektirmez; süreç ile GPU sayısı farklıdır. Worker yerleşimi 2×A5000 üzerinde ölçülür; modelleri aynı anda bellekte tutmak zorunlu değildir. Konteyner veya ayrı environment seçimi rutin uygulama kararıdır. Tek CUDA driver ile kullanılan runtime sürümlerinin uyumu kurulum kapısında sınanır.

## v1.2 addendum — current specification supersedes applicable v1.1 text

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

# Çok frekanslı çalışma ve kontrol zaman sözleşmesi

**Güncel yayın: v1.3.1.** [Entegrasyon sözleşmesi](integration-contract-v1.3.1.md) bu belgedeki nominal ufuk, veri kapsamı ve sürüm uyumluluğunu kesinleştirir; tüm yöntemler korunur.

Architecture Specification v1.1 · Durum: tasarım; hedef donanımda doğrulanmadı.

## 1. Eklenen yöntemler ve sınırları
M16 zamanlayıcı artık yalnız worker sırası tutmaz: bilginin yaşı (Age of Information, AoI), deadline, olay tetikleyicisi, GPU yerleşimi ve kuyruk politikasını yönetir. M22 bağımsız komut gözetmeni, model veya NMPC worker'ının beklemesi halinde kontrol çıkışının da beklemesini engellemek için tasarlanmıştır. M23 hafif kanıt taşıma adaptörü, mevcut aktör izlerini güncel zamana taşır. Algı, iki üretici ve NMPC korunur.

AoI araştırmaları, görevlerin bitiş süresi kadar kararın dayandığı sensör zamanının da önemli olduğunu gösterir. Buradaki politika, bu fikirden türetilen ölçülebilir bir tasarım önerisidir; yayımlanmış zamanlayıcının birebir uygulaması veya teorik garantisinin aktarılması değildir. [AoI-centric scheduling](https://wkui.github.io/AoI_centric_scheduling-ADS.pdf), [2025 ROS 2 uygulaması](https://ieeexplore.ieee.org/document/11044491/)

## 2. Saatler ve bilgi yaşı
Bütün süreçlerde clock_domain açık olmalıdır. Duvar süresi için monotonic clock; simülasyon için simulator timestamp; gecikme enjeksiyonu için ayrıca belirlenmiş mantıksal operasyon zamanı kullanılır. Farklı saat alanları doğrudan birbirinden çıkarılmaz.

Bir çıktının güncelliği, tamamlandığı zamandan değil dayandığı en son gözlemden hesaplanır:
age_current = t_decision − t_latest_observation.
Buna ek olarak history_span ve current_sensor_skew tutulur. Bir modelin bilerek kullandığı 1.5 saniyelik geçmiş, güncel görüntüsü eskiymiş gibi değerlendirilmez. Makaledeki tüm veri soyunu kapsayan AoI ile bizim güncel gözlem yaşı ölçümüzün farkı raporlanır.

Kararda kullanılan kamera, ego, harita, track ve semantik paketlerin zamanları ayrı görünür. Tek ortalama yaş, eski bir kritik ışık durumunu gizleyemez. Eski sonucun koordinatını taşımak, onun kaynak zamanını yenilemez.

## 3. Çalışma profilleri
P0: teacher ve iki üreticiyle senkron araştırma referansı. Simülasyon model yanıtını bekleyebilir; duvar süresi ölçülür.
P1: teacher ve iki üreticiyle asenkron servisler. Model yanıtları yalnız geçerli zaman/sahne için kullanılır.
P2: dış semantik teacher yerine öğrenci; iki üretici ve bağımsız algı aynı kapsamda.
P3: bütçeye göre koşullu üretici çağrısı; model erişilebilirliği ve adayların yaşları açık girdidir.

Pilot frekans taraması: algı 2.5/5/10 Hz; her üretici 1/2/5 Hz; semantik 0.5/1/2 Hz; kanıt taşıma ve kontrol 20 Hz. Bunlar başarılmış hızlar veya güvenli alt sınırlar değildir. Native temporal modelin beklediği görüntü dizisi korunur. Worker'ı seyrek çağırmak ile gereken geçmiş kareleri seyrek kaydetmek aynı işlem değildir.

Seçilen saha/hız/örtülme koşuluna göre izinli yaş ölçümle belirlenir. v1.0'daki 0.5 s semantik/aday sınırı yalnız pilot tarama değeridir; yayınlanmış çalışma garantisi değildir. Kanıt yaşlanırken yeni gözlem yoksa belirsizlik artar; sınır aşımında mod düşürülür.

## 4. Kuyruk ve kaynak yönetimi
Her pahalı worker için bekleyen istek kapasitesi bir: çalışan isteğe ek olarak yalnız en yeni henüz başlamamış istek saklanır. Eski bekleyen istek yenisiyle değiştirilir; FIFO birikimi oluşmaz. Bu kural canlı sürüş içindir; offline veri üretimi kayıpsız batch kuyruğu kullanabilir.

Her istekte generation_id, episode_id, observation_id, requested_deadline ve model_version vardır. Tamamlanan yanıt, yeni episode veya daha yeni generation'ın durumunu ezemez. Mantıksal iptal, çalışan CUDA kernel'ini fiziksel olarak kesmek anlamına gelmez; iptal edilen işin gerçek maliyeti loglanır.

Başlangıç karşılaştırmaları: sabit periyodik sıra, earliest-deadline-first ve AoI/olay farkındalıklı sıra. Önerilen deterministik öncelik: normalize edilmiş gözlem yaşı + olay aciliyeti + deadline yakınlığı; hesap maliyeti yalnız profillenmiş kaynak kabulünde kullanılır. Öncelik ağırlıkları train pilotunda kilitlenir. İkinci bir büyük RL zamanlayıcısı eğitmek zorunlu değildir.

Yeni aktör, ışık değişimi, rota değişikliği, yüksek üretici ayrışması ve düşük grounding güveni yeniden hesaplama tetikleyebilir. Tek olayın çağrı fırtınası yaratmaması için minimum çağrı aralığı ve token bütçesi vardır. Kritik veri yenilenemiyorsa bütçeyi aşmak yerine M22'ye degraded durum bildirilir.

Birlikte çalışma maliyeti tek-model sürelerinin toplamından tahmin edilmez. GPU0/GPU1 üzerinde model çiftleri ve tam yerleşim ölçülür; CARLA renderer, CPU hazırlığı, IPC ve model yükleme de kapsanır. Ağırlık belleği, KV/ara aktivasyon, CUDA context ve simulator belleği ayrı ölçülür. İki GPU belleği tek birleşik havuz sayılmaz.

M03 ve M07 aynı VLM ağırlıklarını kullandığında aynı native model servisinin iki endpoint'i olabilir. Böylece gereksiz ikinci kopya önlenir. Farklı prompt veya görüntü dizilerinde KV cache paylaşımı garanti edilmez. ReCogDrive'ın kendi backbone'u ayrıca maliyetlidir.

## 5. M23: hafif kanıt taşıma
M02'nin son geçerli aktör kimliği, konumu, hızı ve zaman damgası alınır. Mevcut multimodal forecast varsa kendi zaman dizisi üzerinde güncel ana yeniden referanslanır; model ufku dışına aynı tahmin uzatılmaz.

Kısa algı boşluklarında sabit hızlı Kalman predict adımı için hazır FilterPy kullanılabilir. F(Δt) ve Q(Δt) gerçek geçen süreyle kurulmalıdır. P başlangıcı validation hata kestiriminden gelir; detector confidence doğrudan kovaryansa çevrilmez. Doğrulanmış kovaryans yoksa uncertainty_kind=uncalibrated ve ayrı muhafazakâr hata zarfı tutulur. [FilterPy 1.4.5 predict/update](https://github.com/rlabbe/filterpy/blob/582885dd9e01c2784a5786b02fb527b46f090370/filterpy/kalman/kalman_filter.py)

Taşınmış track yeni algı değildir. Yeni beliren/örtülmeden çıkan aktörler bu işlemle keşfedilemez. Işık rengi sabit hız modeliyle ilerletilmez; yaşlanınca UNKNOWN olur. Yaş sınırı aşımında track sessizce silinip “yol boş” denmez. Bu adaptörün kazancı E16'da, yanlış güven üretme riski E5/E9'da ölçülür.

## 6. 50 ms kontrol çevrimi
20 Hz hedefi, kritik kontrol yolunun tamamına 50 ms verir:
T_snapshot + T_reference_check + T_NMPC_feedback + T_command_gate + T_publish + T_jitter ≤ 50 ms.

Pahalı VLM/algı inference'ı bu yolun dışında asenkron çalışır. Ancak çıktı yaşları kritik yolda denetlenir. Örnek pilot bütçe: snapshot+kontrol 4 ms, NMPC feedback 32 ms, komut kapısı+yayın 4 ms, jitter payı 10 ms. Bu dağılım yalnız tasarım denemesidir; ölçülmüş süre veya hard-real-time kanıtı değildir.

NMPC hazırlık fazı ayrıca ölçülür ve kaynak bütçesine dahildir. Hazırlanmış QP'nin model, engel ve durum sürümü güncel feedback ile eşleşmelidir. Hazırlığı gizleyip yalnız feedback süresiyle sistem hızlı ilan edilmez.

## 7. M22: bağımsız deadline guardian
Gözetmen ayrı süreç/iş parçacığı mimarisiyle tasarlanır; NMPC worker'ının blocking çağrısını beklemez. Tek araç komutu yazıcısı M15'tir; M22 hangi komutun M15'e gideceğini belirler. Normal yol M14 → M22 → M15'tir. M13 referansın fiziksel uygunluğunu, M22 zaman/worker/komut geçerliliğini yönetir.

Bir kontrol tick'i için:
1. Geçerli ego ve kanıt snapshot'ını al; generation_id üret.
2. Normal NMPC işini yayınla; gözetmen kendi deadline'ını izlemeyi sürdürsün.
3. Süresinde gelen ve durum/kısıt denetiminden geçen komutu kabul et.
4. Deadline dolduysa gecikmiş yanıtı reddet; yeni tick'i eski sonuçla ezme.
5. Önceki çözümün kalan kontrol dizisi ancak güncel durum, tazelik, yaş ve kısıt denetimi geçerliyse kullanılabilir.
6. Bu koşullar yoksa kalibre edilmiş durma/azaltma profiline geç; yeni solver sonucunu bekleme.
7. Worker yeniden başlatılırsa epoch/generation değiştir; eski shared-memory sonuçları geçersiz kıl.

Fren komutu üretilebilmesi güvenli durmanın ispatı değildir. Yeni görünmeyen engel, düşük sürtünme veya ego hatası müdahaleyi başarısız yapabilir. “Güvenli” etiketi yerine fallback nedeni ve sonucu kaydedilir. NMPC normal ana kontrolcü olarak kalır.

Hazır Autoware command gate, komut seçimi ve heartbeat davranışı için kaynak/isteğe bağlı ROS backend'idir. Ana CARLA yolu yalnız bu işlevleri gerektiren ince bir gözetmen köprüsüdür; bütün Autoware stack'i zorunlu bağımlılık yapılmaz. Kodun doğrudan alınması ile tasarım kalıbından yararlanılması BOM'da ayrıdır. [Autoware command gate](https://autowarefoundation.github.io/autoware_universe/main/control/autoware_vehicle_cmd_gate/)

## 8. Mod geçişleri
NORMAL: yaş, worker ve komut kontrolleri geçerli.
DEGRADED_SEMANTIC: semantik eski/çelişkili; görsel seçim sürer, durum policy'ye verilir.
DEGRADED_EVIDENCE: algı yaşlanmış; tahmin zarfı ve hız kısıtı uygulanır, geçerlilik biterse fallback.
CONTROL_DEADLINE_MISS: solver geç; M22 geçerli kalan komut veya durma profili seçer.
STOP_HOLD: düşük hızda durma tutulur; geçerli veri ve belirlenen sayıda başarılı kontrol tick'i olmadan NORMAL'e dönülmez.

Recovery hysteresis pilotta belirlenir. Bir geçerli paket gelişi, tüm hata geçmişini silmez. E16/E17 testleri; worker hang, eski yanıt, yanlış generation, kamera kaybı ve yoğun GPU çekişmesini kapsar.

## v1.2 addendum — current specification supersedes applicable v1.1 text

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

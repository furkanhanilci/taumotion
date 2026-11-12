# Architecture Specification v1.1 — hazır parçalar ve açık sözleşmeler

**Güncel yayın: v1.3.1.** [Entegrasyon sözleşmesi](integration-contract-v1.3.1.md) bu belgedeki nominal ufuk, veri kapsamı ve sürüm uyumluluğunu kesinleştirir; tüm yöntemler korunur.

Bu belge tanımlanmış tasarımdır. R1–R5 runtime doğrulaması henüz yapılmadı. v1.1 zamanlama, kontrol bütçesi ve doğrulama kuralları [çalışma sözleşmesinde](runtime-contract.md), gerekçeleri [revizyon araştırmasında](revisions-v1.1.md) yer alır.
## 1. Amaç ve tarafsız değerlendirme
Bu tezin amacı, görsel ve dilsel bağlamın kapalı döngü sürüşe katkısını hazır güçlü modellerin üzerinde araştırmaktır. Hedef yalnız iyi bir sürüş skoru değildir: iki üreticinin ne zaman birbirini tamamladığı, semantik gerekçelerin ne zaman yardımcı veya zararlı olduğu, küçük bir politikanın bu bilgiyle nasıl seçim yaptığı ve seçimin araç tarafından uygulanabilir olup olmadığı birlikte ölçülür.

Son mimarinin güçlü yanı planlama, açıklama ve kontrolü tek deney düzeninde ilişkilendirmesidir. Zayıf yanı ise çok sayıda büyük modelin birbirine kendiliğinden uyumlu olmamasıdır. Hazır kod kullanmak temel model eğitimi ihtiyacını azaltır; sensör, koordinat, zaman, checkpoint, bellek ve veri ayrıcalığı uyumsuzluklarını ortadan kaldırmaz. Bu yüzden v1.1'ın ana revizyonu daha fazla büyük model eklemek değil, var olan parçaların sınırlarını kesinleştirmektir.

Mimari bilimsel açıdan savunulabilir; başarı, gerçek zamanlılık veya yenilik düzeyi henüz kanıtlanmış değildir. İki güçlü modelin birleşmesi tek başına özgün katkı sayılmaz. Katkı adayları; iddia ve ufuk bazlı kanıt koşullaması, aynı aday kümesinde risk ve kontrol farkındalığıyla seçim/düzeltme, ve öneriden uygulanan komuta kadar açıklama etkisinin izlenmesidir. Bunlar pozitif veya negatif sonuçlarıyla sınanacaktır.

## 2. Üç katmanlı yeniden kullanım ilkesi
**Hazır motorlar:** Qwen-Drive planlama hattı, ReCogDrive planlama hattı, UniAD algı/tahmin, Autoware ışık sınıflandırma, AutoE2E reasoning parçaları, TorchRL PPO altyapısı, acados/CasADi NMPC çözücüsü ve resmi benchmark değerlendiricileri.

**Entegrasyon köprüleri:** sensör ve zaman adaptörleri; aday biçim normalizasyonu; kanıt dışa aktarımı; iddia-aktör eşleme; süreçler arası veri aktarımı; NMPC referansı ve araç komut dönüşümü. Bunlar yeni bir algı veya optimizasyon motoru değildir.

**Küçük araştırma katmanı:** aday attention + GRU seçicisi, aday koşullu sınırlı residual, kanıtla koşullanan reasoning projeksiyonu, CVaR güncellemesi ve deney müdahale kancaları. Eğitim bu katmanda ve küçük öğrenci modelde yoğunlaşır. Büyük iki üreticinin ağırlıkları ana deneyde değişmez.

Aynı işlevi hazır bir bileşen sağlıyorsa yeniden yazma kararı alınmaz. İstisna, ihtiyaç duyulan sözleşmeyi mevcut API'nin verememesidir; o durumda değişiklik ince bir adaptör veya açıkça kayıtlı küçük yama olur. Üçüncü taraf depoları kopyalayarak tek dev ortam yaratmak yerine commit ile bağımlılık olarak tutmak tercih edilir.

## 3. Çalışma akışı
1. M00–M01 aynı gözlem kesitini, geçmişi, kameraları, ego durumunu, izin verilen rota bilgisini ve kalibrasyonu oluşturur. Her veri kendi zaman damgasını korur.
2. M02'nin bağımsız model hattı BEV/aktör/takip/harita/hareket tahmini üretir. M23 bu kanıtı kaynak zamanını koruyarak güncel zamana taşır. Trafik ışığı rengi ayrı ROI sınıflandırıcısından gelir; eski renk UNKNOWN olur. Algı çıktısı ile gerçek dünya eş tutulmaz.
3. M03–M05 semantik VLM, yapılandırılmış gerekçe ve beş ufuklu temsili üretir. Öğrenci, aynı sözleşmenin düşük gecikmeli araştırma alternatifidir.
4. M06 her semantik iddiayı nesne/harita kanıtı ile eşler; destek, çelişki, bilinmeme ve eskime durumunu ayırır.
5. M07 ve M08 aynı gözlem geçmişinden farklı yöntemlerle adaylar üretir. M09 bunları ortak ego çerçevesine ve dört saniyelik değerlendirme ufkuna getirir.
6. M10 adayların rota ilerlemesi, tahmini çarpışma, rahatlık, ayrışma ve kontrol uygulanabilirliği özelliklerini çıkarır.
7. M11–M12 aday seçer ve sınırlı bir hız/yatay düzeltme önerir. Semantik kanal burada kanıt kalitesiyle koşullanır; doğrulanmamış metin kesin güvenlik kuralı olamaz.
8. M13 önerinin fiziksel uygunluğunu kontrol eder. M14 NMPC sonucu, bağımsız M22 deadline/komut denetiminden geçerek tek araç komutu yazıcısı M15'e gider. M22 geçersiz veya geciken komutta solver'ı beklemeden kayıtlı fallback seçer.
9. NMPC durum kodu, slack, izleme hatası ve müdahale nedeni bir sonraki politika girdisine döner. M17 bütün aşamaları kaydeder. M18 açıklama etkisini, M19 karşılaştırmaları değerlendirir.

M16 zamanlama ve tazelik yönetimi tüm çevrimi kapsar; AoI, deadline, olay önceliği ve bir bekleyen istek kuralı uygulanır. M20 baseline adaptörlerini; M21 veri, platform ve alan aktarımını yönetir. M22 ve M23 yeni köprülerdir. UniAD'nin kendi planlama başlığı ana aday havuzuna üçüncü üretici olarak eklenmez; ayrı baseline olarak korunur.

## 4. Algı ve kanıt revizyonu
Kaynak bağımsızlığı için semantik VLM'den farklı ağırlıkları ve hata mekanizması olan bir kanıt hattı seçildi. CARLA tarafındaki ana aday, Bench2DriveZoo'nun 0.0.4 uyumlu UniAD-Tiny hattıdır. Hazır algı/takip/tahmin modülleri kullanılır; yeni BEV ağı eğitmek başlangıç gereği değildir. Orijinal UniAD backend'i uyumlu gerçek veri deneylerine ayrıdır. Her veri kümesinde sensör uyumu ve alan kayması ayrıca sınanır.

Bağımsızlık istatistiksel hata bağımsızlığı demek değildir: aynı kameraları kullanan iki sistem aynı karanlık/örtülme koşulunda yanılabilir. Ortak hata oranı, aydınlık ve mesafe alt gruplarında raporlanır. Kanıt modeli de emin değilse sonuç UNKNOWN olur. Gelecek aktör hareketi bir tahmindir; gelecekteki gerçek konumu biliniyormuş gibi semantik doğrulama yapılmaz.

Trafik ışığı kutusunu bulmak, rengini ve hangi şeridi yönettiğini bulmakla aynı değildir. Bu nedenle hazır ışık sınıflandırıcısı ve geometrik ışık-şerit eşlemesi eklenmiştir. Harita/rota yalnız protokolün izin verdiği geometriyi verir; simulator API'sindeki güncel ışık durumu adil ana deneyde kullanılmaz.

## 5. Semantik ve planlayıcı ilişkisi
Somut başlangıç ağırlıkları: semantik servis için Qwen/Qwen-Drive-1.0-4B deposunun sürüşe uyarlanmış Qwen3.5 tabanlı VLM'si; A için aynı deponun planner-rl başlığı reasoning kipinde; B için owl10/ReCogDrive-VLM-2B ve ReCogDrive-2B-RL. A'nın planner-sft başlığı direct/reasoning ablasyonuna ayrılır. Qwen3.5 burada genel temel modelin herhangi bir boyutu anlamına gelmez. Ağırlık deposu seçilmiştir; indirilen revision ve dosya hash'leri G0'da kilitlenecektir.

Qwen3.5 ana semantik referanstır; Qwen3.8-27B aynı görev ve kaynak bütçesi altında karşılaştırılır. Daha iyi bulunması halinde değişen parça dış semantik servis olur. Mevcut planlayıcının iç VLM'sini farklı modelle değiştirip aynı latent uzayını varsaymak bu mimarinin bir parçası değildir.

Qwen-Drive kendi planlama akışında gerekçe ve VLM ara temsili kullanır. Aynı checkpoint, prompt, gözlem, token dizisi ve işlem hattı gerçekten ortaksa bu iş bir defa hesaplanabilir. Ayrı yapılandırılmış açıklama isteği veya farklı görüntü kümesi için otomatik cache paylaşımı varsayılmaz. ReCogDrive kendi backbone ve özellik biçimini korur. Ortak dil modeli zorlamak yerine ortak çıktı sözleşmesi kurulur.

Metin, karar verilmeden önce üretilmiş kısa, yapılandırılmış bir gerekçedir. Sonradan üretilen açıklama kullanıcıya sunulabilir fakat kararın nedeni olarak kanıt sayılmaz. Serbest metin saklanabilir; politika girdisi sınırlı etiketler, aktör ilişkileri, ufuklar ve güven özellikleridir. CoT etiketi gizli iç muhakemenin eksiksiz kaydı anlamına gelmez.

## 6. İki planlayıcı ve ufuk
Ana karşılaştırmada toplam altı aday: A'dan üç, B'den üç. K=2,6,12 taraması ve aynı toplam K / aynı hesap bütçesi tabloları ayrı tutulur. Rastgelelik ve örnekleme tohumları adayın kaydına bağlanır.

A'nın yerel beş saniyelik çıktısı ve B'nin yerel dört saniyelik çıktısı korunur. Birlikte sıralanan adaylar dört saniyeye kırpılır; 0.1 saniyelik ortak örnekleme enterpolasyondur, yeni model tahmini değildir. B'nin 0.5 saniyelik yerel çözünürlüğü metadata'da kalır. Beş saniye isteyen bağımsız KITScenes/ADE tablolarında yalnız doğal olarak beş saniye sunan yöntemler değerlendirilir; ana ortak karşılaştırma 1/2/3/4 saniyedir. Beşinci saniye uydurulmaz.

Adayların birbirine benzemesi, ikinci üreticinin kapsamdan çıkmasına yol açmaz. Tamamlayıcılığın düşük olması E2'nin negatif bulgusudur; conditional invocation deneyi böyle durumlarda kaynak tasarrufunun sınırını gösterir.

## 7. Seçim, düzeltme ve kontrol
Küçük politika adayları permütasyonla uyumlu attention pooling ile işler; GRU önceki karar/kontrol geri beslemesini taşır. Maskelenen adaylar yalnız gözlenebilir fiziksel/sözleşmesel nedenlerle elenir. Algoritma adı ve öğrenilen işlev ayrıdır: PPO bir güncelleme yöntemi, GRU bir bellek, attention adaylar arası etkileşimdir. Hiçbiri gerekçesiz dekoratif modül değildir; her biri ablasyona sahiptir.

Residual, doğrudan direksiyon komutu yerine adayın hız ve yatay ofset profilini değiştirir. Başlangıç noktası/başlangıç hareketi sürekliliği ve sınırlar korunur. Yeni eğrinin uygulanabilirliği tekrar kontrol edilir. M13 ve NMPC aynı sınırları kullanır; ikisi birbiriyle çelişen ayrı araç fizik modelleri yaratmaz.

NMPC gerçek ana kontrolcüdür. acados çözüm altyapısı ve hazır yarış aracı örneğinin OCP kurulum iskeleti tekrar kullanılır. Araç modeli, lastik/aktüatör parametreleri ve CARLA komut eşlemesi entegrasyon işidir. Sistem, bir yarış aracı örneğini indirince doğrulanmış otonom sürüş kontrolcüsü haline gelmez. Ana kontrol çıktısı ile baseline'ın yerel PID'si farklı değerlendirme tablolarında açıkça belirtilir.

## 8. Donanım ve çalışma profilleri
İki A5000 için VRAM uygunluğu model boyutu, dtype, context, görüntü sayısı ve aynı anda tutulan worker'larla ölçülecektir. Toplam bellek toplanıp tek GPU belleği gibi varsayılmaz.

P0 araştırma referansı: senkron simülasyon, iki planlayıcı ve teacher; GPU'larda ardışık veya yerleşime göre paralel çalışma. Simülasyon bekleyebilir; bu profil gerçek zaman iddiası taşımaz.

P1 asenkron teacher: farklı hızlarda çalışan servisler, sabit kontrol çevrimi, tazelik sınırları ve gecikmiş kararların taşınması/reddi. İki planlayıcı etkin kalır.

P2 öğrenci: dış semantik servisin yerine küçük öğrenci; aynı iki planlayıcı, aynı kanıt ve NMPC. Bu bir sıkıştırma karşılaştırmasıdır.

P3 koşullu çağrı: bir üreticinin ne zaman çağrılacağını bütçe politikası belirler; önceki aday yalnız hâlâ geçerli kalan ufuk ve sahne için kullanılır. Tam mimari referansı P0/P1'dir. P3 performansı iki üreticinin her adımda hazır olduğu modelin skoru gibi sunulmaz.

Resmi CARLA/Bench2Drive profili 0.05 s simülasyon adımı ve 20 Hz komut güncellemesi üzerinden tanımlanır. 50 Hz deney istenirse 0.02 s kullanan özel bir kontrol deneyi olarak etiketlenir; resmi benchmark ayarları sessizce değiştirilmez. [CARLA senkronizasyon belgesi](https://carla.readthedocs.io/en/0.9.15/adv_synchrony_timestep/)

## 9. Spesifikasyonun statüsü
v1.1 şu kararları sabitler: hangi işlevlerin olduğu, hangi hazır parçalardan alınacağı, aralarındaki sözleşme, öğrenilen katmanın sorumluluğu, deney soruları ve kabul kanıtları. Kaynak commit'leri inceleme temelidir. İndirilmemiş checkpoint hash'leri, ölçülmemiş gecikmeler, risk bütçeleri ve araç parametreleri boş/başlangıç değeri olarak kalır. Bunları uydurarak doldurmak tasarımı daha final yapmaz.

Uyumluluk kapısında sorun çıkarsa işlev korunur; aynı işlevi sağlayan backend veya adaptör revize edilir ve karar kaydına yazılır. Eğitim sırası ile bilimsel kapsam birbirinden ayrıdır.

## v1.2 addendum — current specification supersedes applicable v1.1 text

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

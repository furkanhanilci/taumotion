# v1.3 yayın öncesi ayrıntılı değerlendirme

**12 Kasım 2026 · Sonuç: ana mimari korunabilir; belge ve entegrasyon sözleşmelerinde düzeltmeler gerekliydi.** v1.3.1, kullanıcının sağladığı v1.3 klasörü üzerine inceleme revizyonudur. Kaynak klasör değiştirilmedi. 24 modül, iki ana frozen üretici, bütün deneyler ve onaylı logo korunur.

## Mimari değerlendirme

Hazır iki üreticiyi ortak aday sözleşmesinde buluşturup küçük risk politikasını ve fiziksel kontrolü ayrı tutmak, kullanıcının hazır uygulamalardan parçaları birleştirme hedefine uygundur. Yeni M10 critic; fiziksel risk, veri yaşı ve grounding bilgisinin seçimde işe yarayıp yaramadığını araştırılabilir hale getirir. Visibility/multi-target eklemeleri de tek uzman eylemini tek doğru kabul etme problemini ele alır. Bunlar korunması gereken araştırma işlevleridir.

Ancak sistemin yararı modül sayısından çıkmaz. İki planner aynı sahnede benzer hatalar yapabilir; aday havuzunda uygulanabilir hareket yoksa seçici bunu düzeltemeyebilir; küçük residual her yanlış manevrayı onaramaz. Bağımsız algı ayrı model kaynağıdır, istatistiksel bağımsız hata garantisi değildir. Critic yanlış güvenli sıralama üretebilir. Bu nedenle oracle-gap, fixed-candidate, sensor/compute ve shared-controller karşılaştırmaları ana bilimsel kanıttır.

İşin önemli kısmı hazır inference'i yeniden yazmak değil; timestamp, rig, coordinate, latent, label ve actuator sözleşmelerini doğru bağlamaktır. Bununla birlikte M10 eğiticisi, actor-claim grounding, hybrid recurrent action ve CVaR uyarlaması yalnız kablo bağlantısı değildir; küçük fakat gerçek yeni yazılım/eğitim gerektirir. Hazır kaynak, uyarlanan kod, yalnız yöntem ilhamı ve yeni köprü ayrımı [yeniden kullanım kaydında](reuse-register-v1.2.md) tutulur.

## İncelemede bulunanlar ve yapılan düzeltmeler

| Bulgu | Etki | v1.3.1 düzeltmesi |
|---|---|---|
| M10 ana JSON alanları eski öğrenmesiz tanım; yeni critic yalnız ek alanlarda | Master katalog/CSV yanlış eğitim sorumluluğu gösterebiliyor | Etkin alanlar birleştirildi; eski alanlar tarihçede; katalog ve master aynı JSON'dan üretildi |
| Offline cache/teacher yollarının bazıları ONLINE_OR_EVAL | Gelecek etiketlerinin canlı politika verisi sanılma riski | Offline scope düzeltildi; ağırlık dağıtımı ile teacher payload ayrıldı |
| 54 edge ifadesi farklı payload'lı yinelenen çiftleri sayıyor | Grafik karmaşıklığı yanlış yorumlanabilir | 54 kayıt / 52 yönlü çift açıklandı; hiçbir kayıt silinmedi |
| 4s nominal grid ile gecikince kısalan plan arasındaki kural eksik | Padding veya extrapolation yeni forecast sanılabilir | Ortak geçerli ufuk, time mask, maliyet normalizasyonu ve fallback sözleşmesi eklendi |
| NC/TTC/DDC çıktılarının türü yeterince kesin değil | Native metric skoru kalibre olay olasılığı sanılabilir | Per-head hedef/protokol/horizon/calibration alanları ve no-at-fault ayrımı eklendi |
| LEAD leaderboard satırı bir yerde privileged expert olarak etiketlenmiş | Sensör/bilgi ayrıcalığı kıyası bozulur | Yayımlanmış yöntem satırı olarak düzeltildi; privileged expert ayrı baseline |
| LEAD modern main ile BridgeDrive eski adaptasyonları | Checkpoint/veri/environment uyumsuzluğu | Ayrı native environment ve revision köprüsü açıklandı |
| Sayısal τ tahminleri çok kesin görünebiliyor | Ölçüm yokken güvenilir başarı beklentisi izlenimi | Kullanıcının istediği sayılar korundu; öznel senaryo varsayımı ve empirik dayanak yokluğu açıklandı |
| PDF kod bloklarını 135 karakterde kesiyor, bağlantıları kaldırıyor | Sözleşme içeriği kaybolabiliyor | Yeni builder tam satırları sarıyor ve kaynak bağlantılarını koruyor |
| CI eski v1.2 denetleyicisini çağırıyor; logo/eski rapor başlıkları dağınık | Güncel sürüm denetlenmeden PASS algısı | Güncel portable doğrulayıcı, etkin olmayan CI şablonu, güncel rapor ve onaylı logo hash'i; geçmiş dokümanlar işaretli |
| Full-module figürü seçili bağlantılar çiziyor | 54 kaydın tümünü gösterdiği sanılabilir | Görsel overview açıklaması; tam 54 kayıt ayrıca otomatik Mermaid grafiği |

**Akademik adlandırma:** Hybrid End-to-End, hazır E2E üreticilerin kullanıldığı hibrit sistemi adlandırır. Kamera→aktüatör kapsamı tek başına uçtan uca öğrenme kanıtı değildir; birleşik diferansiyellenebilir eğitim iddiası kullanılmaz.

## İlk beş eleştiriye nihai yanıt

1. **Hesaplama:** 2×A5000 uygunluğu açık deney sorusudur. P0–P3, co-load, bounded queue, AoI ve farklı frekanslar korunur. P0 simülasyonunun bekleyebilmesi gerçek zaman kanıtı değildir.
2. **Sensör eşitliği:** Native A/B girişleri farklıdır. Aynı sahne aynı bilgi anlamına gelmez. Mimari, sensor access ve compute etkileri ayrılmalıdır; uyumsuz camera masking adil eğitim eşitliği sağlamaz.
3. **Eğitim maliyeti:** Offline cache/critic/ranker → küçük closed-loop PPO → residual/CVaR pilotu → tam deneyler korunur. CVaR kuyruk örnekleri ve quantile/CI kararlılığı ayrı raporlanır; tek adım critic skoru episode tail cost değildir.
4. **NMPC:** Ana kontrolcü kalır. Warm-start, kısa/nonuniform horizon, solver ayarları ve AS-RTI karşılaştırması vardır. 50ms tüm kritik yolundur; M22 blocking solver'ı beklemez.
5. **Olgunluk:** Bu teslim Architecture Specification v1.3.1'dir. D0 doküman kontrolleri model inference, adapter parity, sürüş veya gerçek zaman kanıtı sayılmaz; R1–R9 NOT_RUN kalır.

## Araştırma kapsamının korunması

RQ1–RQ9, ek RQ10/RQ11; E1–E24 ve E10-H; N0–N9, C0–C10; visual-vs-language, görsel temsil, veri çeşitliliği ve iteratif toplama, insan XAI, öğrenci, robust testler ve keşifsel AlpaSim/NuRec devam eder. Tam AutoE2E ve klasik Autoware native baseline'ları, same-evidence rule+NMPC, privileged expert, FPD ve BridgeDrive challenger'ları korunur. Üçüncü online ağır planner zorunlu yapılmadı.

**“Final”in anlamı:** Bu sürüm uygulamaya başlanabilecek referans tasarımıdır. Hız, checkpoint eşdeğerliği, ODD yaş sınırları, araç parametreleri ve başarı sonuçları ileride ölçülüp sürümlenir. Bunların ölçülmemiş oluşu gizlenmez; mevcut mimari yayınının tamamlanması için eğitim koşulması gerekmez.

## Yayın paketi

README genişletildi; onaylı τ + LiDAR'sız araç PNG aynen kullanıldı; güncel üç vektör figür, önceki sekiz iki dilli şema ve tam bağımlılık grafiği erişilebilir. Özgün ZIP ve birebir sohbetler yerelde korunur; Git bilimsel dokümanları ve karar özetlerini taşır. [Yayın sınırı](repository-publication.md), [logo kararı](brand-approved-v1.3.md), [belge kontrolü](../reports/documentation_checks.json).

**Yayın yetkisi notu:** GitHub deposu oluşturuldu; ilk push aktif workflow dosyasını yazma kapsamı olmayan OAuth kimliği nedeniyle reddedildi. CI tanımı tools/ci/validate-docs.yml konumunda etkin olmayan şablona taşındı. Mimari yayını bu izinle yapılabilir; otomatik Actions çalışması iddia edilmez.

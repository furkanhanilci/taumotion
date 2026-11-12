# Entegrasyon sözleşmesi — v1.3.1

12 Kasım 2026. Bu ek, v1.2/v1.3 yöntem kapsamını korur ve aşağıdaki uygulama belirsizliklerini çözer. Çalışır runtime veya doğrulanmış güvenlik iddiası değildir.

## 1. Nominal ufuk ve asenkron kalan ufuk

**4 saniye / 40 nokta nominal karşılaştırma sözleşmesidir.** Kaynak zamanı `t_i` olan adayın son geçerli mutlak zamanı `t_i + H_i` olur. Karar zamanı `t_d` için kalan kapsam `H_remaining_i = t_i + H_i - t_d`. Koordinat dönüşümü bu son zamanı uzatmaz. Örneğin 4s üreten B adayının 0.3s gecikmesi kaldığında yalnız 3.7s tahmini vardır; 4s yeni tahmin varmış gibi kullanılamaz.

M09, tazelik kabulünden geçmiş katılımcı adaylar için ortak `H_effective = min(4s, min_i H_remaining_i)` belirler. 0.1s grid'e aşağı yuvarlanır. Sabit boyutlu tensor 40 nokta taşıyabilir; son geçersiz hücreler `time_valid_mask=false` olur. Padding, yeniden örnekleme veya son pozu tekrarlama **tahmin değildir**. M10 tüm adayları aynı geçerli ufukta puanlar; ilerleme ve süreye bağlı maliyetler açıkça normalize edilir. Yaş sınırını aşan aday, diğerlerinin ufkunu keyfî kısaltmadan önce reddedilir. K, katılımcı planner sayısı, maske ve `H_effective` loglanır. Bir planner'ın sık elenmesi başarı tablosunda gizlenmez.

M12'nin dört Δv/dört Δd knot'u geçerli ufkun normalize edilmiş zamanlarına uygulanır; t=0 sürekliliği sabittir. M13/M14 aynı ufku ve engel forecast kapsamını kullanır. Nominal 4s/40 aralık OCP korunur; async kısa-ufuk profili explicit ayrı konfigürasyondur. Geçerli ufuk 2s pilot alt sınırının altına iner veya model/engel kapsamı yetersiz kalırsa M13/M22 fallback kararı verir. Kısaltılan ufuk için stop-distance ve constraint denetimi yeniden yapılır; 2s değeri güvenli duruş kanıtı değildir. Yeni uzun ufuk üretilmiş gibi extrapolation yapılmaz.

Resmî NAVSIM gibi tam ufuk isteyen değerlendirmelerde native zaman ve tam protokol kullanılır. Kısa async aday, resmî 4s sonucu gibi skorlanmaz. P0 nominal karşılaştırması ve P1–P3 operasyonel gecikme deneyleri ayrı satırlardır. Değişken-ufuk maskesi/normalizasyonu eğitim ve değerlendirmede aynı olmalı; E16/E17/E24 kapsamındadır.

## 2. Kanonik modül tanımı ve veri sınırı

`specs/components.json` içindeki ana `input/output/training/source/acceptance` alanları v1.2 eklemeleri dahil **etkin tanımıdır**. M10 hem fiziksel özellik hesaplayıcısı hem küçük trainable SafetyPerformanceCritic içerir. Eski alanlar `legacy_v1_1_fields` içinde tarihçedir. Öğrenilmiş skorun yüksekliği M13 kısıtlarını geçersiz kılmaz.

54 bağımlılık kaydı, **52 farklı yönlü modül çiftini** temsil eder: M10→M11 ve M20→M19 farklı payload'larla iki kez kayıtlıdır. Sayı, 54 farklı fiziksel kanal iddiası değildir. Grafikteki M21→M10, M21→M06, M21→M17, M17→M10 ve M20→M21 veri yolları `OFFLINE_ONLY` olur. M21→M00 veri/konfigürasyon hazırlığı da çevrim dışıdır. Eğitim paketleri worker inference API'sinden erişilebilir olmamalıdır.

Dağıtılan **eğitilmiş ağırlıklar** ile öğretmen paketleri ayrı ürünlerdir. Deployment registry, yalnız checkpoint/schema/calibration hash'lerini yükler; `TeacherTargetSet`, gelecekteki görüntüler ve actor-truth tablosu inference payload'ına bağlanmaz. Sadece kara liste anahtarlarını silmek yerine izinli alanlardan yeni `PolicyObservation` kurulmalıdır.

Grafik mantıksal bağımlılık envanteridir; bütün shared-memory okuma veya alan düzeyi bağlantıların ağ şeması değildir. Ego/rota/aday snapshot'ları ID ile değişmez referanslardan çözülür. M06→M11 paketi grounded horizon özelliklerini taşır; M11→M12 seçilmiş adayın `candidate_set_id/candidate_id` referansını taşır. M10'a yalnız **önceki** kontrol snapshot'ı verilir. Snapshot kimliği/alanı çözülemeyen paket reddedilir; aynı tick'in gelecekteki solver sonucundan döngüsel özellik üretilemez.

## 3. Critic çıktı türleri ve güvenlik semantiği

Her başlık için `head_id`, `target_definition`, `output_type`, `protocol`, `horizon`, `valid_mask`, `calibration_status` ve `calibration_split_hash` saklanır. `p_no_collision` adı tek başına kalibre çarpışmasızlık olasılığı iddiası değildir. NAVSIM'deki **no-at-fault-collision** etiketi ile bütün fiziksel çarpışmalar farklı hedeflerdir; NC kısaltması bu ayrımı gizleyemez. DDC gibi bileşenler protokole göre dereceli olabilir. Bir skor sigmoid'den geçti diye olay olasılığı olarak raporlanmaz.

FPD kaynak scorer'ı altı native latent başlığı sağlar; τMOTION'ın kontrol uygulanabilirliği başlığı, veri köprüsü ve eğiticisi ek çalışmadır. Kaynaktaki ranking aritmetiği/protokolü native baseline için korunur. Yeni critic, farklı latentlere native ağırlık takılmasıyla hazır hale gelmez. Gerekli küçük eğitim ve kalibrasyon ana kapsamdadır.

M10 critic, PPO reward-value ve episode CVaR cost-value ayrı hedeflere sahiptir. Offline supervised cache doğrudan on-policy PPO replay'i sayılmaz. Model ve critic sürümü rollout boyunca kilitlenir; değişiklik sonraki on-policy batch'e geçer. CVaR için terminal maliyet, episode sonlandırma/truncation ayrımı ve quantile kararlılığı yöntem belgesindeki gibi kayıtlıdır.

## 4. Görünürlük ve expert köprüsü

LEAD'in instance/depth/actor-box bilgileri **offline etiketleyiciye** aittir. Runtime visibility yalnız izinli sensörlerden kestirilen bilgidir. Erişilmeyen piksel/nesne veya confidence değeri uydurulmaz; belirsiz kapsama `UNKNOWN` kalır. Kaynak instance ID'leri 16 bit kısaltılır: aynı episode'da ID çakışması varsa görünürlük etiketi maskeleme/association denetimi gerekir. Bu, doğrudan hazır kodun üzerine gereken veri kalite köprüsüdür.

LEAD modern veri üretimi CARLA 0.9.16 gerektirir; ana Bench2Drive 0.9.15 değerlendirmesi ayrı environment/manifest kullanır. BridgeDrive'ın LEAD adaptasyonu daha eski belirli checkout'lara dayanır; modern LEAD main içine körlemesine dosya kopyalanmaz. Native challenger kendi bağımlılık kilidiyle çalıştırılır, ortak değerlendirme yalnız çıktı sözleşmesi üzerinden yapılır. İlgili kaynaklar [yeniden inceleme kaydındadır](source-audit-v1.3.1.md).

## 5. Kontrol, zamanlama ve karar izi

M13 fiziksel referans kontrolünü yapar; M22 bağımsız zaman/epoch/generation kapısıdır; **M15'in tek yetkilendiricisi M22'dir**. Normal/fallback dalı aynı kapıdan geçer. Çizimde fallback kutusunun actuator'a bağlı olması ikinci bir komut sahibi yaratmaz. M15 girdi sözleşmesi buna göre düzeltilmiştir.

20Hz hedefinin 50ms bütçesi snapshot, reference check, NMPC feedback, gate, publish ve jitter toplamıdır. Solver preparation, model yükleme ve CUDA iptal sonrası kalan iş kaynak hesabından çıkarılmaz. AS-RTI/RTI ve timeout davranışları backend'in desteklediği API ile sınanır; ayrı process gözetmeni korunur. Pilot ölçümü olmadan iki A5000 üzerinde gerçek zaman başarısı veya bir frekansın güvenli olduğu ilan edilmez.

Karar izi; observed_at, generation, checkpoint/calibration sürümü, ham aday, critic başlıkları, örneklenen j/residual/logp, post-residual fiziksel risk, supervisor müdahalesi, solver sonucu, gate kararı ve gerçek aktüatör komutunu birlikte tutar. Öğrenilmiş puan ile gerçekleşmiş outcome aynı sütuna yazılmaz.

# v1.1 araştırması ve eleştirilere karşı revizyonlar
## 1. Karar özeti
Başlık Architecture Specification v1.1 olarak değişti. Önceki 22 modül, RQ1–RQ9 ve E1–E15/E10-H korunur. M22 deadline guardian ve M23 kanıt taşıma eklendi. E16 zamanlama, E17 kontrol zaman aşımı ve E18 sensör/hesap karşılaştırması mevcut aileleri derinleştirir. Bu teslim bir sürüş implementation release'i değildir.

| Eleştiri | Somut revizyon | Ölçüm |
|---|---|---|
| Algı + iki üretici + VLM maliyeti | AoI tabanlı çok frekans; bounded queue; paylaşılan VLM ağırlık servisi; M23 | Birlikte latency, bellek, veri yaşı, çağrı/drop oranı |
| Eşdeğer olmayan sensörler | Native, model-içi ablation, eşit K ve eşit hesap ayrı | Her tabloya comparison_class ve çıkarım sınırı |
| CVaR episode maliyeti | Offline → online veri toplama → küçük PPO → CVaR pilotu → tam deney | Episode/saat, policy version, tail CI, toplam bütçe |
| NMPC 50 ms | Bütün kritik yol bütçesi; nonuniform/RTI seçenekleri; bağımsız M22 | Deadline miss, late rejection, fallback ve sürüş sonucu |
| Final/verified karışıklığı | Ayrı doğrulama seviyeleri ve evidence registry | Doküman PASS; runtime NOT_RUN |

## 2. Bilgi yaşı ve zamanlayıcı
AoI literatüründeki bulgu, görev süresi ve throughput'un kararın güncelliğini tek başına tanımlamamasıdır. Bu mimaride çıkarımımız: GPU işi bittiğinde kaynağın zamanı korunmalı; kritik aktörün eski verisi, taze fakat ilgisiz paketlerin ortalaması içinde kaybolmamalıdır. [Xu ve diğerleri, 2022](https://doi.org/10.1109/INFOCOM48880.2022.9796958)

DNN inference süresinin veri, I/O, runtime ve donanım koşullarına göre değişebildiğini inceleyen çalışma, yalnız sıcak tek-model ortalamasını hedef olarak almamak gerektiğini destekler. Bizim pilotumuz paired/full co-location ve burst yüklerini bu nedenle içerir. [Liu ve diğerleri](https://arxiv.org/abs/2209.05487)

Kaynak kabulü ölçümden yapılır. Kullanıcı hedefi 2×A5000 olarak korunur. Bu oturumdaki NVIDIA-SMI denemesi driver ile iletişim kuramadı; bu, GPU donanımının bozuk olduğunun teşhisi değildir. Yerel GPU performans ölçümü yapılmadı. Hedef ortam kurulumu ve driver erişimi G0 koşuludur.

## 3. NMPC'nin hazır optimizasyon seçenekleri
acados nonuniform shooting_nodes/time_steps, partial condensing ve SQP_RTI hazırlık/feedback fazlarını sağlar. Bunlar hazır çözücünün seçenekleridir; yeni optimizer yazılmayacaktır. Belgelenen timeout_max_time, SQP ve SQP_WITH_FEASIBLE_QP içindir; SQP_RTI'de aynı süre kesme varsayımı yapılmaz. Gözetmen bu nedenle ayrı çalışır. [acados seçenekleri](https://docs.acados.org/python_interface/index.html)

AS-RTI, hazırlık aşamasındaki ek hesapla feedback işini ayıran hazır acados uygulamasına sahip araştırma alternatifidir. Ana SQP_RTI referansı korunur; E17'de AS-RTI mevcut implementation ile karşılaştırılır. Hazırlık sırasında kullanılan tahmini durumun hatası ve toplam CPU süresi de ölçülür. [Frey, Nurkanovic, Diehl, 2024](https://arxiv.org/abs/2403.07101)

OCP pilot matrisi: 2/3/4 s ufuk; 20/30/40 aralık; uniform/nonuniform grid; warm/cold start; SQP_RTI ve desteklenen AS-RTI ayarları; farklı partial condensing; seyrek/yoğun dinamik aktör. Her hücreyi tam factorial çalıştırmak zorunlu değildir: önce kontrol edilebilir küçük tarama, sonra validation seçimi ve kilitli test. Dört saniyelik planner çıktısı korunur; kontrolcü daha kısa bölümünü takip edebilir.

## 4. Örnek verimliliği ve CVaR
Offline cache yalnız kaydedilmiş gözlem için geçerlidir. Canlı politika yeni duruma girdiğinde yeni inference gerekir. Offline seçicinin iyi skoru, policy'nin kendi dağılımındaki davranışını garanti etmez. Bu yüzden supervised warm start sonrası model sabitken küçük closed-loop veri turu ve yeniden etiketleme vardır; DAgger-benzeri yaklaşımın teori garantisi bizim etiketleyiciye otomatik aktarılmaz. [Ross ve diğerleri](https://proceedings.mlr.press/v15/ross11a.html)

PPO pilotunun amacı önce maskeler, hibrit log-prob, recurrent state, reward ve shield etkileşimini sınamaktır. CVaR pilotu bundan sonra aynı sürümde tam episode maliyetleriyle çalışır. “50 tail örneği” evrensel yeterlilik eşiği değildir; quantile kararlılığı ve confidence interval genişliği raporlanır. Eski policy episode'larını gelişigüzel biriktirmek yeni policy'nin on-policy CVaR'sini vermez.

Eğitimde riskli senaryoları zenginleştirmek faydalı olabilir; bu dağılım training curriculum olarak etiketlenir. Doğal test dağılımı, stres testi ve varsa önem ağırlıklı tahmin ayrı tutulur. Bilinmeyen örnekleme olasılıklarına sahte importance weight atanmaz. [Risk kısıtlı politika öğrenmesi](https://jmlr.org/papers/v18/15-636.html)

Tahmini eğitim süresi T ≈ episode_sayısı × ortalama_episode_duvar_süresi / etkin_paralellik + güncelleme + değerlendirme maliyetidir. Etkin paralellik iki GPU sayısına eşit varsayılmaz; renderer ve büyük model yerleşimi sınırlar. Episode/saat ve GPU-s/episode pilotta ölçülür, sonra tüm kapsam için bütçe tablosu doldurulur.

## 5. Hazır parça ilkesi
M23 için FilterPy 1.4.5 predict/update kodu incelendi ve commit sabitlendi. Yeni bir takip ağı geliştirilmez. M22'de Autoware command gate davranışı referans alınır; ROS backend seçilirse mevcut node ve mesaj adaptörü kullanılır. Ana native CARLA yolu için küçük zaman/komut gözetimi araştırma entegrasyon kodudur; “Autoware kodu doğrudan kullanıldı” diye yanlış etiketlenmez.

Önceki AutoE2E taksonomi, horizon head, coupling, teacher pipeline, faithfulness, control rollout, speed benchmark ve AlpaSim plugin tekrar kullanımı korunur. Ek yöntemler bu parçaların yerine geçmez; aralarındaki çalışma koşullarını açıklaştırır.

## 6. Ölçüm araçları
PyTorch benchmark Timer sıcak çalıştırma ve CUDA eşzamanlama ayrıntıları için hazır araçtır. Worker'ın ölçümü ile tüm sistem wall-clock ölçümü ayrı yapılır. Başka process'teki GPU işlerinin çekişmesi ayrıca gözlenir; yalnız Python çağrı başlatma süresi inference latency diye yazılmaz. [PyTorch benchmark](https://docs.pytorch.org/tutorials/recipes/recipes/benchmark.html)

NVML üzerinden süreç/GPU belleği ve desteklenen kullanım/güç metrikleri alınır. PyTorch reserved belleği bütün GPU tüketimi değildir; CARLA ve diğer süreçler dahildir. Enerji yalnız ölçüm imkânı ve örnekleme sınırı açıkken raporlanır. [NVIDIA NVML](https://docs.nvidia.com/deploy/nvml-api/latest/index.html)

## 7. Katkı iddiasının sınırı
Yeni büyük model, yeni temel optimizer veya yeni güvenlik garantisi iddia edilmiyor. Katkı adayları; hazır üreticiler üzerinde kanıt/yaş farkındalıklı seçim ve residual, kontrol geri beslemesi, kaynak farkındalıklı çalışma ve etkiyi öneriden komuta kadar ayıran değerlendirmedir. Olumsuz deney sonuçları da araştırma kapsamını tamamlayabilir. Güçlü bir hazır modelin entegrasyonu tek başına yayın yeniliği kanıtı değildir.

# Yöntemler: neden, matematik, öğrenme sorumluluğu

**Güncel yayın: v1.3.1.** [Entegrasyon sözleşmesi](integration-contract-v1.3.1.md) bu belgedeki nominal ufuk, veri kapsamı ve sürüm uyumluluğunu kesinleştirir; tüm yöntemler korunur.

## 1. Semantik bağlamın kontrol edilebilir temsili
Her iddia c=(actor, relation, hazard, cause, action, rule, h) olarak temsil edilir. h ∈ {0,1,2,3,4} saniye. Eşleme bir actor_id'yi kesin belirleyemiyorsa unknown korunur. Güven, VLM'nin kendi söylediği bir sayıdan ibaret değildir.

Girdi temsili z_sem = f(tokens, horizon, evidence_status, calibrated_score, age, visibility) şeklindedir. Şimdiki gözlem ile geleceğe ilişkin tahmin ayrı özelliklerdir. Gelecek için score, iddianın gerçekleşmiş doğruluğu değil mevcut tahminlerle tutarlılığıdır. Grounding eğitiminde yalnız train etiketleri; kalibrasyonda ayrılmış validation bölümü kullanılır.

Gating: z = z_visual + α · g(evidence, age) · P(z_sem). α başlangıçta sıfır olabilir; P normal başlatılır. Hem α hem P sıfırlanırsa öğrenme yolu kapanabilir. Bu nedenle AutoE2E'den alınan başlatma mantığı korunur, yeni giriş projeksiyonları küçük politikada eğitilir. Dondurulmuş planlayıcıların iç katmanlarına yeni coupling ağı eklenmez.

Kalibrasyon için sıcaklık ölçekleme başlangıç yöntemidir; tür/ufuk bazında yeterli doğrulama örneği varsa ayrı kalibratör denenir. ECE tek başına yeterli değildir; Brier ve reliability eğrisi de raporlanır. [Guo ve diğerleri, kalibrasyon](https://proceedings.mlr.press/v70/guo17a.html)

## 2. Öğrenilmiş seçici ve hibrit eylem
K aday için f_i; görsel kanıt, semantik ve kontrol geçmişi için s_t kullanılır. Candidate attention, aday kimliğinin yapay sıra avantajını azaltacak ortak ağırlıklarla uygulanır. GRU durumunun episode başında sıfırlanması ve truncated sequence burn-in protokolü belirlenir. Hafızasız aynı kapasite baseline'ı E3'te tutulur.

πθ(j,u|s) = πθ(j|s) · πθ(u|s,j).
j kategorik aday, u residual'ın sınırsız Gaussian örneğidir. r = b ⊙ tanh(u); b fiziksel başlangıç sınırıdır. PPO oranında kullanılan logp = log π(j|s) + log π(u|s,j) − Σ log[b·(1−tanh²u)] olur. Yalnız etkin residual boyutları hesaba katılır. Değerlendirmede ortalama residual/deterministik aday profili ayrıca kaydedilir.

Aday maskesi çevre ve geometri kaynaklıdır, test geleceğini kullanmaz. Hiç geçerli aday kalmazsa özel STOP seçeneği kullanılır. Shield öneriyi değiştirmiş olsa da PPO kaydında olasılığı hesaplanan eylem, politikanın gerçekten örneklediği (j,u)'dur. Uygulanan eylem ayrıca tutulur. Shield sabit çevrim parçası olarak eğitimde de çalışır; müdahale cezası ve müdahale oranı raporlanır.

TorchRL ClipPPOLoss ve veri toplama altyapısı kullanılır; özel olan küçük politika ve koşullu dağılım adaptörüdür. CompositeDistribution tek başına aday ile residual arasında koşulluluk kurmaz. SB3 MaskablePPO, ayrık seçici baseline'ı olabilir; recurrent maskeli hibrit politika bütün olarak hazır sanılmaz. [TorchRL PPO](https://docs.pytorch.org/rl/stable/reference/generated/torchrl.objectives.ClipPPOLoss.html), [TensorDict dağılımları](https://docs.pytorch.org/tensordict/stable/reference/generated/tensordict.nn.distributions.CompositeDistribution.html)

## 3. Öğrenme sırası
Öğrenci inference sırasında M02'nin havuzlanmış BEV/nesne özellikleri ve ego geçmişinden beslenir; küçük projeksiyonlarla horizon head giriş boyutlarına taşınır. Çevrimiçi VLM token/KV hesabına ihtiyaç duyarsa teacher maliyeti gerçekte kaldırılmış olmaz. E11/E12 bu bağımlılığı ve toplam algı maliyetini denetler. Eğitim hedeflerindeki geleceğe ilişkin etiketler ile canlı VLM'nin nedensel geçmişten ürettiği gelecek tahminleri ayrı provenance taşır.

A. Resmi checkpoint forward'ları ve karşılaştırılabilir candidate cache üretilir. Validation/test sahneleri cache'in eğitim bölümüne girmez.

B. Hazır metrik ve train etiketleriyle aday sıralaması/öğrenci denetimli öğrenmesi yapılır. Teacher'ın yanlış etiketleri maskelenir; otomatik etiket ile insan/geometri doğrulaması aynı kaynak türü sayılmaz.

C. NAVSIM'deki sabit sahne puanlarıyla supervised ranker veya contextual bandit karşılaştırılır. Eylemin sonraki gerçek gözlemi değiştirmediği kayıt düzeni, çok adımlı çevrimiçi PPO olarak adlandırılmaz.

D. CARLA'da küçük politika ve residual, closed-loop on-policy PPO ile geliştirilir. Train ortamı da aynı M13/NMPC hattını kullanır. Büyük planlayıcı ağırlıkları bu ana deneyde sabittir.

E. Risk kısıtı ve teacher/student/conditional-call profilleri ayrı run'larda değerlendirilir. Eğitim verisi toplama döngüsü E14 ile sürümlenir. Büyük model finetuning veya DiffGRPO zorunlu yeni iş paketi değildir.

## 4. Ödül, güvenlik maliyeti ve CVaR
Performans ödülü: rota ilerlemesi, hız hedefi, konfor ve takılma maliyeti. Güvenlik maliyeti C ise episode boyunca biriken çarpışma şiddeti/ihlal/near-miss ve kontrol başarısızlığı bileşenlerinden oluşur. Her bileşenin birimi/ölçeği train pilotunda normalize edilip kilitlenir. Tek birleşik maliyetin yanında çarpışma/km, kırmızı ışık ve infeasibility ayrı raporlanır; ağırlık seçimi bunları gizleyemez.

Amaç, J_R'yi artırırken CVaR_α(C) ≤ d koşulunu sınamaktır:
CVaR_α(C) = min_η [η + E(max(C−η,0))/(1−α)].
L(θ,η,λ) = J_R(θ) − λ[η + E(max(C−η,0))/(1−α) − d], λ ≥ 0.

Uygulanabilir başlangıç seçimi α=0.90'dır; 0.95 duyarlılık deneyi olarak tutulur. d, validation öncesindeki train pilotu ve kabul edilen performans/risk dengesiyle belirlenir; sayısal güvenlik garantisi gibi sunulmaz.

Her on-policy risk güncellemesinde:
1. Tutarlı davranış policy sürümüyle tam episode maliyetlerini topla.
2. η ← η − lr_η [1 − mean(1(C>η))/(1−α)] ile quantile yordamını güncelle; eşitlik/subgradient kuralı sabitlensin.
3. CVaR tahminini hesapla; λ ← max(0, λ + lr_λ(CVaR−d)).
4. η ve λ'yı ilgili PPO epoch'ları boyunca sabit tut; episode sonu dönüştürülmüş maliyet max(C−η,0)/(1−α) için ayrı value/advantage öğren.
5. Ödül avantajından λ ile ölçekli tail-cost avantajını çıkararak clipped PPO güncellemesi yap.

Bu bir **CVaR uyarlaması önerisidir**, hazır PPO parametresi değildir. SafePO'dan multiplier ve cost-critic kalıpları alınabilir; tail dönüşümü yeni küçük kod gerektirir. Sonlu episode amaç fonksiyonunda toplamlar indirgenmemiş olarak tanımlanır; terminal cezanın farklı episode uzunluklarında γ ile istemeden küçülmesine izin verilmez. GAE kullanımının yanlılık/varyans etkisi ayrıca kaydedilir. Cost critic, birikmiş C ve kalan süreyi de görmelidir.

Empirik tail örnek sayısı N·(1−α) açık raporlanır. 50 tail episode hedefi α=.90 için yaklaşık 500 episode anlamına gelir; bu sayı evrensel istatistiksel yeterlilik garantisi değildir. Quantile/CI kararlılığı ayrıca ölçülür. Eski policy'lerden kontrolsüz episode havuzu yeni policy için on-policy sayılmaz. Binary çarpışma maliyetinin seyrekliğinde CVaR ayrım gücü sınırlıdır; near-miss/şiddet ve ayrı olay oranı korunur. Eğitim curriculum dağılımı ile doğal test CVaR'si ayrı raporlanır.

CPO, PPO-Lagrangian ve CVaR aynı algoritma değildir. Ana yöntem clipped PPO + açık CVaR kısıtı uyarlamasıdır; constrained-mean baseline ayrı çalıştırılır. Yakınsama veya sıfır çarpışma garantisi ileri sürülmez. [CVaR politika gradyanı](https://arxiv.org/abs/1406.3339), [risk kısıtlı RL](https://jmlr.org/papers/v18/15-636.html), [SafePO Lagrangian](https://safe-policy-optimization.readthedocs.io/en/latest/algorithms/lag.html), [CPO](https://proceedings.mlr.press/v70/achiam17a.html)

## 5. Residual'ın geometrisi
Başlangıç konfigürasyonu dört knot × iki kanal: boylamsal hız ofseti ve referans normalinde yatay ofset. Tanımlanan b başlangıçta ±2 m/s ve ±0.5 m üst sınırlarıdır; bunlar pilotta araç/hız zarfına göre daraltılabilir veya yeniden ayarlanabilir, residual işlevi kaldırılmaz. t=0 düzeltme ve ilk türev sürekliliği sabitlenir; hız negatif yapılmaz; heading yeni eğrinin teğetinden hesaplanır.

Knot sayısı, düzeltme büyüklüğü ve hızla ölçeklenen sınırlar E7 ablasyonlarıdır. Doğrudan her waypoint için serbest x/y yazmak yerine düşük boyutlu residual, küçük politikanın arama uzayını sınırlar. Düzeltmeden sonra curvature, lateral acceleration ve engel aralığı tekrar hesaplanır. Residual'ın yararı motorun başarısı gibi; motorun yararı residual katkısı gibi yazılmaz. [Residual RL yaklaşımı](https://arxiv.org/abs/1812.03201)

## 6. NMPC modeli ve çözümü
MPC-aware top-N search kapsamda kalır: ana profil bütün adaylarda ucuz proxy, seçilende tam NMPC kullanır. E8'de en iyi N=1/3/6 aday için kısa/full OCP ön çözümü karşılaştırılır. Bu arama, bilgi kazanımı ve toplam hesap maliyetini birlikte ölçer; proxy ile çözülmüş uygulanabilirliği eş tutmaz.

Başlangıç durumları x=[X,Y,ψ,vx,vy,r,δ,a]; girdiler u=[δdot,j]. Dinamik bisiklet modelinde kütle, yaw atalet momenti, aks mesafeleri ve lastik kuvvet katsayıları gerekir. Düşük vx'de slip-angle bölmeleri singular olduğundan kinematik model ile yumuşak geçiş veya doğrulanmış regularization uygulanır. Parametreler seçilen CARLA vehicle blueprint'inden ve kontrollü tanılama sürüşünden elde edilir; örnek yarış aracının parametreleri körlemesine kullanılmaz.

Maliyet: konum/yaw/hız referansı hatası + steering-rate/jerk cezası + slack cezası. Fiziksel actuator sınırları hard; yol/engel modelindeki belirsizlik için belirlenen sınırlı slack açık loglanır. Çok yüksek ceza koymak hard safety garantisi sağlamaz. Çarpışma geometrisi ego footprint ve aktör footprint'leriyle hesaplanır; forecast modları/olasılıkları kullanılır. Ampirik hata quantile'ıyla şişirme, formal kalibre chance constraint olarak sunulmaz.

Kontrol hedefi 20 Hz; başlangıç OCP ufku 4 s ve 40 adet 0.1 s model aralığıdır. 50 ms bütün kritik kontrol yolunun bütçesidir. Örnek pilot dağılımında NMPC feedback'e 32 ms, snapshot/referans ve komut yayınına 8 ms, jitter'a 10 ms ayrılır; bunlar ölçülmemiş tasarım değerleridir. M22, deadline'ı bağımsız gözetir; geç sonuç yeni tick'i ezemez. Kısa/nonuniform ufuk ve AS-RTI karşılaştırması E8/E17 içindedir. Tam zaman sözleşmesi [runtime-contract.md](runtime-contract.md) dosyasındadır.

acados örnek OCP iskeleti, warmstart, SQP_RTI, Gauss-Newton ve HPIPM tekrar kullanılır. CasADi modele ilişkin türevleri sağlar. Yeni optimizer yazılmaz. Frenleme ve düşük hız hataları deneyle bulunur; belirsiz modelde NMPC teorisi tek başına güvenlik sertifikası değildir. [acados Python interface](https://docs.acados.org/python_interface/index.html), [öngörülü güvenlik filtresi literatürü](https://arxiv.org/abs/1812.05506)

## 7. Açıklama etkisi ve nedensellik
Üç ayrı soru sorulur. Açıklama doğru mu? Karar ona duyarlı mı? Duyarlılık doğru eylem yönünde mi? Tek bir yörünge mesafesi üçüne birden cevap vermez.

Metin yolu testi: candidate/evidence/GRU/RNG sabit, yalnız semantik etiket değişir. Çıktılar seçim olasılığı, residual, kabul edilen referans ve uygulanan komut olarak ayrı ölçülür. Bu, seçici düzeyinde kontrollü etkiyi sınar.

Üretici reasoning testi: yerel modelin desteklediği direct/reasoning kipleri aynı budget altında karşılaştırılır. Dış semantik kanalını kapatmak Qwen-Drive'ın iç reasoning'ini ortadan kaldırmaz. Bu iki deney farklı nedensel sınırları hedefler.

Ortam testi: aynı seed/state ile yaya, ışık veya çapraz trafik değiştirilir; hem görsel hem dilsel yol etkilenebilir. Sonuç sistemin müdahaleye doğru tepkisidir; tek başına açıklamanın eyleme aracılık ettiğini kanıtlamaz. Actor dynamics ve fizik yeniden eşlenebildiği ölçüde paired analiz yapılır.

İnsan çalışması: anlaşılabilirlik ve güven algısı yanında, kullanıcıların doğru/yanlış kararı ayırt etme başarısı ölçülür. Akıcı fakat yanlış açıklamaya yüksek güven olumlu sonuç sayılmaz.

## v1.2 addendum — current specification supersedes applicable v1.1 text

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

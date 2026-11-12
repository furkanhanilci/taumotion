# τMOTION v1.2 — güncel bütünleşik mimari: neyi, neden ve nasıl kullanıyoruz?

## Araştırma hedefi ve katkı sınırı

τMOTION'ın araştırma sorusu, büyük görsel-dilsel bir modelin ürettiği açıklamaları doğrudan direksiyon komutuna çevirmek değildir. Sistemde çevreyi açıklayan semantik hat, geometrik olguları tahmin eden bağımsız algı hattı, birbirinden farklı güçlü hareket üreticileri ve bunları değerlendiren küçük, risk duyarlı karar politikası birbirinden ayrılır. Bu ayrımın faydası, herhangi bir iyileşmeyi tek bir büyük ağın gizli optimizasyonuna bağlamak yerine hangi bilginin hangi karar aşamasında etkili olduğunu deneysel olarak inceleyebilmemizdir.

Yeni v1.2 kararıyla fiziksel risk özelliklerinin yanına **öğrenilmiş, çok başlıklı safety/performance critic** ve çevrim dışı **çoklu hedefli, görünürlük farkındalıklı uzman denetimi** eklendi. Amaç yalnız aday seçmek değil; yanlış-güvenli sıralamaların azaltılmasını, örtülü aktörlerin belirsiz tutulmasını ve aynı sahne için birden çok uygun hareketin öğretilmesini araştırmaktır. Bunlar başarı garantisi değil, ablation'la test edilecek hipotezlerdir.

## Bir sürüş kararı nerede başlar?

M00, ham simülasyon kayıtları ve benchmark ayırımlarını *hangi verinin ne için kullanılabileceği* açısından işaretler. Örneğin CARLA'daki eksiksiz dünya durumu veya kayıt sonrası gelecekte gerçekleşen çarpışma, yalnızca teacher/ödül/etiket üretiminde kullanılabilir; çevrim içi öğrenci gözlemine taşınamaz. M01 farklı kameralar, kalibrasyon, ego-state ve rota girdilerini doğru geometrik referans ve zaman damgasına bağlar. İki farklı hazır planlayıcının native preprocess/rig kurallarını silmeden aynı fiziksel sahneyi tanımlar. Girdi eksikse uygun mask ve kaynağı korunur; yanlışlıkla senkron kabul edilmez.

M02, semantik VLM’den bağımsız kamera tabanlı BEV/3D nesne/harita/aktör takip kanıtı üretmeye çalışır. Bunu dış semantik VLM'den ayırmamızın nedeni, aynı modelin bir nesne hakkındaki kendi açıklamasını kendi başına doğrulayamamasıdır. M02'nin çıktısı da kesin değildir: sensör görüşü, field-of-view, görünürlük/örtülme, confidence'ın kalibrasyonu ve domain shift gibi sınırlara tabidir. M23 son tespit edilen aktör izini karar zamanına *tahminle* taşır fakat gerçek `observed_at` bilgisini ve belirsizliği korur. Yeni ölçüm gelmeden yeni aktör keşfi veya trafik ışığı renginin kesin güncellenmesi yapılmaz.

M03 büyük VLM hizmeti sahnenin sürüş açısından anlamını yorumlar. Mevcut model ailesinin Qwen3.5 olduğu, Qwen3.8'in yalnız karşılaştırma olduğu kod/model seçim defterinde açıklanır; bilimsel figürlerde model markası bulunmaz. M04 serbest açıklamayı `actor–relation–hazard–cause–action–rule–horizon` gibi denetlenebilir claim alanlarına dönüştürür. M05 0–4 saniyelik zamansal risk/niyet özelliklerini oluşturur. M06 claim'leri bağımsız fiziksel kanıtlarla eşleştirir: `SUPPORTED`, `CONTRADICTED`, `UNKNOWN`, `CONFLICT`, `STALE`. V1.2 ile örtülü ama simülatörde var olan aktörler için offline `VisibilityEvidence` etiketleri de hazırlandı; bu gerçek runtime'da oracle veri kullanılabileceği anlamına gelmez.

## Neden iki hareket planlayıcı, neden ortak aday sözleşmesi?

M07 görsel-dil temelli flow-matching yaklaşımı, M08 diffusion temelli planlama kullanır. Ana protokolde büyük checkpoint ağırlıkları dondurulur. Amaç farklı model ailelerinden gelen önerilerin gerçekten tamamlayıcı olup olmadığını kanıtlamak, her iki modele ayrı ayrı benchmark avantajı tanımak değildir. Başlangıç aday sayısı `K=6` (3+3); `K=2/6/12` ve eşit compute bütçesinde tekrarlanır. M07 native ufuk 5 saniye, M08 native ufuk 4 saniye; M09 ortak değerlendirmede **4 saniye/0.1 saniye** ve ortak t0/ego frame üretir. Interpolasyon modelin doğal tahmin çözünürlüğünü artırdığı şeklinde raporlanamaz. Orijinal zaman örnekleri, model sürümü, seed, input history ve native confidence ayrı saklanır.

## Yeni M10: fiziksel özellik + öğrenilmiş critic

Eski M10 her aday için route-progress, eğrilik, hız, TTC, drivable-area, konfor, planner disagreement, veri yaşı ve ucuz MPC-feasibility proxy üretir. Bu zorunlu fiziksel özellikler korunur. Yeni eklenen `SafetyPerformanceCritic`, aday yörüngeye, sahne kanıtına, kalibre edilmiş/maskelemiş semantik claim'lere ve önceki *nedensel* kontrol bilgisine göre birkaç ayrı hedef tahmin eder: collision/no-collision, drivable-area, TTC, direction compliance, progress, comfort, control feasibility. Skorlar farklı türde olabilir: ikili güvenlik olasılığı, regresyon, sıralama veya belirsizlik aralığı. Critic'in training loss'u ayrı güvenlik/performance, ranking ve calibration terimlerinden oluşabilir.

Bu modelin amacı tanımlanan gerçek güvenlik sınırlarını kaldırmak değildir. Örneğin bir adayın yüksek critic skoru alması, kısıt denetiminin yerine geçmez. Aynı şekilde mevcut planlayıcıların native scorer head'leri farklı latent ve görüntü temsilinde eğitildiği için bunları kendi adaylarımız üzerinde aynı checkpoint'le kullanamayız. Kaynak kod fikri uyarlanabilir; model head'i yeniden eğitilmeli veya dikkatle doğrulanmış özellik köprüsü gerektirir. Critic ile PPO'nun state value ve CVaR tail-risk maliyet kestiricisi ayrı görevlerdir.

## Öğrenilmiş karar ve residual

M11 küçük Candidate Attention ve GRU kullanan, kanıt ve risk koşullu hibrit politika oluşturur. Aday dağılımı `π(j|s)` ve seçilen adaya koşullu continuous residual `π(u|s,j)` birlikte eğitilir; PPO log-olasılıkları eylemin ayrık+sürekli yapısını doğru yansıtır. M12'nin nihai teknik sözleşmesi **4 düğümde Δv ve Δd**, toplam **8 eylem boyutudur**. Görseldeki `Δx, Δy, Δv, Δa` ifadesi yalnız genel açıklamadır, implemantasyon sözleşmesi değildir. İlk sınırlar |Δv| ≤ 2 m/s ve |Δd| ≤ 0.5 m yalnız başlangıç hipotezidir; sıçrama/başlangıç sürekliliği, eğrilik ve yeniden hesaplanan risk kısıtlarıyla denetlenir.

Öğrenme sırasında önce heuristic ve supervised ranker, sonra küçük kapalı döngü PPO, sonra residual, mean-cost constraint ve CVaR pilotları kullanılır. CVaR `α=0.90/0.95`, episode düzeyi güvenlik maliyetinin tail-risk optimizasyonudur; M10 critic'i tek adım tahmin modeliyle karıştırılmaz. Nadir riskli örneklerde güven aralığı/seed/episode bütçesi zorunludur. `STOP` fallback, geçersiz mask ve güvenli aday kalmaması ayrıca tanımlanır.

## Yörünge yürütme ve kontrol

M13 fiziksel/geometrik uygulanabilirliği ve referans tazeliğini doğrular. Çıkış `AcceptedReference`dır; ham aday, residual sonrası öneri ve kabul edilen referans ayrı saklanır. M14 Dynamic Bicycle NMPC; durum `[X,Y,ψ,vx,vy,r,δ,a]`, girdi `[δ̇,jerk]`. Düşük hız düzenlileştirmesi, sert aktüatör kısıtları, izleme/slack maliyetleri gerekir. İlk hedef 20 Hz kontrol; 4 s/40 OCP aralığı (dt=0.1 s); tüm kritik çevrim 50 ms içinde hedeflenir; yalnız solver süresi 50 ms olarak tanımlanmaz. M22 independent guardian eski generation ID'lerini/timeout'u reddeder, uygun fallback yolunu seçer ve M15 tek komut yazıcısı olarak throttle/brake/steer arayüzüne gönderir. Bunlar gerçek zamanlı garantisi veya araç güvenlik sertifikası değildir.

M16 büyük VLM/algı/çift planlayıcıyı 20 Hz solver çevriminden asenkron ayırır. AoI ölçümü asıl gözlem zamanını esas alır. P0 (senkron referans), P1 (asenkron iki planlayıcı), P2 (küçük semantik student), P3 (koşullu planlayıcı çağrısı) ayrı deney profilleridir. Mevcut 2× A5000 (24 GB/kart) birleşik 48 GB model belleği gibi yorumlanamaz. Native checkpoint VRAM, co-load ve P50/P95/P99 ölçülmeden deployability iddiası yoktur.

## Çevrim dışı eğitimde yeni kontrol mekanizmaları

Uzman veri üretimi, görünürlük/örtülme etiketleri, çoklu geçerli hedeflerin çıkarılması ve geleceğe erişen teacher'lar M00/M21 çevrim dışı hattında yer alır. Tek uzman yörüngesi diğer geçerli davranışları yanlış negatif saymamak için multi-target/mask/safe-set kullanılır. Ancak kayıtlı tek bir gelecek, yapılmamış başka bir eylemin gerçek sonuçlarını belirlemez; karşı-olgusal etiket için re-simulation veya uygun rollout gerekir. Eğitimde privilege kullanımı `PolicyObservation` dışına kilitlenir. Eğitim cache'i rig, sensor schema, preprocess, dataset split, teacher/source checkpoint ve etiketleme sürümü fingerprint'leriyle geçersiz kılınır. Ek küçük safety critic ve opsiyonel temporal student dışında iki büyük planlayıcı ana deneyde yeniden eğitilmez.

## XAI ve bilimsel sınama

M17 kararı `raw candidates -> critic outputs -> RL selected candidate -> residual proposal -> safety-approved trajectory -> NMPC -> guardian -> actuator -> actual vehicle motion` olarak kayıtlar. M18 hem sabit fiziksel aday altında semantik özellik müdahalesini hem CARLA'da çevre koşulunu değiştiren fiziksel karşı-olgusal testleri kullanır. Claim precision, calibration/Brier/ECE, false-safe critic ranking, risk-cost CVaR, traffic violation, TTC, route completion ve executed motion farklı metriklerdir. M19 resmî NAVSIM v1.1 PDMS / v2.1.2 EPDMS / CARLA Bench2Drive v0.0.4 DS/SR / KITScenes 3s ADE/FDE'yi kendi koşullarıyla saklar. M20 privileged expert, aynı-sensör rule-based+NMPC, frozen planner-A/B, heuristic, supervised ranker, advanced native planner, optionally diffusion-bridge gibi karşılaştırmaları ayrı tutar.

Bu mimarinin *başarı garantisi yoktur*. Ana test hipotezi: kanıt güvenilirliği, risk scorer kalibrasyonu ve kontrol uygulanabilirliği birlikte kullanıldığında, aynı hareket adayları üzerindeki yanlış seçimler ve nadir kritik güvenlik maliyetleri azalabilir; bunun GPU/latency maliyeti ölçülür.

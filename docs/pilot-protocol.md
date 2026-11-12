# Ön uygulama ve deneysel kabul pilotları
Bütün satırlar PLANLANMIŞTIR. Bu teslimde native model, NMPC veya CARLA pilotu yürütülmedi.

| Pilot | İş yükü | Ölçüm | Geçiş kanıtı |
|---|---|---|---|
| P-A | Her hazır checkpoint, K=1 native forward | Input/output, ağırlık hash, cold/warm süre | Native örnek üretimi ve hata kaydı |
| P-B | Native/adapter aynı örnek | Tensor ve yörünge farkı, koordinat/zaman | Golden örnek toleransları |
| P-C | Model çiftleri ve tam co-load | GPU-s, VRAM, CPU, kuyruk, AoI | Gerçek yerleşim/frekans zarfı |
| P-D | Klasik referans + NMPC + M22 | Toplam kontrol yolu, deadline, fallback | Geçerli normal/fallback komut izi |
| P-E | Offline selector ve küçük closed-loop turu | Oracle gap, seçim farkı, episode/saat | Öğrenilebilirlik ve bütçe |
| P-F | Küçük PPO, CVaR öncesi | Logp, mask, GRU, reward/override | Tutarlı eğitim güncellemesi |
| P-G | CVaR pilotu | Tail örneği, quantile/CI, λ/η kararlılığı | Tam risk deneyi için kaynak/istatistik planı |

## Zamanlama deneyleri E16
Periyodik, EDF ve AoI/olay politikaları aynı model/checkpoint/K ve senaryoda karşılaştırılır. Her worker için farklı frekans ve yaş sınırı taraması yapılır. Çalışan inference'ın preempt edildiği varsayılmaz. Ortalama latency yanında P95/P99, burst, en eski kritik veri yaşı, queue replacement ve rejected result oranı kaydedilir.

Native temporal geçmiş korunurken çağrı frekansı değiştirilir. Öğrenci profili dahil bütün servis maliyeti hesaba katılır. Farklı frekansla sürüş başarısı düşüyorsa compute tasarrufu tek başına başarı değildir.

## Deadline deneyleri E17
Kontrol yoluna 0/10/30/60/100 ms ek gecikme, worker hang ve yanlış generation sonucu enjekte edilir. Enjeksiyonlar modelin kendi doğal gecikmesinin üstüne etiketlenir. M22'nin hangi tick'te fallback verdiği, M15'in uyguladığı komut ve aracın sonucu aynı izde tutulur.

OCP ufuk/grid/solver taraması validation üzerinde yapılır; en hızlı hücre otomatik seçilmez. Tracking, ihlal, rahatlık, slack, fallback ve deadline birlikte değerlendirilir. Warm-start avantajı sahne resetlerinde ayrı raporlanır.

## Sensör/hesap ayrıştırması E18
Native-system, within-model-sensor, fixed-candidate-selector, matched-K, matched-compute ve shared-controller sınıfları kullanılır. Uyumlu checkpoint olmadan “saf model mimarisi etkisi” iddiası yasaktır. Desteklenmeyen sensör maskesi OOD deneyi olarak kalır.

## İstatistiksel kapılar
Geçiş eşiği keyfi biçimde test sonucuna bakılarak seçilmez. Pilot, metriğin varyansını ve pratik anlamlı farkı belirlemek içindir; confirmatory test ayrı tutulur. Başarısız koşular kayıttan silinmez. Kaynak yetersizliği görüldüğünde uygulanabilir profil ve kapsamı koruyan backend/yerleşim seçeneği belgelenir.

## Gözetmen ve kontrol kabulü
Bir tick için doğru karar, yalnız heartbeat varlığı değildir. Komutun episode/generation/deadline, finite değer, actuator limit ve yaş kontrollerini geçmesi gerekir. Durma komutunun üretilmesi ile çarpışmasız durmanın gerçekleşmesi ayrı sonuçlardır. Ölçülmüş P99 değeri deterministik en kötü süre garantisi değildir.

## v1.2 addendum — current specification supersedes applicable v1.1 text

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

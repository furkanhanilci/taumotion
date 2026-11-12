# Kapsam ve karar izlenebilirliği
Architecture Specification v1.1. Bu belge teknik gereksinimleri ve sürüm kararlarını taşır; kişisel sohbet dökümlerini içermez.

## Korunan kapsam
| Gereksinim | Bileşenler | Deney |
|---|---|---|
| Görsel-dil sahne anlama ve CoT | M03–M06 | E4,E5,E10,E11 |
| İki hazır, ağırlıkları değişmeyen üretici | M07,M08 | E2,E3 |
| Ufuklu reasoning ve küçük öğrenci | M05 | E4,E11,E12 |
| Öğrenilmiş seçim, attention ve GRU | M11 | E3,E4 |
| Sınırlı residual | M12 | E7 |
| Bağımsız algı, grounding ve kalibrasyon | M02,M06 | E5,E9 |
| Risk, CVaR ve constrained kıyas | M11 | E6 |
| MPC-aware proxy ve top-N search | M10 | E8 |
| Dinamik NMPC ana kontrol | M13–M15 | E8 |
| Karşıolgusal ve insan XAI | M18 | E10,E10-H |
| NAVSIM v1.1/v2.1.2, KITScenes, CARLA | M19 | E1,E9 |
| Klasik ve öğrenilmiş baseline'lar | M20 | N0–N9,C0–C10 |
| Qwen3.5/3.8 kıyası | M03 | E11 |
| Hesap profilleri P0–P3 | M16 | E12 |
| Görsel temsil, veri çeşitliliği, yinelemeli toplama | M21 | E13,E14 |
| AlpaSim/NuRec keşifsel aktarım | M21 | E15 |
| Hazır AutoE2E alt parçaları | M04,M05,M11,M18,M20,M21 | İlgili ailelerin tümü |
| Kaynak/provenance/karar izi | M00,M01,M09,M17 | E1 ve tüm run'lar |

RQ1–RQ9'un tamamı experiments.md içinde tanımlıdır. Önceki M00–M21 kimlikleri yeniden numaralanmadı.

## v1.1 ekleri
| Karar | Revizyon | Etki |
|---|---|---|
| D15 | Architecture Specification adı | Tasarım ile çalıştırılmış sistem ayrılır |
| D16 | AoI, olay/deadline sıralaması, bir bekleyen istek | Kuyruk eskimesi ölçülebilir olur |
| D17 | M03/M07 paylaşılan ağırlık servisi | Aynı VLM'nin gereksiz kopyası önlenir |
| D18 | M22 bağımsız deadline guardian | Solver beklemesi komut hattını zorunlu bloke etmez |
| D19 | M23 kanıt taşıma | Seyrek algı ile hızlı kontrol arasındaki yaş açık modellenir |
| D20 | Bütün kritik yol için 50 ms | Solver tek başına bütçe sahibi olmaz |
| D21 | Nonuniform/AS-RTI pilotu | Hazır acados seçenekleri sınanır |
| D22 | Eğitim G4a–G4d | CVaR öncesi öğrenme ve hesap fizibilitesi ölçülür |
| D23 | comparison_class | Sensör/hesap/mimari çıkarım sınırları görünür |
| D24 | D0,S0,R1–R5 kanıt seviyeleri | Doküman PASS runtime PASS gibi sunulmaz |
| D25 | Özgün τ ağırlıklı vektör kimlik | README, şema ve raporda tutarlı marka |

Uygulama aşamasındaki bir başarısızlıkta aynı işlev için adaptör/yerleşim/backend revizyonu değerlendirilir. İlgili araştırma sorusu veya yöntem sessizce kaldırılmaz. Bir yöntemin negatif bulgusu da bilimsel sonuç olarak raporlanır.

## v1.2 addendum — current specification supersedes applicable v1.1 text

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

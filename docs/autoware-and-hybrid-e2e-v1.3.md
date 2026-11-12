# τMOTION v1.3 — Hibrit uçtan uca konumlandırma ve Autoware durumu

## Kesin akademik adlandırma

**Önerilen tam ad:** *τMOTION: An Explainable, Risk-Aware Hybrid End-to-End Autonomous Driving Framework Integrating Vision-Language Reasoning, Reinforcement Learning, and Nonlinear Model Predictive Control.*

“Hybrid End-to-End” bu tezde hazır öğrenilmiş E2E hareket üreticilerini kullanan hibrit sistemin çalışma adıdır. Yalnız kamera girdisinden aktüatöre kadar zincirin bulunması, sistemin akademik anlamda uçtan uca öğrenildiğini göstermez. Yayında öğrenilmiş planlama ile modüler risk seçimi/NMPC sınırı açıkça tanımlanır. “Hybrid” zorunlu niteleyicidir; öğrenilmiş E2E motion model, grounded semantics, risk-aware RL ve modüler NMPC birleştirilir. *Fully E2E trainable/monolithic* **değil**: büyük planner'lar frozen, küçük karar ağı ayrı train edilir, NMPC diferansiyellenebilir tek ağ diye tanımlanmaz.

## AutoE2E zaten nereye dahil?

| Teknik özellik / kod | Nihai modül | Tasarım durumu |
|---|---|---|
| Reasoning taxonomy; `reasoning_taxonomy.py` | M04 | Dahil |
| Horizon-aware reasoning head now..+4s; `horizon_reasoning_head.py` | M05 | Dahil |
| Offline teacher to small reasoning student | M05/M21 | Dahil |
| Zero-init gated reasoning coupling; `reasoning_coupling.py` | M11 | Dahil; küçük policy seviyesinde |
| Candidate Attention ve GRU | M11 | Dahil |
| Horizon-targeted faithfulness interventions; `faithfulness.py` | M18 | Dahil |
| Lightweight temporal BEV+GRU; `gru_planner.py` | M20 | **Baseline**; üçüncü aktif gerekli üretici değil |
| Speed measurement harness | M16 | Dahil, yöntem aracı |
| Data/AlpaSim adapter patterns | M21 | Dahil, yöntem aracı |

**Önemli ayrım:** M02 bağımsız BEV algı kullanır, fakat tam AutoE2E Temporal BEVFormer backbone'unun M02 içerisine doğrudan kopyalandığı iddiası yoktur. M20'de referans planlayıcı bulunması, M09 çevrim içi K=6 havuzunda aktif üçüncü planlayıcı olduğu anlamına gelmez. Son konuşmada önerilmiş “bunları ekleyelim” ifadesi, v1.2'de zaten ekli yöntemleri yeniden yeni modüller sanmaktan kaynaklanıyordu. Bu doküman bunu düzeltir ve mevcut 24 modüllü tasarımı korur.

## Klasik Autoware karşılaştırmasının doğru biçimi

1. **Native Autoware Universe:** tam sensör/yerelleştirme/harita/behavior/planning/control yığını, kendi varsayılan doğru konfigürasyonuyla.
2. **Same-evidence classical planner + same NMPC:** τMOTION'la aynı sensor-derived actor/map evidence ve aynı M14 dinamik kontrolcü; öğrenilmiş karar faydasını ayrıştıran en adil baseline.
3. **Autoware AutoE2E:** Temporal BEV+GRU native checkpoint ile planlama doğruluğu/verimlilik karşılaştırması; varsa map/retrospective navigation privileged bilgiler açıkça not edilir.
4. **Yeni Autoware learned/diffusion tasarım yönü:** yayınlanmış çalışan modüller ve kavramsal roadmap ayrılır; tümü ortak bench score'a sahiptir diye sunulmaz.

Klasik Autoware için aynı NAVSIM/Bench2Drive protokolünde güvenilir yayımlanmış eşleşen DS/SR/PDMS skoru bu arşivde bulunmaz; sayı uydurulmaz. τMOTION için aşağıdaki beklenen değerler ise ölçülmüş sonuçlar olarak değil **koşullu mimari tahmini** olarak tutulur.

## Tasarım önceliği

Kullanıcı açıkça: **“testler vs şu an için önemli değil bizz mimariyi tanımlamışsak yeterli”** kararı vermiştir. Bu nedenle mimari tamlık denetimi modüllerin neden, girdi, çıktı, bağlantı, eğitim rolü ve veri yetkisi açısından tamlığına odaklanır; deneyin koşulması release blocker değildir. Runtime/test statüsü geçmişe doğru yanlış gösterilmez. Yeni mimari önerisi ancak daha önce tanımlı modüllerde karşılanmayan gerçek bir gereksinim varsa tartışılır.

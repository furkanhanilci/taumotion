> Tarihsel sürüm kaydı. Güncel yayın v1.3.1; [güncel belge denetimi](../reports/documentation_checks.json). Arşiv/konuşma kopyaları yerel teslimde korunur, Git yayınına dahil değildir.

# v1.2 uygulama ve doğrulama kapıları — ölçülmeden başarı iddiası yok

| Kapı | İşlem | Geçiş kriteri | Şu an |
|---|---|---|---|
| D0 | Dosya/JSON/sürüm/link/diagram/ZIP doğrulaması | `reports/documentation_checks.json` PASS | Paketleme sırasında otomatik çalıştırılır |
| R1 | Büyük model/native inferenceler | Verilen checkpoint + native preprocess + gerçek örnek | NOT_RUN |
| R2 | Model adapter parity | Native/canonical traj toleransları, time/frame metadata | NOT_RUN |
| R3 | Online wiring / SafetyCritic | Sensor data → candidates → critic → RL → accepted → NMPC; no privilege leak | NOT_RUN |
| R4 | Closed-loop CARLA | Aynı route/seed ile geçerli driving and safety metrics | NOT_RUN |
| R5 | 2×A5000 runtime | VRAM, P50/P95/P99, AoI, 20Hz guardian deadline | NOT_RUN |
| R6 | New critic calibration | FPR false-safe, Brier/ECE, ranking, held-out group | NOT_RUN |
| R7 | Visibility / teacher validity | Occlusion labels, teacher-only boundary, multi-target quality masks | NOT_RUN |
| R8 | Repro benchmark | PDMS/EPDMS/DS/SR/KITScenes metrics vs official eval | NOT_RUN |
| R9 | Counterfactual XAI | Paired intervention + environment change and executed motion | NOT_RUN |

**Riskli varsayımlar:** FPD native scorer'ın latent doğrudan taşınmaması; LEAD main/cvpr2026 checkpoint ayrımı; CARLA 0.9.15/0.9.16 farkı; NAVSIM v1 vs v2; 2×A5000 model co-load; zamana yayılım güvenilirliği; farazi geleceğin online kullanılmaması.

## Yeni pilot prosedürü

A. Frozen iki planner ve varsa advanced challenger native; candidate records and oracle ceiling.
B. LEAD-like expert/normal vs perturbed sensor view/visibility labels küçük CARLA senaryo altkümesi.
C. M10 physical-only safety critic → trained multihead → calibration → visibility/CoT add-on.
D. Native baseline scorer (FPD) **kendi** modelinde; tau critic **kendi** features üzerinde. Farklı latentde model ağırlığı taşımayı yasakla.
E. Same-candidate heuristic vs learned ranker vs PPO (frozen/deterministic) → cross eval.
F. NMPC+guardian physical timing pilot then full closed-loop.
G. CVaR α=.90/.95 episode tail stability; independent evaluation routes and multiple seeds.
H. XAI + occlusion + domain generalization; no reported score until valid metrics.

Deneylerde rakip modellerin published scorları `baseline_published` etiketiyle; yeniden ölçülenler `baseline_rerun`; tau değerleri ancak `tau_measured` ile tutulacaktır. Araştırma hedefleri `target_not_measured` olarak farklı dosyaya yazılır.

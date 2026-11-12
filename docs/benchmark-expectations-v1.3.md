# τMOTION v1.3 — Koşullu benchmark potansiyeli ve referansların sınıflandırılması

**v1.3.1 kaynak notu:** τMOTION sayıları korunmuş öznel planlama senaryolarıdır; kalibre edilmiş başarı tahmini veya güven aralığı üretmezler. Ana güncel tablo [benchmark-expectations-v1.3.md](benchmark-expectations-v1.3.md); eski hedefler sürüm tarihçesidir. [Kaynak yeniden denetimi](source-audit-v1.3.1.md).

**12 Kasım 2026.** Kaynak: önceki konuşmalardaki araştırma karşılaştırması ve v1.2 benchmark belgesi. τMOTION satırlarında kullanıcının istediği gibi **sayısal nokta beklentisi** gösterilir, ancak bu gerçek ölçüm veya güven aralığı değildir. Yayınlanmış karşılaştırmalar benchmark split/versiyon/rig/privilege değişirse aynı rekabet tablosu olarak kullanılamaz.

## τMOTION nokta tahminleri — deney sonucu değil

| Benchmark | Nokta beklentisi | Koşullu olası senaryo bandı | Çok başarılı senaryo | Başlıca belirsizlik |
|---|---:|---:|---:|---|
| NAVSIM v1.1 PDMS↑ | **92.5** | 91.5–93.5 | 94–95 | K=6 combined oracle, ranker/critic kalibrasyonu |
| NAVSIM v2.1.2 `navhard` EPDMS↑ | **53** | 48–58 | 59–62 | Temel iki planner'ın eşleşen v2 baseline skoru yok |
| Bench2Drive v0.0.4 Driving Score↑ | **82** | 75–85 | 88–92 | CARLA adaptör, kontrol/latency, domain shift |
| Bench2Drive v0.0.4 Success Rate↑ | **60%** | 50–65% | 70–80% | Kapalı döngü kritik trafik etkileşimleri |
| KITScenes ADE@3s↓ | **0.60 m** | 0.55–0.70 | 0.48–0.55 | 202 örneklik sample, reference path privileges |
| KITScenes FDE@3s↓ | **1.55 m** | 1.35–1.85 | 1.15–1.35 | Aynı etki |

**Stretch objective (beklenti değil):** NAVSIM v1 ≥95 PDMS; Bench2Drive ≥90 DS ve %75–80 SR; KITScenes aynı 202-keyframe protokolde ADE≤0.565/FDE≤1.397. Bu son KITScenes seviyesi, kendi güçlü donmuş temel planlayıcının yayımlanmış seviyesini koruma/iyileştirme hedefidir. Önceki ana nokta tahminini 0.60/1.55'ten değiştirmez. Safety-oriented seçimin insan kayıt yörüngesinden ayrılması ADE/FDE'yi yükseltebilir.

## Yayınlanmış referanslar — bunlar τMOTION sonucu değildir

| Protokol / kaynak | Yöntem | Raporlanmış sonuç | Yorum |
|---|---|---|---|
| NAVSIM v1 PDMS | PDM-Closed | 89.1 | Privileged rule based |
| NAVSIM v1 PDMS | Qwen-Drive RL | 90.7 | Frozen main candidate generator reference |
| NAVSIM v1 PDMS | ReCogDrive RL | 90.8 | Other frozen main generator reference |
| NAVSIM v1 PDMS | HiPro-AD | 92.6 | Exact protocol matching needed |
| NAVSIM v1 PDMS | FPD-Drive / Pro | 94.88 / 95.57 | Strong learned safety score reference |
| NAVSIM v2 `navhard` EPDMS | FPD-Drive / Pro | 54.75 / 58.07 | NOT interchangeable with v1 PDMS |
| Bench2Drive v0.0.4 DS / SR | LEAD | 95.59 / 87.28% | Published leaderboard method, not automatically simulator oracle expert |
| Bench2Drive v0.0.4 DS / SR | SimLingo | 86.55 / 70.45% | Published leaderboard |
| Bench2Drive v0.0.4 DS / SR | Drive-π0 | 69.71 / 45.91% | Published leaderboard |
| Own adaptation study DS/SR | BridgeDrive | 96.34±0.55 / 89.25±0.50% | Do not assume same experimental protocol |
| KITScenes old 202 ADE/FDE @3s | Qwen-Drive | 0.565 / 1.397 | Some sample/input advantages may differ |
| KITScenes old 202 ADE/FDE @3s | AutoE2E | 0.744 / 1.980 | Legacy transform and privilege details |
| KITScenes canonical 11,035 ADE/FDE @3s | AutoE2E fine-tuned | 0.7556 / 2.0504 | Distinct canonical re-score |

## Autoware sonuçları

Klasik Autoware Universe için aynı veriye, aynı kamera/LiDAR/harita koşuluna ve aynı NAVSIM/Bench2Drive sürümüne ait resmî sonuç arşivde **yoktur**; bu nedenle bilimsel yayınlanmış skor tablosuna hayalî yüzde eklenmez. Autoware AutoE2E'nin 202 ve corrected 11,035 KITScenes skorları ayrı tutulur. Autoware Universe native vs same-evidence classic+NMPC baseline eşit kontrol koşulları ayrıca `docs/autoware-and-hybrid-e2e-v1.3.md` içinde tanımlı.

**Metrikler:** PDMS/EPDMS başarı oranı değildir; Driving Score başarı oranı değildir; SR rota başarısıdır; düşük ADE/FDE insan referansına yakınlık gösterir, otomatik daha yüksek güvenlik değil. Kendi mimari tahminleri yayınlanmış sonuçlarla aynı hücrede olursa `estimate, not measured` etiketi zorunludur.

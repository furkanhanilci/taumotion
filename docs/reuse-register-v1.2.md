# Açık kaynak araştırma/yeniden kullanım defteri — figürlerde genel isim, kaynakta gerçek atıf

Bir yöntemin bilimsel şemada marka adıyla belirtilmemesi, gerçek kodun veya checkpoint'in tezde gizlenebileceği anlamına gelmez. `docs/components.md`, `specs/source_pins.json`, bu defter ve uygulama lisans dosyaları kaynakları açıklar. **Kodun varlığı çalışır entegrasyon anlamına gelmez.** İncelenen kaynak kodu doğrudan vendor edilmemiştir.

| Kaynak | Yayımlanan somut kod | Kullanım hedefi | Dikkat / statü |
|---|---|---|---|
| https://github.com/QwenLM/Qwen-Drive-1.0 | VLM+flow planning, checkpoints | Frozen Planner A / external semantic service | Native preprocess, model-hash, VRAM unknown |
| https://github.com/xiaomi-research/recogdrive | VLM+diffusion planner | Frozen Planner B | Online feature cache/native parity unverified |
| https://github.com/autowarefoundation/auto_e2e | Horizon reasoning taxonomy, labels, faithfulness, control-rollout, profiling | M04/M05/M18/M20 araştırma yapıtaşları | Entire online RL pipeline already complete diye iddia edilmez |
| https://github.com/CountNemoChan/FPD-Drive | `score_module/scorer.py`, `reweighted_ranking.py`, `trajectory_selection.py`, `fpd_drive/selection.py`, `fpd_planner/refiner.py`, native inference Pro-v1 | M10 learned multi-head critic design, M20 native advanced benchmark, M12 optional refiner ablation | Released training teacher source **yok**; checkpoint-native scorer features tau candidate latentleriyle uyumsuz; adapt/retrain necessary; Apache 2.0 + upstream NOTICE |
| https://github.com/kesai-labs/lead | `expert/driving/occlusion.py`, `forecast_kernels.py`, `path_planning.py`, `speed_planning.py`, `expert_agent.py`, modular data/log/cache, custom agents | M02/M06 visibility labels, M20 strong rule/expert, M21 scenario+offline data, M17 trace | Main ve cvpr2026 branch checkpoint/data **uyumsuz**; MIT code; dataset/weights terms check; CARLA 0.9.16 collection |
| https://github.com/ShuLiu-ETHZ/BridgeDrive | LEAD ve NAVSIM için ayrı diffusion bridge adaptation | M08/M20 optional challenger, candidate diversity study | Varsayılan üçüncü online planner **değil**; exact license/components verify |
| https://github.com/Thinklab-SJTU/Bench2DriveZoo | UniAD family evidence model & CARLA agent | M02 independent BEV/map/tracking | Sensor rig/domain mismatch; legacy dependencies |
| https://github.com/acados/acados | optimal-control SQP-RTI / HPIPM | M14 Dynamic NMPC | Vehicle identification, low-speed handling, 50ms **not measured** |
| https://github.com/pytorch/rl | TorchRL / recurrent PPO | M11/M12 candidate + bounded residual | Hybrid logp/masks/reset/CVaR extension own work |

## Detaylı dış kaynak bulguları

**FPD-Drive-Pro:** Native Pro-v1 inference config dört kameralı, 64 proposals ve 12 DDIM steps içerir; scoring heads NC/DAC/TTC/DDC/EP/comfort olarak ayrılmıştır. FPD'nin 95.57 NAVSIM v1 PDMS ve 58.07 NAVSIM v2 EPDMS bildirimleri *kendi protokol sonuçlarıdır*. Kodun uygun parçasını pre-trained weight reuse ile karıştırmayacağız. CVaR dışarıdan alınan scorer'ın birebir parçası değildir. Future-privileged multi-target teacher fikrinin tam training implementation'ı bu incelemede **mevcut değil**.

**LEAD:** Modern modular `main` sürümü 8.930 rota/43 senaryo/12 CARLA town ve yaklaşık 1 TB veri üzerinde açıklama yapıyor; full dataset'i başlangıçta indirme kararı alınmadı. `normal_view` vs `perturbated_view`, instance pixel count ve LiDAR bbox visibility, privilege-expert ile student-görüntü arasındaki asimetri için yararlı. Expert kendi native PID/IDM/route shift sistemiyle güçlü baseline'dır, ancak main TAUMOTION kontrolcüsü Dynamic NMPC olarak kalır.

**BridgeDrive:** LEAD uyumlu diffusion bridge planlayıcı, reported 96.34 DS / 89.25 SR, ancak aynı kaynağın sensör/seed/deney koşullarına bakmadan tau'ya aktarılabilir başarı değildir. Önce challenger olarak native, sonra full adapter and compute pilot.

## Hukuki/yöntemsel gereklilik

Kod için repo `LICENSE` ve `NOTICE` (FPD Apache-2.0, LEAD main MIT), weight model-card, dataset/sim lisansları ayrı doğrulanır. Projeye vendor edilen dosyalarda per-file SPDX ve upstream repository+commit+modified-state korunur. Bu arşiv **yalnızca link, kaynak kod yolu ve yöntem notlarını** içerir, üçüncü taraf kod/weight dağıtmaz.

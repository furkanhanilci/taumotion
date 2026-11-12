# τMOTION benchmark matrisi: yayımlanmış örnekler, yeniden ölçüm ve hedefleri ayırma

**v1.3.1 kaynak notu:** τMOTION sayıları korunmuş öznel planlama senaryolarıdır; kalibre edilmiş başarı tahmini veya güven aralığı üretmezler. Ana güncel tablo [benchmark-expectations-v1.3.md](benchmark-expectations-v1.3.md); eski hedefler sürüm tarihçesidir. [Kaynak yeniden denetimi](source-audit-v1.3.1.md).

**UYARI:** Bu belge, önceki görüşmelerde incelenen yayımlanmış sonuçları ve τMOTION için seçilen **koşullu araştırma hedeflerini** arşivler. Rakip skorlar bizim makinemizde yeniden ölçülmüş değildir. Aynı benchmark sürümü, split, cam/sensor/privilege ve checkpoint olmadan kesin ranking ilan edilmez. v1.2'de **τMOTION'dan ölçülmüş skor yoktur**.

## 1. NAVSIM v1 PDMS (0–100, başarı yüzdesi değil)

| Sistem | Yöntem | Raporda PDMS | Veri statüsü | Kaynak |
|---|---|---:|---|---|
| PDM-Closed | privileged rule-based | 89.1 | published, farklı bilgi | Çalışmaların tabloları / NAVSIM |
| Qwen-Drive RL | VLM + planning expert | 90.7 | published, re-run gerekli | https://github.com/QwenLM/Qwen-Drive-1.0 |
| ReCogDrive RL | VLM + diffusion | 90.8 | published, re-run gerekli | https://github.com/xiaomi-research/recogdrive |
| HiPro-AD | Sparse planning | 92.6 | published, exact protocol verify | ilgili orijinal makale |
| FPD-Drive | Future-policy student | 94.88 | published, native inference available | https://github.com/CountNemoChan/FPD-Drive |
| FPD-Drive-Pro | Student + improved selection/refinement | 95.57 | published, native baseline | https://github.com/CountNemoChan/FPD-Drive |
| τMOTION v1.2 | Evidence-conditioned candidate RL + critic + NMPC | **N/A** | **NOT_RUN** | Bu proje |

**Çalışma hedefleri, sonuç değil:** Başarılı ilk araştırma 91.5–93 PDMS; güçlü hedef 92; 94+ yalnız yeterli candidate oracle/real learned gains varsa. FPD üst referansını geçmek için >95.57 aynı split ve doğru protokol şart. `score selection + online execution` maliyeti de raporlanır. Daha büyük model eklemek otomatik başarı sayılmaz.

## 2. NAVSIM v2 EPDMS (v1 PDMS ile eşit değil)

| Sistem | Bildirilen EPDMS | Statü |
|---|---:|---|
| FPD-Drive | 54.75 | Published |
| FPD-Drive-Pro | 58.07 | Published |
| τMOTION | N/A | NOT_RUN; ilk kapı native evaluator |

## 3. CARLA Bench2Drive (başarı oranı ile Driving Score farklı)

| Sistem | DS | Success Rate | Yorum |
|---|---:|---:|---|
| LEAD yayımlanmış yöntem | 95.59 | 87.28% | Benchmark leaderboard girdisi; privileged expert skoru diye yeniden etiketlenmez |
| LEAD TFv6 | 95.28 | 86.81% | learner, kendi kaynak protokolü; re-run gerekir |
| BridgeDrive | 96.34±0.55 | 89.25±0.50% | LEAD-adapted, reported study, matching verify |
| SimLingo | 86.55 | 70.45% | Başka model; published v0.0.4 leaderboard |
| Drive-π0 | 69.71 | 45.91% | published leaderboard |
| UniAD | 38.69 | 19.09% | published leaderboard |
| τMOTION | **N/A** | **N/A** | No full closed-loop integration |

**Araştırma hedefi:** Başarılı entegrasyon 75–85 DS ve %50–65 SR; güçlü hedef ≥85 DS / ≥%70 SR. Bunlar ölçülmüş başarı *değildir*, olasılıksal tahmin veya CI da değildir. Bazı sonuçlar farklı CARLA/Bench2Drive revizyonu veya privileged sensörler kullanıyor; aynı tablo *sıralama iddiası* için uygun değildir.

## 4. KITScenes @3s open-loop

| Yöntem | ADE (m) | FDE (m) | Örnek | Önemli sınırlama |
|---|---:|---:|---:|---|
| Qwen-Drive 1.0 | 0.565 | 1.397 | 202 | Repo karşılaştırması, first traj |
| AutoE2E KITScenes-finetuned | 0.744 | 1.980 | 202 | Eski GT sözleşmesi, map/retrospective route etkisi |
| AutoE2E nuPlan zero-shot | 0.915 | 2.423 | 11,035 | Başka örneklem |
| Constant Velocity | 1.213 | 3.258 | 202 | Eski benchmark dönüşüm sözleşmesi |
| AutoE2E KITScenes-finetuned canonical | 0.7556 | 2.0504 | 11,035 | Canonical `poses.txt` re-score |
| AutoE2E nuPlan canonical | 0.8897 | 2.3876 | 11,035 | Canonical `poses.txt` re-score |
| τMOTION | N/A | N/A | — | Native rig + exact 3s horizon validation pending |

**Kaynak:** https://github.com/autowarefoundation/auto_e2e , KITScenes benchmark README / https://github.com/autowarefoundation/auto_e2e/issues/210 . Farklı örneklem sayıları ve eski/canonical GT değerlendirmeleri tek sıralamaya zorlanamaz. Açık döngü insan yörünge hatasının azalması, otomatik güvenlik artışı değildir.

**Koşullu araştırma hedefi:** 3s ADE ≤0.55m, FDE ≤1.35m; ancak güvenli kararların expert imitation trajectory'sinden farklılaşması nedeniyle bu metriklerde düşüş gözlenmeyebilir. Nihai kıyas: matched 202 sample, canonical poses, same nav route privilege.

## 5. AutoE2E hız benchmarkı ve yanlış çıkarım riski

AutoE2E'nin bazı *lightweight Reactive* sürümleri farklı GPU'larda 10–50 ms düzeyleri bildirmiştir; bunlar tam temporal BEVFormer T8 + ilgili farklı sürücü adapter'ının ölçümleri değildir. AlpaSim sürücüsünde V100 üzerinde yaklaşık 10.5s/decision örneği raporlanmıştır. Bu iki sayı aynı modeli kıyaslamaz; tau çift büyük planner+semantic+evidence co-load gerçek süresi ölçülmemiştir. Kaynak: repo `Model/speed_benchmark/BENCHMARKS.md` ve `Model/plugins/alpasim_driver/README.md`.

## 6. Ana ablation/çapraz doğrulama matrisi

**Aynı adaylar:** native planner-A, native planner-B, oracle best-of-K (yalnız OFFLINE upper-bound), heuristic ranker, supervised ranker, physical-only safety critic, critic + grounded CoT, critic + visibility, recurrent PPO, PPO+residual, CVaR PPO, full tau + NMPC. **Aynı sensör:** native pretrained baselines için girdi farklıysa ayrı privilege/sensor sütunu ile raporla. **Aynı kontrolcü:** classical rule+NMPC, planner+NMPC, full tau+NMPC; ayrıca native agent kendi kontrolüyle raporlanır.

Her metrikte orijinal publication link, tarih, benchmark commit, split, camera/route privilege, num seeds, own rerun, mean/CI, VRAM ve P50/P95/P99 sütunları bulunacak. Orijinal metrikler kendi benchmark sürümleri içinde korunur, otomatik normalize edilmez.

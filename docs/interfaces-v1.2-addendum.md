# v1.2 arayüz uzantıları ve karşı-olgusal veri izolasyonu

V1.1 `docs/interfaces.md` ve `specs/synthetic_contract_example.json` sözleşmeleri korunur; aşağıdaki ek tipler M10 learner, M06 visibility ve M21 teacher için tasarlanmıştır. Bunlar **örnek tasarım sözleşmesidir**, çalışma zamanı kodu değildir.

## `VisibilityEvidence`

```json
{"actor_id":"track_17","observed_at_s":10.0,"estimated_at_s":10.15,"visibility_state":"PARTIALLY_OCCLUDED","source":"sensor_estimated","visible_pixel_count":12,"lidar_count":null,"uncertainty_kind":"uncalibrated_confidence","privileged_annotation":false}
```

`source=offline_teacher_oracle` olursa paket **PolicyObservation'a giremez**. `visible_pixel_count` gerçek kamerada instance segmentation bulunuyorsa ve güvenilir kalibre edildiyse kullanılabilir; aksi halde `null`.

## `SafetyScoreBundle`

```json
{"candidate_set_id":"example_set","observed_at_s":10.0,"evaluated_at_s":10.31,"calibration_version":"untrained","head_schema":"v1.2","scores":[{"candidate_id":"A0","p_no_collision":null,"p_drivable_area":null,"p_ttc_within_bound":null,"p_direction_compliance":null,"progress_estimate":null,"comfort_estimate":null,"mpc_feasibility_estimate":null,"valid":true,"uncertainty_kind":"unknown","label_source":"inference_only"}]}
```

Örnek alanlar `null`: **hiçbir eğitim veya tahmin çalıştırılmadığı** için skor uydurulmaz. `model_output_type` ve per-head calibration proof version zorunlu olacaktır. M10→M11 payload v1.2'de `physical_features + safety_scores + head_valid_mask + evidence_age`.

## `TeacherTargetSet` — yalnız çevrim dışı

```json
{"scene_id":"example_scene","teacher_privilege":"FUTURE_ALLOWED_OFFLINE_ONLY","source_protocol":"CARLA_counterfactual_rollout","target_horizon_s":4.0,"targets":[{"candidate_id":"A0","safe_label":null,"quality_label":null,"label_mask":false}],"can_enter_online_policy":false}
```

Teacher hedefleri ancak değerlendirilmiş label source ve scenario seed ile beraber saklanır. Tek recorded future, tüm alternative action sonuçlarını kanıtlamaz. Offline teacher dataloader ayrı import/data allowlist boundary içinde bulunur.

## `CriticTrainingExample`

Input: current allowed observation, candidate feature tensor, `TeacherTargetSet` quality masks ve label provenance. Critic-only training'de source `NAVSIM_pseudo_score` ile `CARLA_closed_loop` aynı hedef havuzuna yalnız özel domain/protocol farkı kodlanarak girer. Train/test split fingerprint ve checkpoint pin zorunlu; test verisi teacher calibration setine alınmaz.

## Veri akışı ve algoritmik sözleşme

- M02→M06: `VisibilityEvidence` ve `ActorEvidence` (sensor-estimated), actor association/uncertainty.
- M06→M10: GroundedClaim + per-claim visibility; veri yaşı korunur.
- M09→M10: CandidateSet, K, native sample grid ve valid mask.
- M10→M11: `CandidateFeatureBundle` + `SafetyScoreBundle`; asıl öğrenilmiş critic ile PPO value-function birbirinden ayrıdır.
- M11→M12: j ve `Δv[4], Δd[4]`, latent bağlam ve logprob.
- M13→M17→M19: proposal/accepted/actual ayrımı; safety intervention score leak'i engeller.
- M21→CriticTrainer (offline only): expert episodes, visibility truth, multi-target mask, counterfactual labels.
- M20→M19: native benchmark, same-evidence classical+NMPC, privileged expert, strong advanced planning challenger farklı karşılaştırma flag'leri.

## API sınır testi: reddetme koşulları

1. `PolicyObservation` içinde `future_gt`, `oracle_score`, `carla_actor_truth` varsa FAIL.
2. `SafetyScoreBundle` checkpoint veya calibration version yokken `PROBABILITY_CALIBRATED` işaretlenirse FAIL.
3. Offline `TeacherTargetSet` online policy girişine bağlanırsa FAIL.
4. Öğrenci için görünmeyen aktör `ABSENT` olarak etiketlenirse visibility audit FAIL.
5. Actor observed_at eskimiş ama generated_at yeni diye `FRESH` işaretlenirse FAIL.
6. Native candidate index/4sec horizon bozulursa adapter-parity FAIL.
7. Aynı scorer weights farklı latent features ile doğrudan yüklenirse feature contract FAIL.
8. CVaR episode cost yerine tek aday critic output'u kullanılırsa reward design review FAIL.
9. Runtime guardian'a generation ID veya deadline dönülmezse control gate FAIL.
10. Değerlendirme satırında benchmark version/seed/privilege eksikse publication-ready FAIL.

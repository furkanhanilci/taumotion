# τMOTION — Final Hybrid End-to-End Autonomous Driving Architecture

**Documentation release 1.3.1 (12 November 2026). Frozen research topology v1.2: 24 modules and 54 dependency records (52 unique directed module pairs).**

## Positioning

τMOTION is an **Explainable, Risk-Aware Hybrid End-to-End Autonomous Driving Framework**. Camera observations, ego motion, route context and timestamps enter a learning-based motion generation system and end in steering/throttle/brake commands. It is **not** a monolithic network trained end-to-end: foundational planners are frozen; a compact selection/residual RL policy is separately trained; safety supervision and nonlinear model-predictive control are modular, physics-based components. Thus “fully end-to-end trainable” would be technically incorrect.

## Online end-to-end flow and rationale

**M00/M01: trusted observations.** Data provenance gates off future/oracle ground truth; timestamp-aligned cameras, calibration, ego state and navigation are bundled into a SceneEnvelope. Distinct native preprocessing requirements of the frozen planners are preserved.

**M02/M23: independent sensory evidence.** A separate perception/BEV/actor tracking service provides drivable space and multimodal motion forecasts. Age-aware propagation retains the last *actual* observation time and uncertainty. Occlusion and unknown evidence are never conflated with confirmed absence; predicted objects do not become newly measured objects.

**M03/M04/M05/M06: interpretable semantics.** A vision-language teacher describes agents, relationships, hazards, causes, tactical actions and rules. Structured claims, five temporal horizons (now,+1,+2,+3,+4s) and an optional small horizon student provide action-relevant factors. Independent evidence grounds claims as supported, contradicted, unknown, conflicting or stale. Evidence-age gates and calibration prevent uncertain language from acting as hard fact.

**M07/M08/M09: complementary frozen motion experts.** One generator uses vision-language-conditioned flow matching (native 5s/0.1s), another diffusion (native 4s/0.5s). Their native proposals become a common four-second 0.1-second grid with consistent t0, ego coordinates, provenance and valid masks. Initial K=6 (3+3), then 2/6/12 at compute-matched budgets. Interpolation is not a novel future prediction.

**M10: physical candidate metrics plus learned safety/performance critic.** Collision-free likelihood, driveable-area compliance, critical TTC, driving direction, route progress, comfort, curvature and inexpensive MPC feasibility are computed alongside grounded semantic evidence. A trainable multi-head critic predicts appropriate regression or calibrated classification targets and can be trained via supervision, pairwise ranking correction and calibration. It is distinct from PPO's value estimator and CVaR episode-cost estimator.

**M11/M12: risk-aware decision and bounded corrections.** Candidate Attention and GRU process the current K candidates, historical choices and validated reasoning. Reasoning is injected through a confidence/age-gated, optionally zero-initialized residual coupling in the **small decision policy**, not by retraining the frozen motion generators. Hybrid PPO chooses the discrete candidate index j and conditional 8D corrections (four Δv knots, four lateral Δd knots). Initial limits ±2 m/s and ±0.5 m are design parameters; not safety certificates. Constrained cost and CVaR α=.90/.95 capture episode-tail risk while preserving useful progress.

**M13/M14/M22/M15: physics, feasibility and commands.** A hard/soft-constraint supervisor evaluates each policy proposal, tracks rejection or fallback independently, and forwards accepted references to dynamic NMPC. The dynamic bicycle state is `[X,Y,ψ,vx,vy,r,δ,a]`, with `[δ_dot,jerk]` controls. The initial OCP horizon is 4 seconds/40 intervals; 20 Hz is a target control tick, not the frequency of VLM or trajectory generation. A separate deadline guardian rejects stale/generation-mismatched solver outputs before M15's **single-writer** vehicle command adapter.

**M16/M17/M18: asynchronous execution, traceability, XAI.** Perception/VLM/planning may run at different rates, with age-of-information and scene generation identifiers. DecisionTrace records sensed, proposed, accepted, executed and actual behaviors. Claim/horizon intervention is distinguished from a CARLA world intervention; plausibly worded explanations are not automatically faithful causes of the action.

**M19/M20/M21: research, baselines and offline learning.** Evaluation distinguishes NAVSIM v1 PDMS from v2 EPDMS, CARLA/Bench2Drive Driving Score from Success Rate, KITScenes ADE/FDE, and physical risk, comfort, latency and memory. Native classical Autoware and sensor-matched classical planner + shared NMPC are different baselines; AutoE2E BEV+GRU is already M20 baseline. CARLA expert data, occlusion truth, multi-target proposals and future-privileged labels remain offline (M00/M21), never online policy inputs.

## What was already incorporated from AutoE2E

The final architecture **already** defines structured reasoning taxonomy (M04), horizon-aware reasoning/student (M05), zero-init controlled reasoning coupling and GRU decision memory (M11), reasoning faithfulness interventions (M18), fast temporal BEV/GRU planning *baseline* (M20), inference-speed benchmark techniques (M16) and permitted data adapters (M21). This release does not add a third mandatory active planner nor assert the full AutoE2E temporal BEV backbone is copied into M02. A fast third planner is only an optional candidate-diversity experiment.

## Training separation

Offline expert collection/visibility labels → multiple valid target trajectories and carefully evaluated counterfactuals → structured semantic teacher labels → compact horizon student and safety-critic supervised/ranking/calibration training → supervised candidate ranker → actual CARLA on-policy hybrid PPO and optional CVaR. Simulator privileged objects and future observations may generate offline labels; inference inputs use causal sensors and authorized route only. A logged trajectory’s one observed future is not valid ground truth for every unexecuted candidate without additional simulation.

## Expected benchmark potential, NOT measured results

| Benchmark | τMOTION conditional point estimate | Plausible scenario band | Ambitious scenario |
|---|---:|---:|---:|
| NAVSIM v1 PDMS | 92.5 | 91.5–93.5 | 94–95 |
| NAVSIM v2 navhard EPDMS | 53 | 48–58 | 59–62 |
| Bench2Drive Driving Score | 82 | 75–85 | 88–92 |
| Bench2Drive Success Rate | 60% | 50–65% | 70–80% |
| KITScenes 3s ADE | 0.60m | 0.55–0.70m | 0.48–0.55m |
| KITScenes 3s FDE | 1.55m | 1.35–1.85m | 1.15–1.35m |

These values are **conditional engineering judgments, neither observations nor statistical prediction intervals**. The newer stretch target of ADE≤0.565m and FDE≤1.397m matches the earlier published motion-planner baseline level, but does not replace the conservative point estimate. AutoE2E old KITScenes 202-keyframe results differ from canonical 11,035 case results. Published protocols may differ by camera/route/privilege and version. Classical Autoware does not have a verified like-for-like common score in the source archive; no number is invented.

## Approved identity and reference sources

The approved logo is the **original, unedited PNG** at `assets/brand/TAUMOTION_APPROVED_FINAL_LOGO_2026-11-12.png`, a violet/cyan tau integrated with a sleek car **silhouette without roof LiDAR**. It supersedes older visual approvals without deleting historical art. Research diagrams remain separated by Turkish/English and use generic function labels; source provenance remains in `docs/reuse-register-v1.2.md` and `specs/source_pins.json`.

## Module interface inventory (all 24, frozen)

| Module | Function | Input | Output | Why needed |
|---|---|---|---|---|
| M00 | Data privilege registry | Data/source manifests | Allowed observation view | Isolate oracle and future labels |
| M01 | Scene synchronization | Cameras, ego, calibration, route | Timestamped SceneEnvelope | Preserve native inputs and frames |
| M02 | Independent perception | Permitted sensor history | Actors, map, forecasts, visibility | Test semantic claims against separate sensory evidence |
| M03 | Semantic VLM | Causal images and route context | Rationale and claim proposals | Represent rules, intent and scene meaning |
| M04 | Structured reasoning | VLM proposals | Actor-linked claim taxonomy | Make semantics testable and intervenable |
| M05 | Horizon reasoning / student | Permitted BEV history or causal teacher representation | 0–4s semantic features | Separate current evidence from future intent and reduce teacher cost |
| M06 | Grounding / calibration | Claims, actor evidence, age | GroundedClaim with masks | Distinguish support, contradiction, unknown, conflict and stale |
| M07 | Flow-based planner A | Native camera/ego history | Frozen native A candidates | Provide first pretrained proposal family |
| M08 | Diffusion planner B | Native front view / ego features | Frozen native B candidates | Test complementary proposal errors |
| M09 | Candidate normalization | Native A/B trajectories | Common frame, effective horizon and masks | Enable physical comparison without invented forecast |
| M10 | Physical features + learned safety critic | Candidates, scene, grounded claims, prior control | Features + typed SafetyScoreBundle | Study false-safe ranking; retain physical checks |
| M11 | Risk-aware recurrent selector | Candidate features, critic, grounded horizons | Candidate j, residual distribution, values | Learn evidence-conditioned choice with small policy |
| M12 | Bounded residual | Selected candidate and 8D action | Smooth speed/lateral reference | Refine locally while generators stay frozen |
| M13 | Feasibility supervisor | Refined proposal, fresh scene, limits | Accepted reference or fallback request | Reject infeasible proposals before control |
| M14 | Dynamic NMPC | Accepted reference, ego, constraints | Solver result and tracking/slack diagnostics | Track with explicit vehicle dynamics |
| M15 | Single actuator writer | M22-authorized normal/fallback command | Steer/throttle/brake + trace | Enforce one command owner and actuator calibration |
| M16 | Scheduling / freshness | Worker queues, clock domains, resource budget | Requests, age/deadline and profile trace | Bound queues and measure co-load latency |
| M17 | Decision trace / versions | All proposal, control and provenance packets | Replayable decision/episode record | Attribute sampled, accepted and executed actions |
| M18 | Counterfactual / human XAI | Fixed-state interventions and paired scenes | Faithfulness and human understanding metrics | Separate explanation fluency from causal effect |
| M19 | Benchmark / statistics | Versioned runs, splits, seeds | Protocol-specific scores and uncertainty | Avoid sensor/compute/protocol confounding |
| M20 | Native and shared-control baselines | Baseline-specific inputs/checkpoints | Comparable native / shared-NMPC runs | Compare strong existing systems and experts fairly |
| M21 | Data / transfer / offline teacher | Expert episodes and permitted training data | Visibility labels, multi-target sets, versioned datasets | Preserve diversity, iterative learning and transfer |
| M22 | Independent deadline guardian | Solver result, generation, deadline, fresh snapshot | Authorized normal/fallback command | Reject late or stale results without blocking on solver |
| M23 | Evidence time propagation | Native tracks and original capture times | Retimed predictions, age and uncertainty | Bridge slower perception without pretending new observation |

The table translates the effective module contracts; canonical identifiers remain M00–M23. The learned critic and offline teacher extensions are included in the primary JSON fields. For an exhaustive module-by-module explanation including failure policies and source reuse, read `docs/FINAL_ARCHITECTURE_MASTER_TR.md` plus `docs/components.md`. The exact 54 dependencies are in `specs/architecture_edges.json`. Implementation and actual performance remain separate future work; defining the research architecture is considered complete for this documentation release.


## Publication review v1.3.1

[Detailed review](prepublication-review-v1.3.1.md) and [integration contract](integration-contract-v1.3.1.md) resolve stale module fields, offline edge scopes, effective asynchronous horizon, per-head metric semantics and native environment compatibility. The nominal 4s grid cannot be extended by retiming a delayed 4s forecast: compare the shared valid remainder, mask padding and use an explicit shorter-horizon profile or fallback. The numerical benchmark scenarios remain subjective planning assumptions without measured or calibrated empirical support. All research tracks and the approved logo are retained.

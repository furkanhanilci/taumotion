# Scientific architecture walkthrough

This explanation describes the effective v1.3.1 architecture using scientific method names. Its 24 modules retain the two frozen motion generators, independent evidence, grounded temporal reasoning, learned safety critic, recurrent risk-sensitive policy, bounded residual, dynamic predictive control, independent command guardian, data cycle and explanation studies.

## Inputs, provenance and synchronization — M00–M01

The system begins with camera history, calibration, ego pose and motion, steering state, permitted route information and observation timestamps. M00 declares which information may be used during inference. Future images, simulator actor truth, counterfactual outcomes and oracle trajectory scores belong to training or evaluation paths. Online observations are constructed from an allowlist, rather than obtained by deleting a few forbidden keys from a privileged object.

M01 converts these inputs into a synchronized scene envelope while preserving each pretrained model's native preprocessing. Different cameras, resolutions and temporal histories remain explicit. Sharing a physical traffic scene does not imply that two models receive equal information. Coordinate transformations must jointly handle position, orientation and time, with consistent physical units and a declared ego frame.

These modules prevent integration errors from being mistaken for algorithmic shortcomings. An inverted lateral axis, mismatched camera calibration or stale ego state can invalidate downstream behavior even when each model executes correctly. Simulation time, wall-clock latency and operational decision time therefore remain distinct clock domains.

## Independent perception and time-aware evidence — M02, M23

A visual perception pipeline estimates bird's-eye-view features, actor detections and tracks, drivable space, occupancy and motion forecasts. Traffic-rule evidence also needs association: a detected traffic light must be linked to the relevant lane and stop line before its state can constrain driving. Unknown state and uncertain association remain visible to downstream modules.

This independent evidence path provides a geometric basis for checking language claims. Independence refers to a separate model and observation path; it does not establish independent statistical errors. Poor visibility or a domain shift may affect both branches. Detection confidence therefore requires validation before being interpreted as probability or converted into a state covariance.

Visibility is itself evidence. An actor may be occluded, outside the field of view or too uncertain to associate. Missing evidence is not automatically evidence of absence. M23 bridges gaps between expensive perception updates using native forecasts or short-gap kinematic filtering. Predicted state retains its original capture time, prediction flag, uncertainty and remaining valid horizon.

Retiming cannot discover a newly emerging pedestrian or refresh an unobserved light color. Expired evidence becomes stale or unknown; it must not silently disappear and leave an apparently empty road. This makes observation age a decision variable rather than an implementation detail.

## Structured semantic reasoning and grounding — M03–M06

The semantic model interprets scene meaning, rules, intent and possible hazards from causal visual observations. It produces a short rationale and semantic claims before the driving decision. M04 maps these outputs into actor, relation, hazard, cause, action, rule and horizon fields. An actor reference must be associated with a scene entity or remain unknown.

The structured representation makes claims individually inspectable and suitable for controlled interventions. A persuasive paragraph is not treated as an indivisible control instruction. M05 separates present context from approximately +1, +2, +3 and +4 seconds. A current position observation and a possible future crossing have different evidential status.

A compact horizon student can learn from offline teacher labels using permitted perception features, ego history and route context. Its computational benefit must be measured across the full dependency chain: a small head that still needs a large online language backbone has not removed that backbone's inference cost. Future observations may help construct training targets but cannot enter the student's inference inputs.

M06 checks claims against actor associations, visibility, geometry, forecast compatibility and observation age. Its output states are `SUPPORTED`, `CONTRADICTED`, `UNKNOWN`, `CONFLICT` and `STALE`. A future claim is checked for consistency with available forecasts, not certified as a future fact.

Grounded semantics enter the small policy through an evidence-sensitive gate. One representation is `z = z_base + α · g(evidence, age) · P(z_reason)`. The projection maps reasoning features into the policy space; the gate limits unreliable or stale influence. A near-zero initial coupling can preserve base behavior while a normally initialized projection retains a learning path. The frozen generators' internal layers are not modified by this external fusion mechanism.

## Two frozen proposal families and a common contract — M07–M09

The first generator uses conditional flow matching to produce trajectories through a learned continuous transport process. The second uses iterative diffusion denoising under its own visual and ego conditioning. Both retain their pretrained weights in the main protocol. Their different representations and sampling mechanisms may supply complementary alternatives, but this must be tested: different model families can still make correlated errors.

The nominal candidate pool is K=6, with three proposals from each generator. K=2/6/12 and matched-compute experiments distinguish useful diversity from extra sampling expenditure. Reusable native backbone features may reduce repeated computation, but identical candidate counts do not imply equal compute.

M09 preserves native points, seeds, sample times and source metadata while transforming trajectories into a common frame. The selected native configurations offer approximately five seconds at 0.1-second spacing and four seconds at 0.5-second spacing. Their nominal comparison uses four seconds on a 0.1-second grid. Interpolation does not add predictive information to the coarser output.

Asynchronous operation adds a crucial validity constraint. For source time `t_i`, native horizon `H_i` and decision time `t_d`, remaining coverage is `t_i + H_i − t_d`. A four-second prediction received 0.3 seconds later contains only 3.7 seconds of future coverage. Participating candidates are compared over a common valid overlap. Padded positions remain masked, duration-sensitive features are normalized, and downstream refinement/control use the same valid horizon or a declared fallback.

This contract prevents smooth but fabricated trajectory tails from producing misleading risk estimates. It also records when one generator frequently contributes fewer valid candidates, so that availability and latency cannot be hidden inside the reported selection quality.

## Physical features and a learned safety/performance critic — M10

Each candidate receives explicit geometric and dynamic features: predicted collision proximity, time to collision, road-area compliance, direction, progress, velocity, acceleration, jerk, curvature, generator disagreement, observation age and a control-feasibility proxy. These features remain available when the learned critic is introduced.

The compact critic adds multiple output heads for safety, compliance, progress, comfort and tracking feasibility. Different targets can require classification, regression or ranking. Each head has a target definition, output type, label protocol, horizon, validity mask and calibration status. A sigmoid output is not automatically a calibrated event probability. A no-at-fault-collision metric is also distinct from the probability of avoiding every physical collision.

Training combines supervised losses, candidate ranking and calibration. False-safe ranking receives explicit attention: an unsafe alternative should not appear reliable simply because its predicted progress is high. Evaluation includes incorrect top-choice selection, ranking regret, threshold-dependent false-safe rates and calibration across visibility groups. Class prevalence and label source accompany these results.

Reusable scoring code provides a structure, but its pretrained heads expect the feature representation on which they were trained. Matching tensor dimensions alone cannot establish compatibility. The bridge is an explicit canonical feature representation and a small separately trained critic. This critic is distinct from the policy's reward-value and episode tail-cost value networks. Its score cannot override a physical feasibility check.

## Recurrent candidate choice and episode tail risk — M11

Shared candidate encoding and attention compare the available alternatives. A gated recurrent unit maintains recent context so that choices can account for prior evidence and control outcomes. Candidate permutation tests check that arbitrary array ordering does not create a decision advantage. Recurrent state is reset at episode boundaries and handled consistently during sequence training.

The action combines a categorical candidate index and a continuous correction conditioned on that index: `π(j,u|s) = π(j|s) · π(u|s,j)`. Invalid candidates are masked. If no usable option remains, an explicit stop/fallback branch avoids constructing an empty categorical distribution. Proximal policy optimization combines the discrete and conditional continuous likelihood terms, including the transformation that bounds the residual.

When supervision changes a proposal, the sampled action and executed action remain different trace fields. Training retains the likelihood of the action actually sampled by the policy; it does not substitute a likelihood for the supervisor's replacement command. The supervisor is part of the training environment, and intervention frequency is itself evaluated.

Performance reward encourages route progress, completion and comfortable motion. A separate episode cost captures relevant violations, near-miss severity and control failures. Individual event metrics remain visible so an aggregate objective cannot conceal a deterioration in one safety dimension.

Conditional value at risk concentrates on the upper tail of episode costs: `CVaRα(C) = minη [η + E(max(C−η,0))/(1−α)]`. The design studies reward improvement under a tail-cost budget, with quantile estimation and a nonnegative multiplier. Initial settings include α=0.90 and α=0.95 sensitivity studies. Here CVaR is an episode-level training objective, not a scalar computed only from the six current trajectory scores.

Complete episodes, consistent behavior-policy versions, effective tail counts and quantile stability are needed. Old trajectories from different policies cannot silently become fresh on-policy evidence. Stress training and natural test distributions also yield different tail risks. The formulation does not imply guaranteed convergence, formally certified safety or zero collisions.

## Bounded residual, supervision and predictive control — M12–M15, M22

M12 uses eight continuous dimensions: four speed-offset knots and four lateral-offset knots. Smooth interpolation distributes the correction over the valid horizon. Initial bounds are approximately ±2 m/s and ±0.5 m, to be validated against the vehicle and operating conditions. Start-state continuity, nonnegative speed, updated heading and post-correction curvature and risk checks prevent the small correction from bypassing the physical contract.

A bounded residual enables local improvement without retraining either large generator. It cannot be assumed to recover a maneuver absent from every useful candidate. M13 therefore checks the refined reference against fresh scene evidence, vehicle limits, road geometry and valid horizon. Rejections and fallback requests preserve the proposal that caused them. A previous reference may continue only while its remaining segment passes current validity checks.

M14 tracks the accepted reference using dynamic nonlinear model predictive control. The nominal state is `[X,Y,ψ,vx,vy,r,δ,a]`, and control variables are steering rate and jerk. Tracking costs compete with smoothness and slack penalties under actuator constraints. Vehicle mass, inertia, axle geometry and tire behavior need identification; low-speed dynamics require a regularized or blended formulation.

The nominal optimization horizon is four seconds with forty 0.1-second intervals. Control targets 20 Hz. Shorter or nonuniform grids, warm starts, partial condensing and real-time iteration variants remain comparisons. A low-cost proxy normally screens all candidates before full optimization tracks the chosen reference. Top-N optimization experiments test whether additional solves improve selection enough to justify their cost.

M22 is an independent timing and validity process. It checks episode, generation, snapshot, deadline and command age without waiting for the blocking solver. Late results cannot overwrite newer control ticks. The guardian authorizes a valid result, a still-valid continuation, or a calibrated fallback profile. A commanded stop is not a proof that stopping will avoid every unseen obstacle or friction change.

M15 is the single actuator writer. It converts the authorized physical command into calibrated steering, throttle and brake signals. Normal and fallback commands share the same output authority. Saturation, throttle/brake conflicts and the actual applied command are recorded, allowing the research to distinguish proposed safety from executed behavior.

## Multirate scheduling and resource accounting — M16

The architecture compares a synchronous reference, asynchronous teacher plus dual generators, a compact external semantic student plus dual generators, and conditional generator invocation. All profiles retain the declared research functions. Reducing inference frequency does not permit discarding native history frames required by a pretrained model.

An expensive live worker keeps at most one pending request beyond its running job; new waiting work replaces older pending work. Requests carry source observations, generation IDs and deadlines. Logical cancellation does not necessarily interrupt an active accelerator kernel, whose residual cost remains part of profiling.

Information age is measured from the observation underlying a result, not its completion timestamp. History span, newest observation age and cross-sensor skew are separate measures. Compatible semantic and planning endpoints may share model weights, but different prompts or image histories do not guarantee shared cached activations.

Profiling includes model residency, activations, process contexts, rendering, preprocessing, communication and queue delay. Two device memories are not automatically one combined memory pool. At 20 Hz, **50 ms belongs to the whole critical control path**: snapshot, reference checks, solver feedback, command gate, publication and jitter. Solver preparation remains accounted for even when scheduled separately. Actual timing and safe observation-age limits remain to be measured.

## Offline expert supervision and staged learning — M21

Expert demonstrations, recorded scenes and simulation episodes are versioned with route, weather, scenario, sensor and seed metadata. Label builders may access future observations or world state, while learner inputs remain causal. Cache fingerprints include preprocessing, source models, split and annotation versions. A mismatch must trigger rebuilding rather than silent reuse of stale labels.

Visibility labels address learner–expert asymmetry: an expert can react to an actor the learner cannot observe. Offline instance, depth and actor-state annotations identify such conditions without making them runtime sensor inputs. Multi-target supervision recognizes that a single demonstrated action is not the only acceptable response. Alternative valid trajectories can supervise ranking and critic training.

A recorded future, however, belongs to the action that actually occurred. It cannot prove the outcome of every unexecuted alternative. Counterfactual labels require an appropriate rollout or a clearly declared approximation, with validity masks where evidence is insufficient.

The learning sequence is native-output and adapter verification, candidate caching, critic/student supervision, ranking initialization, a limited closed-loop PPO pilot, bounded residual learning, and then mean-risk/CVaR studies. Freezing the large models removes their gradient updates, not their inference cost during episode collection. Iterative collection uses training failures; held-out test scenes remain outside the data-improvement loop.

## Explanation, intervention and research evaluation — M17–M20

M17 links source observations, candidate sets, critic outputs, policy state, sampled actions, residuals, accepted references, solver diagnostics, guardian decisions and actual motion. This lineage reveals whether an outcome arose from the original policy, a physical supervisor or a timing fallback.

M18 asks whether an explanation is supported, whether it influences the decision, and whether that influence is appropriate. Candidate/evidence snapshots, recurrent state, random state and solver warm starts can be held fixed while a semantic claim or horizon feature is changed. Separate world interventions alter a physical actor or signal and test the system's response; because sensory inputs change too, these do not isolate the semantic channel by themselves.

Human studies measure comprehensibility, trust calibration and the ability to distinguish correct from incorrect decisions. Increased confidence in a fluent but misleading explanation is not considered successful explanation quality.

M19 reports trajectory agreement, route completion, driving success, collisions and violations, proximity, comfort, control feasibility, tail risk, latency and memory under explicit protocols. A safer alternative may differ from the human reference path, so imitation error and safety are distinct outcomes. Paired routes, multiple training and traffic seeds, clustered uncertainty and transparent failures support analysis.

M20 retains strong native pretrained challengers, a complete classical stack, a privileged expert, a same-evidence rule-based planner with shared predictive control, and a lightweight temporal visual planner. Other comparisons isolate individual generators, fixed candidate sets, heuristic ranking, supervised ranking, critic heads, recurrence, residual channels and risk objectives.

Native-system comparisons answer a different question from fixed-candidate selection studies. Matched K controls proposal count; matched compute controls resource expenditure; shared control reduces execution differences. Sensor masking inside an already pretrained model may create out-of-distribution inputs and does not reproduce equal training information. Oracle best-of-K analysis is an offline opportunity estimate, never a deployed input.

## A complete decision at an occluded crossing

At an intersection, a cross-traffic vehicle is visible while a pedestrian is partly occluded. Synchronization establishes which images and ego state each branch observed. Independent perception supplies tracks and uncertain visibility; propagation retains the last real capture time. The semantic branch proposes a yielding rationale and temporal hazard claims, which grounding supports or leaves unresolved.

Meanwhile the frozen generators propose different progress and braking profiles. Their trajectories are aligned over the same valid remaining horizon. Physical features and learned scores expose risk, comfort, progress and tracking implications. The recurrent policy chooses a candidate and a small correction. Supervision checks the refined reference; predictive control computes a constrained command; the guardian checks that the result is still timely and valid.

The single actuator writer applies the authorized command and a new observation closes the loop. Offline analysis can then ask whether the pedestrian claim changed the selection, whether the critic correctly ranked the alternatives, whether supervision intervened, and whether a person understood the explanation of the action actually executed.

## Research scope and status

The design retains RQ1–RQ11, E1–E24 plus E10-H, and N0–N9/C0–C10 baseline families. These cover generator complementarity, grounding, temporal reasoning, visual-versus-language representation, critic calibration, visibility, multi-target supervision, recurrent choice, residuals, CVaR, predictive control, scheduling, robustness, compression, human explanation studies, data diversity, iterative collection and exploratory domain/simulation transfer.

“Hybrid end-to-end” describes pretrained learned motion generation integrated into the complete driving system. The full stack is not trained as one monolithic differentiable network. It remains an architecture specification: native inference, adapter parity, small-model training, closed-loop driving and hardware timing are unverified. Detailed method contracts, source attribution and implementation responsibilities remain in the repository's technical records.

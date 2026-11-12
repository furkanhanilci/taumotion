# Yeni deneyler E19–E24: ön kayıt tasarımı

**E19 — Safety Critic:** physical-only vs multi-head critic vs +grounding vs +visibility vs +MPC; frozen candidate cache, calibration, false-safe and ranking regret. (M10, M11)

**E20 — Multi-target teacher:** single expert target vs valid multi-target mask vs privileged future teacher labels with and without actual counterfactual rollout; reward and safe-set recall. (M21, M11/M12)

**E21 — Occlusion / learner–expert asymmetry:** privileged world-state expert vs sensor-compatible baseline; fully visible / partial / missing actor, false-grounding labels, intervention costs. (M02, M06, M20, M21)

**E22 — Strong native challenger:** advanced native planner, two frozen planners, optional diffusion bridge, matched candidate K and GPU-s budget; oracle topK is only analytic upper bound, never deployed selector. (M07–M10, M20)

**E23 — Learned safety critic + hybrid PPO + CVaR:** same critic, same seeds, critic-scores-only selection vs recurrent PPO+residual and CVaR α=.90/.95; tail cost, mean performance, critical violations, solver overrides. (M10–M14)

**E24 — Cross-domain and compute:** NAVSIM1 PDMS / NAVSIM2 EPDMS / KITScenes canonical ADE/FDE / CARLA Bench2Drive DS/SR; P0/P1/P2/P3; 2×A5000 model co-load and P50/P95/P99 AoI, memory, latency. (M16–M21)

**Statistical contract:** 3–5 random seeds initial, scene/route clustered bootstrap, failure transparency, no best-run cherry-picking, predeclared primary endpoint. Any reported performance value includes `source_type=published|rerun|tau_measured|target`, dataset version, sensor privilege, route/seed, checkpoint hash, CI and test count.

See [benchmark matrix](benchmark-matrix-v1.2.md), [critic methods](safety-critic-and-supervision.md), and [verification](verification-v1.2.md).

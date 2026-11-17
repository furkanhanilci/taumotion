# Architecture poster and presentation update

The poster presents the effective v1.3.1 architecture in eight online columns and five offline research columns. Its two-tier organization, colored cards, method icons and feedback path are inspired by the user-supplied reference. The original approved logo is displayed separately above the poster and remains byte-identical.

The artwork uses generic scientific labels. It retains conditional flow matching, diffusion generation, independent perception and evidence propagation, structured temporal reasoning, grounding, a multihead learned critic, recurrent hybrid PPO, episode-level CVaR, an eight-dimensional speed/lateral residual, feasibility supervision, dynamic NMPC, an independent guardian and a single actuator writer. Training, visibility, multi-target supervision, benchmarking, human explanation studies and transfer remain in scope.

The figure is a functional overview. Selected arrows do not replace the complete dependency graph. Perception, semantic inference and frozen motion generation are concurrent branches; grounded claims feed the critic and small policy rather than being injected into frozen planner layers. The deadline guardian has a separate responsibility from the solver. The 20 Hz value is a design target.

Files: [SVG](../assets/diagrams/v1_3_1/architecture_poster.svg), [PNG](../assets/diagrams/v1_3_1/architecture_poster.png), [PDF](../assets/diagrams/v1_3_1/architecture_poster.pdf). Regenerate with `python3 tools/build_architecture_poster.py`. The PNG is rendered from the vector PDF, and the SVG retains editable text and shapes. Artwork adds no runtime implementation or new research module.

The expanded [scientific walkthrough](scientific-walkthrough.md) explains the methods without named source frameworks. Source-specific attribution remains in the separate source and reuse records. The original architecture specification and report remain version 1.3.1; this is a presentation and explanation update.

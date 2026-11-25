# Trash-detecting TurtleBot3: joint project plan (Autonomous Systems + Edge AI)

> v2.1, 25/11/2026: audit + rewrite of the 24/11 plan. Added that every lecture is covered, the professor's likely expectations, last year's projects as a reference, and the GitHub workflow.
> Board: https://github.com/orgs/TrashRobotEdge/projects/1 · Repos: `TrashRobotEdge/TrashLocalisation`, `TrashRobotEdge/EdgeTrash`
> Rule for this doc and the repos: **every decision has a written "because"**. If you can't explain why, it isn't decided.
> `[W1]` = not verified yet, must be checked in Sprint 0. Never treat it as a fact.

---

# Part A: Shared

## 1. Context & fixed constraints
| | Autonomous Systems (AS) | Edge AI (EAI) |
|---|---|---|
| Brief | Extend TB3 with extra sensors → URDF update → simulation → ROS2 packages with behaviours using the extension → real robot *if time permits* (AS1 p.39) | NN-based edge app → model optimisation + transfer to edge devices → **benchmark protocol + results** (EA1 p.27) |
| Grade | GitHub repo (packages + docs) = grade 1 · demo **19/01** = grade 2 (AS1 p.40) | Report ≤15 p + reproducible repo · PoC 15 min + 5 min Q&A on **20/01** (EA1 p.30) |
| Repo | **TrashLocalisation** (ROS2 workspace) | **EdgeTrash** (data, models, benchmark, report) |

- **Work window: 4 weeks, 25/11 → 21/12.** No work over the break. January = attend lectures + deliver only.
- **Equipment (fixed):** OAK-D Pro (Myriad X VPU) · Pi5 + Hailo-8L (13 TOPS, INT8) · Pi4 (loose board, probably the TB3 computer running Docker `[W1]`) · inline USB-C power meter · TB3 confirmed, **chassis not received yet**.
- **Stack:** Ubuntu 22.04, ROS2 Humble, Gazebo (gz-sim, Fortress per the workshop slides), CycloneDDS.
- **Professor's repo** (`gerald-rocher/Turtlebot3`, checked 25/11): has `projects/turtlebot3_descriptions/urdf/turtlebot3_burger_oak_d_pro.urdf` (RGB + depth 640×480 @30 Hz, HFOV 1.047 rad, **no depth noise, no camera_info**), launched with `PROJECT_MODEL=turtlebot3_burger_oak_d_pro` + `projects_empty_world.launch.py`. Lab packages `turtlebot3_fsm`, `turtlebot3_braitenberg` (`lidar_utils.py`, `diffdrive.py`). **No behaviour tree or micro-ROS material.**
- **Professor = manager** (EA1 p.29): we're autonomous. When something breaks we explain why and propose alternatives.

**Every lecture is covered: thin but real.** "Covered" = one working integration + one ADR + one doc paragraph, not depth everywhere. Lectures after 21/12 are **worked ahead** from the lab PDFs and the official docs. If a week slips, these items are protected and depth slips instead (rung 2, the 2nd input size, extra reps).

| Lecture | How we cover it | Sprint |
|---|---|---|
| AS DDS (24/11) | QoS profiles, deadline QoS, `cyclonedds.xml` | S0–S1 |
| AS URDF/sim (01/12) | OAK-D Pro URDF extensions + can world | S1 |
| AS Architectures/BT (08/12) | BT replaces FSM (likely BehaviorTree.CPP + Groot2, as last year) | S2 |
| AS Braitenberg (15/12) | Approach as a Braitenberg vehicle (lab PDF already available) | S2–S3 |
| AS SLAM/planning (05/01) | Cartographer map + Nav2 goal to the localised can (lab PDF already available) | S2–S3 |
| AS micro-ROS (12/01) | **Backlog**: no microcontroller, last lesson. Ask the professor whether a documented design counts | — |
| EAI Benchmarking (25/11) | The protocol (§14) | S0–S1 |
| EAI TinyML (02/12) | Decide after the lecture (backlog issue): no MCU, so likely a tiny model at the low end of the Pareto front | S1–S2 |
| EAI NXP NPU/TFLite (09/12) | Do the lab, reuse its TFLite INT8 flow, run our model on the NXP board during the lab as one extra data point | S2 |
| EAI ONNX Runtime (16/12) | ORT rows in the matrix + ORT profiler/graph optimisations | S2–S3 |
| EAI TVM (06/01) | TVM-compiled model on the Pi4/Pi5 CPU as one more runtime row (cross-compile on x86) | S3 |

## 2. Audit of the v1 plan
| # | Finding | Why it matters | Decision |
|---|---|---|---|
| 1 | v1 had 6 sprints + holiday work | Real budget is 4 weeks; SLAM, TVM, micro-ROS lectures land after we stop | 4 sprints. Every lecture still covered, thin but real, worked ahead (table above). micro-ROS → backlog (no MCU). Trash map → stretch |
| 2 | Device hello-world in Sprint 2, protocol frozen 14/12 | Toolchain failures found in week 3 = no time left; the slides say write the protocol before measuring | S0: protocol steps 1–5 + hello-world on every device with pretrained zoo models + idle power. Freeze end of S1 |
| 3 | Matrix = 5 devices × 3 precisions × 3 inputs × 3 runtimes = 135 configs | Infeasible, and many cells don't exist (Hailo = INT8 only, VPU = FP16 only, no laptop device) | Valid cells only (~18). One factor at a time, then cross (Benchmarking p.24) |
| 4 | "Whole pipeline" but one benchmark level | Pi5 + Hailo is supported on Raspberry Pi OS, ROS Humble wants Ubuntu 22.04 `[W1]`: ROS on Pi5 is a risk | **L1** = ROS-free, replayed frames, every device. **L2** = in ROS, robot config, capture → `cmd_vel` |
| 5 | OAK on replayed frames | Replayed frames must be sent host → VPU (XLinkIn), which never happens live | Measure and report that transfer. Live camera only for the sensor stage (p.13) |
| 6 | Timestamps not defined | `use_sim_time` makes latency meaningless; 2 machines need synced clocks | No sim time in benchmarks, chrony on multi-machine. Always state both timestamps |
| 7 | Latency requirement may not separate devices | At 0.22 m/s, 200 ms = 4.4 cm travelled | Add requirements that actually discriminate: Pi4 CPU headroom, energy vs battery, detection range vs input size |
| 8 | Sim model lacks camera_info and depth noise | Localiser needs intrinsics; EAI needs a sensor-uncertainty section | These extensions = our real "URDF update" contribution |
| 9 | Gazebo auto-labelling on the critical path | Complex, and it's sim data anyway | Hand-label real OAK-D photos. Auto-label = optional |
| 10 | One model + "comparison" | Benchmarking models is a core requirement; not every model compiles everywhere | 2 NN families chosen by a compile test in S0 + HSV baseline |
| 11 | Unclear where the inference code lives | Duplication across repos; EAI must reproduce without ROS | ROS-free lib in EdgeTrash, thin ROS node in TrashLocalisation |
| 12 | DDS course not used | Default QoS queues stale frames → fake latency | `sensor_data` QoS, depth 1. Deadline QoS = runtime check of the latency requirement |
| 13 | Robot hardware assumed | No chassis, OAK power on Pi4 unknown, Docker image unknown | Sim demo = guaranteed baseline. Robot = Pi4 + OAK on-camera inference, Pi5 + Hailo bench only |
| 14 | Stream swaps every 1–2 sprints | Too much context switching in 4 weeks | No roles: sprints → issues → anyone picks. Learning through cross-review |
| 15 | Report written in the last sprint | Report is due the day after the demo; AS grade 1 is the docs | EAI: LaTeX filled as we go. AS: in-code docs + markdown are the source, a short LaTeX PDF is assembled at the end (cheap if the docs are kept up) |
| 16 | No comparison with what was graded before | Last year's projects show the professor's floor | Reference section below: match their AS scope, beat their benchmark |
| 17 | Things the professor likely wants that were missing | Seen in last year's repos + the slides | Added: DEMO.md/QUICKSTART, reproducible env + one-command launch, CPU pruning experiment, depth↔lidar **sensor fusion** check, computation-graph figures, chase the chassis |
| ✓ | Swappable backends, HSV placeholder, requirement-driven goal, record & replay, point-B meter, ADRs, sim fallback | Sound | Kept |

## 3. Scope ladder (simple first, growth paths ready)
| Rung | Task | AS adds | EAI adds |
|---|---|---|---|
| **1 (MVP)** | Find and approach **Coca-Cola cans** indoors | Full loop: detect → localise → approach → stop | 2 models + HSV, full benchmark |
| 2 | **All cans** | Nothing new (same interface) | Generalisation test. **HSV fails here, which is the honest case for using an NN** |
| 3 | Multi-class (cans, bottles, pizza boxes) | Per-class behaviour | Multi-class mAP, bigger models, more stress on the edge devices |
| 4 | Multi-class over a **large zone** | SLAM + Nav2 exploration, trash map | Long-run stability, energy per area covered |

- Commit to rung 1. Collect rung-2 test images from day 1 (cheap, and it makes the NN case).
- Rungs 3–4 are written up as "future work" with what we'd change, unless S3 closes early.

## 4. Architecture & interfaces
```
OAK-D Pro (RGB+depth) ─► trash_detector ─Detection2DArray─► trash_localizer ─PoseStamped(odom)─► behaviour (FSM→BT) ─► cmd_vel
                         backend ∈ {hsv | onnx | tflite | hailo | oak}        ▲ depth + camera_info + TF2          ▲ /scan safety stop
                         (calls edgetrash lib: preprocess → infer → postprocess, per-stage timers)
```
- **edgetrash** (EdgeTrash repo): pure-Python lib, no ROS. Same code for L1 bench, L2 and the robot, **because** one implementation = what we measure is what runs.
- **trash_detector** (TrashLocalisation): thin ROS wrapper around `edgetrash`, backend = ROS parameter.
- Topics: `rgb_camera/image`, `depth_camera/image`, `camera_info` (to add in sim) → `/trash/detections` (`vision_msgs/Detection2DArray`) → `/trash/target` (`geometry_msgs/PoseStamped`, frame `odom`) → `/cmd_vel`.
- QoS: images `sensor_data` with depth 1, **because** we want the newest frame, not a queue. Detections reliable + deadline = latency budget.
- Each repo's README links to the other. EdgeTrash pins the commit of TrashLocalisation used for L2.

---

# Part B: Autonomous Systems (TrashLocalisation)

## 5. Robot model & simulation
- Start from the professor's OAK-D Pro URDF, **because** rewriting it teaches nothing new and costs a week.
- Our extensions (= the "URDF update" deliverable):
  - add `camera_info` (sensor + bridge), **because** the localiser needs intrinsics
  - add depth noise from **our own OAK-D measurements** (§10), **because** a sim with perfect depth hides the real failure modes
  - match mount pose and FOV to the real OAK-D Pro on our chassis `[W1: datasheet + measure]`
- Gazebo world: a room + Coca-Cola can models (+ other cans for rung 2) + a few obstacles.

## 6. Perception → localisation
- `trash_detector`: HSV backend on day 1, **because** the robotics stream never waits for the ML stream.
- `trash_localizer`: bbox centre + median depth in the box → 3D point via intrinsics → TF2 to `odom`.
- Log per-stage timestamps from the start (needed for L2).

## 7. Behaviour
- **FSM first** (SEARCH → DETECTED → APPROACH → ARRIVED → DONE → SEARCH), building on the lab's `turtlebot3_fsm` + `lidar_utils`, **because** it's known, fast to get working, and gives a comparison point.
- **BT after the 08/12 lecture**, **because** it's a lecture we must cover. Library per the lecture. Evidence points to BehaviorTree.CPP + Groot2 (what Nav2 uses, and what last year's TurtleShot used). FSM kept in the docs as the comparison.
- Approach = visual servoing (centre the bbox, depth for distance), written as a **Braitenberg vehicle** (bbox offset = "light sensor", excitatory wiring = attraction), **because** that covers the 15/12 lecture for almost no extra code.
- **SLAM/Nav2 (thin)**: Cartographer map of the test room + a Nav2 goal sent to the localised can when it's out of direct reach, **because** it covers the 05/01 lecture. The lab PDF (`Workshop_FSM_SLAM.pdf`) already gives the commands.
- **Sensor fusion (cheap)**: cross-check the depth-camera distance against the lidar beam in the same direction, **because** the EAI brief mentions fusion and it catches bad depth readings.
- Lidar safety stop always overrides the behaviour.

## 8. Real robot
- Robot config: **Pi4 + OAK-D Pro with on-camera inference**, **because** it leaves the Pi4 CPU for ROS/drivers and avoids powering a Pi5 + Hailo from the TB3 battery. Pi5 + Hailo = bench only (L1 replay).
- `[W1]` checks: chassis ETA · which Docker image/OS the Pi4 runs · can the Pi4 USB power the OAK-D Pro (else powered hub/Y-cable) · depthai ROS driver on Humble.
- No chassis by S2 → sim demo + bench video of the OAK pipeline. Decided now, not in panic later.

## 9. AS deliverables
- Packages: `trash_description` (URDF ext + world), `trash_detector`, `trash_localizer`, `trash_behaviour`, `trash_bringup` (one-command launch).
- Docs: in-code docstrings + README (install/run), `DEMO.md` + QUICKSTART, architecture, ADRs, `problems.md`. A short LaTeX PDF is **assembled at the end** from `docs/`, **because** it's cheap if the docs are kept up and easier for the professor to read.
- Reproducible env: pinned setup script or Dockerfile, `cyclonedds.xml`, **one launch command**. Computation-graph figure (`rqt_graph`).
- Demo: sim run (guaranteed) + real run if possible + backup video. Format/length to confirm with the professor.

---

# Part C: Edge AI (EdgeTrash)

## 10. Sensors & uncertainty (report section, measured not cited)
- OAK-D Pro RGB: resolution, FOV, exposure/motion blur at robot speed.
- OAK-D Pro depth: error vs distance (e.g. 0.3–3 m steps), with/without IR projector, can reflectivity, lighting.
- Output: working range of the system (where detection + depth are reliable). This feeds the sim noise model (§5) and requirement R3 (§14).

## 11. Dataset construction
- Capture with **the OAK-D Pro itself** (+ phone as extra), **because** train/test must look like deployment.
- Rung 1: Coca-Cola cans (upright, lying, crushed, partly hidden, distances, floors, lighting). Target ~300–500 labelled images `[adjust after first training]`.
- Rung 2 test set from day 1: other cans, + negatives (red objects that aren't cans → the HSV killers).
- A few labelled sim frames, **because** the NN must also work in the sim demo. Gap measured, not assumed.
- Splits: train / val / test / **calibration (disjoint from test)**, **because** calibrating on test data inflates INT8 accuracy (Benchmarking p.13).
- Labelling tool + conventions written in `data/README` (box tight on the can, occlusion rule). Version + checksums + fixed split seed. Licence of any public data (e.g. TACO) checked.
- Pre-processing (resize method, normalisation, colour order) is part of the dataset spec, **because** it changes accuracy.

## 12. Model selection
- Candidates (the professor recommends models available on every toolchain): YOLO-nano family (YOLOv8n…), SSD-MobileNetV2, MobileNetV2 backbone.
- Criteria, in order: (1) **compiles on Hailo-8L, OAK (.blob) and CPU (ONNX/TFLite)** · (2) accuracy on our test set · (3) size/MACs. Licence ignored for now (private repos); set at the end once models are chosen.
- S0 compile test with pretrained zoo versions decides the **2 families** we benchmark. HSV = non-NN baseline.

## 13. Training & optimisation
- Fine-tune pretrained COCO weights on our dataset (Colab/laptop GPU), single class for rung 1.
- Export chain: PyTorch/TF → ONNX → {ONNX RT, TFLite} on CPU · Hailo DFC → `.har` → `.hef` (INT8, calibration set, needs an x86 host `[W1: RAM/OS needs]`) · OpenVINO/Luxonis → `.blob` (FP16).
- Precision: FP32 vs INT8 on CPU (TFLite), INT8 on Hailo, FP16 on OAK. Every conversion setting logged.
- Pruning: **one experiment on CPU** (TFLite, e.g. 50% sparsity + fine-tune), **because** it's on the professor's optimisation list and it shows the trade-off: smaller file, often no speed-up on accelerators. Not ported to Hailo/OAK, with the reason written down.
- Quality gate: on-device mAP within a set drop vs FP32 (threshold set in the protocol).

## 14. Benchmark protocol (8 steps; steps 1–5 drafted in S0, frozen end of S1)
**1. Goal: requirements from the robot** (numbers filled from S0 measurements):
| Req | What | Metric |
|---|---|---|
| R1 Real-time | Decision fast enough for the approach at TB3 speed (0.22 m/s) | pipeline latency p95/p99, sustained FPS |
| R2 Headroom | Detection must leave the Pi4 enough CPU for ROS + drivers | CPU load %, on-robot config |
| R3 Range | Detect a can at the needed distance | recall vs distance, vs input size |
| R4 Energy | Perception budget vs TB3 battery | idle W, active W, mJ per decision |
| R5 Accuracy | Few missed/false cans | mAP@0.5, mAP@0.5:0.95, drop vs FP32 |
| R6 Integration | Porting effort, operator support | hours spent, % ops on accelerator, crashes |

**2. Workload:** 2 NN models + HSV · our test set (fixed list + checksums) · recorded frame sequence (from rosbags) for L1 replay · batch 1.

**3. Variables (valid cells only):**
| Device | Runtime / precision | Input |
|---|---|---|
| Pi4 CPU | ONNX RT FP32 · TFLite FP32 · TFLite INT8 | 320, 640 |
| Pi5 CPU | same as Pi4 (free baseline that isolates the Hailo effect) | 320, 640 |
| Pi5 + Hailo-8L | HailoRT INT8 | 640 (+320) |
| OAK-D Pro VPU | DepthAI FP16 | 640 (+320) |
| Pi4 / Pi5 CPU | TVM-compiled FP32 (S3, worked ahead) | 640 |
| Pi4 / Pi5 CPU | HSV baseline | native |
| NXP board (09/12 lab only) | TFLite INT8 on its NPU | 640 |
- ≈20 configs for model A. Model B only on its fixed input. One factor at a time, then cross factors.

**4. Metrics:** per stage (capture, pre, transfer, infer, post, decision) · pipeline latency p50/p95/p99 · sustained FPS · dropped frames · power avg/peak · energy per inference = ∫(P − P_idle)dt / N · on-device mAP · CPU % · peak RAM · temperature/throttling · load time · model size.
- **L1** = frame read → postprocessed boxes (ROS-free, every device).
- **L2** = `header.stamp` of the image → `cmd_vel` publish (robot config, ROS). Both timestamps always stated.

**5. Setup:** point-B inline meter (reference) + `vcgencmd pmic_read_adc` on Pi5 (cross-check) · state what's powered (board / accelerator / camera / fan) · performance governor · same cooling, PSU, cable, port · record USB/PCIe link speed · room temperature · no sim time, chrony if 2 machines.

**6. Measure:** idle ≥60 s → warm-up (discarded) → ≥60 s steady · every sample kept (raw CSV) · runs interleaved across devices.

**7. Analyze:** ≥5 reps per config · median + IQR · latency CDF, box plots, **Pareto front (latency × energy × accuracy)** · configs below the quality gate rejected · bottleneck per stage.

**8. Report:** one-command scripts, configs, raw logs, versions (OS image, runtimes, compilers), hardware notes. **Someone who didn't write it reruns one config from the README.**

Estimated cost: ~18 configs × 5 reps × ~2 min ≈ 3 h of scripted runs, **because** this has to fit in S2–S3.

## 15. EAI deliverables
- Report (≤15 p, LaTeX), following the professor's outline: context/objectives · sensors, uncertainty, ranges (§10) · data pipeline (§11) · NN architecture + computation graph (§12) · optimisation (§13) · protocol (§14) · results · repo.
- PoC talk 15 min: requirement → protocol → abacus/Pareto → which device for which need → limits.
- Repo: `edgetrash` lib, `bench/` scripts, `data/` spec, `models/` export scripts, `results/raw`, `report/`.

---

# Part D: Execution

## 16. Sprints (each bullet = a GitHub issue; anyone picks it up)

> Sprint issues live on the board (https://github.com/orgs/TrashRobotEdge/projects/1). This list is the summary; S1–S3 become issues at each sprint start.

### S0: Define & de-risk (25/11 → 30/11) · EAI review 25/11
- [ ] Check the base works on your machine (everyone, onboarding)
- [ ] Repo skeletons (both repos)
- [ ] Freeze ROS interfaces (§4): topics, msgs, frames, QoS
- [ ] Robot hardware check: chassis, Pi4 image, OAK power, depthai-ros
- [ ] One issue per device, spec sheet + hello-world with a pretrained model: Pi4 · Pi5 + Hailo-8L · OAK-D Pro
- [ ] Power meter spec + idle power of every device
- [ ] Protocol steps 1–5 drafted (§14)
- [ ] Model compile test → pick 2 families (ADR)
- [ ] Review prep: AS 01/12 · EAI 02/12
- **Done when:** everyone runs the sim · every device has run one inference · protocol 1–5 committed · 2 models chosen with reasons
- Data capture moved to S1 (labelling starts there anyway).

### S1: First loop + protocol freeze (01/12 → 07/12) · AS URDF/sim, EAI TinyML + review 02/12
- [ ] URDF extensions: camera_info, depth noise, mount pose/FOV (§5)
- [ ] Gazebo world with cans + obstacles
- [ ] `trash_detector` (HSV backend) + `trash_localizer` → 3D can pose in `odom`
- [ ] FSM approach + lidar safety stop
- [ ] QoS profiles + `cyclonedds.xml` (DDS lecture)
- [ ] Data capture protocol + captures (OAK-D Pro: Coca-Cola, other cans, negatives)
- [ ] Label the dataset, splits + calibration set, `data/README`
- [ ] Fine-tune model A, record mAP. Model B started
- [ ] `edgetrash` lib + L1 harness v1 (per-stage timers, power sync, raw CSV)
- [ ] Depth-error measurements (§10)
- [ ] Protocol frozen (all 8 steps), presented on 02/12
- **Done when:** in sim, the robot approaches a can and stops · model A trained · first L1 CSV on Pi4 · protocol frozen

### S2: NN in the loop + matrix (08/12 → 14/12) · AS architectures/BT, EAI NXP lab 09/12
- [ ] NN backend in `trash_detector` (via `edgetrash`), working in sim
- [ ] BT replaces the FSM (library per lecture)
- [ ] Braitenberg-style approach · SLAM map of the test room (lab PDF)
- [ ] NXP lab 09/12: run our model on the NXP NPU as one extra data point
- [ ] TinyML: decision after the 02/12 lecture (ADR)
- [ ] Record rosbags (sim + real if possible) → frame sequences for L1
- [ ] Chassis bring-up if it has arrived (Pi4 + OAK, power checked)
- [ ] INT8 quantization + calibration · `.hef` and `.blob` of both models · on-device accuracy checked
- [ ] L1 matrix on all devices (first pass)
- [ ] Report sections 1–4 drafted (both repos)
- **Done when:** sim demo runs with the NN · every valid cell has ≥1 run · on-device mAP known

### S3: System + freeze (15/12 → 21/12) · AS Braitenberg, EAI ONNX RT
- [ ] L2 measurements on the robot config (real if possible, else bench Pi4 + live OAK)
- [ ] Nav2 goal to the localised can · depth↔lidar fusion check
- [ ] TVM row (Pi4/Pi5 CPU) · ONNX RT profiling · pruning experiment on CPU
- [ ] Computation-graph figures (ROS graph + model graph)
- [ ] Full matrix, 5 reps, plots (CDF, box, Pareto)
- [ ] Results + discussion (bottlenecks, trade-offs, threats to validity)
- [ ] One-command launch, READMEs, docs complete
- [ ] Demo videos: sim (mandatory) + real (if possible)
- [ ] Reproducibility check by someone who didn't write the code
- [ ] EAI report ≥80%, AS LaTeX assembled from `docs/`, slides draft, DEMO.md tested by someone else
- **Done when:** everything is pushed and reproducible. **Hard freeze 21/12.**

### January (no new work)
- Lectures (SLAM, TVM, micro-ROS) attended, to check that what we worked ahead matches. Differences go into the reports as discussion, not new code.
- Before 19/01–20/01: final polish of the reports/slides, 2 rehearsals, check the demo still launches.

## 17. Working rules
- Weekly sprint review (15 min), also used to prepare the professor's review. Notes in `docs/journal/sprint-N.md`.
- GitHub: board **Sprint** field = S0–S3, no sprint = backlog. Assign yourself, branch `<issue#>-short-name`, PR with `Closes #N`. **Category** field: Setup / Build / Research / Decision / Review prep / Docs. **Max 2–3 issues per person per sprint.** Repo = course.
- PR reviews are **encouraged, not mandatory** (repos are private on the Free plan: no enforced protection). Aim for cross-course reviews on big PRs, **because** that's how everyone learns both halves.
- Decisions → short ADR (context · options · decision · because). Problems → `problems.md` (symptom · diagnosis · alternatives), which the professor explicitly values.
- Figures generated by scripts only, never hand-made.

## 18. Risks & open questions
| Risk | Mitigation |
|---|---|
| Chassis late / never arrives | Sim demo is the baseline; bench OAK + Pi4 for L2 |
| Gazebo too slow in VirtualBox | Test in S0; native/dual-boot fallback |
| Model doesn't compile on Hailo-8L / OAK | Compile test in S0 picks the models |
| ROS Humble not on Pi5 | L1 is ROS-free by design |
| OAK power on Pi4 USB | Powered hub/Y-cable; state it in the power domain |
| Labelling takes longer | Start in S0; train on the partial set and iterate |
| Sim-to-real gap | Real images from day 1; a few labelled sim frames; gap measured |

| Working ahead on SLAM / TVM / micro-ROS misses what the professor wants | Thin versions only; check at the January lectures; differences = discussion |
| Covering every lecture overloads 4 weeks | "Thin but real" rule; depth slips first, lecture items are protected |
| No microcontroller | micro-ROS in backlog; TinyML decided after 02/12 |

**Ask the professor** (AS review 01/12, EAI review 02/12; tracked in the review-prep issues):
- Demo 19/01: format, length, sim + video OK if no chassis? And where is our chassis?
- Does reusing his OAK-D Pro URDF + our extensions (camera_info, noise, pose) count as the "URDF update"?
- BT library expected? micro-ROS without a microcontroller: is a documented design enough?
- TinyML without a microcontroller: what's expected?
- NXP board: is the 09/12 lab enough, or should it be in the benchmark? Our plan: one extra data point during the lab.
- Is TVM on the Pi CPUs (worked ahead of 06/01) a good use of time?

## Reference: last year's projects (same courses)
- **`Firelods/TurtleShot`** (catapult arm): own URDF/xacro + worlds, BehaviorTree.CPP + Groot2, Nav2 + SLAM, YOLO on OAK (`.blob`), custom interfaces package, `launch_all.sh`, QUICKSTART, `cyclonedds.xml`.
- **`Master-Baiter-Corporation/master-baiter`** (voice + person approach): Dockerfile, DEMO.md, BENCHMARK.md, TFLite FP16/INT8/pruned 50–70%/Coral.
- **Their AS scope = our minimum** (custom URDF + world, BT, Nav2/SLAM, one-command launch, demo doc).
- **Their benchmark = our floor, not our target**: inference time only, mean only, no power, no percentiles, no written protocol. This year's slides warn against exactly that.
- **Don't copy**: model binaries + `Zone.Identifier` junk in git, duplicate packages, "you're on your own" install docs.

## 19. Explainers (what it means for us)
- **URDF / TF2**: robot description (links, joints, sensors) / live tree of frames. We need it to turn "can at pixel (u,v) + depth" into "can at (x,y) in `odom`".
- **gz ↔ ROS bridge**: Gazebo topics aren't ROS topics; `turtlebot3_bridge.yaml` maps them. A new sensor (camera_info) needs a sensor in the URDF **and** a bridge entry.
- **QoS**: per-topic delivery rules. `sensor_data` (best effort, depth 1) = always the latest frame. Deadline = alarm if detections arrive too late.
- **FSM vs BT**: FSM = states + transitions, simple, but grows messy. BT = tree of reusable tasks, easier to extend (safety, retries). We build both and compare.
- **rosbag record/replay**: record sensor topics once, replay identically. Same input on every device = fair comparison.
- **Sim time vs wall time**: Gazebo has its own clock. Latency must be measured in wall time, so no `use_sim_time` in benchmarks.
- **p50 / p95 / p99**: half / 95% / 99% of runs are faster than this. The robot suffers from the slow tail, not from the average.
- **Median + IQR**: robust summary across ≥5 reps (middle value + spread of the middle 50%).
- **CDF / Pareto front**: CDF = full latency distribution in one curve. Pareto = configs where nothing beats you on every axis at once; that's the shortlist.
- **Idle power, energy per inference**: E = ∫(P − P_idle)dt / N. Subtract idle so we count only the work, not the board just being on.
- **Meter points A–D**: A wall, B inline USB-C (our reference), C rail shunt, D internal sensors (pmic). We use B, cross-checked with D.
- **INT8 / calibration**: weights + activations in 8-bit = faster, less energy, some accuracy lost. Calibration images set the value ranges and must not overlap the test set.
- **mAP / IoU**: IoU = box overlap. mAP@0.5 = detection quality at IoU ≥ 0.5, @0.5:0.95 = stricter average. Measured on device output, not on the PC.
- **Operator fallback**: layers the accelerator can't run go back to the CPU, silently. Must be checked and reported (% ops on the accelerator).
- **.hef / .blob**: Hailo compiled model (ONNX → .har → .hef via the Dataflow Compiler) / OAK compiled model (ONNX → OpenVINO → .blob, FP16).
- **L1 vs L2**: L1 = device level (fair, ROS-free, all devices). L2 = system level (real robot pipeline, image stamp → `cmd_vel`). L1 explains, L2 proves.

## 20. Verification
- Each sprint's "Done when" is checked at the sprint review and logged in `docs/journal/`.
- **AS acceptance:** from one launch command, the robot finds a can in view, approaches without collision, stops at d ± tolerance and signals success. Sim mandatory, real if the chassis allows. Logs + video.
- **EAI acceptance:** a teammate who didn't write the code reproduces one benchmark config from the README alone, within the reported IQR. Every report figure regenerates from `results/raw` with one command.

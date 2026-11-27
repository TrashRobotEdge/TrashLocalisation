# 0001: Two repos, one ROS-free inference library

- **Status:** accepted
- **Date:** 25/11/2026 · **Issue:** —

## Context
Two courses, two graded deliverables: AS grades a ROS2 repo + demo, EAI grades a report + a repo the professor must reproduce from its README. Both use the same detector.

## Options
1. One repo for everything.
2. Two repos, detector code duplicated.
3. Two repos; the inference code lives once, ROS-free, in EdgeTrash; TrashLocalisation's `trash_detector` is a thin ROS wrapper importing it.

## Decision
Option 3.

## Because
- What we benchmark (EdgeTrash) is exactly what runs on the robot: one implementation.
- EAI must be reproducible **without ROS** (the Pi5 + Hailo stack may not run ROS Humble, see the plan §4).
- Each course gets a clean repo to grade. Last year's groups did the same (main repo + separate training repo).

## Consequences
- TrashLocalisation depends on a pinned EdgeTrash commit: `EDGETRASH_PIN` in `scripts/setup.sh`, installed editable into the workspace venv (ADR 0002), so `edgetrash` finds its manifest and model folder in the checkout. (First written as "pip install from a git tag": changed 27/11, no tag needed.)
- Interfaces between the two (`edgetrash` API) must stay stable: changes go through a PR on both sides.

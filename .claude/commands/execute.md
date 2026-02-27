---
description: Plan and implementation of the requirements then build the codebase based on the plan
argument-hint: [path-to-requirements]
---

## Variables
PATH_TO_REQUIREMENTS: $1

## Workflow
- If no `PATH_TO_REQUIREMENTS` is provided, STOP immediately and ask the user to provide it.
- Execute the `plan` command with the provided `PATH_TO_REQUIREMENTS` to create an implementation plan.
- Capture the output path of the generated plan as `PLAN_PATH`.
- Execute the `build` command with the generated `PLAN_PATH` to implement the plan into the codebase.


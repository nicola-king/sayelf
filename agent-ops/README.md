# Sayelf Agent Ops — Sprint 01

This directory is the frozen Sprint 01 implementation baseline for Sayelf Agent Ops.

## Scope

Only these components are implemented:

1. WorkItem
2. State Engine
3. Role Registry
4. Skill Registry
5. Deliverable-first Router
6. Minimum Planner
7. Routing Evals

Not included yet: Review, Evidence, Risk, Human Gate, Executor, Connector Runtime.

## Principle

> 工作决定组织，而不是组织决定工作。

Default runtime state:

- Active Roles = 0
- Loaded Skills = 0

A task activates only the minimum professional responsibility and skills needed for its deliverable.

## Run the first vertical slice

```powershell
cd agent-ops
python -m sayelf_agent_ops.demo
```

Expected route:

```text
WorkItem: WI-0001
Industry: Media
Role: Content Planner
Skill: title-writing
State: READY
```

## Run evals

```powershell
cd agent-ops
python -m unittest discover -s evals -v
```

The baseline includes 10 normal routing cases, 5 confusion cases, idle-registry checks, and state-transition guards.

## Sprint boundary

Do not add Review / Risk / Human Gate / Executor until Sprint 01 routing and state tests are stable.

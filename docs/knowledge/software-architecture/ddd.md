---
title: Domain-Driven Design
tags:
  - Level/Advanced
  - Type/Architecture
  - Status/Draft
---

# Domain-Driven Design

<!-- kb:status Draft -->

> An approach to software development that centers the domain model at the heart
> of the system design.

## 一句话理解

DDD aligns software design with the business domain by using a shared language
and modeling the domain explicitly in code.

## 为什么会出现

Eric Evans observed that many software projects failed not because of technical
problems, but because the code didn't reflect the business reality. Developers
and domain experts spoke different languages.

## 解决什么问题

- Misalignment between business and technical teams
- Anemic domain models (data bags with no behavior)
- Complexity that grows without structure
- Communication breakdown in large projects

## 什么时候不要用

- CRUD applications with no business logic
- Purely technical infrastructure projects
- When the team is too small to benefit from the overhead

## 核心概念

### Strategic Design

- **Bounded Context** — a boundary within which a model applies
- **Context Map** — relationships between bounded contexts
- **Ubiquitous Language** — shared language between devs and domain experts

### Tactical Design

- **Entity** — object with identity that changes over time
- **Value Object** — immutable, defined by attributes
- **Aggregate** — cluster of entities treated as a unit
- **Repository** — mediates between domain and data mapping
- **Domain Event** — something important that happened in the domain

## 我的理解

DDD is not about patterns. It's about **communication**. The tactical patterns
(aggregate, repository, etc.) are tools, but the real value is in strategic
design: understanding the domain and modeling it faithfully.

In the AI era, DDD becomes more relevant — AI agents need crisp domain models
to reason about business logic correctly.

## 相关知识

- [[clean|Clean Architecture]]
- [[solid|SOLID Principles]]
- [[design-pattern|Design Pattern]]
- [[event-driven|Event-Driven Architecture]]
- [[hexagonal|Hexagonal Architecture]]

## 推荐阅读

- *Domain-Driven Design* by Eric Evans (the "Blue Book")
- *Implementing Domain-Driven Design* by Vaughn Vernon (the "Red Book")
- *Domain-Driven Design Distilled* by Vaughn Vernon

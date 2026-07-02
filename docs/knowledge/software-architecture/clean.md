---
title: Clean Architecture
tags: [Level/Advanced, Type/Architecture, Status/Draft]
growth: evergreen
updates:
  - date: 2026-07-02
    note: Initial draft — framework overview and key principles
---

# Clean Architecture

<!-- kb:evergreen -->

> An architecture that places the business logic at the center, with all external concerns pushed to the edges.

## 一句话理解

Clean Architecture is the Dependency Inversion Principle applied at the system level — the domain is the core, everything else is a plugin.

## 为什么会出现

Frameworks and databases tend to take over codebases. Clean Architecture inverts this: the framework serves the domain, not the other way around.

## 解决什么问题

- Framework lock-in and database-centric design
- Business logic scattered across controllers, services, and ORM entities
- Hard-to-test code where business rules are tangled with I/O

## 什么时候不要用

- Simple CRUD applications with no business logic
- Prototypes and MVPs where speed matters more than structure
- When the team doesn't understand *why* — patterns without understanding create complexity

## 核心概念

### The Dependency Rule

Dependencies point inward. Outer layers depend on inner layers. The domain
knows nothing about the database, the web framework, or the UI.

### Layers

```
Frameworks & Drivers → Interface Adapters → Application → Domain
```

### Entities (Domain)

Enterprise-wide business rules. The most stable, abstract core.

### Use Cases (Application)

Application-specific business rules. Orchestrates entities to accomplish
a specific goal.

### Interface Adapters

Convert data between the format most convenient for use cases/entities
and the format most convenient for external agencies (DB, Web, etc.).

## 实际案例

- Many modern backend frameworks encourage Clean Architecture patterns
- The pattern appears in Android development, iOS, Flutter, and web apps
- Microservices often use Clean Architecture internally

## 我的理解

Clean Architecture isn't about the layers diagram. It's about **dependency
direction**. If your business logic imports from your framework, you've lost.
If your framework imports from your business logic, you've won.

The test: can you swap your database without touching business logic?
Can you test business rules without spinning up a database?

<!-- kb:updates -->

## 相关知识

- [[ddd|Domain-Driven Design]]
- [[solid|SOLID Principles]]
- [[hexagonal|Hexagonal Architecture]]
- [[layered|Layered Architecture]]
- [[event-driven|Event-Driven Architecture]]

## 推荐阅读

- *Clean Architecture* by Robert C. Martin
- *Get Your Hands Dirty on Clean Architecture* by Tom Hombergs

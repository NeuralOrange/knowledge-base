---
title: Event-Driven Architecture
tags: [Level/Advanced, Type/Architecture, Status/Draft]
---

# Event-Driven Architecture

<!-- kb:status Draft -->

> An architecture where components communicate by producing and consuming events,
> enabling loose coupling and asynchronous processing.

## 一句话理解

Instead of calling each other directly, services publish events. Other services
react to those events — no direct coupling, just shared understanding of what
events mean.

## 相关知识

- [[ddd|Domain-Driven Design]]
- [[mq|Message Queue]]
- [[clean|Clean Architecture]]

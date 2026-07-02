---
title: Hexagonal Architecture
tags: [Level/Advanced, Type/Architecture, Status/Draft]
---

# Hexagonal Architecture

<!-- kb:status Draft -->

> Also known as Ports and Adapters — an architecture that isolates the application core
> from external concerns through ports (interfaces) and adapters (implementations).

## 一句话理解

The application core defines ports (what it needs). Adapters implement those ports
for specific technologies — database, HTTP, message queue, etc.

## 相关知识

- [[clean|Clean Architecture]]
- [[ddd|Domain-Driven Design]]
- [[layered|Layered Architecture]]

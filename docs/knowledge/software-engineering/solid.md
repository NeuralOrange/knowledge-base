---
title: SOLID Principles
tags:
  - Level/Intermediate
  - Type/Concept
  - Status/Draft
---

# SOLID Principles

<!-- kb:status Draft -->

> Five design principles that make software more maintainable, flexible, and scalable.

## 一句话理解

SOLID is a set of five principles that guide object-oriented design toward
code that's easier to maintain and extend.

## 为什么会出现

Robert C. Martin collected these principles to address the common failure modes
of object-oriented software: rigidity, fragility, immobility, and viscosity.

## 解决什么问题

- **S** — Single Responsibility: one reason to change
- **O** — Open/Closed: open for extension, closed for modification
- **L** — Liskov Substitution: subtypes must be substitutable for base types
- **I** — Interface Segregation: many small interfaces > one large interface
- **D** — Dependency Inversion: depend on abstractions, not concretions

## 什么时候不要用

- For simple scripts or throwaway code
- When applying all five dogmatically adds unnecessary complexity
- In non-OOP paradigms (though the principles have analogs)

## 代码示例

```python
# BEFORE: Violates SRP and DIP
class ReportGenerator:
    def generate(self, data):
        report = self._format(data)
        self._save_to_db(report)
        self._send_email(report)

# AFTER: Each class has one reason to change
class ReportFormatter:
    def format(self, data): ...

class ReportRepository:
    def save(self, report): ...

class EmailSender:
    def send(self, content): ...
```

## 实际案例

- Clean Architecture is essentially SOLID applied at the system level
- Most design patterns are consequences of SOLID principles
- Refactoring tools (like IDEs) often suggest SOLID-based improvements

## 我的理解

SOLID is not a goal. It's a compass. When your code feels hard to change,
SOLID tells you which direction to move.

## 相关知识

- [[design-pattern|Design Pattern]]
- [[clean|Clean Architecture]]
- [[ddd|Domain-Driven Design]]
- [[refactoring|Refactoring]]

## 推荐阅读

- *Clean Architecture* by Robert C. Martin
- *Agile Software Development: Principles, Patterns, and Practices*

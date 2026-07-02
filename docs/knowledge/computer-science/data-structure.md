---
title: Data Structure
tags:
  - Level/Beginner
  - Type/Concept
  - Status/Draft
---

# Data Structure

<!-- kb:status Draft -->

> A way of organizing and storing data so it can be accessed and modified efficiently.

## 一句话理解

Data structures are containers that shape how we store and retrieve information.

## 为什么会出现

Different problems require different ways of organizing data. The right structure
can make an algorithm orders of magnitude faster.

## 解决什么问题

- Efficient storage and retrieval of data
- Modeling relationships between data elements
- Optimizing for specific access patterns

## 什么时候不要用

- When the data is small enough that a simple array or hash map suffices
- When you're optimizing prematurely without understanding access patterns

## 代码示例

```python
# Linked List Node
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

# Binary Search Tree
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
```

## 实际案例

- Databases use B-trees for indexing
- Redis uses hash tables, sorted sets, and lists
- Git uses Merkle trees (DAG) for version history

## 我的理解

Choosing the right data structure is often more impactful than choosing the
right algorithm. The two are inseparable.

## 相关知识

- [[algorithm|Algorithm]]
- [[database|Database]]

## 推荐阅读

- *Algorithms* by Robert Sedgewick
- *The Algorithm Design Manual* by Steven Skiena

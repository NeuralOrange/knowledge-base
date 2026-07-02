---
title: Algorithm
tags:
  - Level/Beginner
  - Type/Concept
  - Status/Draft
---

# Algorithm

<!-- kb:status Draft -->

> A finite sequence of well-defined instructions to solve a problem.

## 一句话理解

Algorithms are recipes for computation — step-by-step procedures that transform
input into output.

## 为什么会出现

The need to solve computational problems systematically and efficiently drove
the formalization of algorithms as a field of study.

## 解决什么问题

- Sorting, searching, and organizing data
- Finding optimal solutions to constrained problems
- Processing and transforming information at scale

## 什么时候不要用

- When the problem is trivial and a simple heuristic suffices
- When hardware constraints make algorithmic overhead counterproductive

## 代码示例

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## 实际案例

- Google Search uses PageRank algorithm
- GPS navigation uses Dijkstra's shortest path
- Recommendation systems use collaborative filtering

## 我的理解

Algorithms are not just for interviews. Understanding algorithmic thinking helps
you reason about trade-offs in any system design.

## 相关知识

- [[data-structure|Data Structure]]
- [[design-pattern|Design Pattern]]

## 推荐阅读

- *Introduction to Algorithms* (CLRS)
- *Algorithms* by Robert Sedgewick

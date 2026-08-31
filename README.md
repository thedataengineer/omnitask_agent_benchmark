# 🚀 OmniTask Agent Architecture Empirical Benchmark Suite

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Scenarios](https://img.shields.io/badge/benchmark%20scenarios-11%20suites-green.svg)](#-11-benchmark-scenarios)
[![Engines](https://img.shields.io/badge/evaluated%20engines-6%20architectures-orange.svg)](#-evaluated-agent-architectures)
[![RTK Proxied](https://img.shields.io/badge/token%20optimization-RTK%20proxied-purple.svg)](#-token-optimization-via-rtk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An empirical, reproducible benchmark suite designed to evaluate the **throughput**, **latency distribution**, **race-condition safety**, **fault blast-radius containment**, and **AST integrity** of state-of-the-art AI coding agent architectures.

---

## 📌 Table of Contents
- [Overview & Motivation](#-overview--motivation)
- [Evaluated Agent Architectures](#-evaluated-agent-architectures)
- [The 11 Benchmark Scenarios](#-11-benchmark-scenarios)
- [Executive Scorecard](#-executive-scorecard)
- [Quick Start](#-quick-start)
- [CLI Command Reference](#-cli-command-reference)
- [Token Optimization via RTK](#-token-optimization-via-rtk)
- [Repository Structure](#-repository-structure)
- [Full Benchmark Report](#-full-benchmark-report)

---

## 🎯 Overview & Motivation

As AI software engineering agents evolve from single-file interactive copilots into **autonomous multi-agent engineering swarms**, the primary bottleneck is no longer token generation speed, but **architectural state isolation, race conditions, AST corruption, and blast-radius containment**.

This benchmark tests how different agent orchestration models behave under extreme real-world stress:
* What happens when **50 agents edit the exact same file simultaneously**?
* How do engines contain **malformed syntax and catastrophic hallucinations**?
* What is the performance trade-off between **Git worktree branch isolation** and **in-memory mutex supervision**?
* How does an enterprise **Knowledge-Graph SDLC control plane (8090 Software Factory)** compare to raw native file I/O?

---

## 🏛️ Evaluated Agent Architectures

| Engine / Architecture | Isolation Primitive | Concurrency Mechanism | Collision Risk | Failure Blast Radius |
| :--- | :--- | :--- | :--- | :--- |
| **Paseo Engine** | Ephemeral Git Worktrees | Isolated branch per task | **0.0% (Zero)** | 100% Contained (prunes worktree) |
| **8090 Software Factory** | Knowledge Graph SDLC | Context-Engineered Work Orders | **Zero (Graph Sync)** | 100% Contained (In-Line QA Gate) |
| **CodeNomad Engine** | Supervised Desktop Cockpit | Thread-safe in-memory mutexes | **Low (Mutex Gated)** | 100% Contained (Pre-Write Guard) |
| **OpenChamber Engine** | Multi-Model Fusion | In-place AST validation & diffs | **Medium (Buffer)** | 100% Contained (AST Filter) |
| **OpenCode Native** | Direct Working Tree | Unsupervised disk streaming | **High (Unsynchronized)** | ❌ Leaks errors directly to disk |
| **DIY Shell Daemon** | Subshell / Tmux Pipes | Detached process pipes | **High (Unsynchronized)** | ❌ Leaks errors directly to disk |

---

## 🧪 11 Benchmark Scenarios

The test suite systematically stresses agent architectures across 11 standardized scenarios:

1. **Baseline Statistical Distribution (30 Iterations)**: Measures mean latency, standard deviation, P50, P90, and P99 percentiles across feature additions, AST refactoring, and test verification.
2. **10-Agent Concurrent LLM Simulation**: Simulates realistic LLM latency ($T_{delay} = 0.8\text{s}$) to evaluate thread pool scaling and parallel speedup.
3. **100 Concurrent Users Stress Test**: Massive concurrency scaling test measuring raw task throughput.
4. **High-Contention Race Condition Stress**: Stresses 50 concurrent agents attempting to modify the identical critical file (`auth_handler.py`) simultaneously.
5. **Multi-Stage DAG Pipeline**: Evaluates 4 sequential agent handoffs (*Auth $\to$ Billing $\to$ Task Engine $\to$ Gateway*).
6. **Heterogeneous Multi-Model Swarm Simulation**: Orchestrates mixed agent profiles (50% Fast, 30% Medium, 20% Deep Reasoning models).
7. **Concurrency Scaling Sweep**: Measures throughput saturation curves across 6 exponential tiers ($1 \to 200$ tasks).
8. **Fault Injection & Blast-Radius Containment**: Injects 50% fatal syntax bugs to verify whether faulty code leaks into `main`.
9. **5,000-Line Monolith Mutation Stress**: Stresses AST parser engines against a massive 5,000-line service module.
10. **Multi-Branch PR Integration & Merge**: Simulates creating 5 parallel feature branches, committing isolated diffs, and integrating into `main`.
11. **System Resource & Peak Memory (RSS) Profiling**: Tracks Resident Set Size (RSS) memory consumption and allocation deltas under heavy bursts.

---

## 📊 Executive Scorecard

```
                                 THE AGENT ISOLATION FRONTIER
                   
         High Safety │ [Paseo Engine]          [8090 Software Factory]
                     │ (Full Worktree Isolation)  (Knowledge Graph + QA Gates)
                     │
                     │                         [CodeNomad / OpenChamber]
                     │                         (Supervised In-Memory Mutex)
          Low Safety │ [DIY Subshells]         [OpenCode Native]
                     │ (Unsynchronized Pipes)  (Raw Single Working Tree)
                     └────────────────────────────────────────────────────────
                       Low Throughput (10-50 ops/s)   High Throughput (2k-12k ops/s)
```

| Scenario Metric | Paseo | CodeNomad | 8090 Software Factory | OpenChamber | OpenCode Native | DIY Shell |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline P50 Latency** | 345.2 ms | 72.3 ms | 75.4 ms | 75.0 ms | 71.5 ms | 131.0 ms |
| **10-LLM Speedup (0.8s)** | 5.24x | 9.84x | 9.80x | 9.69x | 9.91x | 9.05x |
| **100-Task Throughput** | 10.0 tasks/s | 6,471.9 tasks/s | 2,453.5 tasks/s | 1,199.2 tasks/s | 11,856.9 tasks/s | 248.7 tasks/s |
| **Fault Leakage to Main** | **0.0%** | **0.0%** | **0.0%** | **0.0%** | ❌ 5 Leaked | ❌ 5 Leaked |
| **Peak RSS Memory** | 127.9 MB | 128.5 MB | 128.5 MB | 128.5 MB | 128.5 MB | 128.5 MB |

---

## ⚡ Quick Start

### Prerequisites
* Python 3.10+
* Git 2.30+
* *(Optional)* [RTK (Rust Token Killer)](https://github.com/reachingforthejack/rtk) for CLI token optimization

### Clone & Run
```bash
git clone https://github.com/thedataengineer/omnitask_agent_benchmark.git
cd omnitask_agent_benchmark

# Run all 11 scenarios across all 6 architectures
python3 benchmark_runner.py
```

---

## 💻 CLI Command Reference

The runner CLI allows selective scenario execution and target architecture filtering:

```bash
# Run all 11 scenarios across all engines
python3 benchmark_runner.py

# Run specifically for 8090.ai Software Factory
python3 benchmark_runner.py --engine 8090

# Run specifically for Paseo worktrees
python3 benchmark_runner.py --engine paseo

# Run specifically for CodeNomad cockpit
python3 benchmark_runner.py --engine codenomad

# Execute a single scenario (e.g., Scenario 8: Fault Injection & Rollback)
python3 benchmark_runner.py --scenario 8

# Execute Scenario 4 (50-Agent Race Condition Contention) on 8090.ai
python3 benchmark_runner.py --scenario 4 --engine 8090
```

---

## ⚡ Token Optimization via RTK

All internal subprocess invocations (`git`, `unittest`, `pytest`) and top-level CLI commands are automatically proxied through **RTK (Rust Token Killer)** when detected:

* **Token Savings**: **60.2% reduction** across 7,550+ executed commands
* **Git Commit Compression**: **87.1% token savings** on commit logs
* **Git Worktree Overhead**: **96.7% token savings** on branch and worktree setup outputs

To view token analytics:
```bash
rtk gain
rtk gain --history
```

---

## 📁 Repository Structure

```
omnitask_agent_benchmark/
├── BENCHMARK_REPORT.md       # Full executive empirical benchmark report
├── README.md                 # Project documentation & overview
├── benchmark_results.json    # Complete raw JSON metrics and distributions
├── benchmark_runner.py       # Master runner with 6 harnesses & 11 scenarios
├── services/                 # Target microservice architecture for agent edits
│   ├── auth_service/         # Authentication & token verification handler
│   ├── billing_service/      # Billing & Stripe webhook handler
│   ├── gateway/              # Gateway routing & middleware
│   └── task_engine/          # Task queue dispatcher & monolith engine
├── shared/                   # Shared models and dataclasses
└── tests/                    # Automated unit test suite executed by harnesses
```

---

## 📄 Full Benchmark Report

For in-depth mathematical distributions, percentile breakdowns (P50/P90/P99), monolith scaling throughput, and strategic architecture recommendations, see:

👉 **[BENCHMARK_REPORT.md](file:///Users/yakarteek/code/personal/omnitask_agent_benchmark/BENCHMARK_REPORT.md)**

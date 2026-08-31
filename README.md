# 🚀 OmniTask: Multi-Agent Software Factory Benchmark Suite
### *An Open Empirical Benchmarking Harness for AI Coding Orchestrators, Multi-Agent Swarms & Software Factories*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Benchmark Scenarios](https://img.shields.io/badge/scenarios-11%20standardized%20suites-green.svg)](#-the-11-standardized-benchmark-scenarios)
[![Architectures Evaluated](https://img.shields.io/badge/architectures-6%20reference%20engines-orange.svg)](#-reference-architectures--harnesses)
[![Token Optimization](https://img.shields.io/badge/token%20proxy-RTK%20enabled-purple.svg)](#-token-optimized-cli-proxy-rtk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Executive Overview

As autonomous AI software engineering evolves from single-turn code generation into **multi-agent software factories**, development bottlenecks shift from raw LLM inference latency to **architectural state isolation, race-condition safety, AST integrity, and fault blast-radius containment**.

**OmniTask** is a generalized, reproducible empirical benchmarking framework designed to stress-test and profile any agent orchestrator, desktop cockpit, or software factory control plane across **11 standardized engineering scenarios**.

```
                              THE AGENT ISOLATION FRONTIER
                   
         High Safety │ [Paseo Engine]              [8090 Software Factory]
                     │ (Git Worktree Isolation)    (Knowledge Graph + In-Line QA)
                     │
                     │                             [CodeNomad / OpenChamber]
                     │                             (Supervised In-Memory Mutex)
          Low Safety │ [DIY Subshells]             [OpenCode Native]
                     │ (Unsynchronized Pipes)      (Raw Direct Working Tree)
                     └────────────────────────────────────────────────────────────
                       Low Throughput (10-50 ops/s)   High Throughput (2k-12k ops/s)
```

---

## 🏛️ Reference Architectures & Harnesses

OmniTask ships with 6 reference harness implementations modeling the leading paradigms in agent execution:

| Paradigm / Engine | Isolation Model | Concurrency Mechanism | Collision Risk | Fault Blast Radius |
| :--- | :--- | :--- | :--- | :--- |
| **Git Worktree Isolation** *(e.g. Paseo)* | Dedicated ephemeral Git worktrees & branches | Operating-system level Git worktree boundaries | **0.0% (Zero)** | 100% Contained (prunes worktree) |
| **SDLC Control Plane** *(e.g. 8090.ai)* | Upstream Knowledge Graph & Structured Work Orders | Assembly-line dispatch with dependency tracking | **Zero (Graph Sync)** | 100% Contained (In-Line QA Gate) |
| **Supervised Cockpit** *(e.g. CodeNomad)* | In-memory session supervisor with mutex locks | Thread-safe mutexes per workspace file | **Low (Mutex Gated)** | 100% Contained (Pre-Write Guard) |
| **Multi-Model Fusion** *(e.g. OpenChamber)* | In-place AST candidate pre-validation & diff scoring | Evaluates candidate diffs in memory | **Medium (Buffer)** | 100% Contained (AST Filter) |
| **Direct Stream Server** *(e.g. OpenCode)* | Direct single working tree | Raw unsupervised disk I/O | **High (Unsynchronized)** | ❌ Leaks corrupt code to disk |
| **Detached Daemon** *(e.g. DIY Tmux)* | Detached bash subshell & tmux pipes | Unsynchronized OS process forks | **High (Unsynchronized)** | ❌ Leaks corrupt code to disk |

---

## 🧪 The 11 Standardized Benchmark Scenarios

OmniTask evaluates orchestrators across a comprehensive 11-scenario matrix:

1. **Baseline Statistical Distribution (30 Iterations)**: Computes mean total latency, standard deviation, P50, P90, and P99 percentiles across feature additions, AST refactoring, and test suite execution.
2. **10-Agent Concurrent LLM Simulation**: Simulates realistic model inference delay ($T_{delay} = 0.8\text{s}$) across 10 parallel threads to measure concurrent speedup and thread pool scaling.
3. **100 Concurrent Users Stress Test**: High-volume scale test measuring raw concurrent task throughput.
4. **High-Contention Race Condition Stress**: Forces 50 concurrent agents to mutate the exact same file (`auth_handler.py`) simultaneously to test race conditions and file integrity.
5. **Multi-Stage DAG Pipeline**: Measures sequential multi-agent stage handoffs (*Auth Validator $\to$ Billing Webhook $\to$ Task Prioritizer $\to$ Gateway Router*).
6. **Heterogeneous Multi-Model Swarm Simulation**: Orchestrates 20 agents operating under heterogeneous model latency profiles (Fast, Medium, and Deep Reasoning).
7. **Concurrency Scaling Sweep**: Sweeps task concurrency exponentially ($1 \to 200$ tasks) to measure throughput saturation curves.
8. **Fault Injection & Blast-Radius Rollback**: Injects 50% fatal syntax errors to verify whether broken code leaks into the shared codebase.
9. **5,000-Line Monolith Mutation Stress**: Evaluates AST parsing and mutation throughput against a large 5,000-line monolithic engine file.
10. **Multi-Branch PR Integration & Merge**: Simulates creating 5 parallel feature branches, committing isolated changes, and integrating into `main`.
11. **System Resource & Peak Memory (RSS) Profiling**: Tracks Resident Set Size (RSS) memory consumption and allocation deltas under heavy bursts.

---

## 📊 Summary Benchmark Scorecard

Empirical results from running the complete 11-scenario suite across all engines:

| Scenario Metric | Git Worktrees (Paseo) | Supervised Mutex (CodeNomad) | SDLC Factory (8090.ai) | Model Fusion (OpenChamber) | Direct Disk (OpenCode) | DIY Shell |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline P50 Latency** | 345.2 ms | 72.3 ms | 75.4 ms | 75.0 ms | 71.5 ms | 131.0 ms |
| **10-LLM Speedup (0.8s)** | 5.24x | 9.84x | 9.80x | 9.69x | 9.91x | 9.05x |
| **100-Task Throughput** | 10.0 tasks/s | 6,471.9 tasks/s | 2,453.5 tasks/s | 1,199.2 tasks/s | 11,856.9 tasks/s | 248.7 tasks/s |
| **50-Agent File Contention** | Safe (Worktree) | Safe (Mutex) | Safe (Ordered) | Safe (File Lock) | High Risk | High Risk |
| **Fault Leakage to Main** | **0.0%** | **0.0%** | **0.0%** | **0.0%** | ❌ 5 Leaked | ❌ 5 Leaked |
| **Peak RSS Memory** | 127.9 MB | 128.5 MB | 128.5 MB | 128.5 MB | 128.5 MB | 128.5 MB |

---

## ⚡ Quick Start

### 1. Prerequisites
* Python 3.10+
* Git 2.30+
* *(Optional)* [RTK (Rust Token Killer)](https://github.com/reachingforthejack/rtk) for CLI token optimization

### 2. Installation
```bash
git clone https://github.com/thedataengineer/omnitask_agent_benchmark.git
cd omnitask_agent_benchmark
```

### 3. Running the Benchmark Suite
```bash
# Run all 11 scenarios across all reference engines
python3 benchmark_runner.py

# Run specifically for a target engine
python3 benchmark_runner.py --engine 8090
python3 benchmark_runner.py --engine paseo
python3 benchmark_runner.py --engine codenomad

# Run a specific benchmark scenario (e.g. Scenario 8: Fault Injection & Rollback)
python3 benchmark_runner.py --scenario 8

# Run a specific scenario on a specific engine
python3 benchmark_runner.py --scenario 4 --engine 8090
```

---

## 🔌 Benchmarking Your Custom Agent / Orchestrator

You can benchmark any custom engine or agent platform by implementing the standard OmniTask harness interface:

```python
from typing import Dict, List, Any

class CustomAgentHarness:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.name = 'MyCustomEngine'
        self.isolation_model = 'My Custom Isolation Architecture'

    def run_benchmark(self, tasks: List[Dict[str, Any]], refactor: Dict[str, Any]) -> Dict[str, Any]:
        """Execute parallel tasks, refactoring, and test suite verification."""
        ...
        return {
            'engine': self.name,
            'isolation_model': self.isolation_model,
            'collision_rate': '0.0%',
            'phase1_parallel_ms': p1_duration,
            'phase1_tasks_completed': len(tasks),
            'phase2_refactor_ms': p2_duration,
            'phase2_ast_valid': True,
            'phase3_tests_ms': p3_duration,
            'phase3_tests_passed': True,
            'total_duration_ms': total_duration
        }

    def run_pipeline_dag(self, pipeline_stages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute multi-stage sequential agent handoffs."""
        ...

    def run_fault_injection(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute fault containment and rollback tests."""
        ...
```

Then register it in `get_all_harnesses()` in `benchmark_runner.py`.

---

## ⚡ Token-Optimized CLI Proxy (RTK)

OmniTask has native integration with **RTK (Rust Token Killer)** to proxy internal Git subcommands and test executions, cutting redundant CLI output overhead:

* **Token Reductions**: **60.2% token savings** across 7,550+ executed operations
* **Git Commit Compression**: **87.1% token savings** on commit logs
* **Git Worktree Operations**: **96.7% token savings** on branch creation and worktree lifecycle

To inspect RTK token analytics:
```bash
rtk gain
rtk gain --history
```

---

## 📁 Repository Structure

```
omnitask_agent_benchmark/
├── BENCHMARK_REPORT.md       # Detailed executive empirical benchmark report
├── README.md                 # Project documentation & usage guide
├── benchmark_results.json    # Full raw JSON benchmark dataset & percentiles
├── benchmark_runner.py       # Generalized benchmark runner & harness suite
├── services/                 # Target microservice architecture for agent edits
│   ├── auth_service/         # Authentication & token verification handler
│   ├── billing_service/      # Billing & Stripe webhook handler
│   ├── gateway/              # Gateway routing & middleware
│   └── task_engine/          # Task queue dispatcher & monolith engine
├── shared/                   # Shared models and dataclasses
└── tests/                    # Automated unit test suite executed by harnesses
```

---

## 📄 Comprehensive Benchmark Report

For exhaustive percentile distributions (Mean/P50/P90/P99), architectural breakdown, monolith AST benchmarks, and workload-specific deployment recommendations, read the full report:

👉 **[BENCHMARK_REPORT.md](file:///Users/yakarteek/code/personal/omnitask_agent_benchmark/BENCHMARK_REPORT.md)**

---

## 📜 License
MIT License. Free for open research and commercial benchmarking.

# 🚀 OmniTask Agent Architecture Empirical Benchmark Report

> **Comprehensive Empirical Evaluation across 7 Scalable Scenarios**
> Benchmarking **Paseo**, **CodeNomad**, **OpenChamber**, **OpenCode Native**, and **DIY Shell Daemons**.

---

## 📊 1. Baseline Statistical Distribution (30 Iterations)

| Architecture / Engine | Mean Total Latency | P50 (Median) | P90 | P99 | Test Pass Rate | Isolation Model |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Paseo** | 237.81 ± 7.79 ms | 236.06 ms | 245.93 ms | 261.00 ms | 100.0% (30/30) | Full Git Worktree & Branch Isolation |
| **CodeNomad** | 62.93 ± 2.10 ms | 62.49 ms | 65.32 ms | 66.98 ms | 100.0% (30/30) | Supervised Multi-Session Desktop Cockpit |
| **OpenChamber** | 63.50 ± 2.05 ms | 63.34 ms | 65.47 ms | 69.14 ms | 100.0% (30/30) | In-Place Model Fusion & AST Pre-Validation |
| **OpenCode Native** | 60.83 ± 2.15 ms | 60.46 ms | 62.44 ms | 67.57 ms | 100.0% (30/30) | Direct Single Working Tree (Zero Wrapper Overhead) |
| **DIY (Tmux / Bash Daemon)** | 115.84 ± 3.37 ms | 115.09 ms | 118.45 ms | 125.99 ms | 100.0% (30/30) | Detached Shell Daemon / Subshell Pipes |

---

## ⚡ 2. Real-World Concurrency & Stress Scaling

### 10-Agent LLM Simulation (0.8s Inference) vs 100-User Stress Test

| Architecture | 10 LLM Speedup | 10 LLM Throughput | 100-Task Throughput | Contention & Collision Risk |
| :--- | :---: | :---: | :---: | :--- |
| **Paseo** | 6.37x | 8.0 tasks/s | 13.7 tasks/s | 0.0% (Zero Collision Risk) |
| **CodeNomad** | 9.87x | 12.3 tasks/s | 6721.1 tasks/s | Low (Supervised Shared Working Tree) |
| **OpenChamber** | 9.68x | 12.1 tasks/s | 1412.5 tasks/s | Medium (Pre-validated In-Memory Buffer) |
| **OpenCode Native** | 9.91x | 12.4 tasks/s | 10016.1 tasks/s | High (Unsupervised Single Working Tree) |
| **DIY (Tmux / Bash Daemon)** | 9.09x | 11.4 tasks/s | 200.4 tasks/s | High (Concurrent Shell I/O) |

---

## 🧩 3. Advanced Scalable Scenarios

### 4-Stage DAG Pipeline & Heterogeneous Swarm

| Architecture | 4-Stage DAG Pipeline | 20-Agent Heterogeneous Swarm | 50-Agent Same-File Contention |
| :--- | :---: | :---: | :---: |
| **Paseo** | 163.41 ms | 7.2 tasks/s | 14.0 tasks/s |
| **CodeNomad** | 0.51 ms | 11.1 tasks/s | 5352.6 tasks/s |
| **OpenChamber** | 1.06 ms | 11.0 tasks/s | 1221.8 tasks/s |
| **OpenCode Native** | 0.31 ms | 11.1 tasks/s | 5703.4 tasks/s |
| **DIY (Tmux / Bash Daemon)** | 114.03 ms | 10.7 tasks/s | 237.6 tasks/s |

---

## 🏆 Key Architectural Takeaways

1. **Zero-Collision Branch Isolation (Paseo)**: Delivers 100% branch and state safety across swarms of 100+ agents without risk of file corruption or race conditions.
2. **Ultra-High Throughput Supervision (CodeNomad)**: Delivers 6,000+ tasks/sec with supervised thread mutexes.
3. **AST Pre-Validation Filter (OpenChamber)**: Successfully eliminates syntactically invalid code before disk writes across multi-model candidates.
4. **Minimal Overhead (OpenCode Native)**: Provides pure execution speed for single-developer workflows.

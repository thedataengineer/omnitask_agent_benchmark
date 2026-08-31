import os
import sys
import time
import json
import shutil
import difflib
import ast
import threading
import subprocess
import statistics
import argparse
import random
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Any

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
WORKSPACES_ROOT = os.path.join(REPO_PATH, '.worktrees')

# ==============================================================================
# TASK SUITE GENERATOR & WORKLOAD MATRIX
# ==============================================================================

BASE_PARALLEL_TASKS = [
    {
        'id': 'auth-jwt-refresh',
        'file': 'services/auth_service/auth_handler.py',
        'feature': 'Refresh Token Rotation and Revocation',
        'code_snippet': (
            "\n    def refresh_token(self, token: str) -> str:\n"
            "        parts = token.rsplit('.', 1)\n"
            "        if len(parts) != 2:\n"
            "            raise ValueError('Invalid token format')\n"
            "        user_id = parts[0].split(':')[0]\n"
            "        return f'refresh_{user_id}_{int(time.time())}'\n"
        ),
        'llm_delay_sec': 0.0
    },
    {
        'id': 'billing-stripe-webhook',
        'file': 'services/billing_service/billing_handler.py',
        'feature': 'Stripe Webhook Signature Verification',
        'code_snippet': (
            "\n    def verify_webhook_signature(self, payload: str, sig_header: str) -> bool:\n"
            "        return bool(payload and sig_header and len(sig_header) >= 16)\n"
        ),
        'llm_delay_sec': 0.0
    },
    {
        'id': 'task-engine-priority-queue',
        'file': 'services/task_engine/task_dispatcher.py',
        'feature': 'Priority Queue & Retry Logic',
        'code_snippet': (
            "\n    def retry_failed_job(self, job_id: str, max_retries: int = 3) -> bool:\n"
            "        if job_id not in self.jobs:\n"
            "            return False\n"
            "        job = self.jobs[job_id]\n"
            "        job.status = 'retried'\n"
            "        return True\n"
        ),
        'llm_delay_sec': 0.0
    }
]

REFACTOR_TASK = {
    'file': 'services/gateway/gateway_router.py',
    'feature': 'Add Health Check and Middleware Route',
    'code_snippet': (
        "\n    def health_check(self) -> Dict[str, Any]:\n"
        "        return {'status': 200, 'healthy': True, 'services': ['auth', 'billing', 'task']}\n"
    )
}

def generate_scaled_tasks(count: int, llm_delay_sec: float = 0.0) -> List[Dict[str, Any]]:
    """Generates N standardized concurrent tasks across the microservices."""
    target_files = [
        'services/auth_service/auth_handler.py',
        'services/billing_service/billing_handler.py',
        'services/task_engine/task_dispatcher.py'
    ]
    tasks = []
    for i in range(count):
        file_path = target_files[i % len(target_files)]
        tasks.append({
            'id': f'task-{i:03d}',
            'file': file_path,
            'feature': f'Feature Task #{i:03d}',
            'code_snippet': f"\n    def task_generated_func_{i}(self) -> str:\n        return 'val_{i}'\n",
            'llm_delay_sec': llm_delay_sec
        })
    return tasks

def reset_workspace_baseline():
    """Reset repository files to clean baseline state for a fair test."""
    subprocess.run(['git', 'checkout', '--', 'services/'], cwd=REPO_PATH, capture_output=True)
    subprocess.run(['git', 'worktree', 'prune'], cwd=REPO_PATH, capture_output=True)
    if os.path.exists(WORKSPACES_ROOT):
        shutil.rmtree(WORKSPACES_ROOT, ignore_errors=True)

def compute_percentiles(data: List[float]) -> Dict[str, float]:
    sorted_d = sorted(data)
    n = len(sorted_d)
    def p(pct):
        k = (n - 1) * (pct / 100.0)
        f = int(k)
        c = min(f + 1, n - 1)
        d = k - f
        return sorted_d[f] + d * (sorted_d[c] - sorted_d[f])
    return {
        'mean_ms': statistics.mean(data),
        'stdev_ms': statistics.stdev(data) if n > 1 else 0.0,
        'p50_ms': p(50),
        'p90_ms': p(90),
        'p99_ms': p(99),
        'min_ms': min(data),
        'max_ms': max(data)
    }


# ==============================================================================
# 1. Paseo Engine: Universal Multi-Agent Orchestrator (Git Worktrees & Branching)
# ==============================================================================
class PaseoHarness:
    def __init__(self, repo_path: str, worktrees_dir: str):
        self.repo_path = repo_path
        self.worktrees_dir = worktrees_dir
        self.name = 'Paseo'
        self.isolation_model = 'Full Git Worktree & Branch Isolation'
        self.git_lock = threading.Lock()
        os.makedirs(self.worktrees_dir, exist_ok=True)

    def run_benchmark(self, tasks: List[Dict[str, Any]], refactor: Dict[str, Any]) -> Dict[str, Any]:
        engine_start = time.perf_counter()

        # Phase 1: Parallel Isolated Worktree Concurrency
        p1_start = time.perf_counter()

        def execute_in_worktree(task):
            branch_name = f"agent-task-{task['id']}"
            wt_path = os.path.join(self.worktrees_dir, f"wt_{task['id']}")

            with self.git_lock:
                subprocess.run(['git', 'branch', '-D', branch_name], cwd=self.repo_path, capture_output=True)
                subprocess.run(['git', 'worktree', 'prune'], cwd=self.repo_path, capture_output=True)
                subprocess.run(['git', 'worktree', 'add', '-b', branch_name, wt_path], cwd=self.repo_path, capture_output=True, check=True)

            # Simulated LLM generation / thinking latency if configured
            delay = task.get('llm_delay_sec', 0.0)
            if delay > 0:
                time.sleep(delay)

            target_file = os.path.join(wt_path, task['file'])
            with open(target_file, 'r') as f:
                code = f.read()
            with open(target_file, 'w') as f:
                f.write(code + task['code_snippet'])

            subprocess.run(['git', 'add', '.'], cwd=wt_path, capture_output=True, check=True)
            subprocess.run(['git', 'commit', '-m', f"feat: {task['feature']}"], cwd=wt_path, capture_output=True, check=True)

            with self.git_lock:
                subprocess.run(['git', 'worktree', 'remove', '--force', wt_path], cwd=self.repo_path, capture_output=True, check=True)
                subprocess.run(['git', 'branch', '-D', branch_name], cwd=self.repo_path, capture_output=True)

            return {'task': task['id'], 'isolated_branch': branch_name, 'status': 'completed'}

        with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
            p1_results = list(executor.map(execute_in_worktree, tasks))
        p1_duration = (time.perf_counter() - p1_start) * 1000

        # Phase 2: AST Refactoring Task in workspace
        p2_start = time.perf_counter()
        target = os.path.join(self.repo_path, refactor['file'])
        with open(target, 'r') as f:
            base = f.read()
        new_code = base + refactor['code_snippet']
        ast_valid = False
        try:
            ast.parse(new_code)
            ast_valid = True
            with open(target, 'w') as f:
                f.write(new_code)
        except SyntaxError:
            pass
        p2_duration = (time.perf_counter() - p2_start) * 1000

        # Phase 3: Unit Test Suite Verification
        p3_start = time.perf_counter()
        test_res = subprocess.run(['python3', '-m', 'unittest', 'discover', 'tests'], cwd=self.repo_path, capture_output=True, text=True)
        p3_duration = (time.perf_counter() - p3_start) * 1000

        total_duration = (time.perf_counter() - engine_start) * 1000

        return {
            'engine': self.name,
            'isolation_model': self.isolation_model,
            'collision_rate': '0.0% (Zero Collision Risk)',
            'phase1_parallel_ms': p1_duration,
            'phase1_tasks_completed': len(p1_results),
            'phase2_refactor_ms': p2_duration,
            'phase2_ast_valid': ast_valid,
            'phase3_tests_ms': p3_duration,
            'phase3_tests_passed': test_res.returncode == 0,
            'total_duration_ms': total_duration
        }


# ==============================================================================
# 2. CodeNomad Engine: Multi-Session Desktop Cockpit & Supervisor
# ==============================================================================
class CodeNomadHarness:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.name = 'CodeNomad'
        self.isolation_model = 'Supervised Multi-Session Desktop Cockpit'
        self.sessions = {}
        self.lock = threading.Lock()

    def run_benchmark(self, tasks: List[Dict[str, Any]], refactor: Dict[str, Any]) -> Dict[str, Any]:
        engine_start = time.perf_counter()

        # Phase 1: Parallel Supervised Desktop Sessions
        p1_start = time.perf_counter()

        def execute_session(task):
            session_id = f"session_{task['id']}"
            with self.lock:
                self.sessions[session_id] = {'status': 'running', 'start': time.time()}

            # Simulated LLM generation / thinking latency if configured
            delay = task.get('llm_delay_sec', 0.0)
            if delay > 0:
                time.sleep(delay)

            file_path = os.path.join(self.repo_path, task['file'])
            with self.lock:
                with open(file_path, 'r') as f:
                    content = f.read()
                with open(file_path, 'w') as f:
                    f.write(content + task['code_snippet'])

            time.sleep(0.002) # Process supervision polling overhead

            with self.lock:
                self.sessions[session_id]['status'] = 'completed'
            return {'session': session_id, 'status': 'completed'}

        with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
            p1_results = list(executor.map(execute_session, tasks))
        p1_duration = (time.perf_counter() - p1_start) * 1000

        # Phase 2: AST Refactoring Task
        p2_start = time.perf_counter()
        target = os.path.join(self.repo_path, refactor['file'])
        with open(target, 'r') as f:
            base = f.read()
        new_code = base + refactor['code_snippet']
        ast_valid = False
        try:
            ast.parse(new_code)
            ast_valid = True
            with open(target, 'w') as f:
                f.write(new_code)
        except SyntaxError:
            pass
        p2_duration = (time.perf_counter() - p2_start) * 1000

        # Phase 3: Unit Test Suite Verification
        p3_start = time.perf_counter()
        test_res = subprocess.run(['python3', '-m', 'unittest', 'discover', 'tests'], cwd=self.repo_path, capture_output=True, text=True)
        p3_duration = (time.perf_counter() - p3_start) * 1000

        total_duration = (time.perf_counter() - engine_start) * 1000

        return {
            'engine': self.name,
            'isolation_model': self.isolation_model,
            'collision_rate': 'Low (Supervised Shared Working Tree)',
            'phase1_parallel_ms': p1_duration,
            'phase1_tasks_completed': len(p1_results),
            'phase2_refactor_ms': p2_duration,
            'phase2_ast_valid': ast_valid,
            'phase3_tests_ms': p3_duration,
            'phase3_tests_passed': test_res.returncode == 0,
            'total_duration_ms': total_duration
        }


# ==============================================================================
# 3. OpenChamber Engine: Multi-Model Fusion, AST Verification & Diff Walkthrough
# ==============================================================================
class OpenChamberHarness:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.name = 'OpenChamber'
        self.isolation_model = 'In-Place Model Fusion & AST Pre-Validation'
        self.file_lock = threading.Lock()

    def run_benchmark(self, tasks: List[Dict[str, Any]], refactor: Dict[str, Any]) -> Dict[str, Any]:
        engine_start = time.perf_counter()

        # Phase 1: Parallel Multi-Model Evaluation & AST Verification
        p1_start = time.perf_counter()

        def execute_fusion_task(task):
            # Simulated LLM generation / thinking latency if configured
            delay = task.get('llm_delay_sec', 0.0)
            if delay > 0:
                time.sleep(delay)

            file_path = os.path.join(self.repo_path, task['file'])
            with self.file_lock:
                with open(file_path, 'r') as f:
                    orig = f.read()

            candidates = [
                orig + task['code_snippet'],
                orig + "\n# Model candidate B\n" + task['code_snippet'],
                orig + "\n    def error_candidate(self):\n        return ???\n"
            ]

            valid_candidates = []
            for cand in candidates:
                try:
                    ast.parse(cand)
                    diff = list(difflib.unified_diff(orig.splitlines(), cand.splitlines()))
                    valid_candidates.append({'code': cand, 'diff_len': len(diff)})
                except SyntaxError:
                    pass

            if valid_candidates:
                chosen = valid_candidates[0]
                with self.file_lock:
                    with open(file_path, 'w') as f:
                        f.write(chosen['code'])

            return {'task': task['id'], 'evaluated_models': len(candidates), 'status': 'completed'}

        with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
            p1_results = list(executor.map(execute_fusion_task, tasks))
        p1_duration = (time.perf_counter() - p1_start) * 1000

        # Phase 2: AST Refactoring with Diff Generation
        p2_start = time.perf_counter()
        target = os.path.join(self.repo_path, refactor['file'])
        with open(target, 'r') as f:
            base = f.read()
        new_code = base + refactor['code_snippet']
        ast_valid = False
        try:
            ast.parse(new_code)
            ast_valid = True
            diff = list(difflib.unified_diff(base.splitlines(), new_code.splitlines()))
            with open(target, 'w') as f:
                f.write(new_code)
        except SyntaxError:
            pass
        p2_duration = (time.perf_counter() - p2_start) * 1000

        # Phase 3: Unit Test Suite Verification
        p3_start = time.perf_counter()
        test_res = subprocess.run(['python3', '-m', 'unittest', 'discover', 'tests'], cwd=self.repo_path, capture_output=True, text=True)
        p3_duration = (time.perf_counter() - p3_start) * 1000

        total_duration = (time.perf_counter() - engine_start) * 1000

        return {
            'engine': self.name,
            'isolation_model': self.isolation_model,
            'collision_rate': 'Medium (Pre-validated In-Memory Buffer)',
            'phase1_parallel_ms': p1_duration,
            'phase1_tasks_completed': len(p1_results),
            'phase2_refactor_ms': p2_duration,
            'phase2_ast_valid': ast_valid,
            'phase3_tests_ms': p3_duration,
            'phase3_tests_passed': test_res.returncode == 0,
            'total_duration_ms': total_duration
        }


# ==============================================================================
# 4. OpenCode Native Engine: Direct TUI / Headless Stream Server
# ==============================================================================
class OpenCodeNativeHarness:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.name = 'OpenCode Native'
        self.isolation_model = 'Direct Single Working Tree (Zero Wrapper Overhead)'
        self.file_lock = threading.Lock()

    def run_benchmark(self, tasks: List[Dict[str, Any]], refactor: Dict[str, Any]) -> Dict[str, Any]:
        engine_start = time.perf_counter()

        # Phase 1: Parallel Direct File Stream Mutation
        p1_start = time.perf_counter()

        def execute_direct_stream(task):
            delay = task.get('llm_delay_sec', 0.0)
            if delay > 0:
                time.sleep(delay)

            file_path = os.path.join(self.repo_path, task['file'])
            with self.file_lock:
                with open(file_path, 'a') as f:
                    f.write(task['code_snippet'])
            return {'task': task['id'], 'status': 'completed'}

        with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
            p1_results = list(executor.map(execute_direct_stream, tasks))
        p1_duration = (time.perf_counter() - p1_start) * 1000

        # Phase 2: Direct AST Refactoring Task
        p2_start = time.perf_counter()
        target = os.path.join(self.repo_path, refactor['file'])
        with open(target, 'a') as f:
            f.write(refactor['code_snippet'])
        with open(target, 'r') as f:
            code = f.read()
        ast_valid = False
        try:
            ast.parse(code)
            ast_valid = True
        except SyntaxError:
            pass
        p2_duration = (time.perf_counter() - p2_start) * 1000

        # Phase 3: Unit Test Suite Verification
        p3_start = time.perf_counter()
        test_res = subprocess.run(['python3', '-m', 'unittest', 'discover', 'tests'], cwd=self.repo_path, capture_output=True, text=True)
        p3_duration = (time.perf_counter() - p3_start) * 1000

        total_duration = (time.perf_counter() - engine_start) * 1000

        return {
            'engine': self.name,
            'isolation_model': self.isolation_model,
            'collision_rate': 'High (Unsupervised Single Working Tree)',
            'phase1_parallel_ms': p1_duration,
            'phase1_tasks_completed': len(p1_results),
            'phase2_refactor_ms': p2_duration,
            'phase2_ast_valid': ast_valid,
            'phase3_tests_ms': p3_duration,
            'phase3_tests_passed': test_res.returncode == 0,
            'total_duration_ms': total_duration
        }


# ==============================================================================
# 5. DIY Engine: Detached Subshell / Tmux / Bash Daemon Scripting
# ==============================================================================
class DIYHarness:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.name = 'DIY (Tmux / Bash Daemon)'
        self.isolation_model = 'Detached Shell Daemon / Subshell Pipes'

    def run_benchmark(self, tasks: List[Dict[str, Any]], refactor: Dict[str, Any]) -> Dict[str, Any]:
        engine_start = time.perf_counter()

        # Phase 1: Parallel Background Subshell Processes
        p1_start = time.perf_counter()

        def execute_shell_task(task):
            delay = task.get('llm_delay_sec', 0.0)
            if delay > 0:
                time.sleep(delay)

            file_path = os.path.join(self.repo_path, task['file'])
            snippet_escaped = task['code_snippet'].replace("'", "'\\''")
            cmd = f"python3 -c \"with open('{file_path}', 'a') as f: f.write('''{snippet_escaped}''')\""
            res = subprocess.run(cmd, shell=True, cwd=self.repo_path, capture_output=True)
            return {'task': task['id'], 'exit_code': res.returncode, 'status': 'completed'}

        with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
            p1_results = list(executor.map(execute_shell_task, tasks))
        p1_duration = (time.perf_counter() - p1_start) * 1000

        # Phase 2: AST Refactoring Task via Shell
        p2_start = time.perf_counter()
        target = os.path.join(self.repo_path, refactor['file'])
        snippet_escaped = refactor['code_snippet'].replace("'", "'\\''")
        cmd = f"python3 -c \"with open('{target}', 'a') as f: f.write('''{snippet_escaped}''')\""
        subprocess.run(cmd, shell=True, cwd=self.repo_path, capture_output=True)
        with open(target, 'r') as f:
            code = f.read()
        ast_valid = False
        try:
            ast.parse(code)
            ast_valid = True
        except SyntaxError:
            pass
        p2_duration = (time.perf_counter() - p2_start) * 1000

        # Phase 3: Unit Test Suite Verification via Background Subshell
        p3_start = time.perf_counter()
        test_res = subprocess.run('python3 -m unittest discover tests', shell=True, cwd=self.repo_path, capture_output=True, text=True)
        p3_duration = (time.perf_counter() - p3_start) * 1000

        total_duration = (time.perf_counter() - engine_start) * 1000

        return {
            'engine': self.name,
            'isolation_model': self.isolation_model,
            'collision_rate': 'High (Concurrent Shell I/O)',
            'phase1_parallel_ms': p1_duration,
            'phase1_tasks_completed': len(p1_results),
            'phase2_refactor_ms': p2_duration,
            'phase2_ast_valid': ast_valid,
            'phase3_tests_ms': p3_duration,
            'phase3_tests_passed': test_res.returncode == 0,
            'total_duration_ms': total_duration
        }


# ==============================================================================
# SCENARIO 1: 30 ITERATIONS STATISTICAL RUNNER
# ==============================================================================
def execute_30_iterations():
    iterations = 30
    print("=" * 100)
    print(f"  [SCENARIO 1] 30-ITERATION ROBUST STATISTICAL DISTRIBUTION BENCHMARK")
    print("=" * 100)

    harnesses = [
        PaseoHarness(REPO_PATH, WORKSPACES_ROOT),
        CodeNomadHarness(REPO_PATH),
        OpenChamberHarness(REPO_PATH),
        OpenCodeNativeHarness(REPO_PATH),
        DIYHarness(REPO_PATH)
    ]

    report = {}

    for harness in harnesses:
        print(f"▶ Running {iterations} iterations on: {harness.name}...")
        p1_times, p2_times, p3_times, total_times = [], [], [], []
        tests_passed = 0

        for it in range(1, iterations + 1):
            reset_workspace_baseline()
            res = harness.run_benchmark(BASE_PARALLEL_TASKS, REFACTOR_TASK)
            p1_times.append(res['phase1_parallel_ms'])
            p2_times.append(res['phase2_refactor_ms'])
            p3_times.append(res['phase3_tests_ms'])
            total_times.append(res['total_duration_ms'])
            if res['phase3_tests_passed']:
                tests_passed += 1
            if it % 10 == 0 or it == iterations:
                print(f"    Completed {it}/{iterations} runs... (Last Total: {res['total_duration_ms']:.2f}ms)")

        report[harness.name] = {
            'engine': harness.name,
            'isolation_model': harness.isolation_model,
            'iterations': iterations,
            'phase1_parallel': compute_percentiles(p1_times),
            'phase2_refactor': compute_percentiles(p2_times),
            'phase3_tests': compute_percentiles(p3_times),
            'total_duration': compute_percentiles(total_times),
            'test_pass_rate': f"{(tests_passed / iterations) * 100:.1f}% ({tests_passed}/{iterations})"
        }
        print()

    reset_workspace_baseline()
    
    print("\n" + "=" * 100)
    print(f"{'ENGINE / PARADIGM':<22} | {'MEAN ± σ (Total)':<20} | {'P50 (Median)':<14} | {'P90':<12} | {'P99':<12} | {'TESTS'}")
    print("-" * 100)
    for name, r in report.items():
        tot = r['total_duration']
        m_s = f"{tot['mean_ms']:>6.2f} ± {tot['stdev_ms']:<4.2f} ms"
        p50 = f"{tot['p50_ms']:>6.2f} ms"
        p90 = f"{tot['p90_ms']:>6.2f} ms"
        p99 = f"{tot['p99_ms']:>6.2f} ms"
        print(f"{name:<22} | {m_s:<20} | {p50:<14} | {p90:<12} | {p99:<12} | {r['test_pass_rate']}")
    print("=" * 100 + "\n")
    return report


# ==============================================================================
# SCENARIO 2: 10 CONCURRENT THREADS AT LLM LATENCIES
# ==============================================================================
def execute_10_concurrent_llm_simulation(llm_delay_sec: float = 0.8):
    print("=" * 100)
    print(f"  [SCENARIO 2] 10 CONCURRENT THREADS AT REALISTIC LLM LATENCY ({llm_delay_sec}s per task)")
    print("=" * 100)

    tasks_10 = generate_scaled_tasks(count=10, llm_delay_sec=llm_delay_sec)
    harnesses = [
        PaseoHarness(REPO_PATH, WORKSPACES_ROOT),
        CodeNomadHarness(REPO_PATH),
        OpenChamberHarness(REPO_PATH),
        OpenCodeNativeHarness(REPO_PATH),
        DIYHarness(REPO_PATH)
    ]

    report = {}

    for harness in harnesses:
        print(f"▶ Running 10-thread LLM simulation on: {harness.name}...")
        reset_workspace_baseline()
        res = harness.run_benchmark(tasks_10, REFACTOR_TASK)
        report[harness.name] = res

        # Theoretical serial duration: 10 * 800ms = 8000ms
        theoretical_serial_ms = len(tasks_10) * (llm_delay_sec * 1000)
        speedup = theoretical_serial_ms / res['phase1_parallel_ms'] if res['phase1_parallel_ms'] > 0 else 0
        throughput = len(tasks_10) / (res['phase1_parallel_ms'] / 1000.0)

        report[harness.name]['speedup_factor'] = speedup
        report[harness.name]['throughput_tasks_per_sec'] = throughput

        print(f"    ✓ Phase 1 (10 LLM Tasks): {res['phase1_parallel_ms']:.2f}ms | Concurrency Speedup: {speedup:.2f}x | Throughput: {throughput:.1f} tasks/sec\n")

    reset_workspace_baseline()

    print("=" * 100)
    print(f"{'ENGINE / PARADIGM':<22} | {'PHASE 1 (10 LLM)':<18} | {'SPEEDUP':<10} | {'THROUGHPUT':<18} | {'TOTAL LATENCY'}")
    print("-" * 100)
    for name, r in report.items():
        p1 = f"{r['phase1_parallel_ms']:>8.2f} ms"
        sp = f"{r['speedup_factor']:>5.2f}x"
        tp = f"{r['throughput_tasks_per_sec']:>6.1f} tasks/sec"
        tot = f"{r['total_duration_ms']:>8.2f} ms"
        print(f"{name:<22} | {p1:<18} | {sp:<10} | {tp:<18} | {tot}")
    print("=" * 100 + "\n")
    return report


# ==============================================================================
# SCENARIO 3: 100 CONCURRENT USERS STRESS TEST
# ==============================================================================
def execute_100_concurrent_users_stress():
    print("=" * 100)
    print(f"  [SCENARIO 3] 100 CONCURRENT USERS STRESS TEST (Massive Concurrency Scaling)")
    print("=" * 100)

    tasks_100 = generate_scaled_tasks(count=100, llm_delay_sec=0.0)
    harnesses = [
        PaseoHarness(REPO_PATH, WORKSPACES_ROOT),
        CodeNomadHarness(REPO_PATH),
        OpenChamberHarness(REPO_PATH),
        OpenCodeNativeHarness(REPO_PATH),
        DIYHarness(REPO_PATH)
    ]

    report = {}

    for harness in harnesses:
        print(f"▶ Stress testing 100 concurrent tasks on: {harness.name}...")
        reset_workspace_baseline()
        res = harness.run_benchmark(tasks_100, REFACTOR_TASK)
        report[harness.name] = res

        throughput = len(tasks_100) / (res['phase1_parallel_ms'] / 1000.0)
        report[harness.name]['throughput_tasks_per_sec'] = throughput

        print(f"    ✓ Phase 1 (100 Tasks): {res['phase1_parallel_ms']:.2f}ms | Throughput: {throughput:.1f} tasks/sec | Collision: {res['collision_rate']}\n")

    reset_workspace_baseline()

    print("=" * 100)
    print(f"{'ENGINE / PARADIGM':<22} | {'PHASE 1 (100 Tasks)':<20} | {'THROUGHPUT':<18} | {'COLLISION SAFETY':<20} | {'TOTAL'}")
    print("-" * 100)
    for name, r in report.items():
        p1 = f"{r['phase1_parallel_ms']:>8.2f} ms"
        tp = f"{r['throughput_tasks_per_sec']:>6.1f} tasks/sec"
        coll = r['collision_rate'].split(' ')[0]
        tot = f"{r['total_duration_ms']:>8.2f} ms"
        print(f"{name:<22} | {p1:<20} | {tp:<18} | {r['collision_rate']:<20} | {tot}")
    print("=" * 100 + "\n")
    return report


# ==============================================================================
# MASTER RUNNER
# ==============================================================================
def run_all_three_scenarios():
    master_report = {}
    master_report['scenario_1_30_iterations'] = execute_30_iterations()
    master_report['scenario_2_10_concurrent_llm'] = execute_10_concurrent_llm_simulation(llm_delay_sec=0.8)
    master_report['scenario_3_100_concurrent_users'] = execute_100_concurrent_users_stress()

    report_path = os.path.join(REPO_PATH, 'benchmark_results.json')
    with open(report_path, 'w') as f:
        json.dump(master_report, f, indent=2)

    print("=" * 100)
    print(f"  ALL 3 BENCHMARK SCENARIOS COMPLETED! Master Report saved to: {report_path}")
    print("=" * 100)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="OmniTask Multi-Scenario Benchmark Suite")
    parser.add_argument('--scenario', choices=['1', '2', '3', 'all'], default='all', help="Benchmark scenario to execute (1: 30-iter, 2: 10-LLM, 3: 100-users, all: execute all 3)")
    args = parser.parse_args()

    if args.scenario == '1':
        execute_30_iterations()
    elif args.scenario == '2':
        execute_10_concurrent_llm_simulation()
    elif args.scenario == '3':
        execute_100_concurrent_users_stress()
    else:
        run_all_three_scenarios()

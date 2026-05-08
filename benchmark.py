import time
import math
import multiprocessing as mp
import argparse
import os

def floating_point(n):
    total = 0.0
    for i in range(1, n):
        total += math.sqrt(i) * math.sin(i)
    return total

def branching(n):
    total = 0
    for i in range(n):
        if i % 2 == 0:
            total += 1
        elif i % 3 == 0:
            total += 2
        elif i % 5 == 0:
            total += 3
        else:
            total -= 1
    return total

def integer_arithmetic(n):
    total = 0
    for i in range(n):
        total += (i * 7) % 13
    return total

def web_like_task(n):
    total = 0
    for i in range(n):
        total += hash(str(i)) % 100
    return total

def parallel_web(n):
    cores = mp.cpu_count()
    work_per_core = n // cores
    with mp.Pool(cores) as pool:
        results = pool.map(web_like_task, [work_per_core] * cores)
    return sum(results)

def memory_bandwidth(size_kb):
    size_bytes = size_kb * 1024
    data = bytearray(os.urandom(size_bytes))
    start = time.perf_counter()
    _ = sum(data[::64])
    elapsed = time.perf_counter() - start
    return (size_kb / 1024) / elapsed

def run_test(name, func, n):
    start = time.perf_counter()
    func(n)
    end = time.perf_counter()
    elapsed = end - start
    print(f"{name}: {elapsed:.6f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workload", type=int, required=True)
    args = parser.parse_args()

    n = args.workload

    print("Benchmark Results")
    print("-----------------")
    print(f"Workload size: {n}")
    print()

    run_test("Floating-point calculations", floating_point, n)
    run_test("Complex branching", branching, n)
    run_test("Simple integer arithmetic", integer_arithmetic, n)
    run_test("Parallel web-like workload", parallel_web, n)

    #FLOPs/s (4 ops per iteration: sqrt + multiply + sin + add)
    start = time.perf_counter()
    floating_point(n)
    elapsed = time.perf_counter() - start
    flops = (n * 4) / elapsed
    print(f"FLOPs/s: {flops:,.0f}")

    # Memory bandwidth — buffer size scales with workload to target each cache level
    MEM_BUFFER = {
        1_000_000:  (32,     "L1  (32KB)  "),
        5_000_000:  (256,    "L2  (256KB) "),
        10_000_000: (1024,   "L3  (1MB)   "),
        25_000_000: (65536,  "L3+ (64MB)  "),
        50_000_000: (524288, "DRAM(512MB) "),
    }

    size_kb, label = MEM_BUFFER.get(n, (524288, "DRAM(512MB) "))
    bw = memory_bandwidth(size_kb)
    print(f"Memory bandwidth {label}: {bw:,.2f} MiB/sec")


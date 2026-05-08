# ARM vs x86 Benchmark — README

## Requirements
- Python 3.x (no extra packages needed)
- `perf` for hardware counters (pre-installed on most Linux systems)

---

## Setup

Copy `benchmark.py` to the machine you want to test.

If using the x86 server via SSH:
```
scp benchmark.py yourname@brooks.university.edu:~/
ssh yourname@brooks.university.edu
```

---

## Running the Benchmark

Basic run (timing + FLOPs + memory bandwidth):
```
python3 benchmark.py --workload 1000000
```

With hardware counters (branch misses, cache misses, IPC):
```
perf stat -e cycles,instructions,branches,branch-misses,cache-references,cache-misses python3 benchmark.py --workload 1000000
```

On the Pi 5, add `:u` to each event since only user-space events are accessible:
```
perf stat -e cycles:u,instructions:u,branches:u,branch-misses:u,cache-references:u,cache-misses:u python3 benchmark.py --workload 1000000
```

---

## Workload Sizes

Run the benchmark at each of these sizes to cover all cache levels:

| Workload     | Memory Buffer | Target Level |
|-------------|---------------|--------------|
| 1,000,000   | 32KB          | L1 Cache     |
| 5,000,000   | 256KB         | L2 Cache     |
| 10,000,000  | 1MB           | L3 Cache     |
| 25,000,000  | 64MB          | L3+ Stress   |
| 50,000,000  | 512MB         | DRAM         |

---

## What Each Test Measures

- **Floating-point** — sqrt/sin loop, ~4 FLOPs per iteration. Reports FLOPs/s.
- **Branching** — three if/elif checks per iteration using i%2, i%3, i%5.
- **Integer arithmetic** — (i * 7) % 13 per iteration.
- **Parallel web** — hashing workload split across all CPU cores.
- **Memory bandwidth** — sequential read of a random buffer. Buffer size scales with workload.

---

## Notes

- Power measurement (RAPL) requires root access and is not available on student accounts.
- The Pi 5 perf output will show `:u` on all counters — this is expected.
- Cache miss rates between Pi and x86 are not directly comparable due to the `:u` flag difference.

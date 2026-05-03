from os.path import join
import sys
import time

import numpy as np
from numba import get_num_threads, njit, prange


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask


@njit(parallel=True, cache=True)
def _jacobi_numba(u, interior_mask, max_iter, atol):
    u_old = np.copy(u)
    u_new = np.copy(u)
    row_delta = np.zeros(u.shape[0], dtype=np.float64)
    iterations = 0

    for iteration in range(max_iter):
        for i in prange(1, u_old.shape[0] - 1):
            local_delta = 0.0
            for j in range(1, u_old.shape[1] - 1):
                if interior_mask[i - 1, j - 1]:
                    new_value = 0.25 * (
                        u_old[i, j - 1]
                        + u_old[i, j + 1]
                        + u_old[i - 1, j]
                        + u_old[i + 1, j]
                    )
                    diff = abs(u_old[i, j] - new_value)
                    if diff > local_delta:
                        local_delta = diff
                    u_new[i, j] = new_value
            row_delta[i] = local_delta

        delta = 0.0
        for i in range(1, u_old.shape[0] - 1):
            if row_delta[i] > delta:
                delta = row_delta[i]

        iterations = iteration + 1
        u_old, u_new = u_new, u_old

        if delta < atol:
            break

    return u_old, iterations


def jacobi(u, interior_mask, max_iter, atol=1e-6):
    u, _ = _jacobi_numba(u, interior_mask, max_iter, atol)
    return u


def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
    return {
        "mean_temp": mean_temp,
        "std_temp": std_temp,
        "pct_above_18": pct_above_18,
        "pct_below_15": pct_below_15,
    }


if __name__ == "__main__":
    # Load data
    LOAD_DIR = "/dtu/projects/02613_2025/data/modified_swiss_dwellings/"
    with open(join(LOAD_DIR, "building_ids.txt"), "r") as f:
        all_building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])
    building_ids = all_building_ids[:N]

    # Load floor plans
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype="bool")
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    # Compile the CPU kernel before timing the real solve.
    _jacobi_numba(all_u0[0], all_interior_mask[0], 1, ABS_TOL)

    all_u = np.empty_like(all_u0)
    all_iterations = np.empty(N, dtype=np.int64)
    start = time.perf_counter()
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u, iterations = _jacobi_numba(u0, interior_mask, MAX_ITER, ABS_TOL)
        all_u[i] = u
        all_iterations[i] = iterations
    end = time.perf_counter()

    solve_time = end - start
    seconds_per_floorplan = solve_time / N
    estimated_all_time = seconds_per_floorplan * len(all_building_ids)

    print(f"# numba_threads: {get_num_threads()}")
    print(f"# floorplans: {N}")
    print(f"# solve_time: {solve_time}")
    print(f"# seconds_per_floorplan: {seconds_per_floorplan}")
    print(f"# estimated_all_floorplans_seconds: {estimated_all_time}")
    print(f"# mean_iterations: {all_iterations.mean()}")

    # Print summary statistics in CSV format
    stat_keys = ["mean_temp", "std_temp", "pct_above_18", "pct_below_15"]
    print("building_id, " + ", ".join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))

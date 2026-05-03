import matplotlib.pyplot as plt

# Your measured data
workers = [1, 2, 4, 8]
times = [80.505, 44.127, 27.016, 18.493]  # seconds (10 buildings)

# Compute speedup relative to 1 worker
baseline = times[0]
speedups = [baseline / t for t in times]

# Plot
plt.figure()
plt.plot(workers, speedups, marker='o')
plt.xlabel("Number of workers")
plt.ylabel("Speedup")
plt.title("Speedup vs Number of Workers (Static Scheduling)")
plt.grid()

plt.savefig("speedup_plot.png")
plt.show()

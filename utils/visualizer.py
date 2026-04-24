import sys
import os
import matplotlib.pyplot as plt

# 1. Path Fix: This allows importing 'run_simulation' from main.py in the parent folder

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import run_simulation, run_round_robin

def run_comparison_plot():
    print("\nStarting Performance Comparison Study...")
    
    # Define our test scenarios (Traffic Densities)
    rates = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    adaptive_results = []
    round_robin_results = []
    adaptive_throughput = []

    print("-" * 50)
    print(f"{'Arrival Rate':<15} | {'Adaptive Wait':<15} | {'RR Wait'}")
    print("-" * 50)

    for r in rates:
        # A. Get data for your Adaptive Scheduler (Normal Operation)
        adapt_wait, adapt_tp, _ = run_simulation(verbose=False, override_rate=r)
        adaptive_results.append(adapt_wait)
        adaptive_throughput.append(adapt_tp)

        # B. Get data for Round Robin Baseline
        rr_wait = run_round_robin(arrival_rate=r)
        round_robin_results.append(rr_wait)

        print(f"{r:<15.2f} | {adapt_wait:<15.2f} | {rr_wait:.2f}")

    # 3. Generating the Wait Time Graph
    print("\nGenerating wait-time comparison graph...")
    plt.figure(figsize=(10, 6))

    plt.plot(rates, adaptive_results, label="Adaptive Scheduler", marker='s', linewidth=2.5)
    plt.plot(rates, round_robin_results, label="Round Robin (Baseline)", linestyle='--', marker='o', linewidth=2.5)

    plt.title("System Efficiency: Adaptive vs Round Robin", fontsize=14)
    plt.xlabel("Arrival Rate (Cars per Tick)", fontsize=12)
    plt.ylabel("Avg Wait Time per Car (Ticks)", fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.savefig("efficiency_comparison.png")
    print("Graph saved as 'efficiency_comparison.png'.")
    plt.show()

    # 4. Generating Throughput Graph
    print("\nGenerating throughput comparison graph...")
    plt.figure(figsize=(10, 6))

    plt.plot(rates, adaptive_throughput, label="Adaptive Scheduler", marker='s', linewidth=2.5)

    plt.title("System Throughput under Varying Load", fontsize=14)
    plt.xlabel("Arrival Rate (Cars per Tick)", fontsize=12)
    plt.ylabel("Cars Cleared per Tick", fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.savefig("throughput_comparison.png")
    print("Graph saved as 'throughput_comparison.png'.")
    plt.show()


if __name__ == "__main__":
    # We must ensure this script is run from the project root
    if not os.path.exists("main.py"):
        print("ERROR: Please run this script from the project root folder:")
        print("python3 utils/visualizer.py")
    else:
        run_comparison_plot()
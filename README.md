# 🚦 Adaptive Traffic Signal Optimization Engine

### A discrete-event simulation system that optimizes traffic flow at a four-way intersection using hybrid scheduling strategies inspired by operating systems.

## 🧠 Overview

This project models traffic flow as a scheduling problem, where each lane competes for access to a shared resource (the intersection).

The system dynamically switches between:

#### Fair scheduling (Round Robin) under low traffic
#### Adaptive scheduling (queue + aging heuristic) under higher load
#### Priority preemption for emergency vehicles

The goal is to minimize:

#### Average wait time
#### Starvation
#### Unnecessary context switching (signal changes)
##⚙️ Key Features
#### 1. Hybrid Scheduling Engine
Uses load-aware decision making
Switches between fairness and optimization regimes
Prevents instability at low traffic densities
#### 2. Adaptive Lane Selection

Each lane is scored using:

##### score = queue_length + (aging_coefficient × waiting_time)

This ensures:

Congested lanes are prioritized
Starved lanes eventually get served
#### 3. Emergency Vehicle Preemption 🚨
Instant override when an emergency vehicle is detected
Zero-latency switching regardless of current state
#### 4. Context Switching Cost Modeling
Yellow light treated as switching overhead
Scheduler avoids unnecessary switches unless beneficial
#### 5. Performance Benchmarking

### Compared against:

#### Traditional Round Robin (baseline)

### Metrics tracked:

#### Average wait time
#### Throughput
#### Maximum wait time
### 📊 Results

The adaptive scheduler shows:

#### Lower wait times at medium and high traffic densities
#### Comparable performance to Round Robin at very low traffic (via fallback)
#### Improved system stability and reduced starvation
### 🖥️ Visualization

The system includes a performance comparison tool using Matplotlib:

python metrics/visualizer.py

This generates:

#### Wait time vs arrival rate graph
#### Adaptive vs Round Robin comparison
### 🧱 Project Structure
.
├── core/
│   ├── engine.py        # Lane model and traffic generation
│   ├── schedulers.py   # Adaptive scheduling logic
│
├── metrics/
│   └── visualizer.py   # Graph generation
│
├── main.py             # Simulation driver
├── config.json         # Tunable parameters

### 🚀 How to Run
1. Run simulation
python main.py
2. Generate performance graph
python metrics/visualizer.py

### 🔧 Configuration

You can tune parameters in config.json:

{
  "simulation": {
    "total_ticks": 200,
    "yellow_penalty": 5,
    "min_green_time": 10
  },
  "scheduler": {
    "aging_coefficient": 1.5,
    "busy_rate_threshold": 0.4,
    "time_quantum": 12
  }
}

### 🧩 Design Insights
#### Low traffic → fairness dominates optimization
#### High traffic → queue-aware scheduling reduces congestion
#### Switching cost must be balanced with responsiveness
#### Naive optimization fails under stochastic input
### 🎯 Future Improvements
#### Multi-intersection coordination
#### Reinforcement learning-based signal control
#### Real-time traffic input integration
#### Lane-specific arrival distributions
### 📌 Tech Stack
##### Python
##### Discrete Event Simulation
##### Matplotlib
### 💡 Key Takeaway
This project demonstrates how classical CPU scheduling concepts can be applied to real-world systems, with careful handling of stochastic inputs and system-level tradeoffs.

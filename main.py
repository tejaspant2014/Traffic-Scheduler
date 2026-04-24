import json
from core.engine import Lane
from core.schedulers import AdaptiveScheduler


def run_simulation(verbose=True, override_rate=None):
    # -----------------------------
    # 1. LOAD CONFIG
    # -----------------------------
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except:
        config = {
            "simulation": {
                "total_ticks": 200,
                "yellow_penalty": 5,
                "min_green_time": 10
            },
            "scheduler": {
                "aging_coefficient": 1.5,
                "busy_rate_threshold": 0.4,
                "time_quantum": 12
            },
            "traffic": {
                "low_arrival_rate": 0.1,
                "high_arrival_rate": 0.3,
                "rush_hour_start": 80
            }
        }

    sim_cfg = config["simulation"]
    sch_cfg = config["scheduler"]
    traf_cfg = config["traffic"]

    # -----------------------------
    # 2. INITIALIZATION
    # -----------------------------
    lanes = [Lane("North"), Lane("South"), Lane("East"), Lane("West")]

    scheduler = AdaptiveScheduler(
        aging_coefficient=sch_cfg["aging_coefficient"],
        busy_rate_threshold=sch_cfg["busy_rate_threshold"],
        time_quantum=sch_cfg["time_quantum"]
    )

    current_lane = lanes[0]
    yellow_timer = 0
    ticks_in_current = 0

    arrival_history = []
    total_cleared = 0

    # -----------------------------
    # 3. LOG HEADER
    # -----------------------------
    if verbose:
        print(f"\n{'Tick':<6} | {'Event':<35} | {'Active':<8} | {'Mode':<5}")
        print("-" * 70)

    # -----------------------------
    # 4. MAIN LOOP
    # -----------------------------
    for tick in range(sim_cfg["total_ticks"]):

        # ---- Traffic Rate ----
        if override_rate is not None:
            current_rate = override_rate
        else:
            current_rate = (
                traf_cfg["low_arrival_rate"]
                if tick < traf_cfg["rush_hour_start"]
                else traf_cfg["high_arrival_rate"]
            )

        # ---- Add Cars ----
        tick_arrivals = 0
        for lane in lanes:
            if lane.add_cars(current_rate):
                tick_arrivals += 1

        # ---- Moving Average Load ----
        arrival_history.append(tick_arrivals)
        if len(arrival_history) > 15:
            arrival_history.pop(0)

        avg_rate = sum(arrival_history) / len(arrival_history)

        # ---- Emergency Event ----
        if tick == 120:
            lanes[3].has_ambulance = True
            if verbose:
                print(f"{tick:<6} | 🚨 Ambulance detected in West")

        ticks_in_current += 1

        # ---- Scheduler Decision ----
        if yellow_timer == 0:
            ambulance_present = any(l.has_ambulance for l in lanes)

    # RR mode → no min green restriction
            if scheduler.mode == "RR":
                next_lane = scheduler.select_lane(
                lanes,
                current_lane,
                sim_cfg['yellow_penalty'],
                ticks_in_current,
                avg_rate
                )
            else:
        # SRTF mode → enforce stability
                if ticks_in_current >= sim_cfg['min_green_time'] or ambulance_present:
                    next_lane = scheduler.select_lane(
                        lanes,
                        current_lane,
                        sim_cfg['yellow_penalty'],
                        ticks_in_current,
                        avg_rate
                    )
                else:
                    next_lane = current_lane
        else:
            next_lane = current_lane

        # ---- Handle Switching ----
        status = ""

        if next_lane != current_lane:
            if current_lane is not None:
                yellow_timer = sim_cfg["yellow_penalty"]
                status = f"🟡 Switch {current_lane.name} → {next_lane.name}"
            current_lane = next_lane
            ticks_in_current = 0

        # ---- Processing ----
        if yellow_timer > 0:
            yellow_timer -= 1
            if not status:
                status = "🟡 Yellow phase"
        else:
            if current_lane and current_lane.clear_car():
                total_cleared += 1
                status = f"🟢 {current_lane.name} clearing"
            else:
                status = f"⚪ {current_lane.name if current_lane else 'None'} idle"

        # ---- Logging ----
        if verbose and (tick % 5 == 0 or "Switch" in status or "🚨" in status):
            mode = "RR" if avg_rate >= sch_cfg["busy_rate_threshold"] else "SRTF"
            active = current_lane.name if current_lane else "None"
            print(f"{tick:<6} | {status:<35} | {active:<8} | {mode:<5}")

        # ---- Update Aging ----
        for lane in lanes:
            lane.update_age(is_active=(lane == current_lane and yellow_timer == 0))

    # -----------------------------
    # 5. METRICS
    # -----------------------------
    total_wait = sum(l.wait_time for l in lanes)
    avg_wait = total_wait / (total_cleared if total_cleared > 0 else 1)
    throughput = total_cleared / sim_cfg["total_ticks"]
    max_wait = max(l.wait_time for l in lanes)

    if verbose:
        print("\n" + "=" * 50)
        print(f"Avg Wait Time : {avg_wait:.2f}")
        print(f"Throughput    : {throughput:.2f} cars/tick")
        print(f"Max Wait Time : {max_wait}")
        print("=" * 50)

    return avg_wait, throughput, max_wait
def run_round_robin(arrival_rate, ticks=200):
    """Simple, fixed rotation. No adaptive logic."""

    lanes = [Lane("North"), Lane("South"), Lane("East"), Lane("West")]

    quantum = 12
    yellow = 5

    current_lane = lanes[0]
    ticks_in_current = 0
    yellow_timer = 0

    total_cleared = 0

    for tick in range(ticks):

        # Traffic Generation
        for lane in lanes:
            lane.add_cars(arrival_rate)

        ticks_in_current += 1

        # Switching Logic (Fixed Rotation)
        if yellow_timer == 0:
            if ticks_in_current >= quantum or current_lane.queue == 0:
                curr_idx = lanes.index(current_lane)
                current_lane = lanes[(curr_idx + 1) % len(lanes)]
                ticks_in_current = 0
                yellow_timer = yellow

        # Processing
        if yellow_timer > 0:
            yellow_timer -= 1
        else:
            if current_lane.clear_car():
                total_cleared += 1

        # Aging Update
        for lane in lanes:
            lane.update_age(is_active=(lane == current_lane and yellow_timer == 0))

    # Metrics
    total_wait = sum(l.wait_time for l in lanes)
    avg_wait = total_wait / (total_cleared if total_cleared > 0 else 1)

    return avg_wait

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    run_simulation(verbose=True)
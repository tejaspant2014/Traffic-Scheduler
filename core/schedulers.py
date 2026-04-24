class AdaptiveScheduler:
    def __init__(self, aging_coefficient=2.5, busy_rate_threshold=0.4, time_quantum=10, mode="SRTF"):
        self.aging_coefficient = aging_coefficient
        self.busy_rate_threshold = busy_rate_threshold
        self.time_quantum = time_quantum
        self.mode = mode

    def select_lane(self, lanes, current_lane, yellow_penalty, ticks_in_current, current_rate):

        # 1. THE PRIORITY PRE-EMPTION
        emergency_lanes = [lane for lane in lanes if lane.has_ambulance]
        if emergency_lanes:
            return max(emergency_lanes, key=lambda l: l.queue)
        if current_rate < 0.08:
            curr_idx = lanes.index(current_lane)
            return lanes[(curr_idx + 1) % len(lanes)]
        # 2. MODE UPDATE WITH HYSTERESIS
        if self.mode == "SRTF" and current_rate > self.busy_rate_threshold + 0.02:
            self.mode = "RR"
        elif self.mode == "RR" and current_rate < self.busy_rate_threshold - 0.02:
            self.mode = "SRTF"

        # 3. ROUND ROBIN MODE
        if self.mode == "RR":

            if current_lane is None:
                return lanes[0]

            if ticks_in_current >= self.time_quantum or current_lane.queue == 0:
                curr_idx = lanes.index(current_lane)

                # skip empty lanes
                for i in range(1, len(lanes) + 1):
                    next_lane = lanes[(curr_idx + i) % len(lanes)]
                    if next_lane.queue > 0:
                        return next_lane

                return current_lane

            return current_lane

        # 4. SRTF MODE
        else:

            def remaining_time(lane):
                base = lane.queue
                return max(0, base - (self.aging_coefficient * lane.age))

            best_lane = min(lanes, key=remaining_time)

            if current_lane is None:
                return best_lane
            
            current_remaining = remaining_time(current_lane)
            best_remaining = remaining_time(best_lane)

            gain = current_remaining - best_remaining

            if best_lane != current_lane:
                return best_lane
            else:
                return current_lane
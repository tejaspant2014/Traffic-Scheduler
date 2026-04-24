import random

class Lane:
    def __init__(self, name):
        self.name = name
        self.queue = 0          # Number of cars waiting
        self.wait_time = 0      # Total wait time for metrics
        self.age = 0            # Ticks since last green light
        self.has_ambulance = False
        self.cars_cleared = 0
        self.history = []       # For graphing later

    def add_cars(self, rate):
        if random.random() < rate:
            self.queue += 1
            return True
        return False
    
    def spawn_ambulance(self):
        self.has_ambulance = True
        self.queue += 1

    def clear_car(self):
        if self.queue > 0:
            if self.has_ambulance:
                # The "Interrupt" logic: Priority vehicle clears first
                self.has_ambulance = False
                self.cars_cleared += 1
                self.queue -= 1
                print(f"🚑 EMERGENCY: Ambulance has cleared the intersection at {self.name}")
                return True
            else:
                # Normal flow logic
                self.queue -= 1
                self.cars_cleared += 1
                return True
        
        # If queue was 0, nothing happens
        return False

    def update_age(self, is_active):
        if not is_active and self.queue > 0:
            self.age += 1
            self.wait_time += self.queue
        else:
            self.age = 0
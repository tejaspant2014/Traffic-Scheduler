import random

class Lane:
    def __init__(self, name):
        self.name = name
        self.queue = 0          # Number of cars waiting
        self.wait_time = 0      # Total wait time for metrics
        self.age = 0            # Ticks since last green light
        self.history = []       # For graphing later

    def add_cars(self, rate):
        """Simulate Poisson arrival of cars."""
        if random.random() < rate:
            self.queue += 1

    def clear_car(self):
        """One car leaves the intersection."""
        if self.queue > 0:
            self.queue -= 1
            return True
        return False

    def update_age(self, is_active):
        if not is_active and self.queue > 0:
            self.age += 1
        else:
            self.age = 0
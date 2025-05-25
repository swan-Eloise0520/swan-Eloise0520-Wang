class FuelGame:
    def __init__(self):
        self.tanks = [9, 0, 0]  # Initialize tanks [Main(9L), Backup(5L), Emergency(4L)]
        self.target = 7          # Target fuel amount to achieve
        self.time_limit = 180    # Total time limit in seconds (3 minutes)
        self.time_used = 0       # Time consumed
        self.steps = []          # Operation history
        self.achievements = set() # Unlocked achievements
        self.optimal_solution = [ # Predefined optimal solution
            "Main→Backup (5L)", "Backup→Emergency (4L)", 
            "Emergency→Main (4L)", "Backup→Emergency (1L)",
            "Main→Backup (5L)", "Backup→Emergency (3L)"
        ]

    def transfer(self, from_idx, to_idx):       #Execute fuel transfer
        if from_idx == to_idx:      # Validate operation
            return False, "Cannot transfer to same tank"
        if self.tanks[from_idx] == 0:
            return False, "Source tank is empty"
        
        # Calculate available capacity
        capacities = [9, 5, 4]  # Tank capacities
        available = capacities[to_idx] - self.tanks[to_idx]
        transfer_amount = min(self.tanks[from_idx], available)
        
        if transfer_amount <= 0:
            return False, "Target tank is full"
        
        # Execute transfer
        self.tanks[from_idx] -= transfer_amount
        self.tanks[to_idx] += transfer_amount
        self.time_used += 5  # Each operation costs 5 seconds
        
        # Record step
        tank_names = ["Main", "Backup", "Emergency"]
        self.steps.append(f"{tank_names[from_idx]}→{tank_names[to_idx]} ({transfer_amount}L)")
        return True, f"Transferred {transfer_amount}L"

    def check_win(self):        #Check win condition
        return self.target in self.tanks

    def check_achievements(self):       #Check achievements
        if len(self.steps) <= len(self.optimal_solution):
            self.achievements.add("Perfect Calculation")
        if self.get_time_left() <= 30:
            self.achievements.add("Last Second Escape")

    def get_time_left(self):       #Calculate remaining time
        return max(0, self.time_limit - self.time_used)

    def is_game_over(self):         #Check game over condition
        return self.get_time_left() <= 0
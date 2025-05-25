from game import FuelGame


class GameUI:
    def __init__(self):
        self.game = FuelGame()
        self.selected_tank = None

    def print_game_state(self):  # Print current game state
        print("\n" + "=" * 40)
        print(f"[Main]: {self.game.tanks[0]}L  [Backup]: {self.game.tanks[1]}L  [Emergency]: {self.game.tanks[2]}L")

        # Print formatted time
        mins, secs = divmod(self.game.get_time_left(), 60)
        print(f"\nTime Left: {mins:02d}:{secs:02d}")

    def show_message(self, msg, is_error=False):  # Display operation feedback
        color_code = 91 if is_error else 92  # Red/Green
        print(f"\033[{color_code}m{msg}\033[0m")

    def show_help(self):  # Show help information
        print("\n\033[96mHELP:")
        print("1→2 : Transfer from Main(1) to Backup(2)")
        print("Tank IDs: 1-Main(9L) 2-Backup(5L) 3-Emergency(4L)")
        print("Each move costs 5 seconds\033[0m")

    def show_replay(self):  # Show operation replay
        print("\n\033[95m=== OPERATION HISTORY ===")
        for i, step in enumerate(self.game.steps, 1):
            print(f"Step {i}: {step}")

        # Check achievements
        self.game.check_achievements()
        if self.game.achievements:
            print(f"\nAchievements: {','.join(self.game.achievements)}")

        # Compare with optimal solution
        diff = len(self.game.steps) - len(self.game.optimal_solution)
        if diff <= 0:
            print("\033[93m★ PERFECT SOLUTION! ★\033[0m")
        else:
            print(f"\033[91mCan optimize by {diff} steps, try again!\033[0m")

    def run(self):  # Main game loop
        print("\033[94m=== Fuel Transfer Game ===\033[0m")
        print("Goal: Get \033[93m7L\033[0m in any tank")
        print("Format: source→target (e.g. 1→2)")

        while True:
            self.print_game_state()

            # Win check
            if self.game.check_win():
                print("\033[95m\n★ ESCAPE SUCCESS! ★\033[0m")
                self.show_replay()
                break

            # Timeout check
            if self.game.is_game_over():
                print("\033[91m\n✖ TIME'S UP! ✖\033[0m")
                print("Press 'r' to retry, any other key to exit")
                if input().lower() == 'r':
                    self.__init__()
                    continue
                break

            # Input handling with error recovery
            while True:  # Inner loop for input validation
                try:
                    cmd = input("Enter move (e.g. 1→2) or 'h' for help: ").strip()

                    if cmd.lower() == 'h':
                        self.show_help()
                        continue  # Show help and re-prompt

                    # Validate input format
                    if '→' not in cmd:
                        raise ValueError("Use '→' to separate tank numbers (e.g. 1→2)")

                    parts = cmd.split('→')
                    if len(parts) != 2:
                        raise ValueError("Need exactly one '→' in input")

                    from_idx, to_idx = map(int, parts)
                    if not (1 <= from_idx <= 3) or not (1 <= to_idx <= 3):
                        raise ValueError("Tank numbers must be 1, 2, or 3")

                    # Execute transfer
                    success, msg = self.game.transfer(from_idx - 1, to_idx - 1)
                    self.show_message(msg, not success)
                    break  # Exit input loop after successful transfer

                except ValueError as e:
                    self.show_message(f"Invalid input! {e}", True)
                except KeyboardInterrupt:
                    print("\nGame exited")
                    return  # Exit entire game
                except Exception as e:
                    self.show_message(f"Unexpected error: {e}", True)
                    break  # Prevent infinite loop on unexpected errors
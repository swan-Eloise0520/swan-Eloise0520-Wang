from ui import GameUI

if __name__ == "__main__":
    print("Initializing Spaceship Fuel Management Game...")
    print("Goal: Achieve exactly 7 liters in any fuel tank through transfers")
    try:
        game = GameUI()     # Create game
        game.run()          # Start the game loop
    except KeyboardInterrupt:
        print("\nGame exited")
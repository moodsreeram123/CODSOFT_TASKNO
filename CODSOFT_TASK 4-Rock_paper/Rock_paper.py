"""Play Rock, Paper, Scissors against the computer."""

import random


CHOICES = ("rock", "paper", "scissors")
BEATS = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}


def get_user_choice() -> str:
    """Prompt until the user enters a valid choice."""
    while True:
        choice = input("Choose rock, paper, or scissors (or q to quit): ").strip().lower()
        if choice in CHOICES:
            return choice
        if choice in ("q", "quit"):
            return "quit"
        print("Please enter rock, paper, or scissors.")


def play_round(user_choice: str, computer_choice: str) -> str:
    """Return 'win', 'loss', or 'tie' for a round."""
    if user_choice == computer_choice:
        return "tie"
    if BEATS[user_choice] == computer_choice:
        return "win"
    return "loss"


def ask_to_play_again() -> bool:
    """Ask whether to start another round."""
    while True:
        answer = input("Play another round? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


def main() -> None:
    user_score = 0
    computer_score = 0
    ties = 0

    print("=" * 38)
    print("       ROCK  PAPER  SCISSORS")
    print("=" * 38)
    print("Rock beats scissors. Scissors beat paper.")
    print("Paper beats rock. Type q any time at the choice prompt to quit.\n")

    while True:
        user_choice = get_user_choice()
        if user_choice == "quit":
            break

        computer_choice = random.choice(CHOICES)
        outcome = play_round(user_choice, computer_choice)

        print(f"\nYou chose:      {user_choice.title()}")
        print(f"Computer chose: {computer_choice.title()}")
        if outcome == "win":
            user_score += 1
            print("You win this round!")
        elif outcome == "loss":
            computer_score += 1
            print("The computer wins this round.")
        else:
            ties += 1
            print("It's a tie!")

        print(f"Score — You: {user_score}  Computer: {computer_score}  Ties: {ties}\n")
        if not ask_to_play_again():
            break
        print()

    print("\nThanks for playing!")
    print(f"Final score — You: {user_score}  Computer: {computer_score}  Ties: {ties}")


if __name__ == "__main__":
    main()

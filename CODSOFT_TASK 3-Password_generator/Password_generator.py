"""Generate a strong random password from a requested length."""

import secrets
import string


CHARACTER_GROUPS = (
    string.ascii_lowercase,
    string.ascii_uppercase,
    string.digits,
    string.punctuation,
)
ALL_CHARACTERS = "".join(CHARACTER_GROUPS)


def generate_password(length: int) -> str:
    """Return a password containing each character type at least once."""
    if length < len(CHARACTER_GROUPS):
        raise ValueError(f"Password length must be at least {len(CHARACTER_GROUPS)}.")

    # Seed the password with one character from every group, then shuffle.
    password_characters = [secrets.choice(group) for group in CHARACTER_GROUPS]
    password_characters.extend(
        secrets.choice(ALL_CHARACTERS)
        for _ in range(length - len(password_characters))
    )
    secrets.SystemRandom().shuffle(password_characters)
    return "".join(password_characters)


def main() -> None:
    try:
        length = int(input("Enter the desired password length (at least 4): "))
        password = generate_password(length)
    except ValueError as error:
        print(f"Invalid input: {error}")
        return

    print(f"Generated password: {password}")


if __name__ == "__main__":
    main()
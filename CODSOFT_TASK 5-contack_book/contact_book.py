"""A simple contact manager that saves contacts in a local JSON file."""

import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("contacts.json")
FIELDS = ("name", "phone", "email", "address")


def load_contacts() -> list[dict[str, str]]:
    """Load contacts from disk, returning an empty list if none exist yet."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            contacts = json.load(file)
        if not isinstance(contacts, list):
            raise ValueError("The contacts file must contain a list.")
        return contacts
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Could not read {DATA_FILE.name}: {error}")
        return []


def save_contacts(contacts: list[dict[str, str]]) -> bool:
    """Save contacts and report whether the write succeeded."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=2, ensure_ascii=False)
        return True
    except OSError as error:
        print(f"Could not save contacts: {error}")
        return False


def prompt_contact(existing: dict[str, str] | None = None) -> dict[str, str] | None:
    """Ask for contact details. Blank fields retain existing values on edit."""
    existing = existing or {field: "" for field in FIELDS}
    contact = {}
    for field in FIELDS:
        label = field.title()
        if field == "name":
            label += " (required)"
        current = existing.get(field, "")
        prompt = f"{label}"
        if current:
            prompt += f" [{current}]"
        prompt += ": "
        value = input(prompt).strip()
        contact[field] = value if value else current

    if not contact["name"]:
        print("A contact must have a name.")
        return None
    return contact


def add_contact(contacts: list[dict[str, str]]) -> None:
    print("\nAdd a contact (name is required; other details are optional).")
    contact = prompt_contact()
    if contact is not None:
        contacts.append(contact)
        if save_contacts(contacts):
            print(f"Added {contact['name']}.")


def view_contacts(contacts: list[dict[str, str]]) -> None:
    print("\nCONTACTS")
    print("-" * 52)
    if not contacts:
        print("No contacts saved yet.")
        return
    for index, contact in enumerate(contacts, start=1):
        print(f"{index}. {contact.get('name', 'Unnamed')}  |  {contact.get('phone') or 'No phone'}")
    print("-" * 52)


def matching_contacts(contacts: list[dict[str, str]], query: str) -> list[tuple[int, dict[str, str]]]:
    query = query.casefold()
    return [
        (index, contact)
        for index, contact in enumerate(contacts)
        if query in contact.get("name", "").casefold()
        or query in contact.get("phone", "").casefold()
    ]


def show_matches(matches: list[tuple[int, dict[str, str]]]) -> None:
    for index, contact in matches:
        print(f"\n{index + 1}. {contact.get('name', 'Unnamed')}")
        print(f"   Phone:   {contact.get('phone') or '—'}")
        print(f"   Email:   {contact.get('email') or '—'}")
        print(f"   Address: {contact.get('address') or '—'}")


def search_contacts(contacts: list[dict[str, str]]) -> None:
    query = input("\nSearch by name or phone number: ").strip()
    if not query:
        print("Enter a name or phone number to search.")
        return
    matches = matching_contacts(contacts, query)
    if matches:
        print(f"Found {len(matches)} contact(s):")
        show_matches(matches)
    else:
        print("No matching contacts found.")


def choose_contact(contacts: list[dict[str, str]], action: str) -> int | None:
    if not contacts:
        print("There are no contacts to " + action + ".")
        return None
    view_contacts(contacts)
    entry = input(f"Enter the contact number to {action} (or press Enter to cancel): ").strip()
    if not entry:
        print("Cancelled.")
        return None
    try:
        index = int(entry) - 1
    except ValueError:
        print("Please enter a number from the list.")
        return None
    if not 0 <= index < len(contacts):
        print("That contact number is not in the list.")
        return None
    return index


def update_contact(contacts: list[dict[str, str]]) -> None:
    index = choose_contact(contacts, "update")
    if index is None:
        return
    print("\nEnter new details. Press Enter to keep each current value.")
    updated = prompt_contact(contacts[index])
    if updated is not None:
        previous = contacts[index]
        contacts[index] = updated
        if save_contacts(contacts):
            print(f"Updated {updated['name']}.")
        else:
            contacts[index] = previous


def delete_contact(contacts: list[dict[str, str]]) -> None:
    index = choose_contact(contacts, "delete")
    if index is None:
        return
    contact = contacts[index]
    confirmation = input(f"Delete {contact.get('name', 'this contact')}? (y/n): ").strip().lower()
    if confirmation not in ("y", "yes"):
        print("Deletion cancelled.")
        return
    removed = contacts.pop(index)
    if save_contacts(contacts):
        print(f"Deleted {removed.get('name', 'contact')}.")
    else:
        contacts.insert(index, removed)


def main() -> None:
    contacts = load_contacts()
    actions = {
        "1": add_contact,
        "2": view_contacts,
        "3": search_contacts,
        "4": update_contact,
        "5": delete_contact,
    }
    while True:
        print("\n" + "=" * 34)
        print("          CONTACT MANAGER")
        print("=" * 34)
        print("1. Add contact")
        print("2. View contact list")
        print("3. Search by name or phone")
        print("4. Update contact")
        print("5. Delete contact")
        print("6. Exit")
        choice = input("\nChoose an option (1-6): ").strip()

        if choice in actions:
            if choice == "2":
                actions[choice](contacts)
            else:
                actions[choice](contacts)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()

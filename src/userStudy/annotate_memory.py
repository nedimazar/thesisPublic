import json
import csv
from pathlib import Path

USER = "J"
USER_DIR = Path(__file__).parent.parent / "agent" / "memory" / USER
ANNOTATIONS_FILE = Path(__file__).parent / "more_annotations.csv"


def concatenate_messages(user_dir):
    messages = []

    # First, process the backup files
    backup_files = sorted([f for f in user_dir.iterdir() if f.name.endswith(".bak")])

    for backup_file in backup_files:
        with backup_file.open("r") as f:
            messages.extend(json.load(f))

    # Now process the current messages file
    current_messages_file = user_dir / "messages.json"
    with current_messages_file.open("r") as f:
        messages.extend(json.load(f))

    return messages


def validate_messages(messages):
    valid_roles = ["user", "assistant"]
    last_role = None

    for message in messages:
        if "role" not in message:
            print(f"Invalid message: {message}. 'role' not found.")
            return False
        if message["role"] not in valid_roles:
            print(
                f"Invalid role: {message['role']}. Role can only be 'user' or 'assistant'."
            )
            return False
        if message["role"] == last_role:
            print(f"Invalid sequence: found consecutive '{last_role}' roles.")
            return False

        last_role = message["role"]

    return True


def write_to_csv(metrics):
    fieldnames = ["name"] + list(metrics.keys())
    file_exists = ANNOTATIONS_FILE.exists()

    with ANNOTATIONS_FILE.open("a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()  # If file does not exist, write header
        writer.writerow({"name": USER, **metrics})


def display_message_pairs(messages):
    metrics = {
        "understood": 0,
        "misunderstood": 0,
        "correct_nl_generation": 0,
        "incorrect_nl_generation": 0,
        "elicitation": 0,
        "failed_elicitation": 0,
        "explanation": 0,
        "bad_explanation": 0,
    }

    for i in range(0, len(messages), 2):
        print(f"Message {i+1} of {len(messages)}")

        print(f"\nUser: {messages[i]['content']}")
        if i + 1 < len(messages):
            print(f"Assistant: {messages[i+1]['content']}")
        else:
            print("Assistant: No reply found for the last user message.")

        user_input = input(
            "\nEnter letters corresponding to metrics | \n(m)isunderstood\n(c)orrect NL\n(i)ncorrect NL\n(e)licitation\n(f)ailed elicitation\n(x)planation\n(b)ad explanation: "
        )

        if "m" not in user_input:
            metrics["understood"] += 1

        for letter in user_input:
            if letter == "m":
                metrics["misunderstood"] += 1
            elif letter == "c":
                metrics["correct_nl_generation"] += 1
            elif letter == "i":
                metrics["incorrect_nl_generation"] += 1
            elif letter == "e":
                metrics["elicitation"] += 1
            elif letter == "x":
                metrics["explanation"] += 1
            elif letter == "b":
                metrics["bad_explanation"] += 1
            elif letter == "f":
                metrics["failed_elicitation"] += 1

    write_to_csv(metrics)  # Write metrics to .csv file
    print("\nFinal Metrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")


def main():
    messages = concatenate_messages(USER_DIR)

    if validate_messages(messages):
        print("All messages are valid. Displaying message pairs...")
        display_message_pairs(messages)
    else:
        print("Found invalid messages.")


if __name__ == "__main__":
    main()

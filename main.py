import os
import subprocess
import sys

def clear_terminal():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True, check=True)

def main_cli():
    while True:
        try:
            clear_terminal()

            print("╔═══════════════════════════════════╗")
            print("║           HABIT TRACKER           ║")
            print("╚═══════════════════════════════════╝\n")

            print("1 - Add New Habit")
            print("2 - Remove Habit")
            print("3 - Show Status")
            print("4 - APP INFO")
            print("")
            input("Choose from menu: ")

        except KeyboardInterrupt:
            clear_terminal()
            print("\nCtrl + C pressed. Exiting program...")
            sys.exit(0)

main_cli()
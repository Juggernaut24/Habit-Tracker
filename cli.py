import os
import subprocess
import sys
from time import sleep
from database import Database

db = Database()

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

            value = input("Choose from menu: ")
            print("")

            match value:
                case "1":
                    clear_terminal()
                    print("--- Adding New Habit ---\n")
                    # (name, description, category, frequency, time_of_day)
                    while True:
                        name = input("Habit name*: ").strip()
                        if name:
                            break
                        print("[-] Habit name cannot be empty ")

                    desc = input("Description: ").strip()
                    cat = input("Category: ").strip()
                    freq = input("Frequency(daily, weekly): ").strip()
                    timeofday = input("Time of Day(morning, afternoon, evening): ").strip()

                    if db.add_habit(name, desc, cat, freq, timeofday):
                        print(f"[+] Habit '{name}' added successfully!")
                    else:
                        print(f"[-] Habit '{name}' already exists.")

                case "2":
                    print("--- Removing Habit ---\n")
                case "3":
                    print("--- Showing Status ---\n")
                case "4":
                    print("--- APP INFO ---\n")
                case _:
                    print("ERROR: PLEASE CHOOSE FROM LIST!")
                    sleep(3)
                    continue

            sleep(3)

        except KeyboardInterrupt:
            clear_terminal()
            print("\nCtrl + C pressed. Exiting program...")
            sys.exit(0)

main_cli()
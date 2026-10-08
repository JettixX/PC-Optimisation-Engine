from pathlib import Path

from PCOptimisationEngine.src.ingestion.opendbloader import (
    load_inventory,
    sync_opendb_repo,
)

from PCOptimisationEngine.src.compatibility.rules import * # Import all compatibility functions


DB_LOCAL_DIR = Path("buildcores_data")


def main() -> None:
    sync_opendb_repo(DB_LOCAL_DIR)

    print("\nLoading component data...")

    inventory = load_inventory(DB_LOCAL_DIR)

    print("\nInventory summary:")
    print("-" * 40)

    for category, items in inventory.items():
        print(f"{category:15} {len(items):>6}")

    count = 0
    count1= 0
    for mobo in inventory["Motherboards"]:
        for cpu in inventory["CPUs"]:
            if (cpu.socket != mobo.socket):
                count+= 1
            count1+= 1
    print(f"There are {count} incompatible motherboard-CPU combinations in the dataset and the fraction of possible pairs is {count/count1}")

if __name__ == "__main__":
    main()
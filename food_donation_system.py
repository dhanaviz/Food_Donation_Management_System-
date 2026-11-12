import json
import os

DONATION_FILE = "donations.json"
USER_FILE = "users.json"


def load_data(filename):
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


donations = load_data(DONATION_FILE)
users = load_data(USER_FILE)


def create_donation():
    print("\n--- CREATE DONATION ---")

    food = input("Food Name: ").strip()
    quantity = input("Quantity: ").strip()
    location = input("Location: ").strip()
    available = input("Available Until: ").strip()
    contact = input("Contact Number: ").strip()

    if not all([food, quantity, location, available, contact]):
        print("Error: All fields are required!")
        return

    number = len(donations) + 1
    donation_id = f"DON{number:03d}"

    donation = {
        "id": donation_id,
        "food": food,
        "quantity": quantity,
        "location": location,
        "available_until": available,
        "contact": contact,
        "status": "Available",
        "volunteer": ""
    }

    donations.append(donation)
    save_data(DONATION_FILE, donations)

    print("\nDonation Created Successfully!")
    print("Donation ID:", donation_id)
    print("Status: Available")


def view_donations():
    print("\n--- AVAILABLE DONATIONS ---")

    found = False

    for d in donations:
        if d["status"] == "Available":
            found = True
            print("\nDonation ID:", d["id"])
            print("Food:", d["food"])
            print("Quantity:", d["quantity"])
            print("Location:", d["location"])
            print("Available Until:", d["available_until"])
            print("Status:", d["status"])

    if not found:
        print("No available donations found.")


def claim_donation():
    print("\n--- CLAIM DONATION ---")

    donation_id = input("Enter Donation ID: ").strip()
    volunteer_id = input("Enter Volunteer ID: ").strip()

    if not donation_id or not volunteer_id:
        print("Error: Fields cannot be empty!")
        return

    for d in donations:
        if d["id"] == donation_id:

            if d["status"] != "Available":
                print("Error: Donation is not available!")
                return

            d["status"] = "Claimed"
            d["volunteer"] = volunteer_id

            if not any(u["id"] == volunteer_id for u in users):
                users.append({
                    "id": volunteer_id,
                    "role": "Volunteer"
                })

            save_data(DONATION_FILE, donations)
            save_data(USER_FILE, users)

            print("\nDonation Claimed Successfully!")
            print("Donation ID:", donation_id)
            print("Status: Claimed")
            print("Volunteer:", volunteer_id)
            return

    print("Error: Donation ID not found!")


def update_status():
    print("\n--- UPDATE STATUS ---")

    donation_id = input("Enter Donation ID: ").strip()

    for d in donations:
        if d["id"] == donation_id:

            if d["status"] == "Claimed":
                d["status"] = "Picked Up"

            elif d["status"] == "Picked Up":
                d["status"] = "Delivered"

            else:
                print("Invalid status operation!")
                return

            save_data(DONATION_FILE, donations)

            print("Status Updated Successfully!")
            print("New Status:", d["status"])
            return

    print("Donation ID not found!")


def main():
    while True:
        print("\n===== FOOD DONATION MANAGEMENT SYSTEM =====")
        print("1. Create Donation")
        print("2. View Available Donations")
        print("3. Claim Donation")
        print("4. Update Donation Status")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            create_donation()

        elif choice == "2":
            view_donations()

        elif choice == "3":
            claim_donation()

        elif choice == "4":
            update_status()

        elif choice == "5":
            print("Thank you for using Food Donation System!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
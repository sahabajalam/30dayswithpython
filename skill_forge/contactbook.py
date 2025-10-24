import os

contactbook = {}

def add_contact(first_name, last_name, phone, email):
    full_name = f"{first_name} {last_name}"
    full_name_lower = full_name.lower()
    contactbook[full_name_lower] = {
        "full_name": full_name,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
        "address": ""
    }

def get_contact(name):
    return contactbook.get(name.lower(), "Contact not found")

def update_contact(name, phone=None, email=None, address=None):
    name_lower = name.lower()
    if name_lower in contactbook:
        if phone:
            contactbook[name_lower]["phone"] = phone
        if email:
            contactbook[name_lower]["email"] = email
        if address:
            contactbook[name_lower]["address"] = address
        return "Contact updated"
    else:
        return "Contact not found"

def delete_contact(name):
    name_lower = name.lower()
    if name_lower in contactbook:
        del contactbook[name_lower]
        return "Contact deleted"
    else:
        return "Contact not found"

def list_contacts(search=None):
    contacts = list(contactbook.values())
    if search:
        search_lower = search.lower()
        contacts = [info for info in contacts if search_lower in info['first_name'].lower() or search_lower in info['last_name'].lower() or search_lower in info['email'].lower() or search_lower in info['phone'].lower()]
    if contacts:
        return "\n".join([f"{info['full_name']}: Phone: {info['phone']}, Email: {info['email']}, Address: {info['address']}" for info in contacts])
    else:
        return "No contacts found"

def clear_contacts():
    contactbook.clear()
    return "All contacts cleared"

def save_contacts():
    contacts_file = os.path.join(os.path.dirname(__file__), "contacts.txt")
    with open(contacts_file, "w") as f:
        for info in contactbook.values():
            f.write(f"{info['full_name']},{info['phone']},{info['email']},{info['address']}\n")

def load_contacts():
    contacts_file = os.path.join(os.path.dirname(__file__), "contacts.txt")
    if os.path.exists(contacts_file):
        with open(contacts_file, "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 4:
                    full_name, phone, email, address = parts
                    names = full_name.split(' ', 1)
                    if len(names) == 2:
                        first_name, last_name = names
                        add_contact(first_name, last_name, phone, email)
                        if address:
                            update_contact(full_name, address=address)

# Interactive menu
def main():
    load_contacts()
    while True:
        print("\nContact Book Menu:")
        print("a - Add contact")
        print("b - Update contact")
        print("c - View contacts")
        print("d - Delete contact")
        print("x - Delete all contacts")
        print("q - Quit")
        
        choice = input("Enter your choice: ").strip().lower()
        
        if choice == 'a':
            first_name = input("Enter first name: ").strip()
            last_name = input("Enter last name: ").strip()
            phone = input("Enter phone number: ").strip()
            email = input("Enter email: ").strip()
            add_contact(first_name, last_name, phone, email)
            save_contacts()
            print("Contact added.")
        
        elif choice == 'b':
            name = input("Enter the full name of the contact to update: ").strip()
            phone = input("Enter new phone (leave blank to skip): ").strip() or None
            email = input("Enter new email (leave blank to skip): ").strip() or None
            address = input("Enter new address (leave blank to skip): ").strip() or None
            result = update_contact(name, phone, email, address)
            if result == "Contact updated":
                save_contacts()
            print(result)
        
        elif choice == 'c':
            search = input("Enter search term (leave blank to view all): ").strip()
            print(list_contacts(search))
        
        elif choice == 'd':
            name = input("Enter the full name of the contact to delete: ").strip()
            result = delete_contact(name)
            if result == "Contact deleted":
                save_contacts()
            print(result)
        
        elif choice == 'x':
            result = clear_contacts()
            save_contacts()
            print(result)
        
        elif choice == 'q':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
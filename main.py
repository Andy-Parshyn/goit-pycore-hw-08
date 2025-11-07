from address_book import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Value Error - {e}"
        
        except KeyError:
            return "There is no such Name. Please add it first "
        
        except IndexError:
            return "No contacts found!"

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_birthday(args, contacts: AddressBook):
    name,birthday = args
    contact = contacts.get(name,None)

    if not contact:
        raise IndexError
    contact.add_birthday(birthday)
    return 'Birthdate added.'


@input_error
def add_contact(args, contacts: AddressBook):
    name, phone = args
    contact = contacts.get(name,None)

    if not contact:
        contact = Record(name)
        contact.add_phone(phone)
        contacts.add_record(contact)
        return 'Contact added.'
    
    contact.add_phone(phone)
    return 'Contact Updated'


@input_error
def change_contact(args, contacts: AddressBook):
    if len(args) < 3:
        return f'Please provide Name, old phone, new phone to proceed.'
    
    name, old_phone, new_phone = args
    contact = contacts.get(name,None)
    
    if not contact:
        raise IndexError    
    
    contact.edit_phone(old_phone,new_phone)
    return 'Contact updated.'


@input_error
def show_birthday(args, contacts: AddressBook):
    if len(args) < 1:
        return 'PLease provide a Name first.'
    
    name = args[0]
    contact = contacts.get(name,None)

    if not contact:
        raise IndexError
    
    if not contact.birthday:
        return f'{name} doesn\'t have a birthday added'
    
    return f'{name}\'s birthday is on {contact.birthday.value}'


@input_error    
def show_phone(args: list, contacts: AddressBook):
    if len(args) < 1 :
        return 'Please provide a Name first.'
    
    name = args[0]
    contact = contacts.get(name,None)

    if not contact:
        raise IndexError
    
    if not contact.phones:
        return f'The Contact {name} has no phones'
    
    phones = ', '.join(phone.value for phone in contact.phones)
    return f'{name}: {phones}'


@input_error
def birthdays(args, contacts: AddressBook):
    upcomming_birthdays = contacts.get_upcoming_birthdays()

    if not upcomming_birthdays:
        return 'There are no birthdays next week.'
    
    return "\n".join(f"{contact['name']}: {contact['congratulation_date']}"for contact in upcomming_birthdays)


@input_error
def show_all(contacts: AddressBook):
    result = ''
    if not contacts.data:
        raise IndexError
    
    for name, phone in contacts.items():
        result += f'{name} -> {phone}\n'
        
    return result
        

def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args,contacts))

        elif command == "phone":
            print(show_phone(args,contacts))

        elif command == "all":
            print(show_all(contacts))

        elif command == "add_birthday":
            print(add_birthday(args,contacts))

        elif command == "show_birthday":
            print(show_birthday(args,contacts))

        elif command == "birthdays":
            print(birthdays(args,contacts))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()



from classes import Record, Birthday


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except (KeyError, ValueError, IndexError) as f:
            return str(f)
    return inner


@input_error
def normalise(number):
    new_phone = (
        number.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    return new_phone


@input_error
def handle_hello():
    return 'How can I help you?\n add - the bot saves in memory a new contact\n change - the bot saves a new phone number for an existing contact in memory\n phone - the bot outputs the phone number for the specified contact to the console.\n show all - By this command, the bot displays all saved contacts with phone numbers to the console.\n good bye, close, exit - on any of these commands, the bot completes its robot after'


@input_error
def handler_add(name, phone, address_book):
    phone = normalise(phone)

    if len(name) == 0 or name.isdigit() or len(phone) < 12 or phone.isalpha():
        raise ValueError(
            'Please enter the correct name and phone number, the name must be a period and the number must be numbers, preferably without symbols')
    record = address_book.get(name.lower())
    if not record:
        record = Record(name)
        address_book.add_record(record)
    record.add_phone(phone)

    return f"Added phone {phone} for contact {name}"


@input_error
def handler_change(name, old_phone, new_phone, address_book):
    old_phone = normalise(old_phone)
    new_phone = normalise(new_phone)
    record = address_book.get(name.lower())
    if not record:
        raise KeyError(f"{name} is not in contacts")
    if not record.edit_phone(old_phone, new_phone):
        raise ValueError(f"{old_phone} is not in {name}'s phones")
    return f"Changed phone {old_phone} to {new_phone} for contact {name}"


@input_error
def handler_phone(name, address_book):
    record = address_book.get(name)
    if not record:
        raise KeyError(f"{name} is not in contacts")
    return "\n".join([phone.value for phone in record.phones])


@input_error
def handle_show_all(address_book):
    return "\n".join([f"{name}: {', '.join([phone.value for phone in record.phones])}" for name, record in address_book.items()])


@input_error
def show_day_to_birthday(day, month):
    return Birthday(day, month).days_to_birthday()

@input_error
def delete_contact(name, address_book):
    if name in address_book.data:
        del address_book.data[name]
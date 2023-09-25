from classes import AddressBook, Birthday, filename
from error_decorator import handle_hello, handler_add, handler_change, handler_phone, delete_contact

def main():
    address_book = AddressBook()

    try:
        load = address_book.from_json(filename)

    except ValueError:
        pass

    while True:
        comands = input('Type hello to see a list of commands: ').lower()

        if comands == 'hello':
            print(handle_hello())

        elif comands == 'add':
            name_and_phone = input(
                'Please enter your name and phone number separated by a comma: ')
            try:
                name, phone = name_and_phone.rsplit(',', 1)
                message = handler_add(name, phone, address_book)
                save = address_book.save(filename)
                print(message)
            except ValueError as e:
                print(str(e))

        elif comands == 'search':
            search_str = input('Please enter a search string: ')
            find_str = address_book.search(search_str)
            for find in find_str:
                print(find[name], find[phone])

        elif comands == 'days birthday':
            dates = input(
                'Please enter a day and month separated by a comma: ')
            day, month = dates.split(',')
            dates = Birthday(int(day), int(month))
            print(dates.days_to_birthday())

        elif comands == 'next birthday':
            dates = input(
                'Please enter a day and month separated by a comma: ')
            day, month = dates.split(',')
            dates = Birthday(int(day), int(month))
            print(dates.next_birthday())

        elif comands == 'change':
            name_and_phone = input(
                'Please enter your name and phone number separated by a comma: ')
            try:
                name, old_phone, new_phone = name_and_phone.split(',', 2)
                message = handler_change(
                    name, old_phone, new_phone, address_book)
                print(message)
            except (KeyError, ValueError) as e:
                print(str(e))

        elif comands == 'phone':
            name = input('Please enter the name: ')
            try:
                message = handler_phone(name, address_book)
                print(message)
            except KeyError as e:
                print(str(e))

        elif comands == "show all":
            if len(address_book) >= 1:
                message = '\n'.join(list(address_book))
                print(message)
            elif len(address_book) == 0:
                message = 'Empty list'
                print(message)

        elif comands == 'delete':
            name = input('Please enter a name fro contact to delete:  ')
            delete_contact(name, address_book)
            save = address_book.save(filename)
            

        elif comands == 'good bye' or 'close' or 'exit':
            print('Good bye =)')
            break
        else:
            message = "Unknown command. Please try again."
            print(message)


if __name__ == '__main__':
    main()

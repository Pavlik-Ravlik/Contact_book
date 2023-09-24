from collections import UserDict
from datetime import date, datetime
import json

filename = 'contacts.json'

class Field():
    def __init__(self, value) -> None:
        self.__value = value

    def __str__(self) -> str:
        return f"{self.__value}"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    def __init__(self, name) -> None:
        self.value = name

    def __repr__(self) -> str:
        return f"Name(value={self.value})"

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, name: str):
        if not name.isalpha():
            raise ValueError
        super(Name, Name).value.fset(self, name)


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return f"Phone(value={self.value})"


class Birthday:
    def __init__(self, day=None, month=None):
        self.day = day
        self.month = month

    def set_value(self, value):
        try:
            datetime.strptime(value, '%y-%m-%d')
        except ValueError:
            raise ValueError('Should be YYYY-MM-DD')
        self.value = value

    def next_birthday(self):
        today = date.today()
        next_birthday = date(today.year, self.month, self.day)
        if next_birthday < today:
            next_birthday = date(today.year+1, self.month, self.day)
        return next_birthday

    def days_to_birthday(self):
        next_birthday = self.next_birthday()
        days_to_birthday = (next_birthday - date.today()).days
        return days_to_birthday


class Record:
    def __init__(
        self,
        name: Name,
        phone: Phone | str | None = None,
    ):
        self.name = name
        self.phones = []
        if phone is not None:
            self.add_phone(phone)

    def days_to_birthday(self):
        return self.days_to_birthday()

    def add_phone(self, phone: Phone | str):
        if isinstance(phone, str):
            phone = self.create_phone(phone)
        self.phones.append(phone)

    def create_phone(self, phone: str):
        return Phone(phone)

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return p.value

    def remove_phone(self, phone):
        for p in self.phones:
            if p == phone:
                self.phones.remove(p)
                return True
        return False

    def to_json(self):
        result = {'name': str(self.name), 'phones': [
            {'value': str(phone)} for phone in self.phones]}
        return result


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name] = record

    def to_json(self):
        result = []
        for name, record in self.data.items():
            result.append(record.to_json())
        return result

    def from_json(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            records = data["records"]
            for record_data in records:
                name = record_data['name']
                phones_data = record_data["phones"]
                record = Record(name=Name(name))
                for phone_data in phones_data:
                    phone = phone_data["value"]
                    record.add_phone(phone)
                self.add_record(record)

    def save(self, filename):
        data = {'records': self.to_json()}
        with open(filename, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def check_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return data

    def search(self, search_str):
        results = []
        for record in self.data.values():
            if search_str.lower() in record.name.value.lower():
                results.append(record)
            else:
                for phone in record.phones:
                    if search_str in phone.value:
                        results.append(record)
                        break
        return results

    def __iter__(self):
        self.index = 0
        self.n = 5
        self.iter_keys = list(self.data.keys())
        return self

    def __next__(self):
        if self.index < len(self.iter_keys):
            records = []
            for key in self.iter_keys[self.index:min(self.index+self.n, len(self.iter_keys))]:
                records.append(
                    f"{self.data[key].name}: {', '.join([phone.value for phone in self.data[key].phones])}")
            self.index += self.n
            return "\n".join(records)
        self.index = 0
        raise StopIteration

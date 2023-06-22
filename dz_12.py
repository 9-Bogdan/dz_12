from collections import UserDict
from datetime import datetime
import pickle


class AddressBook(UserDict):

    def add_record(self, record):
        key = record.name.value
        self.data[key] = record

    def iterator(self, N):
        list_dict = list(self.data)
        index = 0
        while index < len(list_dict):
            yield list_dict[index:index + N]
            index += N

    def save_in_file(self, filename):
        if filename.endswith(".bin"):
            with open(filename, "wb") as f:
                pickle.dump(self.data, f)
        else:
            raise ValueError("File the file must have an extension '.bin'")

    def load_from_file(self, filename):
        if filename.endswith(".bin"):
            with open(filename, "rb") as f:
                self.data = pickle.load(f)
        else:
            raise ValueError("File the file must have an extension '.bin'")

    def find_user(self, char=None, num=None):
        result = []
        if char:
            for k in self.data:
                if char.lower() in k.lower():
                    if self.data[k].birthday:
                        result.append(
                            f"{k} : {self.data[k].phone.value}; birthday = {self.data[k].birthday.value}")
                    else:
                        result.append(
                            f"{k}: {self.data[k].phone.value}")
        if num:
            for k, v in self.data.items():
                if num in v.phone.value:
                    if self.data[k].birthday:
                        result.append(
                            f"{k} : {v.phone.value}; birthday = {self.data[k].birthday.value}")
                    else:
                        result.append(f"{k}: {v.phone.value}")
        users = [i for i in set(result)]
        return users


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.correct_number(new_value):
            self._value = new_value
        else:
            raise ValueError("Incorrect phone number!")

    def correct_number(self, phone):
        if len(phone) == 12 and phone.startswith("38") and (all(not char. isalpha() for char in phone)):
            return True
        else:
            return False


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_date):
        if self.correct_date(new_date):
            self._value = new_date
        else:
            raise ValueError("Incorrect date!")

    def correct_date(self, new_date):
        try:
            dt = datetime.strptime(new_date, "%d/%m/%Y")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phone = phone
        self.birthday = birthday
        if phone:
            self.phones = []
            self.phones.append(phone)
        if birthday:
            self.birthdays = []
            self.birthdays.append(birthday)

    def remove_phone(self):
        for num in self.phones:
            if num.value == self.phone:
                self.phones.remove(num)

    def edit_phone(self, old_number, new_number):
        for num in self.phones:
            if num.value == old_number:
                num.value = new_number

    def days_to_birthday(self):
        if self.birthday:
            dt_birthday = datetime.strptime(self.birthday.value, "%d/%m/%Y")
            days_before_birthday = dt_birthday - datetime(year=dt_birthday.year,
                                                          month=datetime.now().month, day=datetime.now().day)
            return f"{days_before_birthday.days} days to birthday!"

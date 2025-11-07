from collections import UserDict
from datetime import datetime, timedelta


class Field:
    '''Base Class for fields'''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    '''Saves the name of the Contact. Can't be empty.'''

    def __init__(self, value: str):
        if not value.strip():
            raise ValueError('PLease set the Name!')
        super().__init__(value.strip())


class Phone(Field):
    '''Saves teh Contacts Phone number. Should have 10 digits.'''

    def __init__(self, value: str):
        if not self._is_valid(value):
            raise ValueError('Phone should contain 10 digits!')
        super().__init__(value)
        
    @staticmethod
    def _is_valid(value: str) -> bool:
        return value.isdigit() and len(value) == 10



class Birthday(Field):
    '''Saves contacts Birthday. Inout format DD.MM.YYYY'''

    def __init__(self, value: str):
        try:
            self.date = datetime.strptime(value,'%d.%m.%Y').date()
            super().__init__(value)

        except ValueError:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')


class Record:
    '''Holds all Contacts information togeteher '''
    def __init__(self, name: str, phones = None):
        self.name = Name(name)
        self.phones = phones if phones else []
        self.birthday = None
    
    def add_birthday(self,birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone: str):
           self.phones.append(Phone(phone))

    def remove_phone(self,phone_value: str):
           self.phones = [p for p in self.phones if p.value != phone_value] 

    def edit_phone(self, old_value: str, new_value: str):
        for phone in self.phones:
            if phone.value == old_value:

                if not Phone._is_valid(new_value):
                    raise ValueError('Phone should contain 10 digits!')
                
                phone.value = new_value
                return True
        return False
        
    def find_phone(self, phone_value: str):
        for phone in self.phones:
            if phone.value == phone_value:
                  return phone
        raise ValueError('No phone found!')
              

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        record = self.data.get(name)
        if record is None:
            raise KeyError (f'No record found for {name}.')
        return record
    
    def delete(self,name:str):
        if name in self.data:
            del self.data[name]    

    def get_upcoming_birthdays(self) -> list[dict]:
        upcomming_birthdays = []
        today = datetime.now().date()

        for contact in self.data.values():
            b = getattr(contact, 'birthday', None)
            if not b:
                continue

            birthdate = getattr(b, 'date')
            birthdate_this_year = birthdate.replace(year=today.year)

            if birthdate_this_year < today:
                birthdate_this_year = birthdate.replace(year=today.year+1)
            
            days_difference = (birthdate_this_year - today).days

            if  0 <= days_difference <= 7:
                congrats = birthdate_this_year
                if congrats.weekday() == 5:
                    congrats += timedelta(days=2)
                elif congrats.weekday() == 6:
                    congrats += timedelta(days=1)

                if congrats:
                    upcomming_birthdays.append({
                        'name': contact.name.value,
                        'congratulation_date': congrats.strftime('%d.%m.%Y')
                    })

        return upcomming_birthdays
            

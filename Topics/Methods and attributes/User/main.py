class User:
    def __init__(self, name, surname, age, country):
        self.name = name
        self.surname = surname
        self.age = age
        self.country = country

    def user_information(self):
        print(f"{self.name} {self.surname} is {self.age} years old and lives in {self.country}.")


User(input(),input(),input(),input()).user_information()

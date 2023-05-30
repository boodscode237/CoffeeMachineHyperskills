import collections
import enum


class Action(enum.Enum):
    BUY = "buy"
    FILL = "fill"
    TAKE = "take"
    REMAINING = "remaining"
    EXIT = "exit"


def ask_action():
    possible_values = ", ".join([action.value for action in Action])
    while True:
        answer = input(f"Write action ({possible_values}):\n>")
        try:
            return Action(answer)
        except ValueError:
            print(f"This answer is not valid: {answer}")


def ask_drink():
    choices = {1: "espresso", 2: "latte", 3: "cappuccino", "back": "to main menu"}
    possible_values = ", ".join(f"{value} - {name}" for value, name in sorted(choices.items()))
    while True:
        answer = input(f"What do you want to buy?  {possible_values}:\n>")
        try:
            value = int(answer)
            if value in choices:
                return value
            print(f"This answer is not valid: {answer}")
        except ValueError:
            print(f"This is not a number: {answer}")


def ask_quantity(msg):
    while True:
        answer = input(msg + "\n")
        try:
            value = int(answer)
            if value >= 0:
                return value
            print(f"This answer is not valid: {answer}")
        except ValueError:
            print(f"This is not a number: {answer}")


Consumption = collections.namedtuple("Consumption", "water, milk, coffee_beans, cups, money")


class NotEnoughSupplyError(Exception):
    def __init__(self, supply):
        msg = f"Sorry, not enough {supply}"
        super(NotEnoughSupplyError, self).__init__(msg)


class CoffeeMachine:
    def __init__(self):
        # quantities of items the coffee machine already had
        self.water = 400
        self.milk = 540
        self.coffee_beans = 120
        self.cups = 9
        self.money = 550
        self.running = True

    def execute_action(self, action):
        if action == Action.BUY:
            self.buy()
        elif action == Action.FILL:
            self.fill()
        elif action == Action.TAKE:
            self.take()
        elif action == Action.EXIT:
            self.running = False
        elif action == Action.REMAINING:
            self.show_remaining()
        else:
            raise NotImplementedError(action)

    def available_check(self, consumption):
        """
        Checks if it can afford making that type of coffee at the moment

        :param consumption: the Consumption
        :raise NotEnoughSupplyError: if at least one supply is missing.
        """
        if self.water - consumption.water < 0:
            raise NotEnoughSupplyError("water")
        elif self.milk - consumption.milk < 0:
            raise NotEnoughSupplyError("milk")
        elif self.coffee_beans - consumption.coffee_beans < 0:
            raise NotEnoughSupplyError("coffee beans")
        elif self.cups - consumption.cups < 0:
            raise NotEnoughSupplyError("cups")

    def buy(self):
        drink = ask_drink()
        if drink == 9:
            return
        espresso_cons = Consumption(250, 0, 16, 1, 4)
        latte_cons = Consumption(water=350, milk=75, coffee_beans=20, cups=1, money=7)
        cappuccino_cons = Consumption(water=200, milk=100, coffee_beans=12, cups=1, money=6)
        consumption = {1: espresso_cons, 2: latte_cons, 3: cappuccino_cons}[drink]
        try:
            self.available_check(consumption)
        except NotEnoughSupplyError as exc:
            print(exc)
        else:
            print("I have enough resources, making you a coffee!")
            self.water -= consumption.water
            self.milk -= consumption.milk
            self.coffee_beans -= consumption.coffee_beans
            self.cups -= consumption.cups
            self.money += consumption.money

    def fill(self):
        """
        Add supplies to the machine
        """
        self.water += ask_quantity("Write how many ml of water do you want to add:")
        self.milk += ask_quantity("Write how many ml of milk do you want to add:")
        self.coffee_beans += ask_quantity("Write how many grams of coffee beans do you want to add:")
        self.cups += ask_quantity("Write how many disposable cups of coffee do you want to add:")

    def take(self):
        """
        Take the money from the machine
        """
        print(f"I gave you ${self.money}")
        self.money = 0

    def show_remaining(self):
        """
        Display the quantities of supplies in the machine at the moment
        """
        print(f"The coffee machine has:")
        print(f"{self.water} of water")
        print(f"{self.milk} of milk")
        print(f"{self.coffee_beans} of coffee beans")
        print(f"{self.cups} of disposable cups")
        print(f"${self.money} of money")


def main():
    machine = CoffeeMachine()
    while machine.running:
        action = ask_action()
        machine.execute_action(action)


if __name__ == '__main__':
    main()
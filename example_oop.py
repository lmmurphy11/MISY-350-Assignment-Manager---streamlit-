
class Counter:
    def __init__(self, start: int = 0):
        self.value = start

    def increment(self) -> None:
        self.value += 1

    def current(self) -> int:
        return self.value
    
    def increment_2(self):
        self.value += 2


c = Counter(start= 5) # inistantation of the class or creating an object from the class (blue print - concept)

c.increment()

c.increment()

c.increment()

print(f"{c.current()}")

c1 = Counter(start= 10)
c1.increment_2()

print (f"{c1.current()}")


#------------- 00 - Day 2
class Employee:
    def __init__(self, name: str, base_salary: float) -> None:
        self.name = name
        self.base_salary = base_salary


    def calculate_bonus(self, performance_multiplier: float) -> float:
        return self.base_salary * performance_multiplier


emp = Employee("Alice", 50000.0)

bonus = emp.calculate_bonus(1.1)


print(f"The bonus for {emp.name} is {bonus}")

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
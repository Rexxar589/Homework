from random import choice
from time import sleep
from threading import Thread, RLock


class Philosopher_dilemma(Thread):

    def __init__(self, number, has_fork, needs_fork):
        Thread.__init__(self)
        self.number = number
        self.has_fork = has_fork
        self.needs_fork = needs_fork
        self.needs_some_food = False

    def run(self):
        while True:
            sleep(3)
            self.needs_some_food = choice((True, False))
            if self.needs_some_food:
                print(f"The philosopher {self.number} will start eating, looking into the sky abyss thoughtfully")
                self.eats_desired_food()

    def eats_desired_food(self):

        while True:
            with self.has_fork:
                print(f"The philosopher {self.number} captures fork")
                sleep(1)
                with self.needs_fork:
                    print(f"The philosopher {self.number} eats desired food")
                    sleep(1)
                print(f"The philosopher {self.number} finished feeding himself")
                sleep(1)
            break


forks = [RLock() for i in range(5)]
philosophers = [Philosopher_dilemma(i, forks[i % 5], forks[(i + 1) % 5]) for i in range(5)]

for philosopher in philosophers:
    philosopher.start()

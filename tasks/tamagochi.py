import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules import terminal
import time
import random
import threading
import keyboard

MAX_HUNGER = 200
MAX_FUN = 200
SCALES_DIVISION_PRICE = 3
HUNGER_OVERSATURATION_LIMIT = 100
FUN_OVERINDULGANCE_LIMIT = 100
FEED_COOLDOWN = 30
PLAY_COOLDOWN = 15

HUNGER_SCALE_LENGTH = HUNGER_OVERSATURATION_LIMIT
FUN_SCALE_LENGTH = FUN_OVERINDULGANCE_LIMIT
HUNGER_SCALE_DIVISIONS = HUNGER_SCALE_LENGTH // SCALES_DIVISION_PRICE
FUN_SCALE_DIVISIONS = FUN_SCALE_LENGTH // SCALES_DIVISION_PRICE

class Pet:
    def __init__(self, name: str = "Nnican", hunger=100, fun=50) -> None:
        self.name: str = name
        self.is_alive = True
        self.stop_event = threading.Event()
        self.__art: str = "    ≽(._.)≼\n      ( )_"
        self.__hunger: int = hunger
        self.__fun: int = fun
        self.__feed_cooldown: int = 0
        self.__play_cooldown: int = 0

    @property
    def hunger(self) -> int:
        return self.__hunger

    @property
    def fun(self) -> int:
        return self.__fun

    @property
    def feed_cooldown(self) -> int:
        return self.__feed_cooldown

    @property
    def play_cooldown(self) -> int:
        return self.__play_cooldown

    @hunger.setter
    def hunger(self, value) -> None:
        if value < MAX_HUNGER:
            self.__hunger = value
        else:
            self.__hunger = MAX_HUNGER
        if self.hunger <= 0:
            self.is_alive = False
        self.check_state()
        self.display()

    @fun.setter
    def fun(self, value) -> None:
        if value < MAX_FUN:
            self.__fun = value
        else:
            self.__fun = MAX_FUN
        if self.fun <= 0:
            self.is_alive = False
        self.check_state()
        self.display()

    @feed_cooldown.setter
    def feed_cooldown(self, value) -> None:
        self.__feed_cooldown = value
        self.display()

    @play_cooldown.setter
    def play_cooldown(self, value) -> None:
        self.__play_cooldown = value
        self.display()

    def display(self) -> None:
        hunger_scale_divisions: int = self.hunger // SCALES_DIVISION_PRICE
        fun_scale_divisions: int = self.fun // SCALES_DIVISION_PRICE
        terminal.clear()
        output: str = f"""
\033[01;38;05;15m{self.__art}\033[0m

   \033[01;38;05;15mHunger: {self.hunger}\033[m
\033[01;38;05;252m0\033[01;38;05;15m|\033[01;38;05;179m{'▇' * hunger_scale_divisions if hunger_scale_divisions <= HUNGER_SCALE_DIVISIONS else '▇' * HUNGER_SCALE_DIVISIONS}\033[01;38;05;238m{'▇' * ((HUNGER_SCALE_LENGTH // SCALES_DIVISION_PRICE) - hunger_scale_divisions) if hunger_scale_divisions > 0 else '▇' * HUNGER_SCALE_DIVISIONS}\033[01;38;05;15m|\033[01;38;05;252m{HUNGER_SCALE_LENGTH}\033[0m
   \033[01;38;05;15mFun: {self.fun}\033[0m
\033[01;38;05;252m0\033[01;38;05;15m|\033[01;38;05;139m{'▇' * fun_scale_divisions if fun_scale_divisions <= FUN_SCALE_DIVISIONS else '▇' * FUN_SCALE_DIVISIONS}\033[01;38;05;238m{'▇' * ((FUN_SCALE_LENGTH // SCALES_DIVISION_PRICE) - fun_scale_divisions) if fun_scale_divisions > 0 else '▇' * FUN_SCALE_DIVISIONS}\033[01;38;05;15m|\033[01;38;05;252m{FUN_SCALE_LENGTH}\033[0m

feed cooldown: {self.feed_cooldown}; play cooldown: {self.play_cooldown}

[F]eed [P]lay [Q]uit
"""
        print(f"\n{' ' * (6 - (len(self.name) // 2 - 1 if len(self.name) % 2 == 0 else len(self.name) // 2)) if len(self.name) <= 10 else ''}\033[01;37;42m {self.name} \033[0m" if self.is_alive else f"     \033[01;38;05;15;48;05;242m {self.name} \033[0m", output)

    def feed(self) -> None:
        print("f")
        if self.feed_cooldown == 0 and not self.hunger >= 100:
            self.hunger += 20

            self.feed_cooldown = FEED_COOLDOWN

    def play(self) -> None:
        if self.play_cooldown == 0 and not self.fun >= 100 and self.hunger > 10:
            self.fun += 20
            self.hunger -= 10

            self.play_cooldown = PLAY_COOLDOWN

    def check_state(self) -> None:
        if self.fun <= 0 and self.hunger > 0:
            self.__art = "\n≽(‾-‾)≼ )_\n╱     ╲"
        elif self.hunger <= 0:
            self.__art = "\n≽(x_x)≼ )_"

        if self.hunger > 100 and self.fun > 100:
            self.__art = "    ≽(._.)≼\n      (@)_"
        elif self.hunger > 100 and 75 <= self.fun < 100:
            self.__art = "    ≽(^‿ ​^)≼\n      (@)_"
        elif self.hunger > 100 and 25 <= self.fun < 75:
            self.__art = "    ≽(._.)≼\n      (@)_"
        elif self.hunger > 100 and 0 < self.fun < 25:
            self.__art = "    ≽(._.)≼\n      (@)_"

        if 75 <= self.hunger < 100 and self.fun > 100:
            self.__art = "    ≽(^‿ ​^)≼\n      ( )_"
        elif 75 <= self.hunger < 100 and 75 <= self.fun < 100:
            self.__art = "    ≽(._.)≼\n      ( )_"
        elif 75 <= self.hunger < 100 and 25 <= self.fun < 75:
            self.__art = "    ≽(._.)≼\n      ( )_"
        elif 75 <= self.hunger < 100 and 0 < self.fun < 25:
            self.__art = "    ≽(._.)≼\n      ( )_"

        if 25 <= self.hunger < 75 and self.fun > 100:
            self.__art = "    ≽(^‿ ​^)≼\n      ( )_"
        elif 25 <= self.hunger < 75 and 75 <= self.fun < 100:
            self.__art = "    ≽(._.)≼\n      ( )_"
        elif 25 <= self.hunger < 75 and 25 <= self.fun < 75:
            self.__art = "    ≽(._.)≼\n      ( )_"
        elif 25 <= self.hunger < 75 and 0 < self.fun < 25:
            self.__art = "    ≽(._.)≼\n      ( )_"

        if 0 < self.hunger < 25 and self.fun > 100:
            self.__art = "    ≽(^‿ ​^)≼\n      (≋)_"
        elif 0 < self.hunger < 25 and 75 <= self.fun < 100:
            self.__art = "    ≽(._.)≼\n      (≋)_"
        elif 0 < self.hunger < 25 and 25 <= self.fun < 75:
            self.__art = "    ≽(._.)≼\n      (≋)_"
        elif 0 < self.hunger < 25 and 0 < self.fun < 25:
            self.__art = "    ≽(._.)≼\n      (≋)_"


        elif self.hunger > 120 or self.fun > 120:
            state_thread = threading.Thread(target=self.handle_overindulgence)
            state_thread.start()
            # Пооток состояния
            state_thread.join()

    def handle_overindulgence(self) -> None:
        while self.hunger > HUNGER_OVERSATURATION_LIMIT or self.fun > FUN_OVERINDULGANCE_LIMIT and not self.stop_event.is_set():
            time.sleep(30)
            if self.hunger > 120:
                self.hunger -= 10
                if self.hunger < 0:
                    self.hunger = 0
            if self.fun > 120:
                self.fun -= 10
                if self.fun < 0:
                    self.fun = 0

    def update(self) -> None:
        start_time: float = time.time()
        self.display()
        time.sleep(10)
        while (self.is_alive or time.time() - start_time <= 600) and not self.stop_event.is_set():
            self.hunger -= 10
            self.fun -= 5
            for t in range(random.randint(2, 30)):
                if not ((self.is_alive or time.time() - start_time <= 600) and not self.stop_event.is_set()):
                    break
                time.sleep(1)

    def cooldown_timer(self) -> None:
        while self.is_alive and not self.stop_event.is_set():
            time.sleep(1)
            if self.__feed_cooldown > 0:
                self.__feed_cooldown -= 1
            if self.__play_cooldown > 0:
                self.__play_cooldown -= 1

def tamagochi() -> str:
    name: str = input("Set pet name: ")
    if not name:
        name = "Axolotl"
    axolotl = Pet(name)

    def quit() -> None:
        axolotl.stop_event.set()

    def restart() -> None:
        quit()
        game()


    keyboard.add_hotkey('q', quit)
    keyboard.add_hotkey('r', restart)
    keyboard.add_hotkey('f', lambda: axolotl.feed())
    keyboard.add_hotkey('p', lambda: axolotl.play())
    update_thread = threading.Thread(target=axolotl.update)
    cooldown_update_thread = threading.Thread(target=axolotl.cooldown_timer)

    update_thread.start()
    cooldown_update_thread.start()

    update_thread.join()
    quit()

    cooldown_update_thread.join()

    if axolotl.is_alive:
        return f"Вы передали {axolotl.name} в добрые руки."
    else:
        return f"{axolotl.name} ушёл от вас."

def game() -> None:
    result: str = tamagochi()
    print(result)

if __name__ == "__main__":
    game()
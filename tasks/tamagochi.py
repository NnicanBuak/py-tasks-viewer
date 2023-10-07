import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules import terminal
import time
import random
import threading
import keyboard

FEED_COOLDOWN = 10
PLAY_COOLDOWN = 15
SCALES_DIVISION_PRICE = 10
STOP_EVENT = threading.Event()

class Pet:
    def __init__(self, name: str = "Nnican", hunger=100, fun=50) -> None:
        self.name: str = name
        self.is_alive = True
        self.__art: str = "     ≽(._.)≼\n       ( )_"
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
        self.__hunger = value
        self.check_state()
        self.display()
        if self.hunger <= 0:
            self.is_alive = False

    @fun.setter
    def fun(self, value) -> None:
        self.__fun = value
        self.check_state()
        self.display()
        if self.fun <= 0:
            self.is_alive = False

    @feed_cooldown.setter
    def feed_cooldown(self, value) -> None:
        self.__feed_cooldown = value
        self.display()

    @play_cooldown.setter
    def play_cooldown(self, value) -> None:
        self.__play_cooldown = value
        self.display()

    def display(self) -> None:
        fun_scale_divisions = self.fun // SCALES_DIVISION_PRICE
        hunger_scale_divisions = self.hunger // SCALES_DIVISION_PRICE
        terminal.clear()
        print(f"Name: {self.name}; Alive: {self.is_alive}\n\n{self.__art}\n\nHunger: |{'▇' * hunger_scale_divisions if hunger_scale_divisions <= SCALES_DIVISION_PRICE else '▇' * SCALES_DIVISION_PRICE}{(SCALES_DIVISION_PRICE - hunger_scale_divisions) * ' '}|{'▇' * (hunger_scale_divisions - SCALES_DIVISION_PRICE) if hunger_scale_divisions > SCALES_DIVISION_PRICE else ''}\n   Fun: {'|' + '▇' * fun_scale_divisions if fun_scale_divisions <= SCALES_DIVISION_PRICE else '▇' * SCALES_DIVISION_PRICE}{(SCALES_DIVISION_PRICE - fun_scale_divisions) * ' '}|{'▇' * (fun_scale_divisions - SCALES_DIVISION_PRICE) if fun_scale_divisions > SCALES_DIVISION_PRICE else ''}\n\nfeed cooldown: {self.feed_cooldown}; play cooldown: {self.play_cooldown}\nNote: P for play and F for feed <3")

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
            self.__art = "\n≽(‾--‾)≼ )_\n╱     ╲"
        elif self.hunger <= 0:
            self.__art = "\n≽(x__x)≼ )_"


        # if self.hunger >= 120 and self.fun >= 120:
        #     self.__art = "     ≽(^‿ ​^)≼\n       ( )_"
        # elif self.hunger >= 120 and 100 <= self.fun < 120:
        #     self.__art = "     ≽(._.)≼\n       ( )_"
        # elif self.hunger >= 120 and 75 <= self.fun < 100:
        #     self.__art = "     ≽(._.)≼\n       ( )_"
        # elif self.hunger >= 120 and 25 <= self.fun < 75:
        #     self.__art = "     ≽(._.)≼\n       ( )_"
        # elif self.hunger >= 120 and 0 < self.fun < 25:
        #     self.__art = "     ≽(._.)≼\n       ( )_"

        # if 100 <= self.hunger < 120 and self.fun >= 120:
        #     self.__art = "     ≽(^‿ ​^)≼\n       ( )_"
        # elif 100 <= self.hunger < 120 and 100 <= self.fun < 120:
        #     self.__art = "     ≽(._.)≼\n       ( )_"
        # elif 100 <= self.hunger < 120 and 75 <= self.fun < 100:
        #     self.__art = "     ≽(._.)≼\n       ( )_"
        # elif 100 <= self.hunger < 120 and 25 <= self.fun < 75:
        #     self.__art = "     ≽(._.)≼\n       ( )_"
        # elif 100 <= self.hunger < 120 and 0 < self.fun < 25:
        #     self.__art = "     ≽(._.)≼\n       ( )_"

        # if 75 <= self.hunger < 100 and self.fun >= 120:
        #     self.__art = "     ≽(^‿ ​^)≼\n       ( )_"
        # elif 75 <= self.hunger < 100 and 100 <= self.fun < 120:
        #     self.__art = "     ≽(._.)≼\n       ( )_"
        # elif 75 <= self.hunger < 100 and 75 <= self.fun < 100:
        #     self.__art = "     ≽(._.)≼\n       ( )_"
        # elif 75 <= self.hunger < 100 and 25 <= self.fun < 75:
        #     self.__art = "     ≽(._.)≼\n       ( )_"
        # elif 75 <= self.hunger < 100 and 0 < self.fun < 25:
        #     self.__art = "     ≽(._.)≼\n       ( )_"

        # if 25 <= self.hunger < 75 and self.fun >= 120:
        #     self.__art = "     ≽(^‿ ​^)≼\n       ( )_"
        # elif 25 <= self.hunger < 75 and 100 <= self.fun < 120:
        #     self.__art = "     ≽(._.)≼\n       ( )_"
        # elif 25 <= self.hunger < 75 and 75 <= self.fun < 100:
        #     self.__art = "     ≽(._.)≼\n       ( )_"
        # elif 25 <= self.hunger < 75 and 0 < self.fun < 25:
        #     self.__art = "     ≽(._.)≼\n       ( )_"

        # if 0 < self.hunger < 25 and self.fun >= 120:
        #     self.__art = "     ≽(^‿ ​^)≼\n       (@)_"
        # elif 0 < self.hunger < 25 and 100 <= self.fun < 120:
        #     self.__art = "     ≽(._.)≼\n       (@)_"
        # elif 0 < self.hunger < 25 and 75 <= self.fun < 100:
        #     self.__art = "     ≽(._.)≼\n       (@)_"
        # elif 0 < self.hunger < 25 and 25 <= self.fun < 75:
        #     self.__art = "     ≽(._.)≼\n       (@)_"
        # elif 0 < self.hunger < 25 and 0 < self.fun < 25:
        #     self.__art = "     ≽(._.)≼\n       (@)_"


        elif self.hunger > 120 or self.fun > 120:
            state_thread = threading.Thread(target=self.handle_overindulgence)
            state_thread.start()
            # Пооток состояния
            state_thread.join()

    def handle_overindulgence(self) -> None:
        while self.hunger > 120 or self.fun > 120 and not STOP_EVENT.is_set():
            time.sleep(30)
            if self.hunger > 120:
                self.hunger -= 10
                if self.hunger < 0:
                    self.hunger = 0
            if self.fun > 120:
                self.fun -= 10
                if self.fun < 0:
                    self.fun = 0

    def interact(self) -> None:
        while self.is_alive and not STOP_EVENT.is_set():
            try:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    key_name = event.name

                    if key_name == 'f':
                        self.feed()
                    elif key_name == 'p':
                        self.play()
                    elif key_name == 'q':
                        print("Завершение игровых процессов...")
                        break
            except KeyboardInterrupt:
                break


    def update(self) -> None:
        start_time: float = time.time()
        self.display()
        time.sleep(10)
        while (self.is_alive or time.time() - start_time <= 600) and not STOP_EVENT.is_set():
            self.hunger -= 10
            self.fun -= 5
            time.sleep(random.randint(2, 30))

    def cooldown_timer(self) -> None:
        while self.is_alive and not STOP_EVENT.is_set():
            time.sleep(1)
            if self.__feed_cooldown > 0:
                self.__feed_cooldown -= 1
            if self.__play_cooldown > 0:
                self.__play_cooldown -= 1

def tamagochi() -> str:
    axolotl = Pet()

    input_thread = threading.Thread(target=axolotl.interact)
    update_thread = threading.Thread(target=axolotl.update)
    cooldown_update_thread = threading.Thread(target=axolotl.cooldown_timer)

    input_thread.start()
    update_thread.start()
    cooldown_update_thread.start()

    STOP_EVENT.set()
    input_thread.join()
    update_thread.join()
    cooldown_update_thread.join()

    if axolotl.is_alive:
        return f"Вы вознесли {axolotl.name}!"
    else:
        return f"Вы не сохранили {axolotl.name}..."

if __name__ == "__main__":
    result: str = tamagochi()
    print(result)
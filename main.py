from random import choice, randint, random
from time import sleep
      

class Game:
    run: bool = True
    players = {}
    message = ''
    range = tuple(j for i in range(1, 8) for j in range(i * 9 + 1, i * 9 + 8))
    start = (
        (tuple(i for i in range if (i + 3) % 9 and (i + 2) % 9), range[:-14]),
        (tuple(i for i in range if (i + 2) % 9), range[:-7]),
        (range, range)
    )
    format = "··HSM"
    format = "·#HSM"

    def __init__(self):
        self.setup()

    def block(self, pos):
        self.map[pos] = 1
        for offset in (0, 1, 9, 10, 8, -1, -9, -10, -8):
            i = pos + offset
            if i in self.free:
                self.free.remove(i)

    def setup(self):
        self.player = ''
        self.shots = []
        self.ships = []
        self.free = list(self.range)
        self.map = [-1] * 81
        for i in self.range:
            self.map[i] = 0

        for i, count, size in ((0, 1, 3), (1, 2, 2), (2, 4, 1)):
            while count:                              
                if not self.free:
                    self.setup()
                    return
                
                dir = random() < .5
                start = choice(tuple(j for j in self.start[i][dir] if j in self.free))
                if dir:
                    ship = tuple(start + j for j in range(size))
                else:
                    ship = tuple(start + j * 9 for j in range(size))

                if not all((j in self.free for j in ship)):
                    continue

                self.ships.append(ship)
                count -= 1

                for j in ship:
                    self.block(j)


    def render(self):
        print("\033[H\033[J", end='')
        print("    A B C D E F G")
        print(' ' * 24 + (self.player and f"Player: {self.player}"))
        for i in range(1, 8):
            start = i * 9 + 1
            end = i * 9 + 8
            print(i, end='   ')
            for j in self.map[start:end]:
                print(self.format[j], end=' ')
            print(f"  {i}", end='   ')
            if self.player and i == 2:
                print(f"Score: {len(self.shots)}")
            elif self.player and i == 4:
                print("M - miss, H - hit, S - sunk")
            else:
                print()
        print("\n    A B C D E F G")

    def input(self):
        if not self.player:
            self.player = input(f"\nEnter your name.\n\n> ")
        elif not self.ships:
            score = len(self.shots)
            if score > self.players.get(self.player, 0):
                self.players[self.player] = score
            cmd = input(f"\nYour score: {score}. Another game? (Y/n)\n\n> ").lower()
            if cmd == "y" or cmd == "yes":
                self.setup()
            else:
                self.run = False
                players = sorted(self.players.items(), key=lambda i: i[1])
                print("\033[H\033[J", end='')
                print("#   Name     Score")
                for i, (name, score) in enumerate(players):
                    i = str(i + 1)
                    line = i + ' ' * (4 - len(i))
                    line += name + ' ' * (9 - len(name))
                    line += str(score)
                    print(line)
        else:
            cmd = input(f'\n{self.message or 'Enter coordinates. (e.g. "a1" or "g7")'}\n\n> ')
            if len(cmd) == 2 and (x := cmd[0].upper()) in "ABCDEFG" and (y := cmd[1]) in "1234567":
                pos = int(y) * 9 + "ABCDEFG".index(x) + 1
                if pos in self.shots:
                    self.message = f"{cmd} is already checked. Enter another coordinates."
                else:
                    self.message = ''
                    self.shots.append(pos)
                    if self.map[pos]:
                        self.map[pos] = 2
                        for i in self.ships:
                            if pos in i:
                                if 1 not in (self.map[j] for j in i):
                                    for j in i:
                                        self.map[j] = 3
                                    self.ships.remove(i)
                                break
                    else:
                        self.map[pos] = 4
            else:
                self.message = ''

    def main(self):
        try:
            while self.run:
                self.render()
                self.input()
        except KeyboardInterrupt:
            print()
        

if __name__ == "__main__":
    Game().main()

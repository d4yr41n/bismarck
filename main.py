from random import choice, randint, random
      

class Game:
    run: bool = True
    players = {}
    message = ''
    range = tuple(
        j for i in range(1, 8) for j in range(i * 9 + 1, i * 9 + 8)
    )
    format = "··HSM"
    format = "·#HSM"

    def __init__(self):
        self.setup()

    def block(self, pos):
        for offset in (0, 1, 9, 10, 8, -1, -9, -10, -8):
            i = pos + offset
            if self.map[i] == 0 and i in self.free:
                self.free.remove(i)

    def setup(self):
        self.player = ''
        self.shots = []
        self.ships = []
        self.free = list(self.range)
        self.map = [-1] * 81
        for i in self.range:
            self.map[i] = 0

        hor = random() < .5
        if hor:
            start = choice([i for i in self.free if (i + 3) % 9 and (i + 2) % 9])
            ship = (start, start + 1, start + 2)
        else:
            start = choice(self.free[:-14])
            ship = (start, start + 9, start + 18)
        self.ships.append(ship)

        for i in ship:
            self.block(i)
            self.map[i] = 1

        # t = 2
        # s = 4
        # while t: 
        #     ship = None
        #     hor = random() < .5
        #     if hor:
        #         start = choice([i for i in self.free if (i + 2) % 9])
        #         if start + 1 in self.free:
        #             ship = (start, start + 1)
        #         else:
        #             self.map[start] = 1
        #             self.ships.append((start,))
        #             self.block(start)
        #             s -= 1
        #     elif not ship:
        #         start = choice(self.free[:-7])
        #         if start + 9 in self.free:
        #             ship = (start, start + 9)
        #         else:
        #             self.map[start] = 1
        #             self.ships.append((start,))
        #             self.block(start)
        #             s -= 1

        #     if ship:
        #         self.ships.append(ship)
        #         for i in ship:
        #             self.block(i)
        #             self.map[i] = 1

        #         t -= 1
                
        # for i in range(s):
        #     if self.free:
        #         start = choice(self.free)
        #         self.block(start)
        #         self.map[start] = 1
        #         self.ships.append((start,))
        #     else:
        #         self.setup()

    def render(self):
        print("\033[H\033[J", end='')
        print("    A B C D E F G\n")
        for i in range(1, 8):
            start = i * 9 + 1
            end = i * 9 + 8
            print(i, end='   ')
            for j in self.map[start:end]:
                print(self.format[j], end=' ')
            print(f"  {i}")
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

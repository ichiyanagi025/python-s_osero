from random import randint

BLACK = 1
WHITE = -1
STONE = {1:'BLACK', -1:'WHITE'}
OPPONENT = {BLACK: WHITE, WHITE: BLACK}

class Board:
    def __init__(self):
        self.cells = []
        for i in range(8):
            self.cells.append([None for i in range(8)])

        self.cells[3][3] = WHITE
        self.cells[3][4] = BLACK
        self.cells[4][3] = BLACK
        self.cells[4][4] = WHITE

    def put(self, x, y, stone):
        flippable = self.list_flippable_disks(x, y, stone)
        self.cells[y][x] = stone
        for x,y in flippable:
            self.cells[y][x] = stone

        return True

    def show_board(self,turn):
        print("--" * 20)
        print(str(turn) + "ターン目")
        print("  ", end="")   
        for i in range(8):
            print(i, end="")
            print(" ", end="")
        print("\n", end="")

        j = 0
        for i in self.cells:
            print(j, end="")
            print(" ", end="")
            j += 1
            for cell in i:
                if cell == WHITE:
                    print("●", end=" ")
                elif cell == BLACK:
                    print("○", end=" ")
                else:
                    print("*", end=" ")
            print("\n", end="")

    def list_possible_cells(self, stone):
        possible = []
        for x in range(8):
            for y in range(8):
                if self.cells[y][x] is not None:
                    continue
                if self.list_flippable_disks(x, y, stone) == []:
                    continue
                else:
                    possible.append((x, y))
        return possible

    def list_flippable_disks(self, x, y, stone):
        PREV = -1
        NEXT = 1
        DIRECTION = [PREV, 0, NEXT]
        flippable = []

        for dx in DIRECTION:
            for dy in DIRECTION:
                if dx == 0 and dy == 0:
                    continue

                tmp = []
                depth = 0
                while(True):
                    depth += 1

                    rx = x + (dx * depth)
                    ry = y + (dy * depth)

                    if 0 <= rx < 8 and 0 <= ry < 8:

                        request = self.cells[ry][rx]

                        if request is None:
                            break

                        if request == stone:  
                            if tmp != []:      
                                flippable.extend(tmp) 
                            else:              
                                break
                        else:
                            tmp.append((rx, ry))  
                    else:
                        break
        return flippable

class Othello:

    def mode_option(self, mode):
        if mode == 0:
            self.player1 = User(BLACK, "PLAYER1")
            self.player2 = User(WHITE, "PLAYER2")
        elif mode == 1:
            self.player1 = User(BLACK, "あなた")
            self.player2 = Cpu(WHITE, "CPU")
        

    def play(self):
        board = Board()
        turn = 1
        pass_turn = 0
        mode = int(input("mode select: 0)PvP 1)vs.cpu> "))
        self.mode_option(mode)

        while(True):
            board.show_board(turn)
            black_count = 0
            white_count = 0
            for x in range(8):
                for y in range(8):
                    if board.cells[y][x] == BLACK:
                        black_count += 1
                    elif board.cells[y][x] == WHITE:
                        white_count += 1

            
            if (black_count + white_count == 64
                or pass_turn == 2
                or black_count == 0
                or white_count == 0):
                print("--" * 10+ "finished!!" + "--" * 10)
                if black_count > white_count:
                    print("WINNER BLACK!!")
                elif black_count < white_count:
                    print("WINNER WHITE!!")
                else:
                    print("Draw")

                print("results:  " + "B: " + str(black_count) + ", W: " + str(white_count))
                break

            elif turn % 2 == 1:
                stone = BLACK
                possible = board.list_possible_cells(stone)
                if possible == []: 
                    pass
                else:  
                    index = self.player1.main(possible) 

            elif turn % 2 == 0:
                stone = WHITE
                possible = board.list_possible_cells(stone)
                if possible == []:
                    pass
                else:
                    index = self.player2.main(possible)

            if possible == []:
                print("pass")
                pass_turn += 1
                pass
            else:
                board.put(*possible[index],stone)
                pass_turn = 0

            turn += 1

class BasePlayer:

    def __init__(self,stone,name):
        self.stone = stone
        self.name = name
        self.board = Board()
        self.copy_cells = []

class User(BasePlayer):

    def main(self,possible):
        print("player: " + self.name + " (" + STONE[self.stone] + ")")
        print("put to: ", end="[")   
        for i in range(len(possible) - 1): 
            print(str(i) + ":" + str(possible[i]), end=", ")
        print(str(len(possible) - 1) + ":" + str(possible[len(possible) - 1]) + "]")
        index = int(input("choose: ")) 
        print("You put:" + str(possible[index]))
        return index  

class Cpu(BasePlayer):
    def main(self,possible):
        index = randint(0, len(possible) -1)
        return index

if __name__ == "__main__":
    Othello().play()

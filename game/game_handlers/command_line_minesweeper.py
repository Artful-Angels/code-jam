from random import randint


class Board:
    def __init__(self, rows=30, cols=16, mines=100):
        self.rows = rows
        self.cols = cols
        self.mine_squares = {}
        self.squares = {(col, row): 0 for row in range(rows) for col in range(cols)}
        while mines > rows * cols * 0.5:
            mines = int(input("Number of mines too great, enter again:"))
        self.num_mines = mines
        self.mine_squares = set()
        self.uncovered_squares = set()
        self.flags = {}
        self.first_click = True
        self.game_over = False

        self.generate_mines()
        self.start_game()

    def generate_mines(self):
        for mine in range(self.num_mines):
            mine_x, mine_y = randint(0, self.cols - 1), randint(0, self.rows - 1)
            while (mine_x, mine_y) in self.mine_squares:
                mine_x, mine_y = randint(0, self.cols - 1), randint(0, self.rows - 1)
            self.mine_squares.add((mine_x, mine_y))
            self.squares[(mine_x, mine_y)] = "M"
            for x in range(mine_x - 1, mine_x + 2):
                if 0 <= x < self.cols:
                    for y in range(mine_y - 1, mine_y + 2):
                        if 0 <= y < self.rows:
                            if (x != mine_x or y != mine_y) and self.squares[
                                (x, y)
                            ] != "M":
                                self.squares[(x, y)] += 1

    def get_command(self):
        correct = True
        user_data = [data for data in input("Enter a command: ").split()]
        if len(user_data) != 3:
            print("Must enter a command and two co-ordinates seperated by spaces.")
        else:
            both_nums = True
            for coord in user_data[1:]:
                for ltr in coord:
                    if ord(ltr) < 48 or ord(ltr) > 57:
                        both_nums = False
            if not both_nums:
                print("2nd and 3rd values inputted must be positive numbers")
                correct = False
            elif both_nums:
                if int(user_data[1]) >= self.cols:
                    print("The x co-ordinate is out of range.")
                    correct = False
                if int(user_data[2]) >= self.rows:
                    print("The y co-ordinate is out of range.")
                    correct = False

            if user_data[0] not in ["click", "flag", "deflag"]:
                print("Command must be 'click', 'flag' or 'deflag'")
                correct = False

        return user_data, correct

    def start_game(self):
        user_data, valid = self.get_command()

        while not valid or user_data[0] != "click":
            if user_data[0] != "click":
                print("First command must be click.")
            user_data, valid = self.get_command()

        command, x, y = user_data
        x, y = int(x), int(y)

        for x_coord in range(x - 1, x + 2):
            if 0 <= x_coord < self.cols:
                for y_coord in range(y - 1, y + 2):
                    if 0 <= y_coord < self.rows:
                        if self.squares[(x_coord, y_coord)] == "M":
                            self.squares[(x_coord, y_coord)] = 0
                            self.change_mine_nums(x_coord, y_coord)
                            self.scan_for_mines(x_coord, y_coord)
        self.squares[(x, y)] = 0

        for x_coord in range(x - 1, x + 2):
            if 0 <= x_coord < self.cols:
                for y_coord in range(y - 1, y + 2):
                    if 0 <= y_coord < self.rows:
                        self.uncovered_squares.add((x_coord, y_coord))
                        if self.squares[(x_coord, y_coord)] == 0:
                            if x != x_coord or y != y_coord:
                                self.reveal_zeros(x_coord, y_coord)

        while self.click_square(command, x, y):
            user_data = [data for data in input("Enter a command: ").split()]
            while len(user_data) != 3:
                print("Must enter a command and two co-ordinates seperated by spaces.")
                user_data = [data for data in input("Enter a command: ").split()]

            command, x, y = user_data
            x, y = int(x), int(y)
            if self.first_click:
                self.first_click = False

    def scan_for_mines(self, x, y):
        for x_coord in range(x - 1, x + 2):
            if 0 <= x_coord < self.cols:
                for y_coord in range(y - 1, y + 2):
                    if 0 <= y_coord < self.rows:
                        if self.squares[(x_coord, y_coord)] == "M":
                            self.squares[(x, y)] += 1

    def change_mine_nums(self, x, y):
        for x_coord in range(x - 1, x + 2):
            if 0 <= x_coord < self.cols:
                for y_coord in range(y - 1, y + 2):
                    if 0 <= y_coord < self.rows:
                        if self.squares[(x_coord, y_coord)] != "M":
                            if self.squares[(x_coord, y_coord)] > 0:
                                self.squares[(x_coord, y_coord)] -= 1

    def reveal_zeros(self, x, y, reveal=True):
        for x_coord in range(x - 1, x + 2):
            if 0 <= x_coord < self.cols:
                for y_coord in range(y - 1, y + 2):
                    if 0 <= y_coord < self.rows:
                        if self.squares[(x_coord, y_coord)] == 0:
                            if x != x_coord or y != y_coord:
                                if (
                                    x_coord,
                                    y_coord,
                                ) not in self.uncovered_squares:
                                    self.reveal_zeros(x_coord, y_coord)
                        if reveal:
                            self.uncovered_squares.add((x_coord, y_coord))

    def reveal_board(self):
        if self.game_over:
            for coord in self.flags:
                if coord in self.mine_squares:
                    self.squares[coord] = "M"
                else:
                    self.squares[coord] = "W"
            self.uncovered_squares = set(self.squares)
        print("\t", end="")
        for i in range(self.cols):
            print(i % 10, end=" ")
        print("\n")
        for row in range(self.rows):
            print(row % 10, end="\t")
            for col in range(self.cols):
                if (col, row) in self.uncovered_squares:
                    print(self.squares[(col, row)], end=" ")
                elif (col, row) in self.flags:
                    print("F", end=" ")
                else:
                    print("?", end=" ")
            print()

    def click_square(self, command, square_x, square_y):
        if command.lower() == "click":
            if (square_x, square_y) in self.flags:
                print("You have to deflag before clicking.")
            elif (
                square_x,
                square_y,
            ) in self.mine_squares and not self.first_click:
                self.game_over = True
                self.reveal_board()
                print("GAME OVER - FAILED")
                return False
            elif set(self.squares) - self.uncovered_squares == self.mine_squares:
                print("GAME OVER - SUCCESS!")
                return False
            elif (
                square_x,
                square_y,
            ) in self.uncovered_squares and not self.first_click:
                print("You've already clicked this.")
            else:
                self.uncovered_squares.add((square_x, square_y))
                self.reveal_zeros(square_x, square_y, reveal=False)
        elif command.lower() == "flag":
            if (square_x, square_y) in self.uncovered_squares:
                print("You can only flag covered squares.")
            else:
                self.flags[(square_x, square_y)] = self.squares[(square_x, square_y)]
                self.squares[(square_x, square_y)] = "F"
        elif command.lower() == "deflag":
            if (square_x, square_y) not in self.flags:
                print("That square was not flagged.")
            else:
                self.squares[(square_x, square_y)] = self.flags[(square_x, square_y)]
                del self.flags[(square_x, square_y)]
        else:
            print("Command must be 'click', 'flag' or 'deflag'")
            return True

        print()
        self.reveal_board()
        return True


Board(rows=16, cols=30, mines=10)

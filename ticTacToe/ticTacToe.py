import random


class Board:
    def __init__(self):
        self.cells_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]

    def display(self):
        print("%s | %s | %s" % (self.cells_board[0], self.cells_board[1], self.cells_board[2]))
        print("----------")
        print("%s | %s | %s" % (self.cells_board[3], self.cells_board[4], self.cells_board[5]))
        print("----------")
        print("%s | %s | %s" % (self.cells_board[6], self.cells_board[7], self.cells_board[8]))

    def update_board(self, player, place_num):
        self.cells_board[place_num] = player

    def is_place_available(self, place_num):
        if self.cells_board[place_num] == " ":
            return True
        return False

    def check_win(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for c in winning_combinations:
            if self.cells_board[c[0]] == self.cells_board[c[1]] and self.cells_board[c[1]] == self.cells_board[c[2]] and \
                    self.cells_board[c[0]] != " ":
                return self.cells_board[c[0]]

    def is_board_full(self):
        return all(cell != " " for cell in self.cells_board)

    def get_empty_squares(self):
        return [i for i in range(9) if self.cells_board[i] == " "]


class Player:
    def __init__(self):
        self.current_player = "X"

    def switch_player(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"
        return self.current_player


class Game:
    def __init__(self):
        self.board = Board()
        self.player = Player()
        self.win = False
        self.game_modes = [self.input_from_user, self.computer_random, self.computer_smart]
        self.current_game_mode = self.input_from_user

    def input_from_user(self):
        place = int(input("%s Enter your choice from 0 to 8 --> " % self.player.current_player))
        while not self.board.is_place_available(place):
            place = int(
                input("The place is not available, %s Enter your choice from 0 to 8 --> " % self.player.current_player))
        return place

    def computer_random(self):
        place = random.randint(0, 8)
        while not self.board.is_place_available(place):
            place = random.randint(0, 8)
        return place

    def minimax(self, depth, is_maximizing):
        if self.board.check_win() == "X":
            return 1
        if self.board.check_win() == "O":
            return -1
        if self.board.is_board_full():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for move in self.board.get_empty_squares():
                self.board.cells_board[move] = "O"
                score = self.minimax(depth + 1, False)
                self.board.cells_board[move] = " "
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.board.get_empty_squares():
                self.board.cells_board[move] = "X"
                score = self.minimax(depth + 1, True)
                self.board.cells_board[move] = " "
                best_score = min(score, best_score)
            return best_score

    def computer_smart(self):
        best_score = -float('inf')
        place = None
        for move in self.board.get_empty_squares():
            self.board.cells_board[move] = 'X'
            score = self.minimax(0, False)
            self.board.cells_board[move] = ' '
            if score > best_score:
                best_score = score
                place = move
        return place

    def select_mode(self):
        self.current_game_mode = self.game_modes[
            int(input("Welcome! Select a game mode: \n0-two players\n1-random computer "
                      "\n2-smart computer \n"))]

    def play_the_game(self):
        self.board.display()
        while not self.win:
            if self.player.current_player == 'X':
                place = self.current_game_mode()
            else:
                place = self.input_from_user()
            self.board.update_board(self.player.current_player, place)
            self.board.display()
            if self.board.check_win():
                self.win = True
                print(self.player.current_player, "You Won 💃")
                break
            elif self.board.is_board_full():
                print("Tie 🤓")
            self.player.switch_player()


game = Game()
game.select_mode()
game.play_the_game()

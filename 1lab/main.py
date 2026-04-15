student = {
    "name_f": "Каушнян",
    "name_i": "Вадим",
    "name_o": "Романович",
    "group": "ПИ25-1",
}

class Chess:
    def __init__(self):
        self.board = self.create_board()
        self.turn = "white"
        self.history = [] 

    def create_board(self):
        return [
            ["r","n","b","q","k","b","n","r"],
            ["p","p","p","p","p","p","p","p"],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            ["P","P","P","P","P","P","P","P"],
            ["R","N","B","Q","K","B","N","R"]
        ]

    def print_board(self):
        print("\n  a b c d e f g h")
        for i in range(8):
            print(8 - i, end=" ")
            for j in range(8):
                print(self.board[i][j], end=" ")
            print()
        print()

    def parse_move(self, move):
        x1 = 8 - int(move[1])
        y1 = ord(move[0]) - ord('a')
        x2 = 8 - int(move[3])
        y2 = ord(move[2]) - ord('a')
        return x1, y1, x2, y2

    def move(self, move):
        try:
            x1, y1, x2, y2 = self.parse_move(move)

            piece = self.board[x1][y1]
            target = self.board[x2][y2]

            if piece == " ":
                print("Нет фигуры!")
                return

            self.history.append((x1, y1, x2, y2, piece, target))

            self.board[x1][y1] = " "
            self.board[x2][y2] = piece

            self.turn = "black" if self.turn == "white" else "white"

        except:
            print("Ошибка ввода!")

    def undo(self):
        if not self.history:
            print("Нет ходов для отмены!")
            return

        x1, y1, x2, y2, piece, target = self.history.pop()

        self.board[x1][y1] = piece
        self.board[x2][y2] = target

        self.turn = "black" if self.turn == "white" else "white"

    def start(self):
        print(f"""
Студент: {student["name_f"]} {student["name_i"]} {student["name_o"]}
Группа: {student["group"]}
        """)

        while True:
            self.print_board()
            print(f"Ход: {self.turn}")
            print("Введите ход (e2e4), 'undo' или 'exit'")

            command = input(">>> ")

            if command == "exit":
                break
            elif command == "undo":
                self.undo()
            else:
                self.move(command)


# запуск
game = Chess()
game.start()

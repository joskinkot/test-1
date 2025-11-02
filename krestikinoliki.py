print("\t\tKrustiņu-nullīšu spēle")
print ("\n1 speletajs izvelas X vai O ?")
liet_1 = input("").upper()
if liet_1 == "X":
    liet_2 = "O"
    print("Tātad 2. spēlētājs izmanto O.")
elif liet_1 == "O":
    liet_2 = "X"
    print("Tātad 2. spēlētājs izmanto X.")
else:
    print("Nepareiza izvēle! Noklusēti spēlētājs 1 būs X, spēlētājs 2 būs O.")
    
liet_1 = "X"
liet_2 = "O"
board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

def desk ():
    print("\nDesk:")
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]}")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}")
    print("\n")

def win_list(sym):
    win_list =[
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]]
    for pos in win_list:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == sym:
            return True
        return False
desk()
turn = 0

for i in range(9):
    if turn == 0:
        symbol = liet_1
        print("Spēlētājs 1 (" + symbol + ") tavs gājiens:")
    else:
        symbol = liet_2
        print("Spēlētājs 2 (" + symbol + ") tavs gājiens:")

    move = input("Izvēlies vietu (1-9): ")

    if not move.isdigit() or int(move) not in range(1,10):
        print("Nepareiza ievade! Mēģini vēlreiz.")
        continue
    
    move = int(move) - 1

    if board[move] in ["X", "O"]:
        print("Šī vieta jau ir aizņemta! Mēģini vēlreiz.")
        continue

    board[move] = symbol
    desk()

    if win_list(symbol):
        print(f"Spēlētājs {turn + 1} ({symbol}) uzvarēja!")
        break
    turn = 1 - turn
else:
        print("Neizšķirts!")
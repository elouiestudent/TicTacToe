#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6


import sys


class _GetchUnix:

    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def printBoard(board):
    print("\n".join([board[i: i + 3] for i in range(0, len(board), 3)]))


def whichMove(board):
    if len({i for i in range(len(board)) if board[i] != "."}) % 2: return "O"
    else: return "X"


def freePos(board):
    return {index for index in range(len(board)) if board[index] == "."}


def checkWin(board, winMatch, char):
    for s in winMatch:
        boardE = {board[i] for i in s}
        if "." in boardE: continue
        if len(boardE) == 1:
            if char in boardE: return {""}, {}, {}
            else: return {}, {""}, {}
    # if not pos:
    #     return {}, {}, {""}
    return {}, {}, {}


def justCheckWin(board, winMatch, char):
    for s in winMatch:
        boardE = {board[i] for i in s}
        if "." in boardE: continue
        if len(boardE) == 1:
            if char in boardE: return {""}
            else: return {}


def partitionMoves(board, winMatch):
    pos = freePos(board)
    char = whichMove(board)
    testg, testb, testt = checkWin(board, winMatch, char)
    if len(testg) or len(testb) or len(testt): return testg, testb, testt
    if not pos: return {}, {}, {""}
    good, bad, tie = set(), set(), set()
    for move in pos:
        newBoard = board[:move] + char + board[move + 1:]
        tmpGood, tmpBad, tmpTie = partitionMoves(newBoard, winMatch)
        if tmpGood: bad.add(move)
        elif tmpTie: tie.add(move)
        else: good.add(move)
    return good, bad, tie


def playGame(board, hChar):
    getch = _GetchUnix()
    winMatch = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]
    cChar = whichMove(board)
    printBoard(board)
    while freePos(board):
        # printBoard(board)
        if justCheckWin(board, winMatch, hChar): return "W"
        print()
        good, bad, tie = partitionMoves(board, winMatch)
        # print("good:", good, "bad:", bad, "tie:", tie)
        if good: place = good.pop()
        elif tie: place = tie.pop()
        else: place = bad.pop()
        # print("place:", place)
        board = board[:place] + cChar + board[place + 1:]
        printBoard(board)
        if justCheckWin(board, winMatch, cChar): return "L"
        if not freePos(board): return "T"
        print("Input an index (0-7):")
        hIndex = int(getch.__call__())
        print("Index:", hIndex)
        while board[hIndex] != ".":
            print("Not a Valid Move")
            print("Input an index (0-7):")
            hIndex = int(getch.__call__())
            print("Index:", hIndex)
        board = board[:hIndex] + hChar + board[hIndex + 1:]
        printBoard(board)


if len(sys.argv) > 1:
    board, hChar = sys.argv[1:3]
else:
    board, hChar = ".........", "O"
result = playGame(board, hChar)
if result == "W":
    print("You win. Want to play again?")
elif result == "L":
    print("You lose. Want to play again?")
else:
    print("Stalemate. Want to play again?")
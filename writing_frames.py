def other_player(p):
    if p == "x":
        return "o"
    return "x"


def winner(board):
    if board.count("_") > 4:
        return "_"
    for i in range(3):
        if board[i] == board[i + 3] and board[i] == board[i + 6]:
            return board[i]
        if board[3 * i] == board[3 * i + 1] and board[3 * i + 1] == board[3 * i + 2]:
            return board[3 * i]
    if board[0] == board[4] and board[4] == board[8]:
        return board[4]
    if board[2] == board[4] and board[4] == board[6]:
        return board[4]
    if board.count("_") == 0:
        return "d"
    return "_"


def win(board, p1):
    if board.count(p1) < 2:
        return -1
    for i in range(3):
        if sorted(board[i::3]) == ["_", p1, p1]:
            return i + 3 * board[i::3].find("_")
        if sorted(board[3 * i:3 * i + 3]) == ["_", p1, p1]:
            return 3 * i + board[3 * i:3 * i + 3].find("_")
    if sorted(board[0::4]) == ["_", p1, p1]:
        return 4 * board[0::4].find("_")
    if sorted(board[2:7:2]) == ["_", p1, p1]:
        return 2 + 2 * board[2:7:2].find("_")
    return -1


def block(board, p2):
    return win(board, p2)


def fork(board, p1, p2):
    for n, s in enumerate(board):
        if s == "_":
            b1 = board[:n] + p1 + board[n + 1:]
            i = win(b1, p1)
            if i != -1:
                if win(b1[:i] + p2 + b1[i + 1:], p1) != -1:
                    return n
    return -1

def two_in_row(board, p1):
    for n, s in enumerate(board):
        if s == "_":
            b1 = board[:n] + p1 + board[n + 1:]
            if win(b1, p1) != -1:
                return n
    return -1

def block_fork(board, p1, p2):
    if fork(board, p2, p1)==-1:
        return -1
    for n, s in enumerate(board):
        b2=board[:n] + p1 + board[n + 1:]
        if s == "_" and win(b2, p1) != -1:
            if  fork(b2, p2, p1)==-1 or fork(b2, p2, p1)!=win(b2,p1):
                return n
    return -1


def center(board):
    if board[4] == "_":
        return 4
    return -1


def opposite_corner(board, p2):
    corner = [0, 2, 6, 8]
    for i in range(4):
        if board[corner[i]] == p2 and board[corner[-i]] == "_":
            return corner[-i]
    return -1


def empty_corner(board):
    for i in [0, 2, 6, 8]:
        if board[i] == "_":
            return i
    return -1


def empty_side(board):
    for i in [1, 3, 5, 7]:
        if board[i] == "_":
            return i
    return -1


def AI_play(board, player):
    if board.count("_") == 0 or winner(board)!="_":
        return board
    p2 = other_player(player)
    play = win(board, player)
    if play == -1:
        play = block(board, p2)
    if play == -1:
        play = fork(board, player, p2)
    if play == -1:
        play = block_fork(board, player, p2)
    if play == -1:
        if board.count("_") == 9:
            play = 0
        else:
            play = center(board)
    if play == -1:
        play = two_in_row(board, player)
    if play == -1:
        play = opposite_corner(board, p2)
    if play == -1:
        play = empty_corner(board)
    if play == -1:
        play = empty_side(board)
    return board[:play] + player + board[play + 1:]


def print_board(board):
    b = board.replace("_", " ")
    print b[0] + " | " + b[1] + " | " + b[2] + "     " + "1 | 2 | 3"
    print "---------" + "     " + "---------"
    print b[3] + " | " + b[4] + " | " + b[5] + "     " + "4 | 5 | 6"
    print "---------" + "     " + "---------"
    print b[6] + " | " + b[7] + " | " + b[8] + "     " + "7 | 8 | 9"


def interactive_play(board, player):
    while 1:
        if player == "o":
            board = AI_play(board, player)
            player = other_player(player)

        print_board(board)

        if winner(board) == "_":
            print "Enter next move for " + player + ":"
            try:
                play = int(raw_input()) - 1
                if board[play] == "_":
                    board = board[:play] + player + board[play + 1:]
                    player = other_player(player)
            except (ValueError, IndexError):
                print "Please write a number between 1 and 9"
        elif winner(board) == "d":
            print "Draw!"
            break
        else:
            print winner(board) + " wins!"
            break

def write_frame(board, player):
    f.write("\\begin{frame}\n\\label{"+board+"}\n\\begin{figure}\n\\centering\n")
    for i in range(9):
        if board[i]=="_":
            if winner(board)=="_":
                b = AI_play(board[:i]+player+board[i + 1:],other_player(player))
                f.write("\\drawbl{"+b+"} ")
            else:
                f.write("\\drawb")
        else:
            f.write("\\draw"+ board[i] + " ")
        if i%3!=2:
            f.write("\\hspace{0.02cm} ")
        if i==2 or i==5:
            f.write("\\vspace{0.15cm} \\\\\n")
    f.write("\n\\end{figure}\n")
    if winner(board)==other_player(player):
        f.write("\\lose\n")
    if winner(board)=="d":
        f.write("\\draw\n")
    f.write("\\end{frame}\n\n")

def full_play(games, board, player):
    if board not in games:
        write_frame(board, player)
        games += [board]
    if winner(board) == "_":
        for i in range(9):
            b=board[:i] + player + board[i + 1:]
            if board[i] == "_":
                full_play(games, AI_play(b, other_player(player)), player)
    return games

f=open("LaTeX/frames.tex","w")
games = []
full_play(games, "_________", "x")
full_play(games, "x________", "o")
f.close()

#interactive_play(9 * "_", "x")

# Total number of games
print len(games), len(set(games))

# Games finishing in a draw
finished_games = []
for game in games:
    if winner(game) == "d":
        finished_games += [game]

print len(finished_games)
print len(set(finished_games))
for b in set(finished_games):
    print_board(b)
    print ""

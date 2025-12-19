# type:ignore
import chess
import random
import datetime
import math
import csv

# To DO: add old chess moves in ass a database that the chess bot looks at before minimax

def startingMov():
    # itnitializing the dictionary here 
    # keys would be the fen strings themselves
    # constant time lookup
    # check database for
    # supply database in FEN notation
    # lookup of current Fen notation
    # fetch value which would be corresponsifn move
    # then play that move or use minimax if no key found
    # if state exists or player that did that move lost would do mini max
    # two databases 
   
       
    # First steps 
    
    pass 
    
def getEval(captured_piece:chess.Piece|None) -> int:

    if (captured_piece == None):
        return 0
    else:
        if captured_piece.piece_type == chess.PAWN:
        if captured_piece.piece_type == chess.PAWN:
            return 1
        elif captured_piece.piece_type == chess.KNIGHT:
        elif captured_piece.piece_type == chess.KNIGHT:
            return 3
        elif captured_piece.piece_type == chess.BISHOP:
        elif captured_piece.piece_type == chess.BISHOP:
            return 3
        elif captured_piece.piece_type == chess.ROOK:
        elif captured_piece.piece_type == chess.ROOK:
            return 5
        elif captured_piece.piece_type == chess.QUEEN:
        elif captured_piece.piece_type == chess.QUEEN:
            return 9
        else:
            return 0


def min(board:chess.Board, rec_depth:int) -> tuple[float,list[chess.Move]]:
def min(board:chess.Board, rec_depth:int) -> tuple[float,list[chess.Move]]:
    moveList = list(board.legal_moves)
    opp_best_score = +math.inf
    opp_best_moves = []

    for move in moveList:
        baseBoard = chess.BaseBoard(board.board_fen())
        baseBoard = chess.BaseBoard(board.board_fen())
        move_piece = baseBoard.piece_at(move.to_square)
        opp_move_score = -getEval(move_piece)

        if rec_depth == 0:
            return -getEval(move_piece), [move]
        
        board.push(move)

        player_score, player_moves = max(board, rec_depth - 1)

        score = opp_move_score - player_score

        if score < opp_best_score:
            opp_best_score = score
            opp_best_moves = [move]
        elif score == opp_best_score:
            opp_best_moves.append(move)  

        board.pop()
        
    return opp_best_score, opp_best_moves


def max(board:chess.Board, rec_depth:int) -> tuple[float,list[chess.Move]]:
def max(board:chess.Board, rec_depth:int) -> tuple[float,list[chess.Move]]:
    best_moves = []
    moveList = list(board.legal_moves)
    best_score = -math.inf

    for move in moveList:
        baseBoard = chess.BaseBoard(board.board_fen())
        baseBoard = chess.BaseBoard(board.board_fen())
        move_piece = baseBoard.piece_at(move.to_square)
        player_move_score = getEval(move_piece)
        if rec_depth == 0:
            return getEval(move_piece), [move]
        
        board.push(move)
        
        opp_score, opp_move = min(board, rec_depth - 1)

        score = player_move_score + opp_score
    
        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move) 
    
        board.pop()
    return best_score, best_moves

def main () -> None:
    white_move_count = 0
    black_move_count = 0
    

    FEN_moves:dict[str, str] = {}

    with open('chessMoves.csv', mode='r') as data_file:
        data_reader = csv.DictReader(data_file)

        for row in data_reader:
            # neighbors_list = [neighbor.strip() for neighbor in row['NEIGHBORS'].split(",")]
            FEN_moves[row["FEN"]] = row["Next move"]

    # for i in range(5):
    print(FEN_moves.keys())


    print("="*33)
    print(f"\tWelcome to Chess!")
    print("="*33)
    print(f"Time: {datetime.datetime.now()}")
    movecount = 0

    botColor = input("Computer player? (w=white/b=black): ")
    
    startingFEN = input("Starting FEN position? (hit ENTER for standard starting postion): ")
    board = None
    if (startingFEN == ""):
        board = chess.Board()
        board = chess.Board()
    else:
        board = chess.Board(startingFEN)
        board = chess.Board(startingFEN)
    
    botName = ""
    playerName = "" 
    
    if (botColor == "w"):
       botColor = chess.WHITE
       botColor = chess.WHITE
       botName = "Bot (as white)"
       playerName = "Black"
    elif (botColor == "b"):
        botColor = chess.BLACK
        botColor = chess.BLACK
        botName = "Bot (as black)"
        playerName = "White"

    print("Printing Initial Board......")
    print(board)
    print("-----------------")
    while not board.is_game_over() :
        if (board.turn == botColor):
            best_moves = []
            best_move = None
            best_score = 0
            
            # check ig counnt AND color are both white 
            if botColor == chess.WHITE and white_move_count == 0:
                # king pawn opening (e2-e4)
                opening_move = chess.Move.from_uci("e2e4")
                if opening_move in board.legal_moves:
                    best_move = opening_move
                    print(f"{botName}: {best_move} (Opening move)")
            elif botColor == chess.BLACK and black_move_count == 0:
                opening_move = chess.Move.from_uci("e7e5")
                if opening_move in board.legal_moves:
                    best_move = opening_move
                    print(f"{botName}: {best_move} (Opening move)")
            
            # if no opening move, use minimax
            if best_move is None:
                best_score, best_moves = max(board, 3)
                
                if len(best_moves) != 0:
                    best_move = best_moves[random.randint(0, len(best_moves) - 1)]
                    print(f"{botName}: {best_move}")
                else:
                    print("Error: Minimax returning no moves.")
                    break
            
            board.push(best_move)
            
            # add to counter
            if botColor == chess.WHITE:
                white_move_count += 1
            else:
                black_move_count += 1
                
            print(f"New FEN position: {board.fen()}")

        else:
            moveList = list(board.legal_moves)

            playerInput = input(f"{playerName}: ")
            
            playerMove = None

            try:
                playerMove = chess.Move.from_uci(playerInput)
                playerMove = chess.Move.from_uci(playerInput)
            except:
                print("Make sure your input is in UCI format!")
                playerInput = input(f"{playerName}: ")

            if playerMove not in moveList:
                print("That move is not legal! Try again?")
            else:
                board.push(playerMove)
                
                # add to counter 
                if board.turn == chess.WHITE:
                    black_move_count += 1
                else:
                    white_move_count += 1
                    
                print(f"New FEN position: {board.fen()}")
        print(board)

        f = open("gameFen.txt", "w")
        f.write(f"Last Fen: {board.fen()}")

    print("-----------------")
    print(f"Game Result: {board.result()}")
    print(board)

    board.reset()


if __name__ == "__main__":
    main()
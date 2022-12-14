import chess.engine
import chess.pgn
import chess
import csv
import os

def display_board():
    for i, row in enumerate(board.unicode(invert_color=True).split("\n")):
        print(f"{8-i} {row}")
    print("  a b c d e f g h")
    print()

engine = chess.engine.SimpleEngine.popen_uci("Games/stockfish-windows-2022-x86-64-avx2")
directory = os.fsencode(r"Games")
directories = os.listdir(directory)
directories.reverse()

for collection in directories:
    filename = os.fsdecode(collection)
    pgn = open(filename)

    games = []
    i = 0
    
    for game in pgn:
        with open(r"neural_net\Players\mtcs_engine\sample_fen.csv", "w", newline='') as f:
            writer = csv.writer(f)
            current_game = chess.pgn.read_game(pgn)
            # Convert the game to a chess.board object
            board = chess.Board()
            
            # Iterate through all moves and play them on a board.
            for move in current_game.mainline_moves():
                board.push(move)
            games.append(board) 

            # Write the fen and winner to a csv file
            try:
                for i in range(100):
                    board.pop()
                    fen = board.fen()
                    score = engine.analyse(board, chess.engine.Limit(depth=20))["score"].white().score()
                    if fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1":
                        print(f"Game {i} saved")
                        break
                    writer.writerow([fen, score])
            except IndexError:
                pass
        i += 1
    print(f"File {filename} finished")
print("Finished")
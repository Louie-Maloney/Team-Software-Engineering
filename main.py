from puzzle import Puzzle
import json

with open('puzzles.json', 'r') as f:
    puzzles_json = json.load(f)
    puzzles = puzzles_json['puzzles']

p = Puzzle(puzzles[0])
p.print_puzzle_info()
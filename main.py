from puzzle import Puzzle
import json
from colorama import Fore, Style, init

init()

def title_screen():
    screen = f"""
    {Fore.LIGHTBLACK_EX}-----------------------------
    {Fore.LIGHTGREEN_EX}Computer Science Escape Room 
    {Fore.LIGHTBLACK_EX}-----------------------------
    
    {Fore.LIGHTYELLOW_EX}  Press enter to begin...{Style.RESET_ALL}"""
    
    input(screen)


with open('puzzles.json', 'r') as f:
    puzzles_json = json.load(f)
    puzzles = puzzles_json['puzzles']

p = Puzzle(puzzles[0])
p.print_puzzle_info()

    
title_screen()
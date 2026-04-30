from puzzle import Puzzle
import json
from colorama import Fore, Style, init
from puzzles import load_puzzle

init()

def title_screen():
    screen = f"""
    {Fore.LIGHTBLACK_EX}-----------------------------
    {Fore.LIGHTGREEN_EX}Computer Science Escape Room 
    {Fore.LIGHTBLACK_EX}-----------------------------
    
    {Fore.LIGHTYELLOW_EX}  Press enter to begin...{Style.RESET_ALL}
    """
    
    input(screen)

def load_puzzles():
    with open('puzzles.json', 'r') as f:
        puzzles_json = json.load(f)
        return puzzles_json['puzzles']

def play(p: Puzzle):
    p.display()
    while not p.solved:
        text_input = input(f"> ")
        if not text_input:
            continue
        
        result = p.handle_command(text_input)
        if result == 'quit':
            return 'quit'
        if result == 'solved':
            return 'solved'
        if result == 'continue':
            continue
        if result == 'wrong':
            continue
        

puzzles = load_puzzles()

def main():
    title_screen()
    for i, config in enumerate(puzzles):
        p = load_puzzle(config)  
        print("")
        play(p)
  
if __name__ == "__main__":
    main()
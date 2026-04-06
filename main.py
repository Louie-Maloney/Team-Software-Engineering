from puzzle import Puzzle
import json
from colorama import Fore, Style, init

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


puzzles = load_puzzles()

p = Puzzle(puzzles[0])
p.print_puzzle_info()

title_screen()


# uncomment below when actually doign proper runs, no point rn when still early dev

# def main():
#     title_screen()
    
# if __name__ == "__main__":
#     main()
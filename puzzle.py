
class Puzzle():
    def __init__(self, config):
        self.title = config['title']
        self.difficulty = config['difficulty']
        self.data = config['data']
        self.hints = config['hints']
        self.solved = False
        self.hints_used = 0
    
    # this function will be removed in future, just for debug rn
    def print_puzzle_info(self):
        print(f'title: {self.title}')
        print(f'difficulty: {self.difficulty}')
        print(f'data: {self.data}')
        print(f'hints: {self.hints}')
        print(f'solved: {self.solved}')

    def show_hint(self):
        if self.hints_used < len(self.hints):
            hint = self.hints[self.hints_used]
            self.hints_used += 1
            print(f"hint: {hint}")
        else:
            print("out of hints")
        
        
    # display and check_input will be overridden, just more in here 
    # so there is fallback incase forget to include in puzzles.py override
    def display(self):
        print("no display implemented yet for this puzzle")
    
    def check_input(self):
        print("no input checking added for this puzzle yet")
            
    
    # todo --> make function to display the puzzle (have this in the json or hardcode them in seperate puzzle handling?)
    
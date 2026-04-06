
class Puzzle():
    def __init__(self, config):
        self.title = config['title']
        self.difficulty = config['difficulty']
        self.data = config['data']
        self.hints = config['hints']
        self.solved = False
    
    def print_puzzle_info(self):
        print(f'title: {self.title}')
        print(f'difficulty: {self.difficulty}')
        print(f'data: {self.data}')
        print(f'hints: {self.hints}')
        print(f'solved: {self.solved}')

    # todo -->  make generic functions to interact with puzzles
    #           make function to display the puzzle
    #           make function to give hint to person
    
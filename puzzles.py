from puzzle import Puzzle
from colorama import Fore, Style

class BinaryPuzzle(Puzzle):
    def check_input(self, input):
        if input.upper() == self.data['solution'].upper():
            print("correct answer!")
            return True
        print("incorrect answer, try again.")
        return False
    
def load_puzzle(config):
    if config['type'] == 'binary':
        return BinaryPuzzle(config)
    elif config['type'] == 'something else': # future handling for diff puzzle types
        pass
    else:
        return Puzzle(config) # worst case something fucks up
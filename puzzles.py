from puzzle import Puzzle
from colorama import Fore, Style

class BinaryPuzzle(Puzzle):
    
    
    def check_input(self, input):
        # Input validation: must be a non-empty string, only alphabetic characters allowed
        if not isinstance(input, str) or not input.strip():
            print("Input cannot be empty. Please enter your answer.")
            return False
        if not input.isalpha():
            print("Input must only contain letters (A-Z). Try again.")
            return False
        if input.upper() == self.data['solution'].upper():
            print("correct answer!")
            return True
        print("incorrect answer, try again.")
        return False


class CaesarPuzzle(Puzzle):
    # override help to show the DECODE command specific to this puzzle
    def help(self):
        print("commands: HELP, LOOK, EXAMINE <TARGET>, HINT, DECODE <MESSAGE> <SHIFT>, QUIT")

    def caesar_decode(self, text, shift):
        # loop over each character and shift it back in the alphabet
        result = []
        for char in text.upper():
            if char.isalpha():
                # shift back by subtracting shift, wrap around with modulo 26
                decoded = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                result.append(decoded)
            else:
                # non-letter characters (spaces, punctuation) are kept as-is
                result.append(char)
        return ''.join(result)

    def handle_command(self, input):
        command = input.split(None, 1)
        action = command[0].lower()

        if action == 'decode':
            if len(command) > 1:
                # split from the right once to separate the shift number from the message
                parts = command[1].rsplit(None, 1)
                if len(parts) == 2:
                    message = parts[0]
                    shift_str = parts[1]
                    if not shift_str.isdigit():
                        print("Shift value must be a number. Usage: DECODE <message> <shift>")
                        return 'continue'
                    try:
                        shift = int(shift_str)
                        if shift < 0 or shift > 25:
                            print("Shift must be between 0 and 25.")
                            return 'continue'
                        decoded = self.caesar_decode(message, shift)
                        print(f"Output: {decoded}")
                        if decoded.upper() == self.data['solution'].upper():
                            print("Correct! The cipher is broken!")
                            self.solved = True
                            return 'solved'
                        else:
                            print("That doesn't seem right. Try a different shift.")
                            return 'wrong'
                    except ValueError:
                        print("Invalid shift value. Usage: DECODE <message> <shift>")
                        return 'continue'
                else:
                    print("Usage: DECODE <message> <shift>")
                    return 'continue'
            else:
                print("Usage: DECODE <message> <shift>")
                return 'continue'
        else:
            # anything not DECODE falls through to the base class handler
            return super().handle_command(input)

    def display(self):
        print(f"puzzle: {self.title}")
        print(f"difficulty: {self.difficulty}")
        self.look()
        self.help()
        # show the encoded message and dial setting as a reminder at the start
        print(f"\nEncoded message: {self.data['encoded']}")
        print(f"Dial set to: {self.data['shift']}")


class PatternPuzzle(Puzzle):
    def __init__(self, config):
        super().__init__(config)
        self.current_round = 0  # tracks which of the three locks the player is on
        self.rounds = self.data['rounds']

    # override help to show the ENTER command specific to this puzzle
    def help(self):
        print("commands: HELP, LOOK, EXAMINE <TARGET>, HINT, ENTER <NUMBER>, QUIT")

    def display_current_sequence(self):
        # shows the sequence for whichever lock the player is currently solving
        if self.current_round < len(self.rounds):
            round_data = self.rounds[self.current_round]
            seq = ', '.join(str(n) for n in round_data['sequence'])
            print(f"\nLock {self.current_round + 1} of {len(self.rounds)}: [LOCKED]")
            print(f"Sequence: {seq}, ?")

    def display(self):
        print(f"puzzle: {self.title}")
        print(f"difficulty: {self.difficulty}")
        self.look()
        self.help()
        self.display_current_sequence()

    def handle_command(self, input):
        command = input.split(None, 1)
        action = command[0].lower()

        if action == 'enter':
            if len(command) > 1:
                try:
                    number = int(command[1].strip())
                    return self.check_answer(number)
                except ValueError:
                    print("Please enter a valid number.")
                    return 'continue'
            else:
                print("Usage: ENTER <number>")
                return 'continue'
        else:
            # anything not ENTER falls through to the base class handler
            return super().handle_command(input)

    def check_answer(self, number):
        round_data = self.rounds[self.current_round]
        if number == round_data['answer']:
            print(f"Correct! {round_data['explanation']}")
            print(f"Lock {self.current_round + 1}: [OPEN]")
            self.current_round += 1
            # check if all three locks are now open
            if self.current_round >= len(self.rounds):
                print("All locks open! The cabinet swings open.")
                self.solved = True
                return 'solved'
            else:
                # show the next sequence for the player
                self.display_current_sequence()
                return 'continue'
        else:
            print("Incorrect. Try again.")
            return 'wrong'

    def check_input(self, input):
        # fallback in case someone types a bare number without ENTER
        if not isinstance(input, str) or not input.strip():
            print("Input cannot be empty. Please enter a number.")
            return False
        try:
            number = int(input.strip())
            return self.check_answer(number) == 'solved'
        except ValueError:
            print("Please enter a valid integer number.")
            return False

class BooleanPuzzle(Puzzle):
    def __init__(self, config):
        super().__init__(config)
        self.switches = dict(config['data']['switches'])  # copy so we don't mutate config
        self.expression = config['data']['expression']

    def help(self):
        print("commands: HELP, LOOK, EXAMINE <TARGET>, FLIP <SWITCH>, RESET, HINT, QUIT")

    def evaluate(self):
        s = self.switches
        return (s['A'] and s['B']) or (not s['C'] and s['D'])

    def display_switches(self):
        header = "+---" * len(self.switches) + "+"
        labels = "| " + " | ".join(self.switches.keys()) + " |"
        values = "| " + " | ".join(str(v) for v in self.switches.values()) + " |"
        result = self.evaluate()
        print(f"\nExpression: {self.expression}")
        print(header)
        print(labels)
        print(values)
        print(header)
        if result:
            print(f"Result: {Fore.GREEN}TRUE   [UNLOCKED!]{Style.RESET_ALL}\n")
        else:
            print(f"Result: {Fore.RED}FALSE  [LOCKED]{Style.RESET_ALL}\n")

    def display(self):
        print(f"puzzle: {self.title}")
        print(f"difficulty: {self.difficulty}")
        self.look()
        self.help()
        self.display_switches()

    def handle_command(self, input):
        command = input.split(None, 1)
        action = command[0].lower()

        if action == 'flip':
            if len(command) > 1:
                key = command[1].strip().upper()
                if key in self.switches:
                    self.switches[key] ^= 1  # toggle
                    print(f"Switch {key} → {self.switches[key]}")
                    self.display_switches()
                    if self.evaluate():
                        print("The light turns GREEN. The door clicks open!")
                        self.solved = True
                        print(" ")
                        print(" ")
                        return 'solved'
                    return 'continue'

                else:
                    print(f"No switch '{key}'. Valid switches: {', '.join(self.switches.keys())}")
                    return 'continue'
            else:
                print("Usage: FLIP <switch>  e.g. FLIP A")
                return 'continue'

        elif action == 'reset':
            for k in self.switches:
                self.switches[k] = 0
            print("All switches reset to 0.")
            self.display_switches()
            return 'continue'

        else:
            return super().handle_command(input)

class RobotPuzzle(Puzzle):
    def help(self):
        print("commands: HELP, LOOK, PROGRAM <commands>, QUIT")

    def handle_command(self, input):
        parts = input.split(None, 1)

        if parts[0].lower() == "program":
            if len(parts) < 2:
                print("Usage: PROGRAM MOVE, MOVE, RIGHT...")
                return 'continue'

            commands = [c.strip().upper() for c in parts[1].split(",")]

            if commands == self.data['correct_path']:
                print("Robot reached the exit successfully!")
                self.solved = True
                return 'solved'
            else:
                print("Robot crashed into a wall. Try again.")
                return 'wrong'

        return super().handle_command(input)

def load_puzzle(config):
    if config['type'] == 'binary':
        return BinaryPuzzle(config)
    elif config['type'] == 'boolean':
        return BooleanPuzzle(config)
    elif config['type'] == 'caesar':
        return CaesarPuzzle(config)
    elif config['type'] == 'pattern':
        return PatternPuzzle(config)
    elif config['type'] == 'robot':
        return RobotPuzzle(config)
    else:
        return Puzzle(config) # worst case something fucks up

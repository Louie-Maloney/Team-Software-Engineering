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

class ParityPuzzle(Puzzle):
    def __init__(self, config):
        super().__init__(config)

        # 4x4 grid with one wrong bit
        self.grid = [
            [1, 0, 1, 1],
            [0, 1, 0, 1],  # this row has wrong parity
            [1, 1, 0, 0],
            [0, 0, 1, 1]
        ]

        # parity bits (even parity expected)
        self.row_parity = [1, 0, 0, 0]
        self.col_parity = [0, 0, 0, 1]

    # Display
    def display_grid(self):
        print("\n     C1 C2 C3 C4  P")
        for i, row in enumerate(self.grid):
            row_values = "  ".join(str(x) for x in row)
            print(f"R{i+1}: {row_values} [{self.row_parity[i]}]")

        col_parity_str = "".join(f"[{x}]" for x in self.col_parity)
        print(f" P: {col_parity_str}\n")

    def display(self):
        print(f"puzzle: {self.title}")
        print(f"difficulty: {self.difficulty}")
        self.look()
        self.help()
        self.display_grid()

    # Help
    def help(self):
        print("commands: HELP, CHECK ROW <n>, CHECK COL <n>, FIX ROW <r> COL <c>, QUIT")

    # Parity check
    def is_even(self, values):
        return sum(values) % 2 == 0

    def check_row(self, r):
        row = self.grid[r]
        total = sum(row) + self.row_parity[r]

        if total % 2 == 0:
            print(f"Row {r+1} parity: PASS")
            return True
        else:
            print(f"Row {r+1} parity: FAIL")
            return False

    def check_col(self, c):
        col = [self.grid[r][c] for r in range(4)]
        total = sum(col) + self.col_parity[c]

        if total % 2 == 0:
            print(f"Column {c+1} parity: PASS")
            return True
        else:
            print(f"Column {c+1} parity: FAIL")
            return False

    # Error fix
    def fix(self, r, c):
        # flip the bit
        self.grid[r][c] ^= 1
        print(f"Fixed bit at Row {r+1}, Column {c+1}")
        self.display_grid()

        # check if all rows & columns now valid
        all_rows = all(self.check_row(i) for i in range(4))
        all_cols = all(self.check_col(i) for i in range(4))

        if all_rows and all_cols:
            print("\nAll parity checks pass!")
            print("The corrupted file has been repaired.")
            print("Parity checking ensures data integrity in real-world systems.\n")
            self.solved = True
            return 'solved'

        return 'continue'

    # Command handler
    def handle_command(self, input):
        command = input.split()

        if not command:
            return 'continue'

        action = command[0].lower()

        try:
            if action == 'check':
                if command[1].lower() == 'row':
                    r = int(command[2]) - 1
                    self.check_row(r)
                elif command[1].lower() == 'col':
                    c = int(command[2]) - 1
                    self.check_col(c)
                return 'continue'

            elif action == 'fix':
                r = int(command[2]) - 1
                c = int(command[4]) - 1
                return self.fix(r, c)

            elif action == 'help':
                self.help()
                return 'continue'

            elif action == 'quit':
                return 'quit'

            else:
                print("Invalid command. Type HELP.")
                return 'continue'

        except (IndexError, ValueError):
            print("Invalid format. Try: CHECK ROW 2 or FIX ROW 2 COL 3")
            return 'continue'
class RobotPuzzle(Puzzle):
    DIRECTIONS = ['NORTH', 'EAST', 'SOUTH', 'WEST']
    DELTA = {'NORTH': (-1, 0), 'EAST': (0, 1), 'SOUTH': (1, 0), 'WEST': (0, -1)}
    DIR_ARROW = {'NORTH': '^', 'EAST': '>', 'SOUTH': 'v', 'WEST': '<'}

    def __init__(self, config):
        super().__init__(config)
        self.grid = config['data']['grid']
        self.start = tuple(config['data']['start'])
        self.exit_pos = tuple(config['data']['exit'])

    def help(self):
        print("commands: HELP, LOOK, EXAMINE <TARGET>, HINT, PROGRAM <cmds>, QUIT")
        print("  valid moves: MOVE  |  TURN LEFT  |  TURN RIGHT")
        print("  example: PROGRAM MOVE, TURN RIGHT, MOVE, MOVE")

    def _draw_grid(self, pos, direction):
        cols = len(self.grid[0])
        divider = '+' + '---+' * cols
        print(divider)
        for r, row in enumerate(self.grid):
            cells = ''
            for c, cell in enumerate(row):
                if (r, c) == pos:
                    cells += f' {self.DIR_ARROW[direction]} |'
                elif (r, c) == self.exit_pos:
                    cells += ' X |'
                elif cell == 1:
                    cells += ' # |'
                else:
                    cells += '   |'
            print('|' + cells)
            print(divider)
        print(f"  {self.DIR_ARROW[direction]} = Robot ({direction})  X = Exit  # = Wall\n")

    def display(self):
        print(f"puzzle: {self.title}")
        print(f"difficulty: {self.difficulty}")
        self.look()
        self.help()
        print()
        self._draw_grid(self.start, self.data['start_direction'])

    def _simulate(self, commands):
        pos = self.start
        direction = self.data['start_direction']
        rows = len(self.grid)
        cols = len(self.grid[0])

        for step, cmd in enumerate(commands, 1):
            if cmd == 'MOVE':
                dr, dc = self.DELTA[direction]
                nr, nc = pos[0] + dr, pos[1] + dc
                if not (0 <= nr < rows and 0 <= nc < cols) or self.grid[nr][nc] == 1:
                    return 'crash', pos, direction, step
                pos = (nr, nc)
                if pos == self.exit_pos:
                    return 'exit', pos, direction, step
            elif cmd in ('TURN LEFT', 'TURN RIGHT'):
                idx = self.DIRECTIONS.index(direction)
                delta = 1 if cmd == 'TURN RIGHT' else -1
                direction = self.DIRECTIONS[(idx + delta) % 4]
            else:
                return 'invalid', pos, direction, step

        return 'stopped', pos, direction, len(commands)

    def handle_command(self, inp):
        parts = inp.split(None, 1)
        action = parts[0].lower()

        if action == 'program':
            if len(parts) < 2:
                print("Usage: PROGRAM MOVE, TURN RIGHT, MOVE, ...")
                return 'continue'

            cmd_str = parts[1].lstrip(':').strip()
            commands = [c.strip().upper() for c in cmd_str.split(',')]

            result, final_pos, final_dir, steps = self._simulate(commands)
            self._draw_grid(final_pos, final_dir)

            if result == 'exit':
                print(f"Robot reached the exit in {steps} command(s)!")
                self.solved = True
                return 'solved'
            elif result == 'crash':
                print(f"Robot crashed at step {steps} — hit a wall or boundary. Try again.")
                return 'wrong'
            elif result == 'invalid':
                print(f"Unknown command at step {steps}. Valid: MOVE, TURN LEFT, TURN RIGHT")
                return 'continue'
            else:
                print(f"Program finished but robot is at row {final_pos[0]+1}, col {final_pos[1]+1} — exit not reached.")
                return 'wrong'

        return super().handle_command(inp)

class BookshelfPuzzle(Puzzle):
    OPTIMAL_SWAPS = 9  # minimum bubble-sort swaps for [8,3,5,1,9,2]

    def __init__(self, config):
        super().__init__(config)
        self.books = list(config['data']['initial'])
        self.solution = config['data']['solution']
        self.swap_count = 0

    def help(self):
        print("commands: HELP, LOOK, EXAMINE <TARGET>, HINT, SWAP <n> <m>, QUIT")
        print("  (SWAP uses position 1-6, not the number on the book)")

    def display_shelf(self):
        print("   " + " ".join(f"[{b}]" for b in self.books))
        print("    |   |   |   |   |   |")
        print("   =========================")
        print("   |       BOOKSHELF       |")
        print("   =========================")
        print(f"   Swaps: {self.swap_count}")

    def display(self):
        print(f"puzzle: {self.title}")
        print(f"difficulty: {self.difficulty}")
        self.look()
        self.help()
        self.display_shelf()

    def handle_command(self, input):
        parts = input.split()
        if parts and parts[0].lower() == 'swap':
            if len(parts) == 3:
                try:
                    pos1 = int(parts[1])
                    pos2 = int(parts[2])
                except ValueError:
                    print("Book positions must be numbers. Usage: SWAP <n> <m>")
                    return 'continue'

                n = len(self.books)
                if not (1 <= pos1 <= n and 1 <= pos2 <= n):
                    print(f"Book positions must be between 1 and {n}.")
                    return 'continue'
                if abs(pos1 - pos2) != 1:
                    print("You can only swap neighbouring books (bubble sort rule).")
                    return 'continue'

                i, j = pos1 - 1, pos2 - 1
                self.books[i], self.books[j] = self.books[j], self.books[i]
                self.swap_count += 1
                self.display_shelf()

                if self.books == self.solution:
                    print("\nThe bookshelf slides aside — a hidden door is revealed!")
                    print(f"You solved it in {self.swap_count} swap(s). Optimal bubble sort: {self.OPTIMAL_SWAPS}.")
                    self.solved = True
                    return 'solved'
                return 'continue'
            else:
                print("Usage: SWAP <n> <m>  e.g. SWAP 1 2")
                return 'continue'
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
    elif config['type'] == 'parity':
        return ParityPuzzle(config)
    elif config['type'] == 'robot':
        return RobotPuzzle(config)
    elif config['type'] == 'bookshelf':
        return BookshelfPuzzle(config)
    else:
        return Puzzle(config) # worst case if errors

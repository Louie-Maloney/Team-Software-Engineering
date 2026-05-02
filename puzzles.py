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
        print("commands: HELP, LOOK, EXAMINE <TARGET>, HINT, DECODE <MESSAGE> <SHIFT>, SKIP")

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
        self.display_short_desc()
        self.look()
        self.help()
        print(f"\nEncoded message: {self.data['encoded']}")
        print(f"Dial set to: {self.data['shift']}")


class PatternPuzzle(Puzzle):
    def __init__(self, config):
        super().__init__(config)
        self.current_round = 0  # tracks which of the three locks the player is on
        self.rounds = self.data['rounds']

    # override help to show the ENTER command specific to this puzzle
    def help(self):
        print("commands: HELP, LOOK, EXAMINE <TARGET>, HINT, ENTER <NUMBER>, SKIP")

    def display_current_sequence(self):
        # shows the sequence for whichever lock the player is currently solving
        if self.current_round < len(self.rounds):
            round_data = self.rounds[self.current_round]
            seq = ', '.join(str(n) for n in round_data['sequence'])
            print(f"\nLock {self.current_round + 1} of {len(self.rounds)}: [LOCKED]")
            print(f"Sequence: {seq}, ?")

    def display(self):
        self.display_short_desc()
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
        print("commands: HELP, LOOK, EXAMINE <TARGET>, FLIP <SWITCH>, RESET, HINT, SKIP")

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
        self.display_short_desc()
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

from collections import deque

class GraphPuzzle(Puzzle):
    def __init__(self, config):
        super().__init__(config)
        self.graph = config['data']['graph']
        self.start = config['data']['start']
        self.exit = config['data']['exit']
        self.current = self.start
        self.path = [self.start]  # tracks the player's full route

    def help(self):
        print("commands: HELP, LOOK, EXAMINE <TARGET>, MOVE <NODE>, BACK, PATH, HINT, SKIP")

    def bfs_shortest_path(self):
        # BFS to find the shortest path from start to exit
        queue = deque([[self.start]])
        visited = {self.start}

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node == self.exit:
                return path

            for neighbour in self.graph.get(node, []):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(path + [neighbour])

        return None  # no path found

    def look(self):
        # override look to show current node and connections instead of room items
        connections = self.graph.get(self.current, [])
        print(f"\nYou are at node [{self.current}].")
        print(f"Connected tunnels lead to: {', '.join(f'[{n}]' for n in connections)}")
        if self.current == self.start:
            print("(This is where you started.)")

    def display(self):
        print(f"puzzle: {self.title}")
        print(f"difficulty: {self.difficulty}")
        print(f"\n{self.room_description}")
        print("\nItems in the room:")
        for item in self.items:
            print(f"  {item}: {self.items[item]['description']}")
        self.help()
        self.look()

    def handle_command(self, input):
        command = input.split(None, 1)
        action = command[0].lower()

        if action == 'move':
            if len(command) > 1:
                target = command[1].strip().upper()
                return self.move(target)
            else:
                print("Usage: MOVE <node>  e.g. MOVE B")
                return 'continue'

        elif action == 'back':
            return self.go_back()

        elif action == 'path':
            print(f"Your route so far: {' -> '.join(self.path)}")
            return 'continue'

        elif action == 'look':
            self.look()
            return 'continue'

        else:
            return super().handle_command(input)

    def move(self, target):
        connections = self.graph.get(self.current, [])

        if target not in self.graph:
            print(f"[{target}] doesn't exist on the map.")
            return 'continue'

        if target not in connections:
            print(f"There's no tunnel from [{self.current}] to [{target}]. Check the map.")
            return 'continue'

        self.current = target
        self.path.append(target)
        print(f"You move through the tunnel to [{target}].")

        if self.current == self.exit:
            return self.on_exit_reached()

        self.look()
        return 'continue'

    def go_back(self):
        if len(self.path) <= 1:
            print("You're at the start — nowhere to go back to.")
            return 'continue'

        self.path.pop()
        self.current = self.path[-1]
        print(f"You backtrack to [{self.current}].")
        self.look()
        return 'continue'

    def on_exit_reached(self):
        player_steps = len(self.path) - 1  # steps = nodes visited minus start
        optimal = self.bfs_shortest_path()
        optimal_steps = len(optimal) - 1

        print(f"\nYou found the exit!")
        print(f"\nYour route:   {' -> '.join(self.path)} ({player_steps} steps)")
        print(f"Optimal path: {' -> '.join(optimal)} ({optimal_steps} steps)")

        if player_steps == optimal_steps:
            print("\nThat was the shortest possible path. Perfect!")
        else:
            extra = player_steps - optimal_steps
            print(f"\nYou took {extra} extra step{'s' if extra != 1 else ''}.")
            print("The optimal route uses BFS — exploring all neighbours at the current")
            print("distance before going deeper, guaranteeing the shortest path in an")
            print("unweighted graph.")

        self.solved = True
        return 'solved'


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
        self.row_parity = [1, 1, 0, 0]
        self.col_parity = [0, 0, 1, 1]

    # Display
    def display_grid(self):
        print("\n     C1 C2 C3 C4  P")
        for i, row in enumerate(self.grid):
            row_values = "  ".join(str(x) for x in row)
            print(f"R{i+1}: {row_values} [{self.row_parity[i]}]")

        col_parity_str = "".join(f"[{x}]" for x in self.col_parity)
        print(f" P: {col_parity_str}\n")

    def display(self):
        self.display_short_desc()
        self.look()
        self.help()
        self.display_grid()

    # Help
    def help(self):
        print("commands: HELP, CHECK ROW <n>, CHECK COL <n>, FIX ROW <r> COL <c>, SKIP")

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

            elif action == 'skip':
                return 'skip'

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
        self.robot_pos = self.start
        self.robot_dir = config['data']['start_direction']

    def help(self):
        print("commands: HELP, LOOK, EXAMINE <TARGET>, HINT, PROGRAM <cmds>, RESET, SKIP")
        print("  valid moves: MOVE  |  TURN LEFT  |  TURN RIGHT")
        print("  example: PROGRAM MOVE, TURN RIGHT, MOVE, MOVE")
        print("  RESET restarts the robot from the beginning")

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
        self.display_short_desc()
        self.look()
        self.help()
        print()
        self._draw_grid(self.robot_pos, self.robot_dir)

    def _simulate(self, commands):
        pos = self.robot_pos
        direction = self.robot_dir
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
                print(f"Robot crashed at step {steps} — hit a wall or boundary. Use RESET to start over.")
                self.robot_pos = self.start
                self.robot_dir = self.data['start_direction']
                return 'wrong'
            elif result == 'invalid':
                print(f"Unknown command at step {steps}. Valid: MOVE, TURN LEFT, TURN RIGHT")
                return 'continue'
            else:
                self.robot_pos = final_pos
                self.robot_dir = final_dir
                print(f"Robot is now at row {final_pos[0]+1}, col {final_pos[1]+1}, facing {final_dir}.")
                return 'continue'

        elif action == 'reset':
            self.robot_pos = self.start
            self.robot_dir = self.data['start_direction']
            print("Robot reset to starting position.")
            self._draw_grid(self.robot_pos, self.robot_dir)
            return 'continue'

        return super().handle_command(inp)

class BookshelfPuzzle(Puzzle):
    OPTIMAL_SWAPS = 9  # minimum bubble-sort swaps for [8,3,5,1,9,2]

    def __init__(self, config):
        super().__init__(config)
        self.books = list(config['data']['initial'])
        self.solution = config['data']['solution']
        self.swap_count = 0

    def help(self):
        print("commands: HELP, LOOK, EXAMINE <TARGET>, HINT, SWAP <n> <m>, SKIP")
        print("  (SWAP uses position 1-6, not the number on the book)")

    def display_shelf(self):
        print("   " + " ".join(f"[{b}]" for b in self.books))
        print("    |   |   |   |   |   |")
        print("   =========================")
        print("   |       BOOKSHELF       |")
        print("   =========================")
        print(f"   Swaps: {self.swap_count}")

    def display(self):
        self.display_short_desc()
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
    
class StackQueuePuzzle(Puzzle):
    def __init__(self, config):
        super().__init__(config)

      
        self.input_belt = list(config["data"]["input_order"])
        self.target = list(config["data"]["target_order"])

       
        self.stack = []
        self.queue = deque()
        self.output = []
        self.current_crate = None
        self.solved = False

    def help(self):
        print("commands: HELP, LOOK, EXAMINE <TARGET>, HINT,")
        print("          TAKE, PUSH, POP, ENQUEUE, DEQUEUE, PLACE, SKIP")

    def display(self):
        self.display_short_desc()
        self.look()
        self.help()

        print("\n--- PUZZLE STATE ---")
        print("Input:", self.input_belt)
        print("Stack:", self.stack)
        print("Queue:", list(self.queue))
        print("Target:", self.target)
        print("Output:", self.output)
        print("--------------------\n")

    def handle_command(self, input):
        parts = input.strip().upper().split()
        if not parts:
            return "continue"

        action = parts[0]

        
        if action == "TAKE":
            if not self.input_belt:
                print("No more crates on the input belt.")
            else:
                self.current_crate = self.input_belt.pop(0)
                print(f"Took crate {self.current_crate} from input.")
            return "continue"

       
        if action == "PUSH":
            if self.current_crate:
                self.stack.append(self.current_crate)
                print(f"Pushed {self.current_crate} onto stack.")
                self.current_crate = None
            else:
                print("No crate in hand.")
            return "continue"

       
        if action == "POP":
            if self.stack:
                self.current_crate = self.stack.pop()
                print(f"Popped {self.current_crate} from stack.")
            else:
                print("Stack is empty.")
            return "continue"

       
        if action == "ENQUEUE":
            if self.current_crate:
                self.queue.append(self.current_crate)
                print(f"Enqueued {self.current_crate} into queue.")
                self.current_crate = None
            else:
                print("No crate in hand.")
            return "continue"

        
        if action == "DEQUEUE":
            if self.queue:
                self.current_crate = self.queue.popleft()
                print(f"Dequeued {self.current_crate} from queue.")
            else:
                print("Queue is empty.")
            return "continue"

        
        if action == "PLACE":
            if self.current_crate:
                self.output.append(self.current_crate)
                print(f"Placed {self.current_crate} on output shelf.")
                self.current_crate = None

                if self.output == self.target:
                    print("SUCCESS! You solved the puzzle.")
                    self.solved = True
                    return "solved"

                if len(self.output) > len(self.target):
                    print("Too many crates placed.")
                    return "wrong"
            else:
                print("No crate in hand.")
            return "continue"
        return super().handle_command(input)
    
class BinarySearchPuzzle(Puzzle):
    def __init__(self, config):
        super().__init__(config)
        self.number = 86
        self.attempts = 7

    def display(self):
        self.display_short_desc()
        self.look()
        self.help()
        print("\nFINAL EXIT DOOR")
        print("Guess a number between 1 and 100")
        print(f"Attempts left: {self.attempts}\n")

    def help(self):
        print("commands: HELP, LOOK, EXAMINE <TARGET>, HINT, GUESS <n>, SKIP")

    def handle_command(self, input):
        parts = input.strip().split()

        if not parts:
            return "continue"

        action = parts[0].lower()

        if action == "guess":
            if len(parts) < 2:
                print("Usage: GUESS <number>")
                return "continue"

            try:
                guess = int(parts[1])
            except ValueError:
                print("Please enter a valid number.")
                return "continue"

            self.attempts -= 1

            if guess == self.number:
                print("CORRECT! Door opens...")
                self.solved = True
                return "solved"

            if guess > self.number:
                print(f"TOO HIGH (attempts left: {self.attempts})")
            else:
                print(f"TOO LOW (attempts left: {self.attempts})")

            if self.attempts <= 0:
                print("Out of attempts! The door stays locked.")
                print(f"The number was: {self.number}")
                return "wrong"

            return "continue"

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
    elif config['type'] == 'stack_queue':
        return StackQueuePuzzle(config)
    elif config['type'] == 'exit_door':
        return BinarySearchPuzzle(config)
    elif config['type'] == 'graph':
        return GraphPuzzle(config)
    else:
        return Puzzle(config) # worst case if errors


class Puzzle():
    def __init__(self, config):
        self.title = config['title']
        self.difficulty = config['difficulty']
        self.data = config['data']
        self.hints = config['hints']
        self.room_description = config['room_description']
        self.items = config['items']
        self.solved = False
        self.hints_used = 0
        
    # base commands:
    # look: lists everything in room
    # examine: gives the "examine" field from the item
    # hint: shows hint
    # quit: quits game
    
    def help(self):
        print("commands: HELP, LOOK, EXAMINE <TARGET>, HINT, QUIT")
        
    def look(self):
        print(f"room description: {self.room_description}")
        print(f"you can see these items in the room:")
        for item in self.items:
            print(f"{item}: {self.items[item]['description']}")
            
    def examine(self, input):
        item = self.items.get(input.lower()) # allows for incorrect answers compared to using it as the index key
        # item = self.items[input]
        if item:
            print(item['examine'])
        else:
            print(f"{input} doesn't exist here")
            
    def hint(self):
        if self.hints_used < len(self.hints):
            hint = self.hints[self.hints_used]
            self.hints_used += 1
            print(f"hint: {hint}")
        else:
            print("out of hints")   
            
    def handle_command(self, input):
        command = input.split(None, 1) # separator is whitespace (None), only split once (multiword command input)
                
        action = command[0].lower()
        target = None
        
        if len(command) > 1:
            target = command[1]
                    
        if action == 'look':
            self.look()
        elif action == 'examine':
            if target:
                self.examine(target) 
            else: 
                print("choose something to examine")
        elif action == 'hint':
            self.hint()
        elif action == 'quit':
            return 'quit'
        elif action == 'help':
            self.help()
        else:
            if self.check_input(input):
                self.solved = True
                return 'solved'
            return 'wrong'
        return 'continue'
    
    def display_short_desc(self):
        print(f"Puzzle: {self.title}")
        print(f"Difficulty: " + "★ " * self.difficulty)
            
    def display(self):
        self.display_short_desc()
        self.look()
        self.help()
        
    # check_input will be overridden 
    # check_input is used to check against non-command inputs (i.e. the answer)
    # so there is fallback incase forget to include in puzzles.py override
    
    def check_input(self, input):
        print("no input checking added for this puzzle yet")
            
    
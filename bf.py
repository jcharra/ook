
from collections import deque

class Tape(object):
    def __init__(self):
        self.cells = deque([0])
        self.index = 0
        
    def right(self):
        self.index += 1
        if self.index == len(self.cells):
            self.cells.append(0)
        
    def left(self):
        self.index -= 1
        if self.index < 0:
            self.index = 0
            self.cells.appendleft(0)
        
    def inc(self):
        self.cells[self.index] += 1

    def dec(self):
        self.cells[self.index] -= 1

    def get(self):
        return self.cells[self.index]

    def set(self, val):
        self.cells[self.index] = val

    def __repr__(self):
        return " ".join([str(x) for x in self.cells])

class BFInterpreter(object):
    def __init__(self):
        self.tape = Tape()
        self.commands = []
    
    def run_commands(self, cmds):
        self.commands = cmds
        self.command_index = 0
        try:
            while True:
                self.execute_next()
        except IndexError:
            pass

    def execute_next(self):
        cmd = self.commands[self.command_index]
        if cmd == '[':
            if not self.tape.get():
                self.ff_to_matching_closed_paren()
                return
        elif cmd == ']':
            if self.tape.get():
                self.rwd_to_matching_opening_paren()
                return
        else:
            self.interpret(cmd)
        
        self.command_index += 1

    def ff_to_matching_closed_paren(self):
        open = 1
        while open:
            self.command_index += 1
            if self.commands[self.command_index] == ']':
                open -= 1
            elif self.commands[self.command_index] == '[':
                open += 1
        self.command_index += 1

    def rwd_to_matching_opening_paren(self):
        open = 1
        while open:
            self.command_index -= 1
            if self.commands[self.command_index] == '[':
                open -= 1
            elif self.commands[self.command_index] == ']':
                open += 1
        self.command_index += 1

    def interpret(self, item):
        if item == '+':
            self.tape.inc()
        elif item == '-':
            self.tape.dec()
        elif item == '>':
            self.tape.right()
        elif item == '<':
            self.tape.left()
        elif item == '.':
            print chr(self.tape.get())
        elif item == ',':
            try:
                val = int(raw_input())
                self.tape.set(val)
            except:
                # Ignore invalid input
                pass


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print "I need a filename"
        sys.exit()

    fname = sys.argv[1]
    listing = file(fname, 'r').read()

    interpreter = BFInterpreter()
    interpreter.run_commands(listing)

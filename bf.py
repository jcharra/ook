
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
                self.goto_matching_paren(1)
                return
        elif cmd == ']':
            if self.tape.get():
                self.goto_matching_paren(-1)
                return
        else:
            self.interpret(cmd)
        
        self.command_index += 1

    def goto_matching_paren(self, direction):
        onstack = 1
        while onstack:
            self.command_index += direction
            if self.commands[self.command_index] == ']':
                onstack -= direction
            elif self.commands[self.command_index] == '[':
                onstack += direction
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
        print "\nUsage: python bf.py <INPUT_FILE>\n"
        sys.exit()

    fname = sys.argv[1]
    listing = file(fname, 'r').read()

    interpreter = BFInterpreter()
    interpreter.run_commands(listing)

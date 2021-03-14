
import re
import sys
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
            sys.stdout.write(chr(self.tape.get()))
        elif item == ',':
            try:
                val = int(raw_input())
                self.tape.set(val)
            except:
                # Ignore invalid input
                pass

ook2bf = {('ook.', 'ook.'): '+',
          ('ook!', 'ook!'): '-',
          ('ook!', 'ook.'): '.',
          ('ook.', 'ook!'): ',',
          ('ook.', 'ook?'): '>',
          ('ook?', 'ook.'): '<',
          ('ook!', 'ook?'): '[',
          ('ook?', 'ook!'): ']'}

OOK_REGEX = "(ook[\.\!\?])\s*(ook[\.\!\?])"

def convertOokToBF(bf_input):
    output = []
    for match in re.findall(OOK_REGEX, bf_input.lower()):
        if match in ook2bf:
            output.append(ook2bf[match])
    return "".join(output)

def print_usage():
    print("\nUsage: python bf.py [-b|-o] <INPUT_FILE>\n")

if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[1] not in ("-o", "-b"):
        print_usage()
        sys.exit()

    fname = sys.argv[2]
    listing = file(fname, 'r').read()

    if sys.argv[1] == "-o":
        listing = convertOokToBF(listing)

    interpreter = BFInterpreter()
    interpreter.run_commands(listing)

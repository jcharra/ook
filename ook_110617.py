
import sys
from collections import deque

class LoopError(Exception):
    pass

class Ook(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.cells = deque([0])
        self.index = 0
        self.input_buffer = []
        self.output_buffer = []

    def inc(self):
        self.cells[self.index] += 1

    def dec(self):
        self.cells[self.index] -= 1

    def right(self):
        self.index += 1
        if self.index >= len(self.cells):
            self.cells.append(0)

    def left(self):
        if self.index == 0:
            self.cells.appendleft(0)
        else:
            self.index -= 1

    def write(self):
        self.output_buffer.append(self.cells[self.index])
            
    def read(self):
        try:
            self.cells[self.index] = int(raw_input("Your input: "))
        except (TypeError, ValueError):
            print "Invalid input! Continuing ..."

    def as_ascii(self):
        return "".join([chr(c) for c in self.output_buffer])

    def interpret(self, token):
        if token == ('ook.', 'ook.'):
            self.inc()
        elif token == ('ook!', 'ook!'):
            self.dec()
        elif token == ('ook.', 'ook?'):
            self.right()
        elif token == ('ook?', 'ook.'):
            self.left()
        elif token == ('ook!', 'ook.'):
            self.write()
        elif token == ('ook.', 'ook!'):
            self.read()
        else:
            print "Unknown item '%s' found ... ignoring." % (token, )
    
    def interpret_raw_text(self, text):
        self.input_buffer.extend(text.lower().split())
        try:
            self.interpret_items(self.input_buffer)
            self.input_buffer = []
        except IndexError:
            print " ... (incomplete)"
        except LoopError:
            print "LoopError ... exiting"
            sys.exit(1)

    BEGIN_LOOP = ('ook!', 'ook?')
    END_LOOP = ('ook?', 'ook!')
    def interpret_items(self, items):
        idx = 0
        open_loops = 0
        while idx < len(items):
            a, b = items[idx], items[idx+1]
            idx += 2

            if (a, b) == self.BEGIN_LOOP:
                start_idx = idx
                open_loops = 1

                # Increment index until matching end
                while open_loops:
                    loop_next = items[idx], items[idx+1]
                    idx += 2

                    if loop_next == self.BEGIN_LOOP:
                        open_loops += 1
                    elif loop_next == self.END_LOOP:
                        open_loops -= 1
                 
                # Loop contains all elements from start_idx to 
                # current index, except the last expression (i.e. END_LOOP)
                loop = items[start_idx:idx-2]

                # Execute loop while current cell != 0
                while self.cells[self.index]:
                    self.interpret_items(loop)

            elif (a, b) == self.END_LOOP:
                raise LoopError()
            else:
                self.interpret((a, b))

    def interpret_file(self, fname):
        file = open(fname, 'r')
        self.interpret_raw_text(file.read())
        
    def interactive_mode(self):
        print "Ook! interpreter V0.9 - written by Johannes Charra in 2011."
        print "Type '?' to display the status of the Ook! machine. Empty input quits."
        while True:
            inp = raw_input("oo> ").strip()
            if inp == "?":
                print self
            elif inp == "":
                print self
                break
            else:
                self.interpret_raw_text(inp)

    def __repr__(self):
        rep = "\n".join(["Cells\t\t: %s", 
                         "Input\t\t: %s",
                         "Raw output\t: %s",
                         "ASCII output\t: %s"])

        return rep % (list(self.cells),
                      self.input_buffer,
                      " ".join([str(i) for i in self.output_buffer]), 
                      self.as_ascii())
        
if __name__ == '__main__':
    ook = Ook()
    if len(sys.argv) < 2:
        ook.interactive_mode()
    else:
        # Expect a file name as second argument,
        # dismiss all other parameters
        fname = sys.argv[1]
        ook.interpret_file(fname)
        print ook

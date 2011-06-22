
import sys
from collections import deque

class LoopError(Exception):
    pass

class OokParser(object):
    def __init__(self):
        self.BEGIN = ('ook!', 'ook?')
        self.END = ('ook?', 'ook!')
        self.primitives = {('ook.', 'ook.'): 'inc',
                           ('ook!', 'ook!'): 'dec',
                           ('ook.', 'ook?'): 'right',
                           ('ook?', 'ook.'): 'left',
                           ('ook!', 'ook.'): 'write',
                           ('ook.', 'ook!'): 'read'}
                           
    def parse(self, items):
        for i in range(0, len(items), 2):
            yield items[i], items[i+1]

class Interpreter(object):
    def __init__(self, parser):
        self.set_parser(parser)

    def reset(self):
        self.cells = deque([0])
        self.index = 0
        self.input_buffer = []
        self.output_buffer = []
        self.recording = False
        self.open_loops = 0
        self.loop = []

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

    def set_parser(self, parser):
        self.parser = parser
        self.reset()

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

    def interpret_items(self, items):
        for elem in self.parser.parse(items):
            if self.recording:
                if elem == self.parser.END:
                    self.open_loops -= 1
                    if self.open_loops < 0:
                        raise ValueError("End without begin")
                    elif self.open_loops == 0:
                        self.recording = False
                        while self.cells[self.index]:
                            self.interpret_items(self.loop)
                        continue
                elif elem == self.parser.BEGIN:
                    self.open_loops += 1
                self.loop.extend(elem)
            else:
                if elem == self.parser.END:
                    raise ValueError("End without begin")
                elif elem == self.parser.BEGIN:
                    self.recording = True
                    self.open_loops = 1
                    self.loop = []
                elif elem in self.parser.primitives:
                    method = self.parser.primitives[elem]
                    getattr(self, method)()
                else:
                    raise ValueError("Unknown token %s" % (elem, ))

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
    ook = Interpreter(parser=OokParser())
    if len(sys.argv) < 2:
        ook.interactive_mode()
    else:
        # Expect a file name as second argument,
        # dismiss all other parameters
        fname = sys.argv[1]
        ook.interpret_file(fname)
        print ook

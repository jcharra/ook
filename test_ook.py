
import unittest
from ook import Interpreter, OokParser, BrainfuckParser

TEST_STRING_GC = """
    ook. ook. ook. ook. ook. ook. ook. ook. ook! ook.
    ook. ook. ook. ook. ook. ook. ook. ook. ook! ook.
    ook. ook? ook! ook.
    ook. ook. ook! ook.
    ook! ook.
    ook! ook.
    ook! ook! ook! ook.

    ook. ook. ook. ook. ook. ook. ook. ook.
    ook! ook?
    ook. ook? ook. ook. ook. ook? ook. ook. ook. ook. ook? ook. ook? ook. ook! ook!
    ook? ook!
    ook. ook? ook. ook? ook! ook! ook! ook.
    ook? ook. ook! ook.
    ook. ook? ook! ook! ook! ook.
    ook. ook. ook. ook. ook. ook. ook! ook.
    ook! ook! ook! ook.
    ook? ook. ook! ook.
"""

GC_OUTPUT = [4, 8, 0, 1, 1, 1, 0, 7, 4, 6, 9, 8, 4]

class OokParserTest(unittest.TestCase):
    def test_ookparser(self):
        parser = OokParser()
        li = list(parser.parse("ook. OOk. Ook! oOk?"))
        assert li == [("ook.", "ook."), ("ook!", "ook?")], "List is %s" % li

class BrainfuckParserTest(unittest.TestCase):
    def test_bfparser(self):
        parser = BrainfuckParser()
        li = list(parser.parse("++++"))
        assert li == ["+", "+", "+", "+"], "List is %s" % li

class OokTest(unittest.TestCase):
    def setUp(self):
        self.ook = Interpreter()

    def test_incdec(self):
        self.ook.interpret_items([("ook.", "ook.")])
        assert list(self.ook.cells) == [1], "Inc failed"
        self.ook.interpret_items([("ook!", "ook!")])
        assert list(self.ook.cells) == [0], "Dec failed"

    def test_leftright(self):
        self.ook.interpret_items([("ook.", "ook?")])
        assert list(self.ook.cells) == [0, 0], "Right failed"
        assert self.ook.index == 1, "Index move to the right failed"
        self.ook.interpret_items([("ook?", "ook.")])
        assert list(self.ook.cells) == [0, 0], "Left failed"
        assert self.ook.index == 0, "Index move to the left failed"

    def test_raw_inc(self):
        self.ook.interpret_raw_text("ook. ook.")
        assert list(self.ook.cells) == [1], "Raw inc failed"

    def test_javaner(self):
        self.ook.interpret_raw_text(TEST_STRING_GC)
        assert self.ook.output_buffer == GC_OUTPUT, "Output is %s instead of %s" % (self.ook.output_buffer, GC_OUTPUT)

    def test_helloworld(self):
        self.ook.interpret_file('ooktest.txt')
        assert self.ook.as_ascii() == 'Hello World!', 'Helloworld failed: %s' % self.ook.as_ascii()

    def test_simple_loop(self):
        self.ook.interpret_raw_text("ook. ook. ook! ook? ook! ook! ook? ook! ook! ook.")
        assert self.ook.output_buffer == [0], self.ook.output_buffer

    def test_nested_loop(self):
        self.ook.interpret_raw_text("ook. ook. ook! ook? "
                                    "ook. ook. ook! ook? "
                                    "ook! ook! ook? ook! ook? ook! ook! ook.")
        assert self.ook.output_buffer == [0], self.ook.output_buffer

class BFTest(unittest.TestCase):
    def setUp(self):
        self.bf = Interpreter(ook_mode=False)

    def test_incdec(self):
        self.bf.interpret_items(["+"])
        assert list(self.bf.cells) == [1], "Inc failed"
        self.bf.interpret_items(["-"])
        assert list(self.bf.cells) == [0], "Dec failed"

    def test_leftright(self):
        self.bf.interpret_items([">"])
        assert list(self.bf.cells) == [0, 0], "Right failed"
        assert self.bf.index == 1, "Index move to the right failed"
        self.bf.interpret_items(["<"])
        assert list(self.bf.cells) == [0, 0], "Left failed"
        assert self.bf.index == 0, "Index move to the left failed"

    def test_raw_inc(self):
        self.bf.interpret_raw_text("+")
        assert list(self.bf.cells) == [1], "Raw inc failed"

    def test_helloworld(self):
        self.bf.interpret_file('bftest.txt')
        assert self.bf.as_ascii() == "Hello World!\n", "Helloworld failed: '%s'" % self.bf.as_ascii()

    def test_simple_loop(self):
        self.bf.interpret_raw_text("+[-].")
        assert self.bf.output_buffer == [0], self.bf.output_buffer

    def test_nested_loop(self):
        self.bf.interpret_raw_text("+[+[-]].")
        assert self.bf.output_buffer == [0], self.bf.output_buffer
        
    def test_ignore_whitespace(self):
        self.bf.interpret_raw_text("   +   +   +      -  - ")
        assert list(self.bf.cells) == [1], "List is %s" % list(self.bf.cells)

if __name__ == '__main__':
    unittest.main()

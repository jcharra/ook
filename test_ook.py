
import unittest
from ook import Interpreter, OokParser

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

TEST_FILE = 'ook_test.txt'
TEST_FILE_OUTPUT = "Hello World!"

class OokTest(unittest.TestCase):
    def setUp(self):
        self.ook = Interpreter(OokParser())

    def test_incdec(self):
        self.ook.interpret_items(["ook.", "ook."])
        assert list(self.ook.cells) == [1], "Inc failed"
        self.ook.interpret_items(["ook!", "ook!"])
        assert list(self.ook.cells) == [0], "Dec failed"

    def test_leftright(self):
        self.ook.interpret_items(["ook.", "ook?"])
        assert list(self.ook.cells) == [0, 0], "Right failed"
        assert self.ook.index == 1, "Index move to the right failed"
        self.ook.interpret_items(["ook?", "ook."])
        assert list(self.ook.cells) == [0, 0], "Right failed"
        assert self.ook.index == 0, "Index move to the right failed"

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
        
if __name__ == '__main__':
    unittest.main()

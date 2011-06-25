
import unittest
from bf import Tape, BFInterpreter

class BFTest(unittest.TestCase):
    def setUp(self):
        self.interpreter = BFInterpreter()

    def test_inc(self):
        self.interpreter.interpret('+')
        self.assertEqual(self.interpreter.tape.get(), 1)

    def test_dec(self):
        self.interpreter.interpret('-')
        self.assertEqual(self.interpreter.tape.get(), -1)
        
    def test_right(self):
        self.interpreter.interpret('>')
        self.assertEqual(self.interpreter.tape.get(), 0)
        self.assertEqual(list(self.interpreter.tape.cells), [0, 0])
        self.assertEqual(self.interpreter.tape.index, 1)

    def test_left(self):
        self.interpreter.interpret('<')
        self.assertEqual(self.interpreter.tape.get(), 0)
        self.assertEqual(list(self.interpreter.tape.cells), [0, 0])
        self.assertEqual(self.interpreter.tape.index, 0)

    def test_run_commands(self):
        self.interpreter.run_commands("+++++-->>>")
        self.assertEqual(list(self.interpreter.tape.cells), [3, 0, 0, 0])

    def test_loop(self):
        self.interpreter.run_commands("+++[>++<-]")
        self.assertEqual(list(self.interpreter.tape.cells), [0, 6])

        
if __name__ == '__main__':
    unittest.main()

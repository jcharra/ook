
import unittest
from bf import convertOokToBF

ook2bf = {('ook.', 'ook.'): '+',
          ('ook!', 'ook!'): '-',
          ('ook!', 'ook.'): '.',
          ('ook.', 'ook!'): ',',
          ('ook.', 'ook?'): '>',
          ('ook?', 'ook.'): '<',
          ('ook!', 'ook?'): '[',
          ('ook?', 'ook!'): ']'}

class OokConverterTest(unittest.TestCase):
    def test_convert(self):
        text = (" ook.   ook. ook. \n\nook! \nook! "
                " ook!  ook! ook."
                "\n ook. ook? ook? ook.  ook!ook?  ook? ook!")
        self.assertEqual(convertOokToBF(text), "+,-.><[]")

if __name__ == '__main__':
    unittest.main()

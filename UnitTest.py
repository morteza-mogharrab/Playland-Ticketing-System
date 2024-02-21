import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from VancouverPlayland import PlaylandApp

class TestPlaylandApp(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = PlaylandApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_calculate_item_cost(self):
        # Mock entry variables
        self.app.entry_var = [MagicMock(value=str(i)) for i in range(1, 17)]
        # Calculate item cost
        self.app.calculate_item_cost()
        # Assert expected values
        self.assertEqual(self.app.ITEM_PRICES.get(), '$675.00')
        self.assertEqual(self.app.DISCOUNT.get(), '$6.08')
        self.assertEqual(self.app.PAID_TAX.get(), '$94.50')
        self.assertEqual(self.app.TOTAL_COST.get(), '$763.42')

    @patch('builtins.open', create=True)
    def test_generate_receipt(self, mock_open):
        # Mock data for entry variables
        self.app.entry_var = [MagicMock(value=str(i)) for i in range(1, 17)]
        # Call generate_receipt method
        self.app.generate_receipt()
        # Assert if file is opened with correct name and mode
        mock_open.assert_called_once_with('Receipt.txt', 'w')
        # Assert if data is written to the file correctly
        mock_file = mock_open()
        mock_file.write.assert_called_once()
        written_content = mock_file.write.call_args[0][0]
        self.assertIn('Receipt Ref', written_content)
        self.assertIn('BILL Number', written_content)
        # Assert if Receipt Ref is set correctly
        self.assertIsNotNone(self.app.RECEIPT_REF.get())

if __name__ == '__main__':
    unittest.main()

from loan import Loan
from sql_table import Database
from credit_card import CreditCard
from extract_data import ExtractData
from validate_input import Validation
from asyncio.windows_events import NULL
import pandas as pd
import unittest

class TestCases(unittest.TestCase):

    """Making sure that input is validated before continuing with the program"""
    def test_validate_input(self):
        print("Running input validation tests...")
        valid = Validation()
        self.assertEqual(valid.validateCreditUsage(""), NULL)
        self.assertEqual(valid.validateCreditUsage(12.6), 12.6)
        self.assertEqual(valid.validateCreditUsage("5%"), 5.0)
        self.assertEqual(valid.validateCreditUsage("91.44"), 91.44)
        with self.assertRaises(Exception):
            valid.validateCreditUsage("dog")
            valid.validateCreditUsage(0)
            valid.validateCreditUsage("25.7906")
            valid.validateCreditUsage(-32)


        self.assertEqual(valid.validatePayoffTerms(""), NULL)
        self.assertEqual(valid.validatePayoffTerms("78"), 78)
        self.assertEqual(valid.validatePayoffTerms(521), 521)
        with self.assertRaises(Exception):
            valid.validatePayoffTerms("cat")
            valid.validatePayoffTerms(6587)
            valid.validatePayoffTerms("-91")
            valid.validatePayoffTerms(83.6)


    """Making sure the sheet exists. Tested on TestDataset.xlsx."""
    def test_extract_data(self):
        print("Running data extraction tests...")
        extract_data = ExtractData("TestDataset")
        card_df = pd.read_excel("TestDataset.xlsx", 'Credit Card Data')
        loan_df = pd.read_excel("TestDataset.xlsx", 'Loan Data')

        self.assertEqual(extract_data.extractCreditCard().equals(card_df), True)
        self.assertEqual(extract_data.extractLoanData().equals(loan_df), True)

    """Testing Credit Card Methods"""
    def test_credit_card(self):
        print("Running credit card tests...")
        credit_card = CreditCard(15)
        df = credit_card.extractData("TestDataset")
        interest = credit_card.calculateInterest()
        req_payment = credit_card.calculatePayment()
        min_payment = credit_card.calculateMinPayment()
        weighted_payment = credit_card.calculateWeightedPayment()

        self.assertIsInstance(df, pd.DataFrame)
        self.assertIsInstance(interest, pd.Series)
        self.assertIsInstance(req_payment, float)
        self.assertIsInstance(min_payment, pd.Series)
        self.assertIsInstance(weighted_payment, pd.Series)
    
    """Testing Loan Methods"""
    def test_loan(self):
        print("Running loan tests...")
        loan = Loan(20)
        df = loan.extractData("TestDataset")
        min_payments = loan.calculateMinPayments()
        weighted_payments = loan.calculateWeightedPayments()

        self.assertIsInstance(df, pd.DataFrame)
        self.assertIsInstance(min_payments, pd.Series)
        self.assertIsInstance(weighted_payments, pd.DataFrame)
    
    """Testing SQL Table Methods"""
    def test_sql_table(self):
        sql_table = Database("TestDataset")

        # typically, all of these functions are called in Database.createSQLTable() with the parameters passed to them there
        # so for here, I use arbitrary inputs
        card_df = sql_table.formatCreditCardOutput(32)
        min_loan_df = sql_table.formatMinimumLoanOutput(14)
        weighted_loan_df = sql_table.formatWeightedLoanOutput(14)

        self.assertIsInstance(card_df, pd.DataFrame)
        self.assertIsInstance(min_loan_df, pd.DataFrame)
        self.assertIsInstance(weighted_loan_df, pd.DataFrame)
    
if __name__ == '__main__':
    unittest.main()
import pandas as pd
from extract_data import ExtractData

class Loan:
    def __init__(self, payoff_terms):
        self.payoff_terms = payoff_terms


    """Pull credit card data from Excel file."""
    def extractData(self, spreadsheet):
        print("Extracting loan data from Excel file...")
        extract_data = ExtractData(spreadsheet)
        self.df = extract_data.extractLoanData()

        return self.df

    """Calculate minimum payments using amortization formula."""
    def calculateMinPayments(self):
        print("Calculating minimum payments for loans...")
        # total minimum payment is the summation of individual weighted payments
        minimum_payments = self.calculateWeightedPayments().sum()

        return minimum_payments

    """Calculate weighted payments using amortization formula."""
    def calculateWeightedPayments(self):
        print("Calculating weighted payments for loans...")
        # weighted payments are calculated by using the amortization formula
        # and applying it to each loan
        loan_principle = self.df['Current Balance']
        loan_rate = self.df['Interest Rate']
        
        dividend = (loan_rate * ((1 + loan_rate) ** self.payoff_terms))
        divisor = (((1 + loan_rate) ** self.payoff_terms) - 1)

        weighted_payments = round((loan_principle * (dividend / divisor)).fillna(0), 2)

        return weighted_payments.to_frame()


    
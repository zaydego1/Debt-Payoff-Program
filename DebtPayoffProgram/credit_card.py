from asyncio.windows_events import NULL
import pandas as pd
from extract_data import ExtractData

class CreditCard:
    def __init__(self, credit_usage):
        self.credit_usage = credit_usage


    """Pull credit card data from Excel file."""
    def extractData(self, spreadsheet):
        print("Extracting data from Excel file for credit cards...")
        extract_data = ExtractData(spreadsheet)
        self.df = extract_data.extractCreditCard()
        return self.df


    """Calculate the interest accruing in the current month."""
    def calculateInterest(self):
        print("Calculating interest for credit cards...")
        interest = self.df['Current Balance'] * self.df['Interest Rate']
        return interest


    """Calculate the total payment required to satisfy the credit usage limit."""
    def calculatePayment(self):
        print("Calculating sum of total payment required for individual credit cards...")
        #find the difference between our target credit usage and the current balance
        self.target_val = self.df['Max Credit'] * (self.credit_usage / 100)
        self.interest = self.calculateInterest()
        self.current_balance = self.df['Current Balance'] + self.interest

        # if our target value is ever greater than what we currently owe, we don't need to pay anything on that card
        for i in range(self.current_balance.size):
            if self.target_val[i] > self.current_balance[i]:
                self.target_val[i] -= self.target_val[i] - self.current_balance[i]

        payment_required = round((self.current_balance - self.target_val).sum(), 2)

        return payment_required


    """Calculate the minimum payment"""
    def calculateMinPayment(self):
        print("Calculating the minimum payment required for each credit card...")
        #find the difference between what we currently owe versus the target value
        mininum_payment = round(self.current_balance - self.target_val, 2)

        return mininum_payment


    """Calculate the payment required relative to the weight."""
    def calculateWeightedPayment(self):
        print("Calculating weighted payments for each credit card...")
        # we determine weighted payments by:
        # 1. finding what loan accrues the most interest in the current month
        # 2. paying off the most interest-gaining loans first
        # 3. stopping once we've reached the target credit usage
        total_payment = self.calculatePayment()

        balance_and_interest = self.current_balance.to_frame()
        balance_and_interest['Interest'] = self.interest.to_frame()
        
        # We need to keep track of the original order before we sort by weight
        balance_and_interest['Label'] = [i for i in range(self.current_balance.size)]
        balance_and_interest.sort_values(by="Interest", ascending=False)

        weighted_payments = pd.Series(index = range(self.current_balance.size), dtype= float)

        for i in range(self.current_balance.size):
            if total_payment - self.current_balance[i] > 0:
                weighted_payments[i] = self.current_balance[i]
                total_payment -= self.current_balance[i]
            else:
                weighted_payments[i] = total_payment
                break

        # Revert the weighted payments back to order
        weighted_payments = round(weighted_payments.fillna(0), 2)
        balance_and_interest['Weight'] = weighted_payments
        balance_and_interest.sort_values(by="Label", ascending=False)
        weighted_payments = balance_and_interest['Weight']

        return weighted_payments






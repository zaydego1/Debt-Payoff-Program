from asyncio.windows_events import NULL
import sqlite3
import pandas as pd
from credit_card import CreditCard
from loan import Loan

class Database:

    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet

    """Pull data from Credit Card Class"""
    def getCreditCard(self, credit_usage):
        print("Retrieving credit card data...")
        credit_card = CreditCard(credit_usage)
        self.credit_card_data = credit_card.extractData(self.spreadsheet)
        self.credit_weighted_payments = credit_card.calculateWeightedPayment()
        self.credit_min_payments = credit_card.calculateMinPayment()
        self.interest = credit_card.calculateInterest()
        self.credit_balance = credit_card.current_balance

    """Pull data from Loan Class"""
    def getLoan(self, payoff_terms):
        print("Retrieving loan data...")
        loan = Loan(payoff_terms)
        self.loan_data = loan.extractData(self.spreadsheet)
        self.loan_weighted_payments = loan.calculateWeightedPayments()
        self.loan_min_payments = loan.calculateMinPayments()

    """Format the credit card SQL table"""
    def formatCreditCardOutput(self, credit_usage):
        print("Formatting credit card data for output...")
        self.getCreditCard(credit_usage)
        df = self.credit_card_data

        # add the columns needed for output
        df['Remaining Debt Balance (minimum, weighted)'] = [None for i in range(self.credit_weighted_payments.size)]
        df['Paid to Date Percent (minimum, weighted)'] = [None for i in range(self.credit_weighted_payments.size)]

        # fill the data using basic unary operations
        for i in range(self.credit_weighted_payments.size):
            payment_made = "$" + str(round(self.credit_min_payments[i], 2)) + ", $" + \
                str(round(self.credit_weighted_payments[i], 2))
            df.loc[i, "Payment Made (minimum, weighted)"] = payment_made

            minimum_and_weighted_balance = "$" + str(round(self.credit_balance[i] - self.credit_min_payments[i], 2)) + ", $" \
                 + str(round(self.credit_balance[i] - self.credit_weighted_payments[i], 2))
            df.loc[i, 'Remaining Debt Balance (minimum, weighted)'] = minimum_and_weighted_balance

            if self.credit_balance[i] == 0:
                df.loc[i, 'Paid to Date Percent (minimum, weighted)'] = "0.0%, 0.0%"
            else:
                minimum_and_weighted_percent = str(round(self.credit_min_payments[i] / self.credit_balance[i] * 100 ,2)) \
                    + "%, " + str(round(self.credit_weighted_payments[i] / self.credit_balance[i] * 100, 2)) + "%"
                df.loc[i, 'Paid to Date Percent (minimum, weighted)'] = minimum_and_weighted_percent
        
        # add the order in which these cards need to be paid
        # sort by priority
        payment_order = self.interest.to_frame()
        payment_order["Payment Order"] = [i+1 for i in range(self.credit_balance.size)]
        payment_order = payment_order.sort_values(by = 0, ascending=False)
        df["Payment Order"] = payment_order["Payment Order"]

        return df
        
    """Format the loan SQL table for minimum payments"""
    def formatMinimumLoanOutput(self, payoff_terms):
        print("Formatting minimum loan data for output...")
        self.getLoan(payoff_terms)
        df = self.loan_data

        # we need to add these columns to the output table
        # we need the pull the initial terms
        starting_balance = df['Current Balance']
        principle = df['Current Balance'].sum()
        interest = df['Interest Rate']
        terms = [i+1 for i in range(payoff_terms)]

        # we need to add these columns to prepare for output
        rem_balance = [None for i in range(payoff_terms)]
        monthly_payments = [self.loan_min_payments[0] for i in range(payoff_terms)]
        current_balance = [None for i in range(payoff_terms)]
        paid_to_date = [None for i in range(payoff_terms)]
        paid_to_date_percent = [None for i in range(payoff_terms)]

        # paid_off is updated per loop cycle
        paid_off = 0
        for i in range(payoff_terms):
            starting_balance += starting_balance * interest
            rem_balance[i] = "$" + str(round(starting_balance.sum(), 2))
            starting_balance -= self.loan_weighted_payments[0]
            current_balance[i] = round(starting_balance.sum(), 2)
            paid_off += self.loan_min_payments[0]
            paid_to_date[i] = "$" + str(round(paid_off, 2))
            paid_to_date_percent[i] = str(round(paid_off / principle * 100, 2)) + "%"

        #convert to dataframe for output
        data = {"Payoff Term": terms, "Starting Balance": rem_balance, "Monthly Payments": monthly_payments, "Remaining Balance": current_balance,
            "Paid to Date": paid_to_date, "Paid to Date Percent": paid_to_date_percent}
        minimum_schedule = pd.DataFrame(data)

        return minimum_schedule

    """Format the SQL Table output for weighted loan payments"""
    def formatWeightedLoanOutput(self, payoff_terms):
        print("Formatting weighted loan data for output...")
        self.getLoan(payoff_terms)
        df = self.loan_data

        # export will keep track of each row of data we create
        export = []

        # for every loan we have, we keep track of the remaining balance, amount paid off and the percentage paid off
        rem_balance = [0 for i in range(df.shape[0])]
        paid_off = [0 for i in range(df.shape[0])]
        paid_to_date = [0 for i in range(df.shape[0])]

        # loop through our data frame for each payoff term
        for i in range(payoff_terms):
            current_term = i + 1
            loan_number = 0

            # loop through each loan at the current payoff term
            # apply some basic unary operations to convert our data to what we need for output
            for index, row in df.iterrows():
                loan_name = row['Consumer Loan']
                if current_term == 1:
                    principle = row['Current Balance']
                else:
                    principle = rem_balance[loan_number]
                interest = row['Interest Rate']
                starting_balance = principle + principle * interest
                rem_balance[loan_number] = starting_balance - self.loan_weighted_payments.loc[loan_number, 0]
                curr_payment = self.loan_weighted_payments.loc[loan_number, 0]
                paid_off[loan_number] += self.loan_weighted_payments.loc[loan_number, 0]
                if principle != 0:
                    paid_to_date[loan_number] = paid_off[loan_number] / row['Current Balance'] * 100
                else:
                    paid_to_date[loan_number] = 0.0
                loan_number += 1

                # format this output then add to our export list
                curr_row_output = [loan_name, current_term, ("$" + str(round(starting_balance, 2))), (str(round(interest * 100, 2)) + "%"), 
                    ("$" +str(round(curr_payment, 2))), ("$" + str(round(rem_balance[loan_number - 1], 2))), ("$" + str(round(paid_off[loan_number-1], 2))), 
                    (str(round(paid_to_date[loan_number-1], 2)) + "%")]
                export.append(curr_row_output)
            current_term += 1
        
        # return a dataframe that's prepared to be exported to SQL
        output_df = pd.DataFrame(export, columns = ['Loan Number', 'Current Term', 'Starting Balance', 'Interest Rate',
             'Current Payment', 'Remaining Balance', 'Total Paid Off', 'Total Paid Off Percentage'])
        return output_df

            


    """Create the database for the schedule"""
    def createSQLTable(self, credit_usage, payoff_terms):
        print("Outputting data to SQL table...")
        #used to verify whether we were able to get the data
        credit_card = False
        minimum_loan = False
        weighted_loan = False

        if not float(credit_usage) == 0:
            credit_card_df = self.formatCreditCardOutput(credit_usage)
            credit_card = True
        else:
            print("No credit usage detected... Continuing")

        if not int(payoff_terms) == 0:
            minimum_loan_df = self.formatMinimumLoanOutput(payoff_terms)
            weighted_loan_df = self.formatWeightedLoanOutput(payoff_terms)
            minimum_loan = True
            weighted_loan = True
        else:
            print("No payoff terms detected... Continuing")

        #connect to database
        db = sqlite3.connect('Data.db')
        if credit_card:
            credit_card_df.to_sql('Credit Card Data', db, if_exists = 'replace', index = False)
            print("Credit card schedule added to SQL Table")
        if minimum_loan and weighted_loan:
            minimum_loan_df.to_sql('Minimum Loan Data Payoff Schedule', db, if_exists = 'replace', index = False)
            weighted_loan_df.to_sql('Weighted Loan Data Payoff Schedule', db, if_exists = 'replace', index = False)
            print("Loan Data has been added to SQL Table")

        db.commit()
        db.close()
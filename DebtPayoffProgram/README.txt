This program intends to create a SQL database containing payment schedules for credit cards and loans.

It does this by reading from an Excel file stored in this program folder.
It asks the user to input the Excel's name, and it expects to find a sheets named:
- "Credit Card Data" & "Loan Data"
The program will work if one of them is not found, but if both are not found, it will raise an exception.

It also asks the user to input a a target credit utilization as a percentage.
This percentage should be rounded to the nearest hundred. Not including the percent sign will not affect the run.

The program then asks the user to input a number of months that they plan to pay of their loans.
It looks for an integer from 1 - 600. (one month - 50 years)

Class Structure & Methods:
This program has 6 classes and a UnitTest class.
 - main.py is the main class. 
    - It prompts the user for input. 
    - It creates a Validation object to check that input is clean for the rest of the program
    - It then creates a Database object where it calls on Database.createSQLTable(), which executes every other function in the program

- validate_input.py is the validation class
    - The class takes no parameters, instead parameters are passed to its methods for validation
    - validateSpreadsheet(spreadsheet) takes in a string "spreadsheet" & 
        checks to see if the Excel file exists in the project folder and returns True if found
    - validateCreditUsage(credit_usage) takes in a string "credit_usage" & checks to see whether it meets the criteria
        for a credit utilization percent. if it does, it returns the floating point representation of the percentage. if no percentage
        was found, it returns NULL and if the percentage found doesn't meet the criteria, it raises an exception
    - validatePayoffTerms(payoff_terms) takes in a string payoff_terms & checks to see whether it meets the criteria for payoff terms. 
        if so, it returns the integer representation of the string. if no terms were found, it returns null. if the terms don't meet the 
        criteria it raises an exception
    - the program only continues if the validation criteria were met

-extract_data.py is the extraction class
    - this class takes in a string "spreadsheet" as a parameter and creates a workbook with that spreadsheet provided
    - extractCreditCard() takes no parameters, instead it checks if the spreadsheet contains a sheet named "Credit Card Data".
        if so, it will return the DataFrame representation of that. If not, it raises an exception
    - extractLoan() takes no parameters, instead it checks if the spreadsheet contains a sheet named "Loan Data".
        if so, it will return the DataFrame representation of that. If not, it raises an exception

- credit_card.py is the class for finding the minimum and weighted payments required for the credit card sheet
    - the class takes in credit_usage as a parameter
    - extractData() creates an object of ExtractData() type and calls on extractCreditCard() to return the credit card DataFrame if it exists
    - calculateInterest() calculates the amount of interest accruing based on the information gathered from the DataFrame and returns it as a Series
    - calculatePayment() calculates the total payment needed to get credit cards to their target utilization 
        and returns that payment as a float
    - calculateMinPayment() calculates the individual payments needed to get credit cards to their target utilization and returns that answer as a Series
    - calculateWeightedPayment() calculates the individual payments needed to get the total credit utilization to it target percentage and payments
        off the cards according to which ones accrue interest the fastest. returns the answer as a Series

- loan.py is the class for calculating the minimum and weighted payments required for the loan sheet
    - the class takes in payoff_terms as a parameter
    - extractData() creates an object of ExtractData() type and calls on extractLoan() to return the loan DataFrame if it exists
    - calculateMinPayments() calculates the total loan payments needed to get loans to 0 by their target month and returns that answer as a Series
    - calculateWeightedPayments() calculates the individual loan payments required in order to get loans to 0 by its target month and returns
        that answer as a Series

- sql_table.py is the class for formatting the DataFrames to prepare for SQL output as well as creating the SQL Database
    - the class takes in credit_usage and payoff_terms as parameters
    - getCreditCard(credit_usage) & getLoan(payoff_terms) call on their respective classes to get the values needed for the SQL output
    - formatCreditCardOutput(credit_usage) uses the values from getCreditCard(credit_usage) and uses some minor unary operations
        and formatting to create a DataFrame that's ready to be converted to a SQL sql_table
    - formatMinimumLoanOutput(payoff_terms) uses the values from getLoan(payoff_terms) and uses some minor unary operations
        and formatting to create a DataFrame that's ready to be converted to a SQL sql_table for the minimum payment loan payoff schedule
    - formatWeightedLoanOutput(payoff_terms) uses the values from getLoan(payoff_terms) and uses some minor unary operations
        and formatting to create a DataFrame that's ready to be converted to a SQL sql_table for the weighted payment loan payoff schedule
    - createSQLTable(credit_usage, payoff_terms) checks to see if credit_usage and payoff_terms were passed as parameters. if so, it calls on
        the necessary functions (listed above) and gets the necessary DataFrames to output to the SQL Database. it creates a Database named 'Data.db'
        and populates it with all the dataframes it was able to retrieve

    - testing.py is the class for unit testing
        - each class was tested to make sure individual functions could run

Concerns and Shortcomings:
- This program was tested with the TestDataset provided, using various percentages and payoff terms
- I used the amortization formula to calculate payments for loans and I noticed that higher values for payoff_terms seems to reduce the accuracy
    of the payment schedule. The margin of error correlated with the number of terms.
- Testing for the program was as robust as possible, however bugs are almost inevitable with a second person looking over the code.

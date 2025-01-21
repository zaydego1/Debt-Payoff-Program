from asyncio.windows_events import NULL
from validate_input import Validation
from sql_table import Database


"""Main function responsible for executing program"""
print("In order to use the program, " + 
    "please import the Excel file to be read into this folder before continuing.")
print("This simplifies the user from having to copy the entire file path.")


spreadsheet = input("Please enter the name of the Excel spreadsheet: ")
credit_usage = input("Please enter requested credit usage (as a percentage, maximum 2 decimal points): ")
payoff_terms = input("Please enter number of months expected for loan payoff: ")

validify = Validation()
validSpreadsheet = validify.validateSpreadsheet(spreadsheet)

if not validSpreadsheet:
    raise Exception("Program was not able to find file provided in the program folder. " + 
                "Please add the file and restart.")
else:
    print("File found. Continuing...")
    creditusage = validify.validateCreditUsage(credit_usage)
    payoffterms = validify.validatePayoffTerms(payoff_terms)
    print("Spreadsheet found: " + spreadsheet + " | Credit usage found: " + str(creditusage) 
        + "% | Payoff terms found: " + str(payoffterms))
    

sql_table = Database(spreadsheet)
sql_table.createSQLTable(creditusage, payoffterms)




from asyncio.windows_events import NULL
import os.path

class Validation:

    def __init__(self):
        pass

    """Validation is required to check if spreadsheet exists in folder."""
    def validateSpreadsheet(self, spreadsheet):
        print("Validating spreadsheet...")
        spreadsheet = str(spreadsheet)

        file_name = spreadsheet + ".xlsx"
        if not os.path.exists(file_name):
            return False
        else:
            return True
        
        

    """Validation of credit usage is required."""
    def validateCreditUsage(self, credit_usage):
        print("Validating credit card usage...")
        credit_usage = str(credit_usage)

        if len(credit_usage) < 1: 
            print("No credit usage input was detected.")
            return NULL

        else:
            checkPercent = credit_usage[-1]
            parsePercent = credit_usage[:-1]
            if not checkPercent == '%':
                print("You didn't include the percent sign. I guess it's okay this time.")
                parsePercent = credit_usage            
            try:
                float(parsePercent)
            except ValueError:
                raise Exception("Please enter a valid percentage. Percentage found: " + parsePercent)
            if len(parsePercent) > 5:
                raise Exception("Percentage given exceeds limit. Please keep percentage under 100 " +
                    "and a maximum of 2 decimal points")           
            parsePercent = float(parsePercent)
            if parsePercent <= 0:
                raise Exception("Percentage cannot be zero or negative. Are you testing me?")

        credit_usage = parsePercent
        return credit_usage

    """Validation of number of payoff terms is required."""
    def validatePayoffTerms(self, payoff_terms):
        print("Validating payoff terms...")
        payoff_terms = str(payoff_terms)

        if len(payoff_terms) < 1:
            print("No payoff terms detected.")
            return NULL
        elif not payoff_terms.isdigit:
            raise Exception("Please enter a valid integer.")
        else:
            payoff_terms = int(payoff_terms)

            if payoff_terms <= 0 or payoff_terms > 600:
                raise Exception("Number of payoff terms must be between 1 and 600 months.")
        
        return payoff_terms
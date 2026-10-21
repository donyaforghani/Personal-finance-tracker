from datetime import datetime
dateformat= "%d-%m-%Y"
Category={"I":"INCOME","E":"EXPENSE"}

def get_date(prompt, allow_defoult=False):
    date_str=input(prompt)
    if allow_defoult and not date_str:
        return datetime.today().strftime(dateformat)
    
    try:
        v_format= datetime.strptime(date_str, dateformat)
        return v_format.strftime(dateformat)
    except ValueError:
        print("please write correct foemat dd-mm-yyyy")
        return get_date(prompt, allow_defoult)
    
def get_amount():
    try:
        amount=float(input("enter amount:"))
        if amount<=0:
             raise ValueError("amount must be >=0")
        return amount
    except ValueError:
        print("value error")
        return get_amount()
    
def get_catergory():
    category=input("enter category: I for income and E for expense: ").upper()
    if category in Category:
        return Category[category]
    print("entet correct category:")
    return get_catergory()


def get_description():
    return input("enter description:")
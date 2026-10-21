import pandas as pd
import csv
from datetime import datetime
from main import get_catergory,get_date,get_amount,get_description
import matplotlib.pyplot as plt

class CSV:
    Format="%d-%m-%Y"
    csv_file= "data.csv"
    Columns=["date","amount","category","description"]
    
    @classmethod
    def initivilize_csv(cls):
        
        try:
            pd.read_csv(cls.csv_file)
        except FileNotFoundError:
            df=pd.DataFrame(columns=cls.Columns)
            df.to_csv(cls.csv_file, index=False)
            
            
    @classmethod
    def add_entry(cls,date,amount,category,description):
        new_entery={
            "date":date,
            "amount":amount,
            "category":category,
            "description":description }
        with open(cls.csv_file, "a", newline="") as csvfile:
            writer= csv.DictWriter(csvfile, fieldnames=cls.Columns)
            writer.writerow(new_entery)
        print("entery added successfully")   
                
    @classmethod     
    def get_transaction(cls,start_day,end_day):
        df=pd.read_csv(cls.csv_file)
        df["date"]=pd.to_datetime(df["date"],format=CSV.Format)
        start_day=datetime.strptime(start_day,CSV.Format)
        end_day=datetime.strptime(end_day, CSV.Format)
        
        mask=(df["date"]>=start_day) & (df["date"]<=end_day)
        filtered=df.loc[mask]
        
        if filtered.empty:
            print("no transaction find in this range")
        else:
            print(f"transaction from {start_day.strftime(CSV.Format)} to {end_day.strftime(CSV.Format)}")
            print(filtered.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.Format)}))
            
            total_income= filtered[filtered["category"]=="INCOME"]["amount"].sum()
            total_expense=filtered[filtered["category"]=="EXPENSE"]["amount"].sum()
        
            print("\n summery")
            print(f"Total income: ${total_income:.2f}")
            print(f"Total expense: ${total_expense:.2f}")
            print(f"Total save: ${total_income - total_expense:.2f}")
        return filtered 

def add():
    CSV.initivilize_csv()
    date= get_date("enter date:", allow_defoult=True)
    amount=get_amount()
    category=get_catergory()
    description=get_description()
    CSV.add_entry(date,amount,category,description)

def plot(df):
    df.set_index("date", inplace=True)
    df_income=df[df["category"]=="INCOME"]["amount"].resample("D").sum().fillna(0)
    df_expense= df[df["category"]=="EXPENSE"]["amount"].resample("D").sum().fillna(0)
    
    plt.figure(figsize=(10,5))
    plt.plot(df_income.index, df_income, label="Income", color="g")
    plt.plot(df_expense.index, df_expense, label="Expense", color="r")
    plt.xlabel("date")
    plt.ylabel("amount")
    plt.title("Income and Expense over time")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1.Add transaction")
        print("2.Report")
        print("3.Exit")
        choice= input("Enter your choice (1-3): ")
         
        if choice=="1":
            add()
        elif choice=="2":
            start_date= get_date("start date: ")
            end_date= get_date("end date: ")
            df= CSV.get_transaction(start_date, end_date)
            if input("do you want to see a plot? y/n: ").lower() =="y":
                plot(df)
        elif choice=="3":
            print("exiting...")
            break
        else:
            print("enter 1 or 2 or 3")
            
if __name__=="__main__":
    main()
    

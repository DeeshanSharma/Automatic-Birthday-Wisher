'''
Author: Deeshan Sharma
Date: August 16, 2020
Purpose: It is a simple birthday wisher app which will match today's date with the records in the database if present any then it will remind you with a notification and also ask for an option to send them personalized message on your behalf.
File Purpose: It helps to manage the database.
'''

import sqlite3 as sq
from datetime import date, datetime
import winreg as win
import os

class Friend:
    def __init__(self):
        try:
            # Connecting to the Database and initializing a cursor with any unexpected error handling
            self.conn = sq.connect(r"Database\database.sqlite")
            self.cur = self.conn.cursor()
        except Exception as e:
            print(e)

        self.addtoStartup()
        
        print("\t\tMain Menu")
        print("1. Add an entry to the Database")
        print("2. See all Records in the Database")
        print("3. See Records of a particular Month")
        print("4. Delete a Record")
        print("5. Exit")
        # Taking user's choice
        while True:
            ch = int(input("\nChoice = "))
            if ch == 1:
                self.addEntry()
            elif ch == 2:
                self.allRecord()
            elif ch == 3:
                self.monthRecord()
            elif ch == 4:
                self.deleteRecord()
            elif ch == 5:
                print("Have a Good Day")
                self.cur.close()
                self.conn.close()
                exit()
            else:
                print("Please Check Your Input..!!")

    def addEntry(self):
        '''Function for adding  a new record to the database'''
        # Taking all the required inputs for the new record
        name = input("Enter your friends name = ")
        date_entry = input("Enter Date of Birth of your friend (YYYY-MM-DD) = ")
        y, m, d = map(int, date_entry.split("-"))
        dob = date(y, m, d) # Parsing the dob to the proper date format
        number = int(input("Enter your friends WhatsApp no (91XXXXXXXXXX) = "))
        # Inserting new record to the database
        query = ("insert into Friends(Name, DOB, Number) values(?, ?, ?);")
        self.cur.execute(query, (name, dob, number))
        self.conn.commit()
        print("Record updated")
        # Printing the current record
        query = (f"select * from Friends where Number = {number}")
        self.cur.execute(query)
        data = self.cur.fetchall()
        print()
        self.formatPrint(data)

    def allRecord(self):
        '''Function to print all the records from the database'''
        query = "select * from Friends"
        self.cur.execute(query)
        data = self.cur.fetchall()
        print()
        self.formatPrint(data)

    def monthRecord(self):
        '''Function for printing birthdays within a particular month'''
        month = input("Enter month no to see the records (MM) = ")
        query = (f"select * from Friends where DOB like '%-%{month}-%';")
        self.cur.execute(query)
        data = self.cur.fetchall()
        print()
        self.formatPrint(data)

    def deleteRecord(self):
        self.allRecord()
        sno = int(input("\nEnter the Sno whose record you want to delete = "))
        query = (f"delete from Friends where Sno = {sno}")
        self.cur.execute(query)
        self.conn.commit()
        print("Record Deleted Successfully")

    def formatPrint(self, Data):
        '''Function to print data in Table format'''
        if Data:
            # Find the max width for each column
            header = ("Sno", "Name", "DOB", "Number", "Last_Wish")
            widths = [(len(cell)) for cell in header]
            for row in Data:
                for i, cell in enumerate(row):
                    widths[i] = max(len(str(cell)), widths[i])
            # Print in table format
            formatted_row = ' '.join('{:%d}' % width for width in widths)
            print(formatted_row.format(*header))
            for row in Data:
                print(formatted_row.format(*row))
        else:
            print("No Data to Show")

    def addtoStartup(self):
        '''Function to add the autowisher.pyw file to the startup registry key so it runs everyday'''
        self.cur.execute("select * from Friends")
        data = self.cur.fetchone()
        # Checking if there is any data in the database then going further
        if data:
            # Getting the path of the file autowisher.pyw to add to the registry
            path = os.path.dirname(os.path.realpath(__file__))
            filename = "autowisher.pyw"
            path = os.path.join(path, filename)
            # Checking if the registry entry is already present or not if yes then don't go further
            exists = True # Check variable
            aReg = win.ConnectRegistry(None, win.HKEY_CURRENT_USER) # Connecting to the registry
            # Querying for the registry if gets error then entry does not exist then proced to the entry process
            try:
                aKey = win.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, win.KEY_ALL_ACCESS)
                win.QueryValueEx(aKey, "AutoWisher")
            except WindowsError:
                exists = False
            # Registry entry process with the checking for the check variable if False then only perform the process with any error handling
            try:
                if not exists:
                    win.SetValueEx(aKey, "AutoWisher", 0, win.REG_SZ, path) # Setting the registry
                    # Running the script for the first time as it will only run on startup or manually
                    print("Running the Script for the very first time")
                    # Temporarily closing the connection to the database
                    self.cur.close()
                    self.conn.close()
                    # Running the script
                    import autowisher as auto
                    wish = auto.Wish()
                    wish
                    # Restablishing the connection with the database
                    self.conn = sq.connect(r"Database\database.sqlite")
                    self.cur = self.conn.cursor()
            except EnvironmentError:                                          
                print("Encountered problems writing into the Registry...")
            # Closing the connection
            win.CloseKey(aKey)
            win.CloseKey(aReg)

if __name__ == "__main__":
    friend = Friend()
    friend

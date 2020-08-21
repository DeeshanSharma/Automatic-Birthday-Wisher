'''
Author: Deeshan Sharma
Date: August 16, 2020
Purpose: It is a simple birthday wisher app which will match today's date with the records in the database if present any then it will remind you with a notification and also ask for an option to send them personalized message on your behalf.
File Purpose: It is the file which automatically wishes the person.
'''

import sqlite3 as sq
from datetime import date, datetime
import os
from win10toast import ToastNotifier
import random as ran
import webbrowser as web
import time

class Wish:
    def __init__(self):
        try:
            # Connecting to the Database and initializing a cursor with any unexpected error handling
            self.conn = sq.connect(r"Database\database.sqlite")
            self.cur = self.conn.cursor()
        except Exception as e:
            print(e)

        self.checkToday()
        self.cur.close()
        self.conn.close()

    def checkToday(self):
        '''Function to check if today's anyone birthday'''
        today = datetime.now().strftime("%m-%d") # Getting today's date
        # Data retrival from the database commands 
        query = (f"select Sno, Name, Last_Wish from Friends where DOB like '%-%{today}';")
        self.cur.execute(query)
        data = self.cur.fetchall()
        # Check if there is anybody's birthday and then only do the process
        if data:
            temp = []
            name_list = []
            # Getting present year
            present_year = datetime.now().strftime("%Y")
            for i in data:
                # Appending only names of the person in a name_list and all the data in temp List 
                name_list.append(f"{i[1]} ")
                temp.append(i)
            # Converting name_list to string for the notification
            names = "".join(name_list)
            # Get the path of the Icon file for the notification
            iconpath = os.path.dirname(os.path.realpath(__file__))
            filename = r"Icon\birthday.ico"
            iconpath = os.path.join(iconpath, filename)
            # Message for the notification
            msg = (f"We have Birthday of {names}. Wishing them on your behalf. Make sure you are connected to Internet. You have 30 seconds.")
            noti = ToastNotifier() # Norification Initialiation
            noti.show_toast("Let's Make Your Loved Ones Birthday Special", msg, iconpath, 30) # Showing the notification
            # Data preparation for commiting it to the database
            for j in temp:
                sno = j[0]
                last_wish = str(j[2])
                # Check if the person is already wished or not: if not then wish and add current year in the Last_Wish column of the database to avoid wishing multiple times
                if present_year not in last_wish:
                    # Fetching the contact no for the birthday person
                    query = (f"select Number from Friends where Sno = {sno};")
                    self.cur.execute(query)
                    contact = self.cur.fetchall()
                    self.sendMsg(contact) # sendmsg function call to send message to the person passing his contact no as argument
                    # Updating the Last_Wish for the person already wished
                    query = (f"update Friends set Last_Wish = Last_Wish || '{present_year},' where Sno = {sno}")
                    self.cur.execute(query)
                    self.conn.commit()
            time.sleep(5)
    
    def sendMsg(self, contact):
        '''Function for sending WhatsApp messages to the person'''
        wishes = [r'Wishing+you+a+day+filled+with+happiness+and+a+year+filled+with+joy.+Happy+birthday%21', r'Sending+you+smiles+for+every+moment+of+your+special+day%E2%80%A6Have+a+wonderful+time+and+a+very+happy+birthday%21', r'On+your+birthday+we+wish+for+you+that+whatever+you+want+most+in+life+it+comes+to+you+just+the+way+you+imagined+it+or+better.+Happy+birthday%21', r'Sending+your+way+a+bouquet+of+happiness%E2%80%A6To+wish+you+a+very+happy+birthday%21', r'Wishing+you+a+beautiful+day+with+good+health+and+happiness+forever.+Happy+birthday%21'] # Custom Birthday messages url encoded
        # Preparing the url for each individual with a random custom message from the wishes list
        for no in contact:
            msg = ran.choice(wishes)
            url = (f"https://web.whatsapp.com/send?phone={no[0]}&text={msg}&source&data&app_absent")
            web.open(url) # Opening url in the browser
            time.sleep(3)

if __name__ == "__main__":
    wish = Wish()
    wish
# Automatic Birthday Wisher
It is a simple automatic birthday wisher app which will match today's date with the records in the database if present any then it will remind you with a notification and also send them personalized WhatsApp message on your behalf.

## Features
- Sqlite Database to store data
- Automatically send WhatsApp Messsages
- Auto run on startup, Query Database and Sends the Message
- Separate file to manage the Database and to Auto Wish
- Windows Notification for the Birthday Remainder with Name of the person
- Uses WhatsApp Web
- Custom set of Birthday Wishes
- Easy to Use

## Application Currently Works On
Currently it is available for
- Windows 10

# Installation & Requirements
- Clone the repo
	- HTTPS<br>
	`git clone https://github.com/DeeshanSharma/Automatic-Birthday-Wisher.git`
	- SSH<br>
  `git clone git@github.com:DeeshanSharma/Automatic-Birthday-Wisher.git`
- win10toast<br>
  `pip install win10toast`
- Stay Loged in to WhatsApp Web

# Usage
Use [manage.py](manage.py) to play with the Database. <br>
[autowisher.pyw](autowisher.pyw)  is the file which will be used to send the messages and giving the notifications add custom birthday wishes to this file (URL encoded).

# To-Do
- Add Buttons to the Notification
- Email Wishing
- Support for more platform

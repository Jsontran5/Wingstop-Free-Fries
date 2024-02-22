from yopmail import Yopmail
from pandacouponparser import pandamailparse
import pytz
import re
from datetime import datetime
import firebase_admin
import pyrebase
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

dotenv_path = '/etc/secrets/.env' #for render.com
load_dotenv(dotenv_path=dotenv_path) #for render.com

# load_dotenv()



config = {
    "apiKey": os.getenv("API_KEY"),
    "authDomain": os.getenv("AUTH_DOMAIN"),
    "databaseURL": os.getenv("DATABASE_URL"),
    "projectId": os.getenv("PROJECT_ID"),
    "storageBucket": os.getenv("STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("MESSAGING_SENDER_ID"),
    "appId": os.getenv("APP_ID"),
    "measurementId": os.getenv("MEASUREMENT_ID")
}

firebase = pyrebase.initialize_app(config)

db= firebase.database()

pacific_tz = pytz.timezone('America/Los_Angeles')

y = Yopmail('wffpandaexpress', proxies=None)

mails_ids = y.get_mail_ids(page=1) + y.get_mail_ids(page=2) + y.get_mail_ids(page=3)
#print(len(mails_ids))


for mail_id in mails_ids:

    mail = y.get_mail_body(mail_id, show_image=True)
    yopmail_str = str(mail)

    code, realexpiredate = pandamailparse(yopmail_str)
    print(code)
    print(realexpiredate)
    date_format = "%m/%d/%Y"

    #Parse the date string into a datetime object
    date_object = datetime.strptime(realexpiredate, date_format)
    localized_date_object = pacific_tz.localize(date_object)

    #Convert the datetime object to a Unix timestamp
    realexpiredateunix = int(date_object.timestamp())

    #Print the Unix timestamp
    print(realexpiredateunix)

    safeexpiredateunix = realexpiredateunix - 24 * 60 * 60 * 2
    print(safeexpiredateunix)

    safeexpiredate = datetime.fromtimestamp(safeexpiredateunix, tz=pytz.utc).astimezone(pytz.timezone('America/Los_Angeles')).strftime("%m/%d/%Y")
    print(safeexpiredate)

    date_added = datetime.now(pacific_tz).strftime('%m/%d/%Y')
    print(date_added)

    dateaddedunix = int(datetime.now(pacific_tz).timestamp())
    print(dateaddedunix)
    
    db_ref = db.child("Pandacoupons")
    db_ref.child(code).set({
        "realexpiredate": realexpiredate,
        "realexpiredateunix": realexpiredateunix,
        "safeexpiredate": safeexpiredate,
        "safeexpiredateunix": safeexpiredateunix,
        "dateadded": date_added,
        "dateaddedunix": dateaddedunix
    })


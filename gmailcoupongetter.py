import imaplib
import email
from email.header import decode_header
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
from wingstopcouponparser import wingstopemailparse
from pandacouponparser import pandamailparse
import firebase_admin
import pyrebase
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

dotenv_path = '/etc/secrets/.env' #for render.com
load_dotenv(dotenv_path=dotenv_path) #for render.com

# load_dotenv()

pacific_tz =pytz.timezone('America/Los_Angeles')

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

def wingstopcoupongetter():
    IMAP_SERVER = 'imap.gmail.com'
    IMAP_PORT = 993
    EMAIL = os.getenv("EMAIL_USER")
    PASSWORD = os.getenv("EMAIL_PASS")

    # Connect to the server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

    # Login to your account
    mail.login(EMAIL, PASSWORD)

    # Select the mailbox you want to access (e.g., 'INBOX')
    mail.select('inbox')

    # Search for emails
    # Move each email to the "USED" label

    status, data = mail.search(None, '(FROM "WINGS@smg.com")')
    mail_ids = data[0].split()
    print("Wingstop Emails Found: ",len(mail_ids))

    i=0
    pacific_tz = pytz.timezone('America/Los_Angeles')

    # Read each email
    current_time = datetime.now(pacific_tz).strftime('%I:%M:%S%p %m/%d/%Y')
    for mail_id in mail_ids:
        # Fetch the email data
        status, email_data = mail.fetch(mail_id, '(RFC822)')
  
        # Extract the email content
        raw_email = email_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Extract sender
        sender = decode_header(msg['From'])[0][0]
        if isinstance(sender, bytes):
            sender = sender.decode()
        
        # Extract date/time received
        date_received = decode_header(msg['Date'])[0][0]
        if isinstance(date_received, bytes):
            date_received = date_received.decode()
        # Parse date into a datetime object
        date_received = datetime.strptime(date_received, '%d %b %Y %H:%M:%S %z')
        
        # Convert to Pacific Time Zone
        date_received_pacific = date_received.astimezone(pacific_tz)
        
        # Convert time to 12-hour format
        datemailreceived = date_received_pacific.strftime('%b %d, %Y %I:%M %p')
        date_object = datetime.strptime(datemailreceived, '%b %d, %Y %I:%M %p')

        # Convert the datetime object to Unix timestamp
        datemailreceivedunix = int(date_object.timestamp())
        # Subtract the time to get only the date in Unix timestamp
        safeexpiredateunix = (datemailreceivedunix) + (9 * 24 * 60 * 60)
        
       # print("safeexpiredateunix:", safeexpiredateunix)

        #print("datemailrecievedunix:", datemailreceivedunix)
        
        safeexpiredate = datetime.fromtimestamp(safeexpiredateunix, tz=pytz.utc).astimezone(pytz.timezone('America/Los_Angeles')).strftime("%m/%d/%Y")
        

        #print("Date from Unix timestamp:", safeexpiredate)

        # Extract text content
        body = msg.get_payload(decode=True).decode()
        #print('nonmultipart')
        #print('Sender:', sender)
        #print('Date/Time Received (Pacific Time Zone):', datemailreceived)
        #print('Body:', body)
        code = wingstopemailparse(body)
        #print(code)
       # print((type(body)))
        dateadded = datetime.now(pacific_tz).strftime('%b %d, %Y %I:%M%p')
        dateaddedunix = int(datetime.now(pacific_tz).timestamp())

        db_ref = db.child("Wingstopcoupons")
        db_ref.child(code).set({
            "type": "gmail:wingstop",
            "datemailreceived": datemailreceived,
            "datemailreceivedunix": datemailreceivedunix,
            "safeexpiredate": safeexpiredate,
            "safeexpiredateunix": safeexpiredateunix,
            "dateadded": dateadded,
            "dateaddedunix": dateaddedunix
        })
        mail.store(mail_id, '+X-GM-LABELS', '"UNUSED: IN DB"') #added the email to the USED label
        mail.store(mail_id, '+FLAGS', '\\Deleted') #removed the email from the inbox
        i +=1
    print(f"Added {i} Wingstop coupons at {current_time}")
    mail.expunge()
    mail.logout()

def PEcoupongetter():
    IMAP_SERVER = 'imap.gmail.com'
    IMAP_PORT = 993
    EMAIL = os.getenv("EMAIL_USER")
    PASSWORD = os.getenv("EMAIL_PASS")

    # Connect to the server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

    # Login to your account
    mail.login(EMAIL, PASSWORD)

    # Select the mailbox you want to access (e.g., 'INBOX')
    mail.select('inbox')

    # Search for emails
    # Move each email to the "USED" label

    status, data = mail.search(None, '(FROM "PandaExpressFeedback@smg.com")')
    mail_ids = data[0].split()
    print("Panda Express Emails Found: ", len(mail_ids))


    pacific_tz = pytz.timezone('America/Los_Angeles')

    # Read each email
    i=0
    current_time = datetime.now(pacific_tz).strftime('%I:%M:%S%p %m/%d/%Y')
    for mail_id in mail_ids:
        # Fetch the email data
        status, email_data = mail.fetch(mail_id, '(RFC822)')
        
        # Extract the email content
        raw_email = email_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Extract sender
        sender = decode_header(msg['From'])[0][0]
        if isinstance(sender, bytes):
            sender = sender.decode()
        
        # Extract date/time received
        date_received = decode_header(msg['Date'])[0][0]
        if isinstance(date_received, bytes):
            date_received = date_received.decode()
        # Parse date into a datetime object
        date_received = datetime.strptime(date_received, '%d %b %Y %H:%M:%S %z')
        
        # Convert to Pacific Time Zone
        date_received_pacific = date_received.astimezone(pacific_tz)
        
        # Convert time to 12-hour format
        datemailreceived = date_received_pacific.strftime('%b %d, %Y %I:%M %p')
        date_object = datetime.strptime(datemailreceived, '%b %d, %Y %I:%M %p')

        # Convert the datetime object to Unix timestamp
        datemailreceivedunix = int(date_object.timestamp())
        # Subtract the time to get only the date in Unix timestamp
        safeexpiredateunix = (datemailreceivedunix) + (11 * 24 * 60 * 60)
        
        #print("safeexpiredateunix:", safeexpiredateunix)

        #print("datemailrecievedunix:", datemailreceivedunix)
        
        safeexpiredate = datetime.fromtimestamp(safeexpiredateunix, tz=pytz.utc).astimezone(pytz.timezone('America/Los_Angeles')).strftime("%m/%d/%Y")
        

        #print("Date from Unix timestamp:", safeexpiredate)

        # Extract text content
        body = msg.get_payload(decode=True).decode()
        #print('nonmultipart')
       # print('Sender:', sender)
       # print('Date/Time Received (Pacific Time Zone):', datemailreceived)
        #print('Body:', body)
        code, realexpiredate = pandamailparse(body)
        print(f" {code} : {realexpiredate}")
        date_format = "%m/%d/%Y"
        date_object = datetime.strptime(realexpiredate, date_format)
        localized_date_object = pacific_tz.localize(date_object)

        realexpiredateunix = int(date_object.timestamp())
       # print(realexpiredateunix)
        safeexpiredateunix = realexpiredateunix - 24 * 60 * 60 * 2
        safeexpiredate = datetime.fromtimestamp(safeexpiredateunix, tz=pytz.utc).astimezone(pytz.timezone('America/Los_Angeles')).strftime("%m/%d/%Y")
      #  print(safeexpiredate)
       # print(safeexpiredateunix)

        dateadded = datetime.now(pacific_tz).strftime('%b %d, %Y %I:%M%p')
      #  print("dateadded: ", dateadded)
        dateaddedunix = int(datetime.now(pacific_tz).timestamp())
        #print("dateaddedunix: ", dateaddedunix)

        db_ref = db.child("Pandacoupons")
        db_ref.child(code).set({
            "type": "gmail:pandaexpress",
            "datemailreceived": datemailreceived,
            "datemailreceivedunix": datemailreceivedunix,
            "realexpiredate": realexpiredate,
            "realexpiredateunix": realexpiredateunix,
            "safeexpiredate": safeexpiredate,
            "safeexpiredateunix": safeexpiredateunix,
            "dateadded": dateadded,
            "dateaddedunix": dateaddedunix
        })
        mail.store(mail_id, '+X-GM-LABELS', '"UNUSED: IN DB"') #added the email to the USED label
        mail.store(mail_id, '+FLAGS', '\\Deleted') #removed the email from the inbox
        i +=1
    print(f"Added {i} PE coupons at {current_time}")
    mail.expunge()
    mail.logout()

def PEcoupondeleter():
    db_ref = db.child("Pandacoupons")
    all_coupons = db_ref.get()
    before_delete = count_panda_coupons()

    IMAP_SERVER = 'imap.gmail.com'
    IMAP_PORT = 993
    EMAIL = os.getenv("EMAIL_USER")
    PASSWORD = os.getenv("EMAIL_PASS")

    # Connect to the server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

    # Login to your account
    mail.login(EMAIL, PASSWORD)
    mail.select('"UNUSED: IN DB"')

    i = 0
    for coupon in all_coupons.each():
        coupon_dict = coupon.val()
        safeexpiredate = coupon_dict["safeexpiredateunix"]
        currentdate = int(datetime.now(pacific_tz).timestamp())
        
        if currentdate > safeexpiredate:
            db.child("Pandacoupons").child(coupon.key()).remove()
            print(f"Removed {coupon.key()}, expired on {coupon_dict['safeexpiredate']}")

            #MOVING EMAIL LABELS
            search_text = coupon.key()
            search_criteria = f'(TEXT "{search_text}")'
            result, data = mail.search(None, search_criteria)
            i += 1
            if result == 'OK':
                for num in data[0].split():
                    mail.store(num, '+X-GM-LABELS', '"UNUSED: NOT IN DB"')

                    mail.store(num, '+FLAGS', '\\Deleted')
                    mail.expunge()

                    print(f'Moved {coupon.key()} from "UNUSED: IN DB" to "UNUSED: NOT IN DB"')
    after_delete = count_panda_coupons()
    total_deleted = before_delete - after_delete
    print(f"Removed {total_deleted} Panda Express coupons")

def wingstopcoupondeleter():
    db_ref = db.child("Wingstopcoupons")
    all_coupons = db_ref.get()
    before_delete = count_wingstop_coupons()

    IMAP_SERVER = 'imap.gmail.com'
    IMAP_PORT = 993
    EMAIL = os.getenv("EMAIL_USER")
    PASSWORD = os.getenv("EMAIL_PASS")

    # Connect to the server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

    # Login to your account
    mail.login(EMAIL, PASSWORD)
    mail.select('"UNUSED: IN DB"')

    i=0
    for coupon in all_coupons.each():
        coupon_dict = coupon.val()
        safeexpiredate = coupon_dict["safeexpiredateunix"]
        currentdate = int(datetime.now(pacific_tz).timestamp())
        
        if currentdate > safeexpiredate:
            db.child("Wingstopcoupons").child(coupon.key()).remove()
            print(f"Removed {coupon.key()}, expired on {coupon_dict['safeexpiredate']}")
            search_text = coupon.key()
            search_criteria = f'(TEXT "{search_text}")'
            result, data = mail.search(None, search_criteria)
            i += 1
            if result == 'OK':
                for num in data[0].split():
                    mail.store(num, '+X-GM-LABELS', '"UNUSED: NOT IN DB"')

                    mail.store(num, '+FLAGS', '\\Deleted')
                    mail.expunge()

                    print(f'Moved {coupon.key()} from "UNUSED: IN DB" to "UNUSED: NOT IN DB"')
                
           
    after_delete = count_wingstop_coupons()
    total_deleted = before_delete - after_delete
    print(f"Removed {total_deleted} Wingstop coupons")

def count_panda_coupons():
    db_ref = db.child("Pandacoupons")
    all_coupons = db_ref.get()
    count = len(all_coupons.each())
    #print(f"Total number of coupons in the database: {count}")
    return count

def count_wingstop_coupons():
    db_ref = db.child("Wingstopcoupons")
    all_coupons = db_ref.get()
    count = len(all_coupons.each())
    #print(f"Total number of coupons in the database: {count}")
    return count


def usedcoupon(code):
    IMAP_SERVER = 'imap.gmail.com'
    IMAP_PORT = 993
    EMAIL = os.getenv("EMAIL_USER")
    PASSWORD = os.getenv("EMAIL_PASS")

    # Connect to the server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

    # Login to your account
    mail.login(EMAIL, PASSWORD)
    mail.select('"UNUSED: IN DB"')

    i=0
    search_text = code
    search_criteria = f'(TEXT "{search_text}")'
    result, data = mail.search(None, search_criteria)
    i += 1
    if result == 'OK':
        for num in data[0].split():
            mail.store(num, '+X-GM-LABELS', '"USED: NOT IN DB"')
            mail.store(num, '+FLAGS', '\\Deleted')
            mail.expunge()
            
            print(f'Moved {code} from "UNUSED: IN DB" to "USED: NOT IN DB"')


def main():

    #wingstopcoupongetter()
    wingstopcoupondeleter()
   # PEcoupongetter()
    PEcoupondeleter()

    total_panda_coupons = count_panda_coupons()
    print("Total Panda Express coupons: ", total_panda_coupons)
    total_wingstop_coupons = count_wingstop_coupons()
    print("Total Wingstop coupons: ", total_wingstop_coupons)


if __name__ == "__main__":
    main()



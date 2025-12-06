import imaplib
import email
from email.header import decode_header
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
from wingstopcouponparser import wingstopemailparse
from pandacouponparser import pandamailparse
from blazecouponparser import blazeemailparse
from rubiosfunction import rubios_survey
import firebase_admin
import pyrebase
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

dotenv_path = "/etc/secrets/.env"
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv()

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
    if all_coupons and all_coupons.each():
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
    if all_coupons and all_coupons.each():
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
    if all_coupons and all_coupons.each():
        count = len(all_coupons.each())
    else:
        count = 0
    #print(f"Total number of coupons in the database: {count}")
    return count

def count_wingstop_coupons():
    db_ref = db.child("Wingstopcoupons")
    all_coupons = db_ref.get()
    if all_coupons and all_coupons.each():
        count = len(all_coupons.each())
    else:
        count = 0
    #print(f"Total number of coupons in the database: {count}")
    return count

def blazecoupongetter():
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

    # Search for emails from Blaze Pizza
    status, data = mail.search(None, '(FROM "BlazePizza@smg.com")')
    mail_ids = data[0].split()
    print("Blaze Pizza Emails Found: ", len(mail_ids))

    pacific_tz = pytz.timezone('America/Los_Angeles')

    # Read each email
    i = 0
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

        # Extract text content
        body = msg.get_payload(decode=True).decode()
        code, realexpiredate = blazeemailparse(body)
        print(f" {code} : {realexpiredate}")
        
        # Parse the real expire date
        date_format = "%m/%d/%Y"
        date_object = datetime.strptime(realexpiredate, date_format)
        localized_date_object = pacific_tz.localize(date_object)

        realexpiredateunix = int(date_object.timestamp())
        
        # Set safe expire date to 28 days from email received date
        safeexpiredateunix = datemailreceivedunix + (28 * 24 * 60 * 60)
        safeexpiredate = datetime.fromtimestamp(safeexpiredateunix, tz=pytz.utc).astimezone(pytz.timezone('America/Los_Angeles')).strftime("%m/%d/%Y")

        dateadded = datetime.now(pacific_tz).strftime('%b %d, %Y %I:%M%p')
        dateaddedunix = int(datetime.now(pacific_tz).timestamp())

        db_ref = db.child("Blazecoupons")
        db_ref.child(code).set({
            "type": "gmail:blazepizza",
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
        i += 1
    print(f"Added {i} Blaze Pizza coupons at {current_time}")
    mail.expunge()
    mail.logout()

def blazecoupondeleter():
    db_ref = db.child("Blazecoupons")
    all_coupons = db_ref.get()
    before_delete = count_blaze_coupons()

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
    if all_coupons and all_coupons.each():
        for coupon in all_coupons.each():
            coupon_dict = coupon.val()
            safeexpiredate = coupon_dict["safeexpiredateunix"]
            currentdate = int(datetime.now(pacific_tz).timestamp())
            
            if currentdate > safeexpiredate:
                db.child("Blazecoupons").child(coupon.key()).remove()
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
    after_delete = count_blaze_coupons()
    total_deleted = before_delete - after_delete
    print(f"Removed {total_deleted} Blaze Pizza coupons")

def count_blaze_coupons():
    db_ref = db.child("Blazecoupons")
    all_coupons = db_ref.get()
    if all_coupons and all_coupons.each():
        count = len(all_coupons.each())
    else:
        count = 0
    #print(f"Total number of coupons in the database: {count}")
    return count

def rubiosemailfunction():
    """
    Generate a Rubios coupon using the rubios_survey function and add it to the database.
    Sets expiration date to 3 days from now since no date is provided by Rubios.
    """
    try:
        # Call the rubios survey function to get the result
        result = rubios_survey()
        print(f"Rubios survey result: {result}")
        
        # Check if the result indicates success
        if not result or not result.startswith("Success!"):
            print(f"Rubios survey failed or returned unexpected result: {result}")
            return None
            
        # Extract the code from the result string
        # Format: "Success! Online Code for a free drink or dessert with your next purchase at Rubio's: CAS32AS"
        code_part = result.split(": ")
        if len(code_part) < 2:
            print(f"Could not extract code from result: {result}")
            return None
            
        code = code_part[-1].strip()  # Get the last part after the colon
        print(f"Extracted code: {code}")
        
        # Set up dates - expire 3 days from now
        pacific_tz = pytz.timezone('America/Los_Angeles')
        current_time = datetime.now(pacific_tz)
        
        # Date added
        dateadded = current_time.strftime('%b %d, %Y %I:%M%p')
        dateaddedunix = int(current_time.timestamp())
        
        # Safe expire date - 3 days from now
        from datetime import timedelta
        expire_time = current_time + timedelta(days=3)
        safeexpiredateunix = int(expire_time.timestamp())
        safeexpiredate = expire_time.strftime("%m/%d/%Y")
        
        # Add to database
        db_ref = db.child("Rubioscoupons")
        db_ref.child(code).set({
            "type": "api:rubios",
            "safeexpiredate": safeexpiredate,
            "safeexpiredateunix": safeexpiredateunix,
            "dateadded": dateadded,
            "dateaddedunix": dateaddedunix,
            "result": result  # Store the full result string for reference
        })
        
        print(f"Added Rubios coupon {code} to database, expires: {safeexpiredate}")
        return code
        
    except Exception as e:
        print(f"Error in rubiosemailfunction: {str(e)}")
        return None

def count_rubios_coupons():
    """Count the number of Rubios coupons in the database."""
    try:
        db_ref = db.child("Rubioscoupons")
        all_coupons = db_ref.get()
        if all_coupons.each():
            count = len(all_coupons.each())
        else:
            count = 0
        return count
    except Exception as e:
        print(f"Error counting Rubios coupons: {str(e)}")
        return 0

def rubioscoupondeleter():
    """Delete expired Rubios coupons from the database."""
    try:
        db_ref = db.child("Rubioscoupons")
        all_coupons = db_ref.get()
        
        if not all_coupons.each():
            print("No Rubios coupons found in database")
            return
            
        before_delete = count_rubios_coupons()
        pacific_tz = pytz.timezone('America/Los_Angeles')
        
        deleted_count = 0
        for coupon in all_coupons.each():
            coupon_dict = coupon.val()
            safeexpiredate = coupon_dict.get("safeexpiredateunix", 0)
            currentdate = int(datetime.now(pacific_tz).timestamp())
            
            if currentdate > safeexpiredate:
                db.child("Rubioscoupons").child(coupon.key()).remove()
                print(f"Removed {coupon.key()}, expired on {coupon_dict.get('safeexpiredate', 'unknown date')}")
                deleted_count += 1
        
        after_delete = count_rubios_coupons()
        total_deleted = before_delete - after_delete
        print(f"Removed {total_deleted} Rubios coupons")
        
    except Exception as e:
        print(f"Error in rubioscoupondeleter: {str(e)}")


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
    #wingstopcoupondeleter()
   # PEcoupongetter()
    #PEcoupondeleter()
    #blazecoupongetter()
    #blazecoupondeleter()

    total_panda_coupons = count_panda_coupons()
    print("Total Panda Express coupons: ", total_panda_coupons)
    total_wingstop_coupons = count_wingstop_coupons()
    print("Total Wingstop coupons: ", total_wingstop_coupons)
    total_blaze_coupons = count_blaze_coupons()
    print("Total Blaze Pizza coupons: ", total_blaze_coupons)


if __name__ == "__main__":
    main()



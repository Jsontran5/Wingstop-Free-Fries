from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import requests
from blazefunction import blaze_pizza_survey
from pandafunction import panda_survey
from wingstopfunction import wingstop_survey
from rubiosfunction import rubios_survey
from gmailcoupongetter import  PEcoupondeleter, PEcoupongetter, wingstopcoupongetter, wingstopcoupondeleter, count_panda_coupons, count_wingstop_coupons, usedcoupon
from datetime import datetime
import pytz
import firebase_admin
import pyrebase
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv
from threading import Thread

RESTRICTED_EMAILS = ['foodsurveycodes@gmail.com','', " "]
ALLOWED_EMAILS = ['JasonBruincardNFC']
pacific_tz = pytz.timezone('America/Los_Angeles')

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

def create_app():
    app = Flask(__name__)


    @app.route('/')
    def af():
        visitor = request.headers.get('cf-connecting-ip')
        if visitor:
            print(f"AF Visitor: {visitor}")
        return render_template('theend.html')
    
    @app.route('/announcement')
    def announcement():
        visitor = request.headers.get('cf-connecting-ip')
        if visitor:
            print(f"AF Visitor: {visitor}")
        return render_template('announcement.html')
    
    @app.route('/af')
    def index():
        visitor = request.headers.get('cf-connecting-ip')
        if visitor:
            print(f"fooled Visitor: {visitor}")
        return render_template('index.html')

    @app.route('/submit', methods=['POST'])
    def submit():
        input = request.form.get('email').lower()
        timestamp = datetime.now(pacific_tz).strftime('%I:%M:%S %p %m/%d/%Y')
        selected_option = request.form.get('option')
        print('=======================')
        visitor = request.headers.get('cf-connecting-ip')
        print(f"{selected_option} Manual Mode:  {input} ({visitor}): {timestamp}")
        
        if visitor:
            print(f"Visitor: {visitor}")
        else:
            print(f"Visitor: Unable to determine")

        # Default message in case no option is selected
        result = "Please select an option."
        if input in RESTRICTED_EMAILS:
            return redirect(url_for('error'))
        if "@" not in input or "." not in input:
            return redirect(url_for('error'))
        

        
        if selected_option == 'Wingstop':
            result = wingstop_survey(input)
        elif selected_option == 'Rubios':
            result = rubios_survey()
        elif selected_option == 'Panda Express':
            result = panda_survey(input)
        elif selected_option == 'Blaze Pizza':
            result = blaze_pizza_survey(input)

        if result.startswith("Success"):
            increment_uses_count()
            increment_money_saved(result)
        print('=======================')
            

        return result
    
    def increment_uses_count():
        stats_ref = db.child('stats')

        # Get the current count of uses
        current_uses_count = stats_ref.child('uses').get().val()
        current_uses_count = int(current_uses_count) + 1

        db.child('stats').update({'uses': current_uses_count})
        print("+1")
    
    def increment_money_saved(result):
        stats_ref = db.child('stats')
        # Get the current count of uses
        current_money_saved = stats_ref.child('money_saved').get().val()
        current_money_saved = float(current_money_saved)

        if "Panda Express" in result:
            current_money_saved += 5.78
        elif "Blaze Pizza" in result:
            current_money_saved += 3.49
        elif "Wingstop" in result:
            current_money_saved += 4.00
        else:
            current_money_saved += 3.60

        current_money_saved_str = '{:.2f}'.format(current_money_saved)

        # Update the 'stats' node with the new values
        db.child('stats').update({'money_saved': current_money_saved_str})
        
    @app.route('/statsaf')
    @app.route('/statisticsaf')
    def stats():
        uses = db.child('stats').child('uses').get().val()
        money_saved = db.child('stats').child('money_saved').get().val()
        return render_template('stats.html', uses=uses, money_saved=money_saved)


    @app.route('/robots.txt')
    def static_from_root():
        return send_from_directory(app.static_folder, request.path[1:])
    
    
    @app.route('/pandaemail/<email>')
    def pandaemail(email):
        panda_survey(email)
        string = "Populated Panda Express: " + email
        return string
    @app.route('/wingstopemail/<email>')
    def wingstopemail(email):
        wingstop_survey(email)
        string = "Populated Wingstop: " + email
        return string

    @app.route('/wingstopaf')
    @app.route('/wsaf')
    def wingstop():
        return render_template('wingstop.html', option="Wingstop")
    
    @app.route('/rubiosaf')
    @app.route('/raf')
    def rubios():
        return render_template('rubios.html', option="Rubio's")

    @app.route('/pandaexpressaf')
    @app.route('/pandaaf')
    @app.route('/peaf')
    def pandaexpress():
        return render_template('pandaexpress.html', option="Panda Express")

    @app.route('/blazepizzaaf')
    @app.route('/bpaf')
    def blazepizza():
        return render_template('blazepizza.html', option="Blaze Pizza")
    
    @app.route('/dunkinaf')
    @app.route('/donutsaf')
    @app.route('/ddaf')
    def dunkin():
        return render_template('dunkin.html', option="Dunkin")
    
    @app.route('/resultaf')
    def result():
        result = request.args.get('result', 'Please select an option.')
        return render_template('result.html', result=result)
    
    @app.route('/updatecoupondatabase')
    def updatecoupondatabase():
        print("=====FETCHING========")
        PEcoupongetter()
        wingstopcoupongetter()
        print("======DELETING=======")
        PEcoupondeleter()
        wingstopcoupondeleter()
        print("=======COUNTING========")
        panda__coupon_count = count_panda_coupons()
        wingstop__coupon_count = count_wingstop_coupons()

        date_added = datetime.now(pacific_tz).strftime('%I:%M:%S%p %m/%d/%Y')
        print(f"Total Panda Coupons at {date_added} : {panda__coupon_count}")
        print(f"Total Wingstop Coupons at {date_added} : {wingstop__coupon_count}")
        print("======================")
        return "UPDATED DATABASE"
    
    @app.route('/deleteexpiredcoupons')
    def deleteexpiredcoupons():
        print("======DELETING=======")
        PEcoupondeleter()
        wingstopcoupondeleter()
        print("=======COUNTING========")
        panda__coupon_count = count_panda_coupons()
        wingstop__coupon_count = count_wingstop_coupons()

        date_added = datetime.now(pacific_tz).strftime('%I:%M:%S%p %m/%d/%Y')
        print(f"Total Panda Coupons at {date_added} : {panda__coupon_count}")
        print(f"Total Wingstop Coupons at {date_added} : {wingstop__coupon_count}")
        print("======================")
        return "DELETED EXPIRED COUPONS"
    
    @app.route('/fetchcoupons')
    def fetchcoupons():
        print("=====FETCHING========")
        PEcoupongetter()
        wingstopcoupongetter()
        print("=======COUNTING========")
        panda__coupon_count = count_panda_coupons()
        wingstop__coupon_count = count_wingstop_coupons()

        date_added = datetime.now(pacific_tz).strftime('%I:%M:%S%p %m/%d/%Y')
        print(f"Total Panda Coupons at {date_added} : {panda__coupon_count}")
        print(f"Total Wingstop Coupons at {date_added} : {wingstop__coupon_count}")
        print("======================")
        return "FETCHED COUPONS"


    @app.route('/pandalightning')
    def pandalightningtemp():
        
        return render_template('theend.html')
    
    @app.route('/pandalightningaf')
    def pandalightning():
        panda_coupon_count = count_panda_coupons()
        return render_template('pandaexpresslightningform.html', option="pandalightning", panda_coupon_count=panda_coupon_count)
    
    @app.route('/bruincardnfcpandalightningsubmit', methods=['GET'])
    @app.route('/pandalightningsubmit', methods=['POST'])
    def pandalightningsubmit():
        print('=======================')
        if request.method == 'GET':
            input = "JasonBruincardNFC"
        else:
            input = request.form.get('email').lower() or "None"
        
        timestamp = datetime.now(pacific_tz).strftime('%I:%M:%S%p %m/%d/%Y')
        visitor = request.headers.get('cf-connecting-ip')
        print(f"Panda Lightning Mode: {input} ({visitor}): {timestamp}")

        
        if visitor:
            print(f"Unique ID: {visitor}")
        else:
            print(f"Unique ID: Unable to determine")
        
        if input in RESTRICTED_EMAILS:
            return redirect(url_for('error'))
        if "@" not in input or "." not in input:
            if input not in ALLOWED_EMAILS:
                return redirect(url_for('error'))
        

        # Retrieve the first coupon entry from Pandacoupons and delete it
        url = os.getenv("PANDA_URL")
        response = requests.get(url)
        response.raise_for_status()
        first_coupon_data = response.json()

        first_coupon_id = list(first_coupon_data.keys())[0]
        first_coupon = first_coupon_data[first_coupon_id]

        code = first_coupon_id
        print(code)
  

        safeexpiredate = first_coupon["safeexpiredate"]
        print("Expiration Date:", safeexpiredate)

        source = first_coupon.get("type", None)
        print("Source:", source)
        

        # Delete the first coupon entry from the database
        db.child("Pandacoupons").child(first_coupon_id).remove()
        increment_uses_count()
        increment_money_saved("Panda Express")
        print('=======================')
        #Change coupon labels
        t = Thread(target=usedcoupon, args=(code,))
        t.start()

        return redirect(url_for('pandalightningresult',  code=code, safeexpiredate=safeexpiredate))


    @app.route('/pandalightningresultaf')
    def pandalightningresult():
        code = request.args.get('code', 'ERROR')
        safeexpiredate = request.args.get('safeexpiredate', 'ERROR')

        

        return render_template('pandalightningresult.html',code=code, safeexpiredate=safeexpiredate)

    @app.route('/wingstoplightning')
    def wingstoplightningtemp():
        
        return render_template('theend.html')
    
    @app.route('/wingstoplightningaf')
    def wingstoplightning():
        wingstop_coupon_count = count_wingstop_coupons()
        return render_template('wingstoplightningform.html', option="wingstoplightning", wingstop_coupon_count=wingstop_coupon_count)
    
    @app.route('/bruincardnfcwingstoplightningsubmit', methods=['GET'])
    @app.route('/wingstoplightningsubmit', methods=['POST'])
    def wingstoplightningsubmit():
        print('=======================')
        if request.method == 'GET':
            input = "JasonBruincardNFC"
        else:
            input = request.form.get('email').lower() or "None"
    
        timestamp = datetime.now(pacific_tz).strftime('%I:%M:%S%p %m/%d/%Y')
        visitor = request.headers.get('cf-connecting-ip')
        print(f"Wingstop Lightning Mode:  {input} ({visitor}): {timestamp}")
        
        if visitor:
            print(f"Unique ID: {visitor}")
        else:
            print(f"Unique ID: Unable to determine")
        if input in RESTRICTED_EMAILS:
            return redirect(url_for('error'))
        if "@" not in input or "." not in input:
            if input not in ALLOWED_EMAILS:
                return redirect(url_for('error'))

        

        # Retrieve the first coupon entry from Pandacoupons and delete it
        url = os.getenv("WINGSTOP_URL")
        response = requests.get(url)
        response.raise_for_status()
        first_coupon_data = response.json()

        first_coupon_id = list(first_coupon_data.keys())[0]
        first_coupon = first_coupon_data[first_coupon_id]

        code = first_coupon_id
        print(code)
  

        safeexpiredate = first_coupon["safeexpiredate"]
        print("Expiration Date:", safeexpiredate)

        source = first_coupon.get("type", None)
        print("Source:", source)

        # Delete the first coupon entry from the database
        db.child("Wingstopcoupons").child(first_coupon_id).remove()
        increment_uses_count()
        increment_money_saved("Wingstop")
        print('=======================')
        #Change coupon labels
        t = Thread(target=usedcoupon, args=(code,))
        t.start()

        return redirect(url_for('wingstoplightningresult',  code=code, safeexpiredate=safeexpiredate))

    @app.route('/wingstoplightningresultaf')
    def wingstoplightningresult():
        code = request.args.get('code', 'ERROR')
        safeexpiredate = request.args.get('safeexpiredate', 'ERROR')

        return render_template('wingstoplightningresult.html',code=code, safeexpiredate=safeexpiredate)
    
    @app.route('/sendfeedback', methods=['POST'])
    def send_feedback():
        
        feedback = request.json.get('feedback')

        # Print the feedback
        print("Feedback:", feedback)

        
        return 'Feedback received successfully'


    @app.route('/error')
    def error():
        return render_template('error.html')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)

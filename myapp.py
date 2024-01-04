from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from blazefunction import blaze_pizza_survey
from pandafunction import panda_survey
from wingstopoptimizedfunction import wingstop_survey
from rubiosfunction import rubios_survey
from datetime import datetime
import pytz
import firebase_admin
import pyrebase
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

RESTRICTED_EMAILS = ['foodsurveycodes@gmail.com','', " "]
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
    def index():
        return render_template('index.html')

    @app.route('/submit', methods=['POST'])
    def submit():
        email = request.form.get('email').lower()
        timestamp = datetime.now(pacific_tz).strftime('%I:%M:%S %p %m/%d/%Y')

        # Default message in case no option is selected
        result = "Please select an option."
        if email in RESTRICTED_EMAILS:
            return redirect(url_for('error'))
        if "@" not in email or "." not in email:
            return redirect(url_for('error'))
        print(f"{email}: {timestamp}")

        selected_option = request.form.get('option')
        if selected_option == 'wingstop':
            result = wingstop_survey(email)
        elif selected_option == 'rubios':
            result = rubios_survey()
        elif selected_option == 'pandaexpress':
            result = panda_survey(email)
        elif selected_option == 'blazepizza':
            result = blaze_pizza_survey(email)

        if result.startswith("Success"):
            increment_uses_count()
            increment_money_saved(result)

        return result
    
    def increment_uses_count():
        stats_ref = db.child('stats')

        # Get the current count of uses
        current_uses_count = stats_ref.child('uses').get().val()
        current_uses_count = int(current_uses_count) + 1

        db.child('stats').update({'uses': current_uses_count})
    
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
        
    @app.route('/stats')
    @app.route('/statistics')
    def stats():
        uses = db.child('stats').child('uses').get().val()
        money_saved = db.child('stats').child('money_saved').get().val()
        return render_template('stats.html', uses=uses, money_saved=money_saved)


    @app.route('/robots.txt')
    def static_from_root():
        return send_from_directory(app.static_folder, request.path[1:])

    @app.route('/wingstop')
    def wingstop():
        return render_template('wingstop.html', option="Wingstop")
    
    @app.route('/rubios')
    def rubios():
        return render_template('rubios.html', option="Rubio's")

    @app.route('/pandaexpress')
    def pandaexpress():
        return render_template('pandaexpress.html', option="Panda Express")

    @app.route('/blazepizza')
    def blazepizza():
        return render_template('blazepizza.html', option="Blaze Pizza")

    @app.route('/result')
    def result():
        result = request.args.get('result', 'Please select an option.')
        return render_template('result.html', result=result)

    @app.route('/error')
    def error():
        return render_template('error.html')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)

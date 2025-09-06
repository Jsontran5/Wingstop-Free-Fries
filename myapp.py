from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort, jsonify
import requests
from flask_cors import CORS
from blazefunction import blaze_pizza_survey
from pandafunction import panda_survey
from wingstopfunction import wingstop_survey
from rubiosfunction import rubios_survey
from gmailcoupongetter import  PEcoupondeleter, PEcoupongetter, wingstopcoupongetter, wingstopcoupondeleter, blazecoupongetter, blazecoupondeleter, count_panda_coupons, count_wingstop_coupons, count_blaze_coupons, rubiosemailfunction, count_rubios_coupons, rubioscoupondeleter, usedcoupon
from datetime import datetime
import pytz
import firebase_admin
import pyrebase
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv
from threading import Thread
import re

RESTRICTED_EMAILS = ['foodsurveycodes@gmail.com','', " "]

ALLOWED_EMAILS = ['JasonBruincardNFC']
pacific_tz = pytz.timezone('America/Los_Angeles')

dotenv_path = "/etc/secrets/.env"
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv()

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
    app = Flask(__name__, static_folder='wfffrontend/dist', static_url_path='')
    
    # Enable CORS only in development mode
    if os.getenv('FLASK_ENV') == 'development':
        CORS(app)

    @app.before_request
    def block_request():
        if re.match(r"^/wp-.*", request.path):
            abort(403)  # Forbidden
    

    @app.route('/aprilfools')
    def af():
        return render_template('theend.html')
    
    @app.route('/afannouncement')
    def announcement():
        return render_template('announcement.html')

    @app.route('/')
    def index():
        visitor = request.headers.get('cf-connecting-ip')
        if visitor:
            print(f"Visitor: {visitor}")
        # Serve React SPA in production, fallback to legacy template if React build not available
        try:
            return send_from_directory(app.static_folder, 'index.html')
        except Exception:
            return render_template('index.html')

    
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
        
    @app.route('/statistics')
    def statistics():
        # Redirect legacy /statistics to React /stats page
        return redirect('/stats')


    @app.route('/robots.txt')
    def static_from_root():
        return send_from_directory(app.static_folder, request.path[1:])
    
    @app.route('/static/<path:filename>')
    def serve_legacy_static(filename):
        # Serve files from the original static folder for Flask templates
        return send_from_directory('static', filename)
    
    
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

    @app.route('/blazeemail/<email>')
    def blazeemail(email):
        blaze_pizza_survey(email)
        string = "Populated Blaze Pizza: " + email
        return string

    @app.route('/rubiosemail/<email>')
    def rubiosemail(email):
        result = rubiosemailfunction()
        if result:
            string = f"Populated Rubios: {email} - Generated coupon: {result}"
        else:
            string = f"Populated Rubios: {email} - Failed to generate coupon"
        return string

    @app.route('/wingstop')
    @app.route('/ws')
    def wingstop():
        return redirect('/restaurant/wingstop')
    
    @app.route('/rubios')
    @app.route('/r')
    def rubios():
        return redirect('/restaurant/rubios')

    @app.route('/pandaexpress')
    @app.route('/panda')
    @app.route('/pe')
    def pandaexpress():
        return redirect('/restaurant/panda')

    @app.route('/blazepizza')
    @app.route('/bp')
    def blazepizza():
        return redirect('/restaurant/blaze')
    
    
    
    @app.route('/updatecoupondatabase')
    def updatecoupondatabase():
        print("=====FETCHING========")
        PEcoupongetter()
        wingstopcoupongetter()
        blazecoupongetter()
        print("======DELETING=======")
        PEcoupondeleter()
        wingstopcoupondeleter()
        blazecoupondeleter()
        rubioscoupondeleter()
        print("=======COUNTING========")
        panda__coupon_count = count_panda_coupons()
        wingstop__coupon_count = count_wingstop_coupons()
        blaze__coupon_count = count_blaze_coupons()
        rubios__coupon_count = count_rubios_coupons()

        date_added = datetime.now(pacific_tz).strftime('%I:%M:%S%p %m/%d/%Y')
        print(f"Total Panda Coupons at {date_added} : {panda__coupon_count}")
        print(f"Total Wingstop Coupons at {date_added} : {wingstop__coupon_count}")
        print(f"Total Blaze Pizza Coupons at {date_added} : {blaze__coupon_count}")
        print(f"Total Rubios Coupons at {date_added} : {rubios__coupon_count}")
        print("======================")
        return "UPDATED DATABASE"
    
    @app.route('/deleteexpiredcoupons')
    def deleteexpiredcoupons():
        print("======DELETING=======")
        PEcoupondeleter()
        wingstopcoupondeleter()
        blazecoupondeleter()
        rubioscoupondeleter()
        print("=======COUNTING========")
        panda__coupon_count = count_panda_coupons()
        wingstop__coupon_count = count_wingstop_coupons()
        blaze__coupon_count = count_blaze_coupons()
        rubios__coupon_count = count_rubios_coupons()

        date_added = datetime.now(pacific_tz).strftime('%I:%M:%S%p %m/%d/%Y')
        print(f"Total Panda Coupons at {date_added} : {panda__coupon_count}")
        print(f"Total Wingstop Coupons at {date_added} : {wingstop__coupon_count}")
        print(f"Total Blaze Pizza Coupons at {date_added} : {blaze__coupon_count}")
        print(f"Total Rubios Coupons at {date_added} : {rubios__coupon_count}")
        print("======================")
        return "DELETED EXPIRED COUPONS"
    
    @app.route('/fetchcoupons')
    def fetchcoupons():
        print("=====FETCHING========")
        PEcoupongetter()
        wingstopcoupongetter()
        blazecoupongetter()
        print("=======COUNTING========")
        panda__coupon_count = count_panda_coupons()
        wingstop__coupon_count = count_wingstop_coupons()
        blaze__coupon_count = count_blaze_coupons()
        rubios__coupon_count = count_rubios_coupons()

        date_added = datetime.now(pacific_tz).strftime('%I:%M:%S%p %m/%d/%Y')
        print(f"Total Panda Coupons at {date_added} : {panda__coupon_count}")
        print(f"Total Wingstop Coupons at {date_added} : {wingstop__coupon_count}")
        print(f"Total Blaze Pizza Coupons at {date_added} : {blaze__coupon_count}")
        print(f"Total Rubios Coupons at {date_added} : {rubios__coupon_count}")
        print("======================")
        return "FETCHED COUPONS"


    @app.route('/pandalightning')
    def pandalightning():
        return redirect('/restaurant/panda')
    
    @app.route('/bruincardnfcpandalightningsubmit', methods=['GET'])
    def bruincardnfcpandalightningsubmit():
        # NFC endpoint - redirect to React result page using lightning API logic
        print('=======================')
        input = "JasonBruincardNFC"
        timestamp = datetime.now(pacific_tz).strftime('%I:%M:%S%p %m/%d/%Y')
        visitor = request.headers.get('cf-connecting-ip')
        print(f"Panda Lightning Mode: {input} ({visitor}): {timestamp}")
        
        if visitor:
            print(f"Unique ID: {visitor}")
        else:
            print(f"Unique ID: Unable to determine")
        
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

        # Redirect to React result page with parameters
        return redirect(f'/result?code={code}&safeexpiredate={safeexpiredate}&restaurant=panda')


    
    @app.route('/wingstoplightning')
    def wingstoplightning():
        return redirect('/restaurant/wingstop')
    
    @app.route('/bruincardnfcwingstoplightningsubmit', methods=['GET'])
    def bruincardnfcwingstoplightningsubmit():
        # NFC endpoint - redirect to React result page using lightning API logic
        print('=======================')
        input = "JasonBruincardNFC"
        timestamp = datetime.now(pacific_tz).strftime('%I:%M:%S%p %m/%d/%Y')
        visitor = request.headers.get('cf-connecting-ip')
        print(f"Wingstop Lightning Mode:  {input} ({visitor}): {timestamp}")
        
        if visitor:
            print(f"Unique ID: {visitor}")
        else:
            print(f"Unique ID: Unable to determine")
        
        # Retrieve the first coupon entry from Wingstopcoupons and delete it
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

        # Redirect to React result page with parameters
        return redirect(f'/result?code={code}&safeexpiredate={safeexpiredate}&restaurant=wingstop')
    

    
    @app.route('/sendfeedback', methods=['POST'])
    def send_feedback():
        
        feedback = request.json.get('feedback')

        # Print the feedback
        print("Feedback:", feedback)

        
        return 'Feedback received successfully'



    # =====================
    # JSON API Routes for React Frontend
    # =====================
    
    @app.route('/api/restaurants/<restaurant_name>', methods=['POST'])
    def api_restaurant_submit(restaurant_name):
        """Handle restaurant coupon requests from React frontend"""
        try:
            data = request.get_json(silent=True) or {}
            email = (data.get('email') or '').lower()
            
            # Email validation (same logic as existing submit route)
            if email in RESTRICTED_EMAILS:
                return jsonify({"success": False, "redirect": "/error", "error": "Error: restricted email"}), 403
            if "@" not in email or "." not in email:
                return jsonify({"success": False, "redirect": "/error", "error": "Invalid email address"}), 400
            
            # Log the request (same as existing submit route)
            timestamp = datetime.now(pacific_tz).strftime('%I:%M:%S %p %m/%d/%Y')
            visitor = request.headers.get('cf-connecting-ip')
            print('=======================')
            print(f"{restaurant_name} API Mode: {email} ({visitor}): {timestamp}")
            
            # Call appropriate survey function based on restaurant
            result = "Please select an option."
            
            # Rubios is now lightning mode only - redirect to lightning endpoint
            if restaurant_name == 'rubios':
                return jsonify({"success": False, "error": "Rubios only supports lightning mode. Please use the lightning endpoint."}), 400
            
            # Blaze Pizza is now lightning mode only - redirect to lightning endpoint
            elif restaurant_name == 'blaze':
                return jsonify({"success": False, "error": "Blaze Pizza only supports lightning mode. Please use the lightning endpoint."}), 400
            
            # Regular handling for other restaurants (Wingstop/Panda manual mode)
            elif restaurant_name == 'wingstop':
                result = wingstop_survey(email)
            elif restaurant_name == 'panda':
                result = panda_survey(email)
            else:
                return jsonify({"success": False, "error": "Restaurant not found"}), 404
            
            # Process result for Wingstop/Panda manual mode (same logic as existing submit route)
            if isinstance(result, str) and result.startswith("Success"):
                increment_uses_count()
                increment_money_saved(result)
                print('=======================')
                return jsonify({
                    "success": True,
                    "message": result,
                    "code": None  # Manual mode emails coupon, code not immediately available
                })
            else:
                print('=======================')
                return jsonify({"success": False, "error": result}), 400
                
        except Exception as e:
            print(f"API Error: {str(e)}")
            return jsonify({"success": False, "error": "Internal server error"}), 500

    @app.route('/api/stats', methods=['GET'])
    def api_stats():
        """Return statistics data in JSON format for React frontend"""
        try:
            uses = db.child('stats').child('uses').get().val() or 0
            money_saved = db.child('stats').child('money_saved').get().val() or 0.0
            
            return jsonify({
                "totalCoupons": int(uses),
                "totalSaved": float(money_saved),
                "activeUsers": max(1, int(uses) // 3),  # Rough estimate for display
                "averageTime": "12s"
            })
        except Exception as e:
            print(f"Stats API Error: {str(e)}")
            return jsonify({"success": False, "error": "Failed to fetch statistics"}), 500

    @app.route('/api/coupon-counts', methods=['GET'])
    def api_coupon_counts():
        """Get available coupon counts for React frontend"""
        try:
            panda_count = count_panda_coupons()
            wingstop_count = count_wingstop_coupons()
            blaze_count = count_blaze_coupons()
            rubios_count = count_rubios_coupons()
            
            print(f"Coupon counts - Panda: {panda_count}, Wingstop: {wingstop_count}, Blaze: {blaze_count}, Rubios: {rubios_count}")
            
            return jsonify({
                "success": True,
                "counts": {
                    "panda": panda_count,
                    "wingstop": wingstop_count,
                    "blaze": blaze_count,
                    "rubios": rubios_count
                }
            })
        except Exception as e:
            print(f"Error fetching coupon counts: {e}")
            return jsonify({"success": False, "error": "Failed to fetch coupon counts"}), 500

    @app.route('/api/restaurants/<restaurant_name>/lightning', methods=['POST'])
    def api_lightning_submit(restaurant_name):
        """Lightning mode for Panda, Wingstop, Blaze, and Rubios: pull coupon from Firebase and return JSON."""
        try:
            data = request.get_json(silent=True) or {}
            email = (data.get('email') or '').lower()

            # Validate email similar to lightning routes
            if email in RESTRICTED_EMAILS:
                return jsonify({"success": False, "redirect": "/error", "error": "Error: restricted email"}), 403
            if "@" not in email or "." not in email:
                if email not in ALLOWED_EMAILS:
                    return jsonify({"success": False, "redirect": "/error", "error": "Invalid email"}), 400

            timestamp = datetime.now(pacific_tz).strftime('%I:%M:%S%p %m/%d/%Y')
            visitor = request.headers.get('cf-connecting-ip')
            print('=======================')
            print(f"{restaurant_name.title()} Lightning Mode: {email} ({visitor}): {timestamp}")

            if visitor:
                print(f"Unique ID: {visitor}")
            else:
                print(f"Unique ID: Unable to determine")

            if restaurant_name not in ['panda', 'wingstop', 'blaze', 'rubios']:
                return jsonify({"success": False, "error": "Lightning not supported for restaurant"}), 400

            if restaurant_name == 'panda':
                url = os.getenv("PANDA_URL")
                coupon_collection = "Pandacoupons"
                saved_label = "Panda Express"
            elif restaurant_name == 'wingstop':
                url = os.getenv("WINGSTOP_URL")
                coupon_collection = "Wingstopcoupons"
                saved_label = "Wingstop"
            elif restaurant_name == 'blaze':
                url = os.getenv("BLAZE_URL")
                coupon_collection = "Blazecoupons"
                saved_label = "Blaze Pizza"
            else:  # rubios
                rubios_url = os.getenv("RUBIOS_URL")
                url = rubios_url
                coupon_collection = "Rubioscoupons"
                saved_label = "Rubios"

            # Retrieve first coupon entry
            response = requests.get(url)
            response.raise_for_status()
            first_coupon_data = response.json()

            first_coupon_id = list(first_coupon_data.keys())[0]
            first_coupon = first_coupon_data[first_coupon_id]

            code = first_coupon_id
            print(code)

            safeexpiredate = first_coupon.get("safeexpiredate", None)
            print("Expiration Date:", safeexpiredate)

            source = first_coupon.get("type", None)
            print("Source:", source)

            # Delete used coupon
            db.child(coupon_collection).child(first_coupon_id).remove()
            increment_uses_count()
            increment_money_saved(saved_label)
            print('=======================')

            # Fire-and-forget label change
            t = Thread(target=usedcoupon, args=(code,))
            t.start()

            return jsonify({
                "success": True,
                "code": code,
                "safeexpiredate": safeexpiredate,
                "source": source,
                "restaurant": restaurant_name
            })
        except Exception as e:
            print(f"Lightning API Error: {str(e)}")
            return jsonify({"success": False, "error": "Failed to retrieve coupon"}), 500

    # Specific routes for React Router paths
    @app.route('/restaurant/')
    @app.route('/restaurant/<path:subpath>')
    def serve_restaurant(subpath=None):
        print(f"DEBUG: Restaurant route hit with subpath: {subpath}")
        try:
            return send_from_directory(app.static_folder, 'index.html')
        except Exception as e:
            print(f"DEBUG: Error serving restaurant route: {e}")
            return render_template('index.html')
    
    @app.route('/result')
    @app.route('/result/')
    def serve_result():
        print("DEBUG: Result route hit")
        try:
            return send_from_directory(app.static_folder, 'index.html')
        except Exception as e:
            print(f"DEBUG: Error serving result route: {e}")
            return render_template('index.html')
    
    @app.route('/error')
    @app.route('/error/')
    def serve_error():
        print("DEBUG: Error route hit")
        try:
            return send_from_directory(app.static_folder, 'index.html')
        except Exception as e:
            print(f"DEBUG: Error serving error route: {e}")
            return render_template('index.html')

    # Catch-all route to serve React SPA for client-side routing
    @app.route('/<path:path>')
    def serve_spa(path):
        """Serve React SPA files or fallback to index.html for client-side routing"""
        import os
        
        print(f"DEBUG: Catch-all route hit with path: {path}")
        
        # For static files, try to serve them
        try:
            full_path = os.path.join(app.static_folder, path)
            if os.path.isfile(full_path):
                print(f"DEBUG: Serving static file: {path}")
                return send_from_directory(app.static_folder, path)
        except Exception as e:
            print(f"DEBUG: Error checking static file: {e}")
        
        # Default to serving index.html for SPA
        print("DEBUG: Serving index.html from catch-all")
        try:
            return send_from_directory(app.static_folder, 'index.html')
        except Exception as e:
            print(f"DEBUG: Error serving index.html: {e}")
            return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)

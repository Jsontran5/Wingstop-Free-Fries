from flask import Flask, render_template, request, redirect, url_for
from blazefunction import blaze_pizza_survey
from pandafunction import panda_survey
from wingstopoptimizedfunction import wingstop_survey
from rubiosfunction import rubios_survey

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    # Default message in case no option is selected
    result = "Please select an option."

    # Check if a specific option was selected and call the respective function
    selected_option = request.form.get('option')
    if selected_option == 'wingstop':
        result = wingstop_survey(email)
    elif selected_option == 'rubios':
        result = rubios_survey()
    elif selected_option == 'pandaexpress':
        result = panda_survey(email)
    elif selected_option == 'blazepizza':
        result = blaze_pizza_survey(email)

    return redirect(url_for('result', result=result))

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


if __name__ == '__main__':
    app.run(debug=True)

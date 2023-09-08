from flask import Blueprint, render_template, request, flash, redirect, url_for, session


second = Blueprint('second', __name__, static_folder= 'static',template_folder='templates')

@second.route('/home')
@second.route('/')
def home():
    return render_template("home.html")

from . import app
from .upload import *
from flask import render_template

@app.route('/home/')
@app.route('/home/<message>/')
def home():
    
    return render_template('home.html')



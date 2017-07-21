from flask import Flask
import time
from random import randrange

app = Flask(__name__)

from flask import render_template

@app.route('/users/mnovackova/repos')
def repos():
    return render_template('repos.json')

@app.route('/repos/mnovackova/<site>/subscribers')
def followers(site):
    time.sleep(randrange(1, 5))
    return render_template('{}.json'.format(site))

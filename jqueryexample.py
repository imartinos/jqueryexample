# -*- coding: utf-8 -*-
"""
    jQuery Example
    ~~~~~~~~~~~~~~

    A simple application that shows how Flask and jQuery get along.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import numpy as np
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
"""
@app.route('/_add_numbers')
def add_numbers():
    #Add two numbers server side, ridiculous but well...
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)
"""

@app.route('/_add_numbers')
def bday_numbers():
    """compute the probability on the server side"""
    number_of_people = request.args.get('a', 0, type=int)
    max_days_appart = request.args.get('b', 0, type=int)

    number_of_simulations = 1000000
    number_of_days = 365
    wrap_days = number_of_days / 2

    data = np.random.randint(number_of_days, size=(number_of_simulations, number_of_people))
    # print np.sort(data, axis=1)
    # print np.diff(np.sort(data, axis=1))
    # print np.diff(np.sort(data, axis=1)).min(axis=1)
    result = np.diff(np.sort(data, axis=1)).min(axis=1)

    #In order to take into account cases like two people having birthdays one day apart
    #Dec 31st and Jan 1st we need to subtract half a year from differnces that are greater than that
    result = np.absolute(result - ((result > wrap_days).astype(int) * number_of_days))
    # print result
    # print wrap_days
    count = np.sum(result <= max_days_appart)
    probability = float(count) / float(number_of_simulations)


    probability="{0:.1f}".format(probability*100)

    return jsonify(result=probability+'%')




@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

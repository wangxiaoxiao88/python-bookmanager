# -*- coding: utf-8 -*-

from flask import Flask, g
import MySQLdb
import MySQLdb.cursors
import config

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# before every request
@app.before_request
def before_request():
    g.conn = MySQLdb.connect(host=config.DB_HOST, user=config.DB_USER,passwd=config.DB_PASSWD,db=config.DB_NAME,charset='utf8',cursorclass=MySQLdb.cursors.DictCursor)
    g.cursor = g.conn.cursor()

# after every request
@app.teardown_request
def teardown_request(exception):
    g.conn.close()

import controllers


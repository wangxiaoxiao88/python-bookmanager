# coding:utf-8
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    author = db.Column(db.String(40))
    price = db.Column(db.Float)
    url = db.Column(db.String(100))

    def __repr__(self):
        return '<Book %s>' % self.name

    def __init__(self, name, author, price, url):
        self.name = name
        self.author = author
        self.price = price
        self.url = url

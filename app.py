# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, \
        render_template, session, flash, abort
import config
from book import db,Book

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config.from_object(config)

db.init_app(app)

#route
@app.route('/',methods=['GET'])
def list():
    
    books = Book.query.all()
    
    return render_template('list.html', books = books)

@app.route('/create',methods=['POST'])
def create():
    if not session.get('user_id'):
        abort(401)
   
    name = request.form['name']
    author = request.form['author']
    price = request.form['price']
    url = request.form['url']

    book = Book(name, author, price, url)
    
    db.session.add(book)
    db.session.commit()
    return redirect(url_for('list'))

@app.route('/delete',methods=['POST'])
def delete():
    if not session.get('user_id'):
        abort(401)
    id = request.form['id']
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('list'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        if cmp(username,passwd) == 0:
            session['user_id'] = username 
            return redirect(url_for('list')) 
        else:
            flash('password is incorrect')
    return render_template('login.html') 

@app.route('/logout')
def logout():
    session.pop('user_id',None)
    flash('you were logged out')
    return redirect(url_for('list'))

if __name__ == '__main__':
    app.debug = True
    app.run()

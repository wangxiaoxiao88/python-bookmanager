# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, \
        render_template,  _app_ctx_stack, session, flash, abort
import MySQLdb

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

TABLENAME = ' book '
FIELDS = ' name,author,price,url '
ALL_FIELDS = 'id,' + FIELDS

class Book:
    id=0
    name=''
    author=''
    price=0
    url=''

#route
@app.route('/',methods=['GET'])
def list():
    sql = 'select ' + ALL_FIELDS + ' from '+ TABLENAME
    results = get_db(sql)
    books = []
    for b in results:
        book = Book()
        book.id = b[0]
        book.name = b[1]
        book.author = b[2]
        book.price = b[3]
        book.url = b[4]
        books.append(book)
    
    return render_template('list.html', books = books)

@app.route('/create',methods=['POST'])
def create():
    if not session.get('user_id'):
        abort(401)
    name = request.form['name']
    author = request.form['author']
    price = request.form['price']
    url = request.form['url']

    sql = 'insert into ' + TABLENAME + '(' + FIELDS + ') values (%s,%s,%s,%s)'
    add_db(sql,[name,author,price,url])
    return redirect(url_for('list'))

@app.route('/delete',methods=['POST'])
def delete():
    if not session.get('user_id'):
        abort(401)
    id = request.form['id']
    sql = 'delete from ' + TABLENAME + 'where id = '+id
    del_db(sql)
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

@app.teardown_appcontext
def close(exception):
    top=_app_ctx_stack.top
    if hasattr(top,'db'):
        top.db.close()

#db operation
def init_db():
    top = _app_ctx_stack.top
    if not hasattr(top,'db'):
        conn = MySQLdb.connect(host='10.2.206.196', user='root',passwd='root',db='test',charset='utf8') 
        top.db = conn
    
    return top.db

def get_db(sql,one = False):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute(sql) 
    if one:
        res = cursor.fetchone()
    else:
        res = cursor.fetchall()
    cursor.close()
    return res

def add_db(sql,value):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute(sql,value)
    conn.commit()
    cursor.close()

def del_db(sql):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()

if __name__ == '__main__':
    app.debug = True
    app.run(host='10.2.45.79')

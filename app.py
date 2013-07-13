# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack
import MySQLdb
import config

app = Flask(__name__)

TABLENAME=' book '
FIELDS=' name,author,price,url '

class Book:
    id=0
    name=''
    author=''
    price=0
    url=''

#route

@app.route('/getAllBooks',methods=['GET'])
def getAllBooks():
    sql='select id,' + FIELDS + ' from '+ TABLENAME
    results = get_db(sql)
    books=[]
    for b in results:
        book=Book()
        book.id=b[0]
        book.name=b[1]
        book.author=b[2]
        book.price=b[3]
        book.url=b[4]
        print book.url
        books.append(book)
    
    return render_template('show_books.html',books=books)

@app.route('/add',methods=['POST'])
def addBook():
    name=request.form['name']
    author=request.form['author']
    price=request.form['price']
    url=request.form['url']
    print 'url===='+url
    sql='insert into ' + TABLENAME + '(' + FIELDS + ') values (%s,%s,%s,%s)'
    add_db(sql,[name,author,price,url])
    return redirect(url_for('getAllBooks'))

@app.route('/del',methods=['POST'])
def delBook():
    id=request.form['id']
    sql='delete from ' + TABLENAME + 'where id = '+id
    del_db(sql)
    return redirect(url_for('getAllBooks'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        passwd=request.form['passwd']
        if cmp(username,passwd) == 0:
            return redirect(url_for('getAllBooks')) 
        else:
            error='wrong'
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    return 'logout'


@app.teardown_appcontext
def close(exception):
    top=_app_ctx_stack.top
    if hasattr(top,'db'):
        top.db.close()

#db operation

def init_db():
    top=_app_ctx_stack.top
    if not hasattr(top,'db'):
        conn = MySQLdb.connect(host=config.DB_HOST, user=config.DB_USER,passwd=config.DB_PASSWD,db=config.DB_NAME,charset='utf8') 
        top.db=conn
    
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

@app.route('/')
def show():
    sql = 'select * from book'
    res = get_db(sql,True)
    return str(res[1].encode('utf8'))

if __name__ == '__main__':
    app.debug = True
    app.run()

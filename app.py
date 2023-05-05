from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'india@123'
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bookstore")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', bookstore=data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        bookname = request.form['bookname']
        authorname = request.form['authorname']
        publication = request.form['publication']
        category = request.form['category']
        price = request.form['price']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bookstore (bookname, authorname, publication,category,price) VALUES (%s, %s, %s,%s, %s)", (bookname, authorname, publication,category,price))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM bookstore WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        bookname = request.form['bookname']
        authorname = request.form['authorname']
        publication = request.form['publication']
        category = request.form['category']
        price = request.form['price']

        

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE bookstore SET bookname=%s, authorname=%s, publication=%s,category=%s,price=%s
        WHERE id=%s
        """, (bookname, authorname, publication,category, price,id))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))




if __name__ == "__main__":
    app.run(debug=True)

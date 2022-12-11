from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def getConnection():
  return pymysql.connect(
    host="db",
    db="flask_dev",
    user="user",
    password="password",
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
  )

@app.route('/', methods=["GET", "POST"])
def select_sql():
    if request.method == "GET":
        connection = getConnection()
        sql = "SELECT * FROM todos"
        cursor = connection.cursor()
        cursor.execute(sql)
        todos = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('index.html', todos = todos)
    else:
        connection = getConnection()
        try:
            with connection.cursor() as cursor:
                sql = ('''
                INSERT INTO todos
                    (name)
                VALUES
                    (%s)
                ''')
                cursor.execute(sql, (request.form["name"]))
                connection.commit()
        finally:
            connection.close()

        return redirect(url_for('select_sql'))

# @app.route('/create', methods=["POST"])
# def create_post():

#     connection = getConnection()
#     try:
#         with connection.cursor() as cursor:
#             sql = ('''
#             INSERT INTO todos
#                 (name, content)
#             VALUES
#                 (%s, %s)
#             ''')
#             cursor.execute(sql, (request.form["name"], request.form["content"]))
#             connection.commit()
#     finally:
#         connection.close()

#     return redirect(url_for('select_sql'))

if __name__ == '__main__':
  app.run()


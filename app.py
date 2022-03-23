import flask
from flaskext.mysql import MySQL
from flask import request
import pymysql

app = flask.Flask(__name__)

mysql = MySQL()


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'roytuts'
app.config['MYSQL_DATABASE_HOST'] = 'db'
mysql.init_app(app)

@app.route('/')
def fetch_users():
    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM user")

    rows = cursor.fetchall()

    resp = flask.jsonify(rows)
    resp.status_code = 200
    cursor.close()
    conn.close()
    return resp

@app.route('/ins_data/',methods=['GET'])
def insert_users():
    if 'name' in request.args:
        name = str(request.args['name'])
    if 'id' in request.args:
        id = int(request.args['id'])
    if 'ph' in request.args:
        ph = int(request.args['ph'])
    query = execute_query(name,id,ph)
    return query


def execute_query(name,id,ph):
    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = f"""insert  into `user`(`id`,`name`,`email`,`phone`,`address`) values
({id},{name},'vj@gmail.com',{ph},'Venus');"""
    # query = f"""INSERT INTO USER (address,email,id,name,phone) values ('venus','vj@gmail.com',{id},'{name}',{ph});"""
    cursor.execute(query)
    conn.commit()
    conn.close()
    cursor.close()
    return f'inserted one row through {query}'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

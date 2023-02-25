from flask import Flask, request, jsonify
import os
from model.predict import *

app = Flask(__name__)

@app.route('/api/create-texture', methods=['POST'])
def create_texture():   
    front_image = request.files["front"].read()
    back_image = request.files["back"].read()
    primary_color = request.form["color"]

    front_output = predict_h5(front_image)
    back_output = predict_h5(back_image)

    return jsonify({"front": front_output, "back" : back_output})

@app.route('/api/ping', methods=['GET'])
def ping():
    dir = os.getcwd()   
    print(dir)
    dir += "//model"
    print(os.listdir(dir))

    return "erhhehe"

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))
    # serve(app, host="0.0.0.0", port=5000)
    # app.run()
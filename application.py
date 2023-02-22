from flask import Flask, request, jsonify
import os
from waitress import serve
from model.predict import *

app = Flask(__name__)

@app.route('/api/create-texture', methods=['POST', 'GET', 'DELETE'])
def create_texture():   
    front_image = request.files["front"].read()
    back_image = request.files["back"].read()
    primary_color = request.form["color"]

    front_output = predict_h5(front_image)
    back_output = predict_h5(back_image)

    return jsonify({"front": front_output, "back" : back_output})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    serve(app, host="0.0.0.0", port=port)
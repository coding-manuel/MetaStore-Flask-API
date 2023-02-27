from flask import Flask, request, jsonify
import os
from model.predict import *
import streamlit as st

app = Flask(__name__)

def main():
    st.title('Image Segmentation App')

    # Add the API functionality
    st.server.set_page_config(
        page_title="Image Segmentation API",
        page_icon=":guardsman:",
        layout="wide",
    )

    @st.experimental_api(allowed_methods=["POST"])
    def segment_image(file):
        front_image = request.files["front"].read()
        back_image = request.files["back"].read()
        primary_color = request.form["color"]

        front_output2 = predict_h5(front_image)
        back_output2 = predict_h5(back_image)

        return ({"front2": front_output2, "back2" : back_output2})


# @app.route('/api/create-texture', methods=['POST'])
# def create_texture():   
#     front_image = request.files["front"].read()
#     back_image = request.files["back"].read()
#     primary_color = request.form["color"]

#     front_output1 = predict(front_image)
#     # back_output1 = predict(back_image)
#     front_output2 = predict_h5(front_image)
#     back_output2 = predict_h5(back_image)

#     return jsonify({"front": front_output1, "back" : back_output1, "front2": front_output2, "back2" : back_output2})

# @app.route('/api/ping', methods=['GET'])
# def ping():
#     dir = os.getcwd()   
#     print(dir)
#     dir += "//model"
#     print(os.listdir(dir))

#     return "erhhehe"

# @app.route('/')
# def index():
#     return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

if __name__ == '__main__':
    main()
    # app.run(debug=True)
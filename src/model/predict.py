import base64
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.utils import CustomObjectScope

def iou(y_true, y_pred):
    def f(y_true, y_pred):
        intersection = (y_true * y_pred).sum()
        union = y_true.sum() + y_pred.sum() - intersection
        x = (intersection + 1e-15) / (union + 1e-15)
        x = x.astype(np.float32)
        return x
    return tf.numpy_function(f, [y_true, y_pred], tf.float32)

smooth = 1e-15
def dice_coef(y_true, y_pred):
    y_true = tf.keras.layers.Flatten()(y_true)
    y_pred = tf.keras.layers.Flatten()(y_pred)
    intersection = tf.reduce_sum(y_true * y_pred)
    return (2. * intersection + smooth) / (tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) + smooth)

def dice_loss(y_true, y_pred):
    return 1.0 - dice_coef(y_true, y_pred)

def predict(file):
    #Load Model
    interpreter = tf.lite.Interpreter(model_path='model/segmentation_model.tflite')
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Global Parameters
    H = 512
    W = 384

    # Set up your input data.
    # Convert File to np array
    file_bytes = np.fromstring(file, np.uint8)
    # convert numpy array to image
    image = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)

    resized_image = cv2.resize(image, (W, H))
    x = resized_image/255.0
    x = x.astype(np.float32)
    x = np.expand_dims(x,0)

    # Input Data to Model
    interpreter.set_tensor(input_details[0]['index'], x)
    interpreter.invoke()

    #Geting Output
    print("geting output")
    prediction = interpreter.get_tensor(output_details[0]['index'])[0]

    prediction = cv2.resize(prediction, (W, H))
    prediction = np.expand_dims(prediction, axis=-1)
    prediction = prediction > 0.5

    mask = np.uint8(prediction) * 255
    prediction = cv2.merge([mask, mask, mask])

    mask_inv = cv2.cvtColor(prediction, cv2.COLOR_BGR2GRAY)

    output_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2BGRA)
    output_image[..., 3] = mask_inv

    retval, buffer = cv2.imencode('.png', output_image)
    encoded_image = base64.b64encode(buffer).decode('utf-8')

    return encoded_image

def predict_h5(file):
    #Load Model
    with CustomObjectScope({'iou': iou, 'dice_coef': dice_coef, 'dice_loss': dice_loss}):
        model = tf.keras.models.load_model("model/model.h5")

    # Global Parameters
    H = 512
    W = 384

    # Set up your input data.
    # Convert File to np array
    file_bytes = np.fromstring(file, np.uint8)
    # convert numpy array to image
    image = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)

    resized_image = cv2.resize(image, (W, H))
    x = resized_image/255.0
    x = x.astype(np.float32)
    x = np.expand_dims(x,0)

    # Input Data to Model

    #Geting Output
    prediction = model.predict(x)[0]

    prediction = cv2.resize(prediction, (W, H))
    prediction = np.expand_dims(prediction, axis=-1)
    prediction = prediction > 0.5

    mask = np.uint8(prediction) * 255
    prediction = cv2.merge([mask, mask, mask])

    mask_inv = cv2.cvtColor(prediction, cv2.COLOR_BGR2GRAY)

    output_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2BGRA)
    output_image[..., 3] = mask_inv

    retval, buffer = cv2.imencode('.png', output_image)
    encoded_image = base64.b64encode(buffer).decode('utf-8')

    return encoded_image
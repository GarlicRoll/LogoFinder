import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
import cv2
import numpy as np
import pandas as pd
from warnings import filterwarnings

filterwarnings("ignore")


def recognizer(path):
    nn = tf.keras.models.load_model("models/nn128.keras")
    #nn.load_weights("models/model_fast_food_big.weights.h5")
    '''
    op = cv2.imread(path)
    op = cv2.resize(op, (30, 30))
    op = np.array(op)
    op = op.reshape(1, 30, 30, 3)
    model = nn.predict(op)

    store_name = ['burger king', 'mcdonalds', 'starbucks', 'subway']

    # Convert to DataFrame
    val = []
    for i in model:
        val.append(i)
    data_fram = pd.DataFrame([store_name, val[0]]).T
    data_fram.columns = ["Outlate", "Output"]

    # Final Output
    op_final = data_fram.groupby('Output').max().tail(1).values[0][0]

    # Get the index of the predicted class
    predicted_class_index = np.argmax(model)

    # Get the predicted class associated probability
    probability = model.squeeze()[predicted_class_index] * 100  # Convert to percentage
    print(f"Given Image is {op_final} Store with a probability of {probability:.2f}%")
    '''
    store_names = list(pd.read_csv("datasets/glebs_data.csv")["name"])

    op = cv2.imread(path)
    op = cv2.resize(op, (128, 128))
    op = np.array(op)
    # op = op.reshape(1,30,30,3)

    x_min, y_min = 4, 4
    x_max, y_max = 124, 124
    op_xml = np.array([x_min, x_max, y_min, y_max])
    op_image = np.array(op).reshape(1, *op.shape)
    op_xml = np.array(op_xml).reshape(1, *op_xml.shape)

    model = nn.predict([op_image, op_xml])

    # Convert to DataFrame
    val = []
    for i in model:
        val.append(i)
    data_fram = pd.DataFrame([store_names, val[0]]).T
    data_fram.columns = ["Outlate", "Output"]

    # Final Output
    op_final = data_fram.groupby('Output').max().tail(1).values[0][0]

    # Get the indices of the top 5 classes sorted by probability
    top_5_indices = np.argsort(model.squeeze())[-5:][::-1]

    # Get the top 5 probabilities
    top_5_probabilities = model.squeeze()[top_5_indices] * 100

    # Get the corresponding class labels for the top 5 indices
    top_5_classes = [store_names[i] for i in top_5_indices]

    # Print the top 5 most possible classes and their probabilities
    for class_name, probability in zip(top_5_classes, top_5_probabilities):
     print(f"Class: {class_name}, Probability: {probability:.2f}%")
    return op_final

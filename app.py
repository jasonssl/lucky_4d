from flask import Flask, jsonify, render_template, send_from_directory
from keras.models import Sequential
from keras.layers.core import Dense
from sklearn.model_selection import train_test_split
import numpy as np
from two_weeks import update_data

app = Flask(__name__,static_folder='static',template_folder='template')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/lucky', methods=['GET'])
def get_num():
    # sample data
    # numbers=[9378, 3034, 8594, 3676, 1267, 9104, 6944, 4476, 6224, 9489, 7164, 6218, 3719, 3787, 3045, 8634, 4244, 7578, 5393, 9131, 8427, 125, 9229, 9108, 2178, 3432, 4946]

    # Getting actual data
    numbers=update_data()
    print(f"Data Size: ",len(numbers))

    # Split your data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(numbers, numbers, test_size=0.8)

    # Create a neural network model
    model = Sequential()
    model.add(Dense(10, input_dim=1, activation='relu'))
    model.add(Dense(1))

    # Compile and fit the model
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=305, batch_size=32, verbose=0)

    predicted_number = model.predict(x_test)

    # Round the output to the nearest integer
    predicted_number = np.round(predicted_number)
    predicted_number = np.clip(predicted_number, 0, 9999)

    # Convert the output to an integer
    predicted_number = int(predicted_number[0][0])

    # Fill leading zeros if the number is less than 1000
    if int(predicted_number) < 1000:
        predicted_number = "{:04d}".format(int(predicted_number))

    print(str(predicted_number))
    return jsonify(lucky_number=predicted_number)

if __name__ == '__main__':
    app.run(debug=True)
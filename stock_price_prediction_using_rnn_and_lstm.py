# -*- coding: utf-8 -*-
"""Google Stock Price Prediction using RNN and LSTM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fTASQJpdTLqzIFEoEksjeo_9-y7KmeaN

# **STEP 1 : INSTALLATION AND SETUP**
"""

pip install tensorflow[and-cuda]

import tensorflow as tf
print(len(tf.config.list_physical_devices('GPU')))

print(tf.__version__)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""# **STEP 2 : DATA PREPROCESSING**"""

# import the dataset
from google.colab import files
uploaded = files.upload()

import pandas as pd

trainingdata = pd.read_csv('/content/trainingdata.csv')

trainingdata.head()

trainingdata.tail()

trainingdata.info()

training_set = trainingdata.iloc[:,1:2].values

training_set.shape, trainingdata.shape

# feature scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range=(0,1))
training_set_scaled = sc.fit_transform(training_set)

training_set_scaled

import numpy as np

# Creating a data structure with 60 timesteps and 1 output
x_train = []
y_train = []

for i in range(60, 1259):
    x_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])

# Convert x_train and y_train into numpy arrays
x_train, y_train = np.array(x_train), np.array(y_train)

x_train

y_train

x_train.shape

# reshaping dataset
x_train = x_train.reshape(1199, 60, 1)

x_train.shape

"""Step 3: Building **LSTM**

# **Step 3: Building LSTM**
"""

import tensorflow as tf

# Define an object (initialize RNN)
model = tf.keras.models.Sequential()

# Assuming x_train is your input data
x_train = x_train.reshape(-1, 60, 1)

# Rest of your model definition...
model = tf.keras.Sequential()
model.add(tf.keras.layers.LSTM(units=60, activation='relu', return_sequences=True, input_shape=(60, 1)))
model.add(tf.keras.layers.Dropout(0.2))


# Second LSTM layers and dropout
model.add(tf.keras.layers.LSTM(units=60, activation='relu', return_sequences=True))
model.add(tf.keras.layers.Dropout(0.2))


# Third LSTM layers and dropout
model.add(tf.keras.layers.LSTM(units=80, activation='relu', return_sequences=True))
model.add(tf.keras.layers.Dropout(0.2))


# Forth LSTM layers and dropout
model.add(tf.keras.layers.LSTM(units=120, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))

#Output layer
model.add(tf.keras.layers.Dense(units=1))

model.summary()

# Compile the model...
model.compile(optimizer='adam', loss='mean_squared_error')

"""# **Step 4 :  Training the model**"""

model.fit(x_train, y_train, batch_size=32, epochs=100)

"""# **Step 5 : Making Predictions**"""

# Getting The Real Stock Prices of Month APRIL 2024
test_data = pd.read_csv('/content/testdata.csv')

test_data.shape

test_data.info()

real_stock_price = test_data.iloc[:, 1:2].values

real_stock_price

real_stock_price.shape

# Getting predicted stock prices of month APRIL 2024

# Concatination
dataset_total = pd.concat((trainingdata['Open'], test_data['Open']), axis=0)

# Stocks prices of previous 60 days for each day of Nov 2019
inputs = dataset_total[len(dataset_total)-len(test_data)-60:].values

# Reshape (Convert into numpy array)
inputs = inputs.reshape(-1,1)

# Feature Scaling
inputs = sc.transform(inputs)

# creating a test set

X_test = []
for i in range(60, 80):
    X_test.append(inputs[i-60:i, 0])

# Convert to numpy array
X_test = np.array(X_test)

# Convert in 3D (required to Process)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Getting predicted stock price
predicted_stock_price = model.predict(X_test)

predicted_stock_price = sc.inverse_transform(predicted_stock_price)

print(predicted_stock_price[5]), print(real_stock_price)

"""# **Step 6: Visualization**"""

import matplotlib.pyplot as plt

# Visualizing the results
plt.plot(real_stock_price, color='red', label='Real Google Stock Price')
plt.plot(predicted_stock_price, color='blue', label='Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()
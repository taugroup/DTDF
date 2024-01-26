from DTDF import DigitalTwin
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Create an instance of the digital twin
dt = DigitalTwin()

# Create some sample data using pandas DataFrame
ambient_temp = np.random.normal(20, 5, 100)
ambient_humidity = np.random.normal(50, 10, 100)
room_temp = ambient_temp + np.random.normal(0, 2, 100)
data = pd.DataFrame({'Ambient_Temp': ambient_temp,
                     'Ambient_Humidity': ambient_humidity,
                     'Room_Temp': room_temp})

# Add MQTT connection for multiple topics from one broker
dt.add_mqtt_connection(client_id="client1",
                       broker_address="datahub.tamids.tamu.edu",
                       topics=["air_quality"])

# Set the data and update the model
# dt.set_data(data)
# dt.set_model(LinearRegression())
# dt.update()

# print(dt.data)

#
# # Make a prediction using a DataFrame
# input_data = pd.DataFrame({'Ambient_Temp': [22], 'Ambient_Humidity': [55]})
# prediction = dt.predict(input_data)

# print(prediction)
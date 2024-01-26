import paho.mqtt.client as mqtt
import pandas as pd
import json
import time

# Sample DataFrame
df = pd.DataFrame({
    'Time': ['2023-01-01', '2023-01-02', '2023-01-03'],
    'Value': [100, 200, 300]
})

# MQTT Configuration
broker_address = "192.168.2.128"  # Replace with your broker address
port = 1883  # Replace with your broker port
topic = "topic1"


# Callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


# Callback for when a PUBLISH message is sent to the server
def on_publish(client, userdata, mid):
    print("Message Published.")


# Create an MQTT client and attach our routines to it
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the broker
client.connect(broker_address, port, 60)

# Start the loop
client.loop_start()

try:
    while True:
        # Convert DataFrame to JSON
        json_data = df.to_json(orient='records')

        # Publishing the DataFrame
        client.publish(topic, json_data)

        # Wait for some time before next publish
        time.sleep(5)  # Sleep for 5 seconds

except KeyboardInterrupt:
    print("Stopping the publisher.")

finally:
    # Stop the loop and disconnect
    client.loop_stop()
    client.disconnect()

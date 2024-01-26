import numpy as np
import logging
import sys
import pandas as pd
from sklearn.linear_model import LinearRegression
import paho.mqtt.client as mqtt


class DigitalTwin:
    """
    A Digital Twin class for simulating and predicting real-world systems.

    Attributes:
        logger (logging): The logger for debugging purpose.
        model (LinearRegression): The machine learning model used for predictions.
        data (np.ndarray): The dataset used for training the model.
        num_features (integer): Number of features in the data
        simulation_params (dict): Parameters for running simulations.
        real_time_data (dict): Data collected in real-time for predictions.
        actuator (object): An actuator object for controlling a real-world system.
    """

    def __init__(self):
        self.mqtt_clients = None
        self.logger = logging.getLogger(self.__class__.__name__)
        
        self.model = None
        self.data = None
        self.num_features = 0  # Number of features in the data
        self.simulation_params = {}
        self.real_time_data = {}
        self.actuator = None

        # Initialize with an additional attribute for number of features
        self.setup_logging(filename="digital_twin.log")
        self.logger.debug("Initializing DigitalTwin instance.")

    def setup_logging(self, level=logging.DEBUG, filename='digital_twin.log'):
        """
        Set up the logging for debugging purposes in the Digital Twin class.

        This method configures the logging system to write messages to a file with a specified format.
        The format includes the timestamp of the log entry, the name of the logger, the severity level
        of the message, and the message itself.

        Parameters:
            level (int): Logging level to capture. For example, logging.DEBUG, logging.INFO, etc.
                         Determines the severity of the messages that will be captured. Lower levels
                         will capture more detailed logging information.
            filename (str): The name of the file where log messages will be written. If the file does
                            not exist, it will be created. If it exists, logs will be appended to it.

        The logging format is set to include the timestamp ('%(asctime)s'), the logger's name ('%(name)s'),
        the level of severity ('%(levelname)s'), and the actual log message ('%(message)s').
        """

        # Create logger

        self.logger.setLevel(level)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create file handler and set level and formatter
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # Create stream handler for standard output and set level and formatter
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)


    def add_mqtt_connection(self, client_id, broker_address, topics):
        """
        Add a new MQTT connection for a specific broker and subscribe to multiple topics.

        Parameters:
            client_id (str): Unique identifier for the MQTT client.
            broker_address (str): Address of the MQTT broker.
            topics (list): List of topics to subscribe to.
        """
        client = mqtt.Client(client_id)

        def on_connect(client, userdata, flags, rc):
            self.logger.debug(f"Connected to MQTT Broker ({broker_address}) with result code {rc}")
            for topic in topics:
                client.subscribe(topic)
                self.logger.debug(topic)

        def on_message(client, userdata, msg):
            self.logger.debug(f"MQTT message received from {msg.topic}: {msg.payload}")
            self.update_real_time_data(client_id, msg.topic, msg.payload)

        client.on_connect = on_connect
        client.on_message = on_message

        try:
            client.connect(broker_address)
            client.loop_start()  # Start the network loop in a separate thread
            self.mqtt_clients[client_id] = client
        except Exception as e:
            self.logger.error(f"Failed to connect to MQTT Broker ({broker_address}): {e}")

    def set_model(self, model):
        """
        Set the model for the digital twin.

        Parameters:
            model: A regression model.
        """
        self.logger.debug(f"Setting model: {model}")
        self.model = model

    def set_data(self, data: pd.DataFrame):
        """
        Set the training data for the digital twin using a pandas DataFrame.

        Parameters:
            data (pd.DataFrame): Training data.

        Raises:
            ValueError: If the data is not a pandas DataFrame.
        """

        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame.")
        self.data = data
        self.num_features = data.shape[1] - 1  # Assume last column is the target
        self.logger.debug(f"Setting data (show first 5 entries): \n{self.data.head()}\n...")

    def update(self):
        """
        Update the data-driven model with new data.
        """

        self.logger.debug("Updating the digital twin model.")

        if self.model is not None:
            if self.data is not None and self.data.shape[1] > 1:
                features = self.data.iloc[:, :self.num_features]
                target = self.data.iloc[:, -1]
                self.model.fit(features, target)
        else:
            self.logger.debug("No model was selected.")

    def predict(self, input_data: pd.DataFrame):
        """
        Make predictions using the digital twin model.

        Parameters:
            input_data (pd.DataFrame): Input data for making predictions.

        Returns:
            np.ndarray: Predicted values.

        Raises:
            ValueError: If input_data is not a pandas DataFrame or does not have the expected number of columns.
        """

        self.logger.debug(f"Making prediction with input data: {input_data}")

        if not isinstance(input_data, pd.DataFrame) or input_data.shape[1] != self.num_features:
            raise ValueError(f"Input data must be a pandas DataFrame with exactly {self.num_features} columns.")
        return self.model.predict(input_data)

    def set_simulation_params(self, params):
        """
        Set the simulation parameters.

        Parameters:
            params (dict): A dictionary of simulation parameters.
        """
        self.logger.debug(f"Setting simulation parameters: {params}")

        self.simulation_params = params

    def set_actuator(self, actuator):
        """
        Set the actuator for the digital twin.

        Parameters:
            actuator (object): An actuator object.
        """
        self.logger.debug(f"Setting actuator: {actuator}")

        self.actuator = actuator

    def run_simulation(self):
        """
        Run a simulation using the set parameters. (To be implemented)
        """
        self.logger.debug("Running simulation.")

    def update_real_time_data(self, data):
        self.logger.debug(f"Updating real-time data: {data}")
        # rest of the method

    def run_real_time_prediction(self):
        """
        Use real-time data and the model to make predictions. (To be implemented)
        """
        self.logger.debug("Running real-time prediction.")

    def control_actuator(self, control_signal):
        """
        Control the actuator using a control signal.

        Parameters:
            control_signal (Any): The control signal for the actuator.
        """

        self.logger.debug(f"Controlling actuator with signal: {control_signal}")

        # Ensure the actuator is set before sending a control signal
        if self.actuator is not None:
            self.actuator.set_control_signal(control_signal)

    def visualize(self):
        """
        Visualize simulation results, real-time predictions, and actuator control. (To be implemented)
        """
        self.logger.debug("Visualizing results.")


# Example usage
if __name__ == "__main__":
    # Create an instance of the digital twin
    dt = DigitalTwin()

    # Create some sample data using pandas DataFrame
    ambient_temp = np.random.normal(20, 5, 100)
    ambient_humidity = np.random.normal(50, 10, 100)
    room_temp = ambient_temp + np.random.normal(0, 2, 100)
    data = pd.DataFrame({'Ambient_Temp': ambient_temp,
                         'Ambient_Humidity': ambient_humidity,
                         'Room_Temp': room_temp})

    # Set the data and update the model
    dt.set_data(data)
    dt.set_model(LinearRegression())
    dt.update()

    # Make a prediction using a DataFrame
    input_data = pd.DataFrame({'Ambient_Temp': [22], 'Ambient_Humidity': [55]})
    prediction = dt.predict(input_data)

    print(prediction)
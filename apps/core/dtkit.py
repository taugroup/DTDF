import random
import time

class PhysicalObject:
    """
    A simulated physical object with some random parameters.
    """
    def __init__(self, name):
        self.name = name
        self.temperature = 0
        self.pressure = 0

    def update_conditions(self):
        """
        Simulate condition changes.
        """
        self.temperature = random.randint(-10, 40)
        self.pressure = random.randint(1, 10)

    def get_data(self):
        """
        Get current conditions of the physical object.
        """
        return {'temperature': self.temperature, 'pressure': self.pressure}

class DigitalTwin:
    """
    Digital Twin of a physical object, following a simplified version of ISO 23247.
    """
    def __init__(self, physical_object):
        self.physical_object = physical_object
        self.data = {}

    def ingest_data(self):
        """
        Ingest data from the physical object.
        """
        self.data = self.physical_object.get_data()

    def analyze_data(self):
        """
        Analyze the ingested data.
        """
        if self.data['temperature'] > 30:
            return "Warning: High temperature"
        elif self.data['pressure'] < 3:
            return "Alert: Low pressure"
        else:
            return "Conditions are normal"

    def generate_report(self):
        """
        Generate a report of the current data and analysis.
        """
        analysis = self.analyze_data()
        report = f"Report for {self.physical_object.name}:\n"
        report += f"Temperature: {self.data['temperature']} C\n"
        report += f"Pressure: {self.data['pressure']} atm\n"
        report += f"Analysis: {analysis}\n"
        return report

# Example Usage
physical_obj = PhysicalObject("Pump1")
digital_twin = DigitalTwin(physical_obj)

# Simulating data updates and analysis
for _ in range(5):
    physical_obj.update_conditions()
    digital_twin.ingest_data()
    print(digital_twin.generate_report())
    time.sleep(1)

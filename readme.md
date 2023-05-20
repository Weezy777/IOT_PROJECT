# IoT Platform for Simple Appliance Control - Readme

This project aims to build an IoT platform for controlling simple appliances such as lighting fixtures (e.g., lamps, in-wall lighting) and cooling/heating appliances (e.g., fans, air conditioning units). The platform allows users to interact with the IoT devices through a web interface and provides features like time-based control, temperature-based control, presence detection, and combined logic.

## Requirements

To implement this IoT platform, the following components are required:

1. **Espressif ESP32 Development Module:** This module serves as the central sensor unit for the IoT platform.
2. **Appliances:** A lamp and a fan are connected to the ESP32 module and controlled through the platform.
3. **RESTful API:** A FastAPI-based Python framework is used to create a middle-man API that facilitates communication among all platform components.
4. **Software and Libraries:** Software and libraries are needed to enable the ESP32 module to control the connected appliances, communicate with connected sensors, and interact with the web API.
5. **Webpage:** A webpage is provided to allow users to remotely control and interact with the IoT devices.

## Features

The IoT platform includes several features to enhance control and automation of the connected appliances:

### 1. Time-based Control

Users can specify a time for the lights to turn on. The platform compares the current time to the user-specified time and only turns on the lights if the current time is later. Additionally, the platform can integrate a sunset API to determine the actual time of sunset for the user's location. This ensures that the lights are turned on at the appropriate time, whether the user sets a specific time or chooses the sunset option. This feature improves user experience and helps conserve energy.

### 2. Temperature-based Control

Users can set a temperature threshold for the fan to turn on. A temperature sensor connected to the ESP32 module measures the current room temperature. The platform compares the current temperature to the user-specified temperature and activates the fan if the current temperature exceeds the threshold. This feature provides automated control of the fan based on room temperature, improving comfort and energy efficiency.

### 3. Presence Detection

The platform incorporates a sensor, such as a passive infrared (PIR) sensor, to detect the presence of a person in the room. The PIR sensor detects changes in infrared radiation when a person moves within its field of view. The platform utilizes this information to determine whether to turn on the lights. By considering presence detection, the platform avoids unnecessary use of lights when no one is present in the room, further saving energy.

### 4. Combined Logic

The IoT platform combines temperature-based control, time-based control, and presence detection features to ensure appliances are activated only when relevant conditions are met. The platform checks both the current temperature and the presence sensor data before deciding whether to turn on the fan. Similarly, it checks both the current time and the presence sensor data before deciding whether to turn on the lights. By applying combined logic, the platform provides more intelligent and context-aware control of the appliances.

### 5. Customizable Settings

Users have the ability to customize various settings, such as the fan's temperature threshold and the time and duration for the lights to turn on. The web interface allows users to input their preferred values for these settings, tailoring the IoT platform to their specific needs. Customizable settings enhance user control, making the platform more effective and user-friendly.

### 6. Historical Sensor Data

The platform provides a request method that returns the most recent sensor readings from the IoT platform to the webpage. This data includes temperature readings and time spent in the room. The webpage can use this data to plot graphs, visualizing how the temperature has changed over time and how much
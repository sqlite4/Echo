# What is Echo?

Echo is a comprehensive application designed to monitor and display key statistics related to the performance of a server. The system is implemented in Python, utilizing the Flask web framework for creating a web interface. The monitored statistics include network traffic, CPU usage, and various server logs.

# Server Statistics:

The system collects and displays real-time data on sent and received network traffic, CPU usage, and other relevant server metrics.
This information is updated at one-second intervals, providing an accurate representation of the server's current state.
Port Status and Logs:

The application maintains a log of active ports along with their respective statuses (e.g., Running).
Each log entry includes the port number, status, and timestamp, offering insights into the operational status of different ports.

# IP Pool List:

The system keeps track of IP addresses associated with the server.
Whenever there is a change in the server's external IP address, the new IP is recorded along with a timestamp. This feature aids in monitoring IP address variations over time.
Web Interface:

The web interface provides a user-friendly dashboard with separate sections for each component.
Statistics are displayed in tabular form, allowing users to easily grasp the historical data and trends.
The use of color-coded badges (e.g., green for success, red for failure) enhances the visibility of status information.

# User Interaction:

Users can access the monitoring system through a web browser, interacting with the real-time and historical data.
The dashboard offers a clean and modern design, ensuring a positive user experience.

# Usage

The system is executed as a multi-threaded application, with one thread dedicated to running the Flask web server, and another handling the server monitoring tasks.
Threading allows the simultaneous execution of both components, ensuring a seamless user experience.
In summary, Echo is a powerful tool for server administrators, providing a visually appealing and intuitive platform for monitoring essential server statistics, port status, and IP address changes. Its modular design allows for easy expansion and customization based on specific monitoring needs.

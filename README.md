# Orange Pi Zero 3 Fan Control Script

This Python script provides a simple and effective way to control a cooling fan on an Orange Pi Zero 3 based on the CPU's temperature. It's designed to run as a background service, ensuring your system stays cool without manual intervention.

---

### **Features**

* **Temperature-Based Control:** Automatically turns the fan on and off based on configurable temperature thresholds.
* **GPIO-Driven:** Uses the `gpiod` library to interact with a specific GPIO pin on your Orange Pi Zero 3.
* **Lightweight:** A simple script with minimal overhead, perfect for running on a single-board computer.

---

### **Prerequisites**

To use this script, you will need:

* An **Orange Pi Zero 3** running a Linux-based operating system.
* A **fan** connected to **GPIO pin 78** (`gpiochip1`, line 78) on the 26-pin header.
* The `gpiod` Python library.

---

### **Installation**

#### **1. Install the `gpiod` library**

The script requires the `gpiod` library to interact with the GPIO pins. It's best to install this in your virtual environment.

```bash
cd /home/wan/
# Activate your virtual environment if you haven't already
source venv/bin/activate
pip install python-gpiod
```

#### **2. Place the Script**

Save the Python script as `fan_control_temp.py` in your home directory: `/home/wan/`.

#### **3. Create a Systemd Service**

To ensure the script runs automatically on boot, create a systemd service file.

Create a new file for the service:

```bash
sudo nano /etc/systemd/system/fan-control.service
```

Paste the following content into the file. Be sure to replace `/home/wan/` with your user's home path if it's different.

```
[Unit]
Description=Orange Pi Zero 3 Fan Control
After=network.target

[Service]
Type=simple
User=wan
ExecStart=/home/wan/venv/bin/python3 /home/wan/fan_control_temp.py
Restart=always

[Install]
WantedBy=multi-user.target
```

* `User=wan` should be set to your username.
* `ExecStart` points to the Python interpreter in your virtual environment and the script's location.

Save and exit the file (**Ctrl+X**, then **Y**, then **Enter**).

#### **4. Enable and Start the Service**

Enable the service to start automatically on boot and then start it manually for the first time.

```bash
sudo systemctl daemon-reload
sudo systemctl enable fan-control.service
sudo systemctl start fan-control.service
```

---

### **Configuration**

You can easily adjust the fan control logic by editing the following variables at the top of the `fan_control_temp.py` script:

* `FAN_ON_TEMP`: The temperature in Celsius at which the fan will turn on.
* `FAN_OFF_TEMP`: The temperature in Celsius at which the fan will turn off.
* `POLLING_INTERVAL`: The time in seconds between each temperature check.

After making changes, remember to restart the service:

```bash
sudo systemctl restart fan-control.service
```

---

### **Troubleshooting**

* **Permission denied error:** This usually happens if you try to run the script manually without `sudo`, or if the GPIO pins are in use. The systemd service runs with elevated privileges, so this shouldn't be an issue once the service is running.
* **Fan not turning on:** Check that your fan is correctly wired to GPIO pin 78 and that the temperature thresholds in the script are appropriate for your use case.

---

### **License**

This project is licensed under the MIT License.

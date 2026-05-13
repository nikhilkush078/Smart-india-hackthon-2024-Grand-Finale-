import tkinter as tk
import serial
import time
from threading import Thread

# Set up the serial connection
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)  # Replace 'COM3' with your Arduino port

# Tkinter setup
root = tk.Tk()
root.title("Arduino Voltage Reader")

# Label to display voltage
voltage_label = tk.Label(root, text="Voltage: -- V", font=("Helvetica", 16))
voltage_label.pack(pady=20)

def read_voltage():
    """Reads voltage data from Arduino and updates the Tkinter label."""
    while True:
        if arduino.in_waiting > 0:  # Check if there's data to read
            try:
                data = arduino.readline().decode('utf-8').strip()  # Read and decode the data
                voltage_label.config(text=f"Voltage: {data} V")  # Update the label
            except Exception as e:
                voltage_label.config(text="Error reading data")

# Run the serial reading in a separate thread
serial_thread = Thread(target=read_voltage)
serial_thread.daemon = True  # This ensures the thread will close when the main program exits
serial_thread.start()

# Run the Tkinter event loop
try:
    root.mainloop()
except KeyboardInterrupt:
    print("Program stopped")
    arduino.close()  # Close the serial connection

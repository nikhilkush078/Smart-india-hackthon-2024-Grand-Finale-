import tkinter as tk
from tkinter import ttk
import serial
import threading

# Configure the serial port (update with your Arduino's port)
ser = serial.Serial('COM11', 9600, timeout=1)

# Variables to track voltages
voltage_a0 = 0
voltage_a1 = 0
voltage_a3 = 0

# Function to read and display voltages
def read_voltages():
    global voltage_a0, voltage_a1, voltage_a3
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if data.startswith("A0:") and "A1:" in data and "A3:" in data:
                a0, a1, a3 = data.split(",")
                voltage_a0 = float(a0.split(":")[1])
                voltage_a1 = float(a1.split(":")[1])
                voltage_a3 = float(a3.split(":")[1])

                # Update voltage labels
                a0_voltage_label.config(text=f"A0 Voltage: {voltage_a0:.2f} V")
                a1_voltage_label.config(text=f"A1 Voltage: {voltage_a1:.2f} V")
                a3_voltage_label.config(text=f"A3 Voltage: {voltage_a3:.2f} V")

                # Update production/consumption status
                if voltage_a0 < 3.0:
                    status_label.config(text="Production", bg="#4CAF50")  # Green for production
                else:
                    status_label.config(text="Consumption", bg="#F44336")  # Red for consumption

# Function to send commands to Arduino
def send_command(command):
    ser.write(command.encode())

# Function to toggle button state
def toggle_button(button, command):
    if button["bg"] == "#4CAF50":  # If active (green)
        button.config(bg="#FF9800")  # Change to normal (orange)
        send_command(f'{command}0')  # Send deactivate command
    else:
        button.config(bg="#4CAF50")  # Change to active (green)
        send_command(f'{command}1')  # Send activate command

# Create the main GUI window
root = tk.Tk()
root.title("Arduino Control Panel")
root.geometry("800x700")
root.configure(bg="#2E2E2E")

# Voltage Display Frame
voltage_frame = tk.LabelFrame(root, text="Voltage Readings", font=("Arial", 14), bg="#2E2E2E", fg="white", padx=10, pady=10)
voltage_frame.pack(pady=10, fill="x")

a0_voltage_label = tk.Label(voltage_frame, text="A0 Voltage: 0.00 V", font=("Arial", 14), bg="#2E2E2E", fg="white")
a0_voltage_label.grid(row=0, column=0, sticky="w")

a1_voltage_label = tk.Label(voltage_frame, text="A1 Voltage: 0.00 V", font=("Arial", 14), bg="#2E2E2E", fg="white")
a1_voltage_label.grid(row=1, column=0, sticky="w")

a3_voltage_label = tk.Label(voltage_frame, text="A3 Voltage: 0.00 V", font=("Arial", 14), bg="#2E2E2E", fg="white")
a3_voltage_label.grid(row=2, column=0, sticky="w")

# Status Display Frame
status_frame = tk.LabelFrame(root, text="Production vs Consumption Status", font=("Arial", 14), bg="#2E2E2E", fg="white", padx=10, pady=10)
status_frame.pack(pady=10, fill="x")

status_label = tk.Label(status_frame, text="Status: Normal", font=("Arial", 16), bg="#FF9800", fg="white", width=30)
status_label.pack(pady=10)

# Motor Control Frame
motor_frame = tk.LabelFrame(root, text="Motor Controls", font=("Arial", 14), bg="#2E2E2E", fg="white", padx=10, pady=10)
motor_frame.pack(pady=10)

# Add motor control buttons
up_button = tk.Button(motor_frame, text="Up", width=10, height=2, bg="#4CAF50", fg="white")
up_button.grid(row=0, column=1, padx=10, pady=5)
up_button.bind("<ButtonPress>", lambda e: send_command('U'))
up_button.bind("<ButtonRelease>", lambda e: send_command('S'))

left_button = tk.Button(motor_frame, text="Left", width=10, height=2, bg="#4CAF50", fg="white")
left_button.grid(row=1, column=0, padx=10, pady=5)
left_button.bind("<ButtonPress>", lambda e: send_command('L'))
left_button.bind("<ButtonRelease>", lambda e: send_command('S'))

stop_button = tk.Button(motor_frame, text="Stop", width=10, height=2, bg="#F44336", fg="white", command=lambda: send_command('S'))
stop_button.grid(row=1, column=1, padx=10, pady=5)

right_button = tk.Button(motor_frame, text="Right", width=10, height=2, bg="#4CAF50", fg="white")
right_button.grid(row=1, column=2, padx=10, pady=5)
right_button.bind("<ButtonPress>", lambda e: send_command('R'))
right_button.bind("<ButtonRelease>", lambda e: send_command('S'))

down_button = tk.Button(motor_frame, text="Down", width=10, height=2, bg="#4CAF50", fg="white")
down_button.grid(row=2, column=1, padx=10, pady=5)
down_button.bind("<ButtonPress>", lambda e: send_command('D'))
down_button.bind("<ButtonRelease>", lambda e: send_command('S'))

# Rotor Lock Frame
rotor_frame = tk.LabelFrame(root, text="Rotor Lock", font=("Arial", 14), bg="#2E2E2E", fg="white", padx=10, pady=10)
rotor_frame.pack(pady=10, fill="x")

rotor_lock_button = tk.Button(rotor_frame, text="Rotor Lock", width=15, height=2, bg="#FF9800", fg="white")
rotor_lock_button.pack(pady=5)
rotor_lock_button.config(command=lambda: toggle_button(rotor_lock_button, 'K'))

# Additional Pins Control Frame
pins_frame = tk.LabelFrame(root, text="Control Pins (10-15)", font=("Arial", 14), bg="#2E2E2E", fg="white", padx=10, pady=10)
pins_frame.pack(pady=10, fill="x")

buttons = []
for i, pin in enumerate(range(10, 16)):
    button = tk.Button(pins_frame, text=f"Pin {pin}", width=10, height=2, bg="#FF9800", fg="white")
    button.grid(row=0, column=i, padx=5, pady=5)
    button.config(command=lambda b=button, p=pin: toggle_button(b, f'P{p}'))
    buttons.append(button)

# Start the voltage reading thread
thread = threading.Thread(target=read_voltages, daemon=True)
thread.start()

# Run the GUI
root.mainloop()

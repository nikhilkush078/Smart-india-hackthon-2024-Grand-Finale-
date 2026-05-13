import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb  # Modern themes
import serial
import threading

# Arduino communication setup
arduino_port = "COM3"  # Update with your Arduino's port
baud_rate = 9600

try:
    arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
except Exception as e:
    print(f"Error: Unable to connect to Arduino: {e}")

# Function to update sensor values
def update_sensor_values():
    while True:
        if arduino.is_open:
            try:
                line = arduino.readline().decode().strip()
                if line:
                    # Expected format: VOLTAGE,CURRENT,POWER,STATUS,POSITION,ENERGY,MOTOR_SPEED,GENERATOR_SPEED,LOCK
                    values = line.split(",")
                    if len(values) == 9:
                        voltage_var.set(f"{values[0]} V")
                        current_var.set(f"{values[1]} A")
                        power_var.set(f"{values[2]} W")
                        status_var.set(values[3])
                        position_var.set(values[4])
                        energy_var.set(f"{values[5]} J")
                        motor_speed_var.set(f"{values[6]} RPM")
                        generator_speed_var.set(f"{values[7]} RPM")
                        lock_status_var.set("Locked" if values[8] == "1" else "Unlocked")
            except Exception as e:
                print(f"Error reading data: {e}")

# Command functions for buttons
def send_command(command):
    if arduino.is_open:
        arduino.write(f"{command}\n".encode())

# GUI setup
root = tb.Window(themename="solar")
root.title("Renewable Energy Storage System Control Panel")
root.geometry("600x500")
root.resizable(False, False)

# Voltage, Current, Power Section
frame1 = ttk.LabelFrame(root, text="Electrical Readings", padding=10)
frame1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

voltage_var = tk.StringVar(value="--- V")
current_var = tk.StringVar(value="--- A")
power_var = tk.StringVar(value="--- W")

ttk.Label(frame1, text="Voltage:", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
ttk.Label(frame1, textvariable=voltage_var, font=("Arial", 12), foreground="blue").grid(row=0, column=1, sticky="w")
ttk.Label(frame1, text="Current:", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
ttk.Label(frame1, textvariable=current_var, font=("Arial", 12), foreground="blue").grid(row=1, column=1, sticky="w")
ttk.Label(frame1, text="Power:", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
ttk.Label(frame1, textvariable=power_var, font=("Arial", 12), foreground="blue").grid(row=2, column=1, sticky="w")

# Status, Position, Energy Section
frame2 = ttk.LabelFrame(root, text="System Status", padding=10)
frame2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

status_var = tk.StringVar(value="---")
position_var = tk.StringVar(value="---")
energy_var = tk.StringVar(value="--- J")

ttk.Label(frame2, text="Status:", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
ttk.Label(frame2, textvariable=status_var, font=("Arial", 12), foreground="green").grid(row=0, column=1, sticky="w")
ttk.Label(frame2, text="Position:", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
ttk.Label(frame2, textvariable=position_var, font=("Arial", 12), foreground="green").grid(row=1, column=1, sticky="w")
ttk.Label(frame2, text="Energy Stored:", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
ttk.Label(frame2, textvariable=energy_var, font=("Arial", 12), foreground="green").grid(row=2, column=1, sticky="w")

# Motor Speed, Generator Speed, Lock Status Section
frame3 = ttk.LabelFrame(root, text="Control Panel", padding=10)
frame3.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

motor_speed_var = tk.StringVar(value="--- RPM")
generator_speed_var = tk.StringVar(value="--- RPM")
lock_status_var = tk.StringVar(value="Locked")

ttk.Label(frame3, text="Motor Speed:", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
ttk.Label(frame3, textvariable=motor_speed_var, font=("Arial", 12), foreground="orange").grid(row=0, column=1, sticky="w")
ttk.Label(frame3, text="Generator Speed:", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
ttk.Label(frame3, textvariable=generator_speed_var, font=("Arial", 12), foreground="orange").grid(row=1, column=1, sticky="w")
ttk.Label(frame3, text="Safety Lock:", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
ttk.Label(frame3, textvariable=lock_status_var, font=("Arial", 12), foreground="red").grid(row=2, column=1, sticky="w")

# Control Buttons
button_frame = ttk.Frame(root, padding=10)
button_frame.grid(row=3, column=0, pady=10)
150
ttk.Button(button_frame, text="Start Motor", command=lambda: send_command("START_MOTOR"), bootstyle="success").grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Start Generator", command=lambda: send_command("START_GENERATOR"), bootstyle="success").grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="Lock Position", command=lambda: send_command("LOCK_POSITION"), bootstyle="primary").grid(row=1, column=0, padx=5)
ttk.Button(button_frame, text="Unlock Safety Lock", command=lambda: send_command("UNLOCK_SAFETY"), bootstyle="danger").grid(row=1, column=1, padx=5)

# Thread for sensor updates
sensor_thread = threading.Thread(target=update_sensor_values, daemon=True)
sensor_thread.start()

# Start GUI loop
root.mainloop()

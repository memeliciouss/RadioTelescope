import serial
import matplotlib.pyplot as plt
from collections import deque
import time
# pip intall pyserial matplotlib

# Configuration
SERIAL_PORT = 'COM7'  # Replace with your serial port
BAUD_RATE = 9600
MAX_DATA_POINTS = 100  # Number of data points to show on the graph

# Initialize serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# Initialize data storage
time_data = deque(maxlen=MAX_DATA_POINTS)
voltage_diff_data = deque(maxlen=MAX_DATA_POINTS)

# Initialize plot
plt.ion()  # Interactive mode on
fig, ax = plt.subplots()
line, = ax.plot(time_data, voltage_diff_data)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage Difference (V)')
ax.set_title('Voltage Difference Over Time')
ax.grid(True)

# Start time
start_time = time.time()

try:
    while True:
        # Read data from serial
        if ser.in_waiting > 0:
            try:
                # Read the line and decode it, ignoring invalid UTF-8 characters
                line_data = ser.readline().decode('utf-8', errors='ignore').strip()
                
                # Check if the line contains the voltage difference data
                if "Voltage Difference:" in line_data:
                    # Extract the voltage difference value
                    voltage_diff = float(line_data.split(": ")[1])
                    
                    # Calculate elapsed time
                    elapsed_time = time.time() - start_time
                    
                    # Append data to the deques
                    time_data.append(elapsed_time)
                    voltage_diff_data.append(voltage_diff)
                    
                    # Update the plot
                    line.set_xdata(time_data)
                    line.set_ydata(voltage_diff_data)
                    ax.relim()
                    ax.autoscale_view()
                    fig.canvas.draw()
                    fig.canvas.flush_events()
            except ValueError:
                print("Error parsing voltage difference value")
            except UnicodeDecodeError:
                print("Error decoding serial data (non-UTF-8 data)")
        
        # Small delay to prevent CPU overuse
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    ser.close()
    plt.ioff()
    plt.show()
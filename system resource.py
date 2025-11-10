import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create window
root = tk.Tk()
root.title("🖥️ System Resource Dashboard")
root.geometry("950x650")
root.config(bg="#1e1e1e")

# Matplotlib figure setup
fig, ax = plt.subplots(3, 1, figsize=(7, 6), facecolor="#f4f4f4")
plt.subplots_adjust(hspace=0.6)

# Lists to store data
cpu_usage, mem_usage, disk_usage = [], [], []
paused = False
current_view = "ALL"

# Function to update system metrics
def update_data():
    global paused
    if not paused:
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        cpu_usage.append(cpu)
        mem_usage.append(mem)
        disk_usage.append(disk)

        # Keep last 30 readings
        if len(cpu_usage) > 30:
            cpu_usage.pop(0)
            mem_usage.pop(0)
            disk_usage.pop(0)

        draw_chart()

    root.after(1000, update_data)  # refresh every 1 sec

# Function to draw chart
def draw_chart():
    for a in ax:
        a.clear()
        a.set_ylim(0, 100)
        a.grid(True, linestyle='--', alpha=0.6)

    # Draw based on selected view
    if current_view == "CPU":
        ax[0].plot(cpu_usage, color="#ff6600", marker='o')
        ax[0].set_title("CPU Usage (%)")

    elif current_view == "MEM":
        ax[1].plot(mem_usage, color="#0096FF", marker='o')
        ax[1].set_title("Memory Usage (%)")

    elif current_view == "DISK":
        ax[2].plot(disk_usage, color="#00cc66", marker='o')
        ax[2].set_title("Disk Usage (%)")

    else:  # ALL
        ax[0].plot(cpu_usage, color="#ff6600", marker='o')
        ax[0].set_title("CPU Usage (%)")
        ax[1].plot(mem_usage, color="#0096FF", marker='o')
        ax[1].set_title("Memory Usage (%)")
        ax[2].plot(disk_usage, color="#00cc66", marker='o')
        ax[2].set_title("Disk Usage (%)")

    canvas.draw()

# Functions for buttons
def show_cpu():
    global current_view
    current_view = "CPU"
    draw_chart()

def show_mem():
    global current_view
    current_view = "MEM"
    draw_chart()

def show_disk():
    global current_view
    current_view = "DISK"
    draw_chart()

def show_all():
    global current_view
    current_view = "ALL"
    draw_chart()

def toggle_pause():
    global paused
    paused = not paused
    if paused:
        pause_btn.config(text="▶ Resume", bg="#4CAF50")
    else:
        pause_btn.config(text="⏸ Pause", bg="#FF4500")

def reset_data():
    global cpu_usage, mem_usage, disk_usage
    cpu_usage, mem_usage, disk_usage = [], [], []
    draw_chart()

# UI Title
title = tk.Label(root, text="🖥️ System Resource Dashboard", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white")
title.pack(pady=10)

# Chart frame
chart_frame = tk.Frame(root, bg="#1e1e1e")
chart_frame.pack()

# Embed matplotlib in Tkinter
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.get_tk_widget().pack()

# Button Frame
button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=20)

# Buttons
btn_style = {"font": ("Arial", 11, "bold"), "width": 12, "pady": 5, "bd": 0, "relief": "ridge"}

cpu_btn = tk.Button(button_frame, text="CPU", command=show_cpu, bg="#ff6600", fg="white", **btn_style)
cpu_btn.grid(row=0, column=0, padx=5)

mem_btn = tk.Button(button_frame, text="Memory", command=show_mem, bg="#0096FF", fg="white", **btn_style)
mem_btn.grid(row=0, column=1, padx=5)

disk_btn = tk.Button(button_frame, text="Disk", command=show_disk, bg="#00cc66", fg="white", **btn_style)
disk_btn.grid(row=0, column=2, padx=5)

all_btn = tk.Button(button_frame, text="Show All", command=show_all, bg="#6A5ACD", fg="white", **btn_style)
all_btn.grid(row=0, column=3, padx=5)

pause_btn = tk.Button(button_frame, text="⏸ Pause", command=toggle_pause, bg="#FF4500", fg="white", **btn_style)
pause_btn.grid(row=0, column=4, padx=5)

reset_btn = tk.Button(button_frame, text="🔄 Reset", command=reset_data, bg="#808080", fg="white", **btn_style)
reset_btn.grid(row=0, column=5, padx=5)

# Start monitoring
update_data()

root.mainloop()

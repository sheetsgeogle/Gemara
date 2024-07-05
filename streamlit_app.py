import tkinter as tk
from tkinter import ttk
from pycalverter import Calverter

# Function to update the calendar based on selected month and year
def update_calendar():
    selected_month = month_var.get()
    selected_year = int(year_var.get())
    
    # Clear previous calendar display
    for widget in calendar_frame.winfo_children():
        widget.grid_forget()
    
    # Calculate and display new calendar
    cal = Calverter()
    hebrew_month_names = ['ניסן', 'אייר', 'סיון', 'תמוז', 'אב', 'אלול', 'תשרי', 'חשון', 'כסלו', 'טבת', 'שבט', 'אדר']
    hebrew_month = selected_month + 1  # pycalverter uses 1-based index for Hebrew months
    
    for day in range(1, 32):
        try:
            gregorian_date = cal.hebrew_to_jd(int(selected_year), hebrew_month, day)
            (year, month, day) = cal.jd_to_gregorian(gregorian_date)
            day_label = ttk.Label(calendar_frame, text=f'{day}', borderwidth=2, relief="ridge")
            day_label.grid(row=(day - 1) // 7, column=(day - 1) % 7)
        except ValueError:
            break

# Create main window
root = tk.Tk()
root.title("Hebrew Calendar")

# Create widgets
month_var = tk.IntVar(root)
year_var = tk.StringVar(root, value='5784')  # Initial Hebrew year example

# Month selection dropdown
month_label = ttk.Label(root, text="Month:")
month_label.pack()
month_dropdown = ttk.Combobox(root, textvariable=month_var, values=list(range(12)), state="readonly")
month_dropdown.pack()

# Year input
year_label = ttk.Label(root, text="Year:")
year_label.pack()
year_entry = ttk.Entry(root, textvariable=year_var)
year_entry.pack()

# Update calendar button
update_button = ttk.Button(root, text="Update Calendar", command=update_calendar)
update_button.pack()

# Frame for calendar display
calendar_frame = ttk.Frame(root)
calendar_frame.pack()

# Start GUI main loop
root.mainloop()

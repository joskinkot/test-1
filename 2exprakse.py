from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror

def changes(*args):
    for widget in right_frame.winfo_children():
        widget.destroy()
   
    global voltage_entry, current_entry, resistance_entry
   
    if lang.get() == "current":

        voltage_label = ttk.Label(right_frame, text="Voltage (V): ")
        voltage_label.pack()
        voltage_entry = ttk.Entry(right_frame)
        voltage_entry.pack()
       
        resistance_label = ttk.Label(right_frame, text="Resistance (Ω): ")
        resistance_label.pack()
        resistance_entry = ttk.Entry(right_frame)
        resistance_entry.pack()

    elif lang.get() == "voltage":

        current_label = ttk.Label(right_frame, text="Current (A): ")
        current_label.pack()
        current_entry = ttk.Entry(right_frame)
        current_entry.pack()
       
        resistance_label =ttk.Label(right_frame, text="Resistance (Ω): ")
        resistance_label.pack()
        resistance_entry = ttk.Entry(right_frame)
        resistance_entry.pack()
       
    elif lang.get() == "resistance":

        current_label =ttk.Label(right_frame, text="Current (A): ")
        current_label.pack()
        current_entry = ttk.Entry(right_frame)
        current_entry.pack()
       
        voltage_label =ttk.Label(right_frame, text="Voltage (V): ")
        voltage_label.pack()
        voltage_entry = ttk.Entry(right_frame)
        voltage_entry.pack()
       
def calculate():
    try:
        for widget in result_frame.winfo_children():
            widget.destroy()
   
        if lang.get() == "current":
            voltage = float(voltage_entry.get())
            resistance = float(resistance_entry.get())
            current = voltage / resistance
            result_text = f"Current = {current:.2f} A"
       
        elif lang.get() == "voltage":
            current = float(current_entry.get())
            resistance = float(resistance_entry.get())
            voltage = current * resistance
            result_text = f"Voltage = {voltage:.2f} V"
           
        elif lang.get() == "resistance":
            current = float(current_entry.get())
            voltage = float(voltage_entry.get())
            resistance = voltage / current
            result_text = f"Voltage = {resistance:.2f} Ω"
   
        res_label = ttk.Label(result_frame, text=result_text)
        res_label.pack()
   
    except ValueError:
        showerror ("Error, incorrect input")
       
def reset():
   
    for widget in right_frame.winfo_children():
        if isinstance(widget, ttk.Entry):
            widget.delete(0, END)
           
    for widget in result_frame.winfo_children():
        widget.destroy()
        
root = Tk()
root.title ("Ohm's Law")
root.geometry("600x300+500+300")


#photo = PhotoImage(file="triangle.png")
#smaller_photo = photo.subsample(2, 2)
#img = Label(root, image=smaller_photo)
#img.place(x=120 ,y=80)

calc_btn = ttk.Button(text="Calculate", command=calculate)
calc_btn.place(x=150 ,y= 250)

reset_btn = ttk.Button(text ="Reset", command=reset)
reset_btn.place(x=400 , y= 250)

lang = StringVar(value="current")

right_frame = ttk.Frame(root)
right_frame.place(x=420, y=65)

result_frame = ttk.Frame(root)
result_frame.place(x=220, y=20)

header = ttk.Label(root, textvariable=lang)

current_btn = ttk.Radiobutton(text="current",value="current",variable=lang)
current_btn.place(x=40,y=75)
voltage_btn =ttk.Radiobutton(text="voltage",value="voltage",variable=lang)
voltage_btn.place(x=40,y=150)
resistance_btn = ttk.Radiobutton(text="resistance",value="resistance",variable=lang)
resistance_btn.place(x=40,y=225)

lang.trace_add("write", changes)

changes()

root.mainloop()

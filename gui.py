import cocotb
from cocotb.triggers import Timer
from cocotb_tools.runner import get_runner
import time
import tkinter as tk


clock_freq = 1    # Hz
clocktime = 1/clock_freq


window = tk.Tk()
window.title("Reaction Game")
window.geometry("400x400")
screen = tk.Frame(window)
screen.grid(row=0, column=0)

begin = False
open = True
btn_press = 0

# verilog simulation
@cocotb.test()
async def gui(dut):
    while not begin and open:
        screen.update()

    await init_counter(dut)
    
    while open:
        await count_up(dut)

        count = dut.count.value
        update_circles(count)

        current = time.time()
        while time.time() < current + clocktime:
            dut.btn.value = btn_press
            await Timer(2, unit="ns")

            green = dut.green.value
            red = dut.red.value

            update_results(green, red)

            screen.update()
            time.sleep(0.01)
    
    window.destroy()



# initialize counter to 000
async def init_counter(dut):
    dut.clk.value = 0
    dut.rst.value = 1

    await Timer(2, unit="ns")

    dut.clk.value = 1

    await Timer(2, unit="ns")

    dut.clk.value = 0
    dut.rst.value = 0

# one clock cycle
async def count_up(dut):
    dut.clk.value = 0
    await Timer(2, unit="ns")

    dut.clk.value = 1        
    await Timer(2, unit="ns")

# start button
def set_begin(event):
    global begin
    begin = True

# button
def on_press(event):
    setbtn(1)
    click_ind.pack()

def on_release(event):
    setbtn(0)
    click_ind.pack_forget()

def setbtn(state):
    global btn_press
    btn_press = state

# window closed
def on_closing():
    global open
    open = False

# update circles for counter
def update_circles(q):
    for i in range(3):
        fill_color = "green" if q[2-i] else "gray"
        counter_canvas.itemconfig(count_disp[i], fill=fill_color)
    count_text.config(text=str(int(q)))

# update red & green LED
def update_results(green_output, red_output):
    greenLED_color = "green" if green_output else "gray"
    redLED_color = "red" if red_output else "gray"
    results_canvas.itemconfig(green_led, fill=greenLED_color)
    results_canvas.itemconfig(red_led, fill=redLED_color)


counter_canvas = tk.Canvas(screen, width=400, height=150)
counter_canvas.pack()
count_disp = []
for i in range(3):
    circle = counter_canvas.create_oval(25+125*i, 25, 125+125*i, 125, fill="gray")
    count_disp.append(circle)
count_text = tk.Label(screen, text="0", fg="blue", font=("Arial", 14))
count_text.pack()

results_canvas = tk.Canvas(screen, width=275, height = 150)
results_canvas.pack()
red_led = results_canvas.create_oval(25, 25, 125, 125, fill="gray")
green_led = results_canvas.create_oval(150, 25, 250, 125, fill="gray")

window.bind("<space>", set_begin)

screen.bind("<Button-1>", on_press)
screen.bind("<ButtonRelease-1>", on_release)
click_ind = tk.Label(screen, text="Clicked!", fg="black", font=("Arial", 14))

window.protocol("WM_DELETE_WINDOW", on_closing)
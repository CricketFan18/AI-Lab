import tkinter as tk
import tkinter.font as tkFont

def calculate(operator):
    try:
        a = float(inputA.get())
        b = float(inputB.get())
        res = 0.0
        
        if operator == '+':
            res = a + b
        elif operator == '-':
            res = a - b
        elif operator == '*':
            res = a * b
        elif operator == '/':
            if b != 0:
                res = a / b
            else:
                label_result.config(text="Result = Error (Div by 0)")
                return
                
        label_result.config(text="Result = " + str(round(res, 2)))
        
    except ValueError:
        label_result.config(text="Result = Invalid Input")

root = tk.Tk()
print(tkFont.families())
root.title("Calculator Agent")
root.geometry("600x800")
default_font = ("times",20,"bold")
entry_font = default_font

labelA = tk.Label(root, text="Enter first Number", font=default_font)
labelA.pack(pady=(20, 5))

inputA = tk.Entry(root, font=entry_font) 
inputA.pack(pady=5)

labelB = tk.Label(root, text="Enter second Number", font=default_font)
labelB.pack(pady=(20, 5))

inputB = tk.Entry(root, font=entry_font) 
inputB.pack(pady=5)

labelChoose = tk.Label(root, text="Select Operator", font=default_font)
labelChoose.pack(pady=(20, 10))

button_add = tk.Button(root, text="+", command=lambda: calculate('+'), font=default_font, width=5, bg="red")
button_add.pack(pady=5)

button_sub = tk.Button(root, text="-", command=lambda: calculate('-'), font=default_font, width=5, bg="blue")
button_sub.pack(pady=5)

button_mul = tk.Button(root, text="*", command=lambda: calculate('*'), font=default_font, width=5, bg="yellow")
button_mul.pack(pady=5)

button_div = tk.Button(root, text="/", command=lambda: calculate('/'), font=default_font, width=5, bg="green")
button_div.pack(pady=5)

label_result = tk.Label(root, text="Result = ", font=default_font, fg="blue")
label_result.pack(pady=20)

root.mainloop()
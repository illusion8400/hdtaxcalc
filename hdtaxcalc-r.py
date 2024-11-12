
""" HD TAX CALCULATOR"""
import tkinter as tk
import tktooltip as tktool
import sys

class Version():
    def __init__(self):
        self.version = "2.1"
version = Version()

def main(entry1, entry2, entry3, checkbox1):
    try:
        count = 0
        # Entry 1-3
        # entry1 amounts
        amounts = entry1
        amounts = amounts.split()
        # entry3 total
        if entry3:
            total = entry3
        else:
            total = 0
        # entry2 taxes
        if checkbox1:
            tax_percent = (float(entry2) / (float(entry3) - float(entry2))) * 100
        else:
            tax_percent = entry2
        tax_percent = float(tax_percent) / 100
        amounts_with_tax = []
        print("***")
        for x in amounts:
            count += 1
            amount_of_tax_for_item = float(x) * float(tax_percent)
            amt_with_tax = float(x) + float(amount_of_tax_for_item)
            amounts_with_tax.append(float(amt_with_tax))
            print(f"{count}: ${float(x):.2f} + ${round(amount_of_tax_for_item, 2):.2f} = ${round(amt_with_tax, 2):.2f}")
        # END continue
        print (f"\nTotal input: ${total}")
        print(f"Total added: ${round(sum(amounts_with_tax), 2):.2f}")
        if checkbox1:
            print(f"Tax Percent: {round(tax_percent * 100, 2):.2f}%  Tax Total: ${entry2}")
        else:
            print(f"Tax Percent: {round(tax_percent * 100, 2):.2f}%")
        difference_calc = float(total) - float(round(sum(amounts_with_tax), 2))
        print(f"Difference(input-added=): ${round(difference_calc, 2):.2f}\n")        
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(e)

class App:
    def __init__(self, root):
        # Minimal tkinter app
        self.root = root
        self.root.title(f"HD Tax Calculator - v{version.version}")
        self.root.minsize(400, 600)
        self.root.maxsize(400,600)
        # Entry box; input
        self.title_label = tk.Label(self.root, text="Enter each amount with a space in between.")
        self.title_label.pack(side="top")
        # Amounts
        self.entry1_label = tk.Label(self.root, text="Amounts: ")
        self.entry1_label.place(x=20, y=30)
        self.entry1 = tk.Entry(self.root)
        self.entry1.pack(pady=5, side="top")
        # Taxes
        self.entry2_label = tk.Label(self.root, text="Tax Percent: ")
        self.entry2_label.place(x=20, y=65)
        self.entry2 = tk.Entry(self.root)
        self.entry2.pack(pady=5, side="top")
        # Total
        self.entry3_label = tk.Label(self.root, text="Total Invoice: ")
        self.entry3_label.place(x=20, y=100)
        self.entry3 = tk.Entry(self.root)
        self.entry3.pack(pady=5, side="top")
        # Add check box for total tax
        self.checkbox1_var = tk.IntVar()
        self.checkbox1 = tk.Checkbutton(self.root, text="Tax Total", variable=self.checkbox1_var, onvalue=1,offvalue=0)
        self.checkbox1.place(x=300,y=65)
        self.checkbox1_tip = tktool.ToolTip(self.checkbox1, "Calculate tax percentage by inputting total tax")
        # We add a button to test our setup
        self.go_button = tk.Button(self.root, text="Go", command=lambda: main(self.entry1.get(), self.entry2.get(), self.entry3.get(), self.checkbox1_var.get()))
        self.go_button.pack(side="top")
        # Add windows where we are going to write the std output. 
        self.console_text = tk.Text(self.root, state='disabled', height=10)
        self.console_text.pack(expand=True, fill='both')
        # Bind return and keypad enter key to function
        self.root.bind('<Return>', lambda x: main(self.entry1.get(), self.entry2.get(), self.entry3.get(), self.checkbox1_var.get()))
        self.root.bind('<KP_Enter>', lambda x: main(self.entry1.get(), self.entry2.get(), self.entry3.get(), self.checkbox1_var.get()))
        # We redirect sys.stdout -> TextRedirector
        self.redirect_sysstd()

    def redirect_sysstd(self):
        # We specify that sys.stdout point to TextRedirector
        sys.stdout = TextRedirector(self.console_text, "stdout")
        sys.stderr = TextRedirector(self.console_text, "stderr")
    
class TextRedirector(object):
    def __init__(self, widget, tag):
        self.widget = widget
        self.tag = tag

    def write(self, text):
        self.widget.configure(state='normal') # Edit mode
        self.widget.insert(tk.END, text, (self.tag,)) # insert new text at the end of the widget
        self.widget.configure(state='disabled') # Static mode
        self.widget.see(tk.END) # Scroll down 
        self.widget.update_idletasks() # Update the console

    def flush(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
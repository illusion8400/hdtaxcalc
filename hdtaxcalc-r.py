
""" HD TAX CALCULATOR"""
import tkinter as tk
import sys
import time

class Version():
    def __init__(self):
        self.version = "2.0-r"
version = Version()

def main(entry1, entry2, entry3):
    try:
        count = 0
        # Entry 1-3
        amounts = entry1
        amounts = amounts.split()
        tax_percent = entry2
        tax_percent = float(tax_percent) / 100
        if entry3:
            total = entry3
        else:
            total = 0
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
        self.root.minsize(300, 600)
        # Entry box; input
        self.title_label = tk.Label(self.root, text="Enter each amount with a space in between.")
        self.title_label.pack(side="top")
        # Amounts
        self.entry1_label = tk.Label(self.root, text="Amounts: ")
        self.entry1_label.place(x=155, y=25)
        self.entry1 = tk.Entry(self.root)
        self.entry1.pack(pady=5)
        # Taxes
        self.entry2_label = tk.Label(self.root, text="Tax Percent: ")
        self.entry2_label.place(x=155, y=55)
        self.entry2 = tk.Entry(self.root)
        self.entry2.pack(pady=5)
        # Total
        self.entry3_label = tk.Label(self.root, text="Total Invoice: ")
        self.entry3_label.place(x=155, y=85)
        self.entry3 = tk.Entry(self.root)
        self.entry3.pack(pady=5)
        # We add a button to test our setup
        self.go_button = tk.Button(self.root, text="Go", command=lambda: main(self.entry1.get(), self.entry2.get(), self.entry3.get()))
        self.go_button.pack()
        # Add windows where we are going to write the std output. 
        self.console_text = tk.Text(self.root, state='disabled', height=10)
        self.console_text.pack(expand=True, fill='both')
        # Bind return and keypad enter key to function
        self.root.bind('<Return>', lambda x: main(self.entry1.get(), self.entry2.get(), self.entry3.get()))
        self.root.bind('<KP_Enter>', lambda x: main(self.entry1.get(), self.entry2.get(), self.entry3.get()))
        # We redirect sys.stdout -> TextRedirector
        self.redirect_sysstd()

    def redirect_sysstd(self):
        # We specify that sys.stdout point to TextRedirector
        sys.stdout = TextRedirector(self.console_text, "stdout")
        sys.stderr = TextRedirector(self.console_text, "stderr")

    def test_text_redirection(self):
        for x in range(10):
            print(x+1)
            time.sleep(1)
    
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
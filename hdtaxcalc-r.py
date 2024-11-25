
""" HD TAX CALCULATOR"""
import requests
import tkinter as tk
from tkinter import ttk
import tktooltip as tktool
import sys
from ttkthemes import ThemedTk

class Version():
    def __init__(self):
        self.version = "2.3.1"
version = Version()

def main(entry1, entry2, entry3, checkbox1):
    try:
        count = 0
        # Entry 1-3
        # entry1 amounts
        amounts = entry1
        amounts = amounts.split("+") if "+" in amounts else amounts.split()
        # entry2 taxes
        tax_percent = (float(entry2) / (float(entry3) - float(entry2))) * 100 if checkbox1 else entry2
        tax_percent = float(tax_percent) / 100
        # entry3 total
        total = entry3 if entry3 else 0
        # lists
        amounts_with_tax = []
        tax_list = []
        ###
        print("***")
        # start calc
        for x in amounts:
            count += 1
            amount_of_tax_for_item = float(x) * float(tax_percent)
            amt_with_tax = float(x) + float(amount_of_tax_for_item)
            amounts_with_tax.append(float(amt_with_tax))
            tax_list.append(amount_of_tax_for_item)
            print(f"{count}: ${float(x):.2f} + ${amount_of_tax_for_item:.2f} = ${amt_with_tax:.2f}")
        difference_calc = float(total) - float(sum(amounts_with_tax))
        # end calc
        print (f"\nTotal input: ${float(total):.2f}")
        print(f"Total added: ${sum(amounts_with_tax):.2f}")
        if checkbox1:
            print(f"Tax Percent: {tax_percent * 100:.2f}%  Tax Total: ${float(entry2)}")
        else:
            print(f"Tax Percent: {tax_percent * 100:.2f}%  Tax Total: ${sum(tax_list):.4f}")
        print(f"Difference(input-added=): ${difference_calc:.2f}\n")
    except ValueError:
        print("Bad Input")
    except Exception as e:
        print(e)

def about():
    print("***")
    print(f"HDTAXCALC v{version.version}\nNov 2024 - illusion")
    print(f"https://github.com/illusion8400/hdtaxcalc\n")
    try:
        print("Checking for updates...")
        url = "https://api.github.com/repos/illusion8400/hdtaxcalc/releases/latest"
        latest_release = requests.get(url)
        latest_release_git = latest_release.json()["name"]
        if latest_release_git == f"v{version.version}":
            print(f"Current version up to date\n")
        else:
            print(f"***New version available!***")
            print(f"Current version from github: {latest_release_git}\n")
            print(f"{latest_release.json()["assets"][1]["browser_download_url"]}")
            print(f"{latest_release.json()["assets"][0]["browser_download_url"]}\n")

    except Exception as e:
        print(e)

def clear_boxes(self):
    self.entry1.delete(0, 'end')
    self.entry2.delete(0, 'end')
    self.entry3.delete(0, 'end')

def clear_all(self):
    clear_boxes(self)
    self.console_text.configure(state='normal')
    self.console_text.delete("1.0", tk.END)
    self.console_text.configure(state='disable')

class App:
    def __init__(self, root):
        # Minimal tkinter app
        self.root = root
        self.root.title(f"HD Tax Calculator - v{version.version}")
        self.root.minsize(400, 700)
        self.root.maxsize(400, 800)
        # Entry box; input
        self.title_label = tk.Label(self.root, text="Enter each amount with a plus or space in between.")
        self.title_label.pack(side="top")
        self.title_label.configure(bg='lightblue')
        # Amounts
        self.entry1_label = tk.Label(self.root, text="Amounts: ")
        self.entry1_label.place(x=20, y=30)
        self.entry1_label.configure(bg='lightblue')
        self.entry1 = ttk.Entry(self.root)
        self.entry1.pack(pady=5, side="top")
        # Taxes
        self.entry2_label = tk.Label(self.root, text="Tax Percent: ")
        self.entry2_label.place(x=20, y=65)
        self.entry2_label.configure(bg='lightblue')
        self.entry2 = ttk.Entry(self.root)
        self.entry2.pack(pady=5, side="top")
        # Total
        self.entry3_label = tk.Label(self.root, text="Total Invoice: ")
        self.entry3_label.place(x=20, y=100)
        self.entry3_label.configure(bg='lightblue')
        self.entry3 = ttk.Entry(self.root)
        self.entry3.pack(pady=5, side="top")
        # Total Tax Checkbox
        self.checkbox1_var = tk.IntVar()
        self.checkbox1 = tk.Checkbutton(self.root, text="Tax Total", variable=self.checkbox1_var, onvalue=1,offvalue=0)
        self.checkbox1.configure(bg='lightblue')
        self.checkbox1.place(x=300,y=65)
        self.checkbox1_tip = tktool.ToolTip(self.checkbox1, "Calculate tax percentage by inputting total tax in dollar amount")
        self.checkbox1.select()
        # Go Button
        self.go_button = ttk.Button(self.root, text="Go", command=lambda: main(self.entry1.get(), self.entry2.get(), self.entry3.get(), self.checkbox1_var.get()))
        self.go_button.pack(side="top")
        # Clear Input
        self.clear_button = ttk.Button(self.root, text="Clear Input", command=lambda: clear_boxes(self))
        self.clear_button.place(x=300,y=95)
        # Clear All
        self.clear_all_button = ttk.Button(self.root, text="Clear All", command=lambda: clear_all(self))
        self.clear_all_button.place(x=280,y=129)
        # About
        self.about_button = ttk.Button(self.root,text="?", command=about)
        self.about_button.place(x=360, y=129)
        # STD OUTPUT - CONSOLE_TEXT
        self.console_text = tk.Text(self.root, state='disabled', height=10)
        self.console_text.pack(expand=True, fill='both')
        # Bind return and keypad enter key to function
        self.root.bind('<Return>', lambda x: main(self.entry1.get(), self.entry2.get(), self.entry3.get(), self.checkbox1_var.get()))
        self.root.bind('<KP_Enter>', lambda x: main(self.entry1.get(), self.entry2.get(), self.entry3.get(), self.checkbox1_var.get()))
        # Redirect out
        self.redirect_sysstd()

    def redirect_sysstd(self):
        # Pit stop
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
    # root = tk.Tk()
    root = ThemedTk(theme='blue')
    root.configure(bg='lightblue')
    app = App(root)
    root.mainloop()
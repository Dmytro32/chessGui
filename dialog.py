import tkinter as tk
import tkinter.simpledialog
class ChoicePopup:
    def __init__(self,master):
        self.top =tk.Toplevel(master)
        self.top.geometry("250x150")
        self.top.resizable(False, False)
        self.master = master
        self.top.title("Promotion")
        choices=["q","r","b","n",]
        tk.Label(self.top, text= "Choose piece:").pack(pady=10)
        
        self.choice_var = tk.StringVar(self.top)
        self.choice_var.set(choices[0] )  # Set default selection
        
        self.option_menu = tk.OptionMenu(self.top, self.choice_var, *choices)
        self.option_menu.pack(pady=5)
        
        self.ok_button = tk.Button(self.top, text="OK", command=self.on_ok)
        self.ok_button.pack(pady=10)
        self.selected_choice=None
        
    def on_ok(self):
        self.selected_choice = self.choice_var.get()
        self.top.destroy()
    
    @staticmethod
    def get_choice(master):
        choice=ChoicePopup(master)
        choice.top.wait_window()

        return choice.selected_choice 



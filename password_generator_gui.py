import tkinter as tk
from tkinter import messagebox
import string
import secrets
from datetime import datetime

current_password = ""

def generate_password(lenght, use_numbers, use_symbols):
    password_chars = []
    
    password_chars.append(secrets.choice(string.ascii_letters))
    
    if use_numbers:
        password_chars.append(secrets.choice(string.digits))
    if use_symbols:
        password_chars.append(secrets.choice(string.punctuation))
    
    characters = string.ascii_letters
    
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
        
    while len(password_chars) < lenght:
        password_chars.append(secrets.choice(characters))
        
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def check_strenght(password):
      
    score = 0 
    if len(password) >= 8:
        score += 1
    if any(char.islower() for char in password):
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(not char.isalnum() for char in password):
        score += 1
        
    if score <= 2:
        return "Weak"
    if score == 3:
        return "Medium"
    if score == 4:
        return "Strong"
    else:
        return "Very Strong"


def generate_gui_password():
    global current_password
    try:
        lenght = lenght_var.get()
        if lenght < 4:
            status_label.config(text="Lenght must be atleast 4")
            return
        
        password = generate_password(lenght, use_number.get(), use_symbol.get())
        current_password = password
        password_label.config(text=password)
        strenght = check_strenght(password)
        strenght_label.config(text=f"Strenght: {strenght}")
        status_label.config(text="")
    except ValueError:
        password_label.config(text="Password Lenght must be greater than 7")


def copy_password():
    if current_password:
        root.clipboard_clear()
        root.clipboard_append(current_password)
        status_label.config(
            text="Copied to Clipboard" )


def save_password():
    if not current_password:
        status_label.config(text=f"[!] There is no password to save")
        return
    strenght = check_strenght(current_password)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("password.txt", "a") as file:
        file.write(f"{timestamp} \n")
        file.write(f"{current_password} \n")
        file.write(f"strenght: {strenght}\n\n")
        status_label.config(text="password saved") 
        

def create_widgets():
    global lenght_var
    global lenght_entry
    global password_label
    global strenght_label
    global status_label
    global tittle_label
    global use_number
    global use_symbol
    global lenght_scale
    
    main_frame = tk.Frame(
        root,
        bg="#2C3E50"
    )
    main_frame.pack(
        padx=20,
        pady=20
    )
    
    
    tittle_label = tk.Label(
    main_frame,
    text="Password Generator",
    font=("Arial", 16, "bold"),
    bg="#2C3E50",
    fg="white")
    tittle_label.pack(pady=10)

    form_frame = tk.Frame(main_frame,
                          bg="#34495E")
    form_frame.pack()


    lenght_label = tk.Label(
        form_frame,
        text="Password Lenght:",
        bg="#2C3E50",
        fg="white")
    lenght_label.grid(
        row=0,
        column=0,
        padx=5,
        pady=5
    )

    lenght_var = tk.IntVar(
    value=12)
    lenght_scale = tk.Scale(
        form_frame,
        from_=4,
        to=64,
        orient="horizontal",
        variable=lenght_var,
        bg="#34495E",
        fg="white"
    )
    lenght_scale.grid(
        row=0,
        column=1,
        padx=5,
        pady=5
    )


    use_number = tk.BooleanVar()
    use_symbol = tk.BooleanVar()


    number_checkbox = tk.Checkbutton(
        form_frame,
        text= "Include Number",
        variable=use_number,
        fg="#3498DB",
        bg="#34495E")
    number_checkbox.grid(
        row=1,
        column=0,
        columnspan=2,
        sticky="w",
        padx=5,
        pady=5
    )


    symbol_checkbox = tk.Checkbutton(
        form_frame,
        text="Include Symbols",
        variable=use_symbol,
        fg="#3498DB",
        bg="#34495E")
    symbol_checkbox.grid(
        row=2,
        column=0,
        columnspan=2,
        sticky="w",
        padx=5,
        pady=5
    )

        
    generate_button = tk.Button(
        form_frame,
        text="Generate",
        command=generate_gui_password,
        bg="#3498DB",
        fg="white")
    generate_button.grid(
        row=3,
        column=0,
        padx=5,
        pady=10
    )


    copy_button = tk.Button(
        form_frame,
        text="copy password",
        command=copy_password,
        fg="white",
        bg="#F39C12"
    )
    copy_button.grid(
        row=3,
        column=1,
        padx=5,
        pady=10
    )

    save_button = tk.Button(
        form_frame,
        text="Save password",
        command=save_password,
        fg="white",
        bg="#3498DB"
    )
    save_button.grid(
        row=4,
        column=0,
        columnspan=2,
        pady=5
    )

    password_label = tk.Label(
        main_frame,
        text="Generated passwords will apear here",
        wraplength=300,
        bg="#34495E",
        fg="white")
    password_label.pack(pady=10)


    strenght_label = tk.Label(
        main_frame,
        text="Strenght: ",
        bg="#34495E",
        fg="white"
    )
    strenght_label.pack()


    status_label = tk.Label(
        main_frame,
        text="",
        bg="#34495E",
        fg="white"
    )
    status_label.pack()
    
   
def show_about():
    messagebox.showinfo(
        "About\n",
        "Password Generator v2.1 \n\nCreated by EmmanuelPYDev\n"
        "Features: \n"
        "- Password Generation\n"
        "- Strenght Analysis\n"
        "- Clipboard copy\n"
        "- Password History \n"
        "- GUI Interface"
        
    )

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Password History")
    history_window.geometry("500x400")
    history_window.resizable(False,
                             False)
    
    scrollbar = tk.Scrollbar(
        history_window,
    )
       
    text_area = tk.Text(
        history_window,
        wrap="word",
        yscrollcommand=scrollbar.set
    )
    
    scrollbar.config(
        command=text_area.yview)
    scrollbar.pack(
        side="right",
        fill="y"
    )
    
    text_area.pack(
        side="left",
        fill="both",
        expand=True
    )
    
    try:
        with open("password.txt", "r") as file:
            content = file.read()
            text_area.insert("1.0", content)
    except FileNotFoundError:
        text_area.insert(
            "1.0", "No saved passwords found"
        )
        
    text_area.config(state="disabled")

def main():
    global root
    
    root = tk.Tk()
    root.config(bg="#2C3E50")
    root.resizable(
        False,
        False
    )
    
    menu_bar = tk.Menu(root)
    root.config(menu= menu_bar)
    
    file_menu = tk.Menu(
        menu_bar,
        tearoff=0)
    menu_bar.add_cascade(
        label="File",
        menu=file_menu)
    file_menu.add_command(
        label="View History",
        command=show_history,)
    file_menu.add_command(
        label= "Exit",
        command=root.quit
    )
    
    help_menu = tk.Menu(
        menu_bar,
        tearoff= 0)
    menu_bar.add_cascade(
        label= "Help",
        menu=help_menu)
    help_menu.add_command(
        label="About",
        command=show_about
    )
    
    root.title("Password Generator")
    root.geometry("600x500")
    
    create_widgets()
    
    root.mainloop()
    
if __name__ == "__main__":
    main()
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q',
               'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for char in range(nr_letters)]
    password_list.extend(random.choice(symbols) for char in range(nr_symbols))
    password_list.extend(random.choice(numbers) for char in range(nr_numbers))

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    new_data = {
        website_entry.get(): {
            "email": email_entry.get(),
            "password": password_entry.get()
        }
    }
    if website_entry.get() == "" or password_entry.get() == "":
        messagebox.showinfo(title="Oops", message="Please , don't leave any fields empty!")

    elif messagebox.askokcancel(title=website_entry.get(),
                                message=f"These are details entered: \nEmail: {email_entry.get()} \n"
                                        f"Password: {password_entry.get()} \nIs it ok to save?"):
        try:
            with open("data.json", "r") as data_file:
            # json.dump(data_dict, data, indent=4)
            # data.write(f"{website_entry.get()} | {email_entry.get()} | {password_entry.get()}\n")
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            email = data[website]['email']
            password = data[website]['password']

    except KeyError:
        messagebox.showinfo(title=website, message=f"No details for this website exists.")
    else:
        messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password}")
        website_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entry
website_entry = Entry(width=21)
website_entry.grid(row=1, sticky=W, column=1, columnspan=2)
website_entry.focus()

email_entry = Entry(width=40)
email_entry.grid(row=2, column=1, columnspan=2, sticky=W)
email_entry.insert(0, 'agata.kabot@vp.pl')

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky=W)

# Buttons
password_button = Button(text='Generate Password', width=15, command=generate_password)
password_button.grid(row=3, column=1, columnspan=2, sticky=E)

add_button = Button(text="Add", width=34, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky=W)

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=1, column=1, columnspan=2, sticky=E)

window.mainloop()

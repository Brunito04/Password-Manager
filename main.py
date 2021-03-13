from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_letters + password_symbols
    shuffle(password_list)

    password = "".join(password_list)

    if len(password) == 0:
        password_entry.insert(0, password)
        pyperclip.copy(password)
    else:
        password_entry.delete(0, END)
        password_entry.insert(0, password)
        pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    # Blank spaces left
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Ooops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("Data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("Data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("Data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


# ---------------------------- Find Password ----------------------------#

def find_password():
    website = website_entry.get()

    if len(website) == 0:
        messagebox.showwarning(title="Ooops", message="Enter a website to search!")
    else:
        try:
            with open("Data.json") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File found")
        else:
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=f"{website} (password copied to clipboard)", message=f"email: {email} \npassword: {password}")
                pyperclip.copy(password)
            else:
                messagebox.showinfo(title="Error", message=f"No info for {website}, please try again")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=15, pady=30, bg="#eae3c8")

canvas = Canvas(height=200, width=200, bg="#eae3c8", highlightthickness=0)
logo_img = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels -----------------------------------------------------------------
website_label = Label(text="Website:", bg="#eae3c8")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:", bg="#eae3c8")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:", bg="#eae3c8")
password_label.grid(row=3, column=0)

# Entries -------------------------------------------------------------
website_entry = Entry(width=35, bg="#cfc5a5")
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
website_entry.insert(0, "")

email_entry = Entry(width=35, bg="#cfc5a5")
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "bruno2004b@gmail.com")

password_entry = Entry(width=35, bg="#cfc5a5")
password_entry.grid(row=3, column=1, columnspan=2)
password_entry.insert(0, "")

# Buttons
generate_password_button = Button(text="Generate", width=7, bg="#a1cae2", highlightthickness=0, command=generate_password)
generate_password_button.grid(row=3, column=3)

add_button = Button(text="Add", width=29, bg="#a1cae2", highlightthickness=0, command=save)
add_button.grid(row=5, column=1)

search_button = Button(text="Search", width=7, bg="#a1cae2", highlightthickness=0, command=find_password)
search_button.grid(row=1, column=3)

window.mainloop()

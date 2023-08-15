from tkinter import *
from tkinter import messagebox

# Create a Tkinter window
root = Tk()
root.title("Register/Login System")
root.geometry("400x300")

# Create a function to register a new user
def register():
    # Open the registration form
    reg_window = Toplevel(root)
    reg_window.title("Register")
    reg_window.geometry("250x150")

    # Create the registration form fields
    Label(reg_window, text="Enter your username:").grid(row=0, column=0)
    Label(reg_window, text="Enter your password:").grid(row=1, column=0)
    username = Entry(reg_window)
    password = Entry(reg_window, show="*")
    username.grid(row=0, column=1)
    password.grid(row=1, column=1)

    # Create a function to handle the registration process
    def register_user():
        # Get the username and password entered by the user
        username_val = username.get()
        password_val = password.get()

        # Check if the username is already taken
        with open("users.txt", "r") as file:
            for line in file.readlines():
                if username_val in line:
                    messagebox.showwarning("Registration Error", "Username already taken!")
                    return

        # If the username is not taken, add the user to the file
        with open("users.txt", "a") as file:
            file.write(username_val + "," + password_val + "\n")
            messagebox.showinfo("Registration Successful", "User registered successfully!")
            reg_window.destroy()

    # Create a registration button
    register_btn = Button(reg_window, text="Register", command=register_user)
    register_btn.grid(row=2, column=0, columnspan=2)

# Create a function to handle the login process
def login():
    # Open the login form
    login_window = Toplevel(root)
    login_window.title("Login")
    login_window.geometry("250x150")

    # Create the login form fields
    Label(login_window, text="Enter your username:").grid(row=0, column=0)
    Label(login_window, text="Enter your password:").grid(row=1, column=0)
    username = Entry(login_window)
    password = Entry(login_window, show="*")
    username.grid(row=0, column=1)
    password.grid(row=1, column=1)

    # Create a function to handle the login process
    def login_user():
        # Get the username and password entered by the user
        username_val = username.get()
        password_val = password.get()

        # Check if the username and password are correct
        with open("users.txt", "r") as file:
            found = False
            for line in file.readlines():
                if username_val in line and password_val in line:
                    found = True
                    break

            if found:
                messagebox.showinfo("Login Successful", "Welcome, " + username_val + "!")
                login_window.destroy()
            else:
                messagebox.showwarning("Login Error", "Invalid username or password!")

    # Create a login button
    login_btn = Button(login_window, text="Login", command=login_user)
    login_btn.grid(row=2, column=0, columnspan=2)

# Create the login and register buttons
register_btn = Button(root, text="Register", command=register)
login_btn = Button(root, text="Login", command=login)
register_btn.pack(pady=10)
login_btn.pack(pady=10)



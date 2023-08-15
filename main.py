import tkinter.messagebox
import webbrowser
import pygame
import time
from functools import partial
from tkinter import ttk
import imdb_recommendation_system as ims
from tkHyperlinkManager import *
import re


# Register
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
                    tkinter.messagebox.showwarning("Registration Error", "Username already taken!")
                    return

        # If the username is not taken, add the user to the file
        with open("users.txt", "a") as file:
            file.write(username_val + "," + password_val + "\n")
            tkinter.messagebox.showinfo("Registration Successful", "User registered successfully!")
            reg_window.destroy()

    # Create a registration button
    register_btn = Button(reg_window, text="Register", command=register_user)
    register_btn.grid(row=2, column=0, columnspan=2)




# login
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
                tkinter.messagebox.showinfo("Login Successful", "Welcome, " + username_val + "!")
                login_window.destroy()
            else:
                tkinter.messagebox.showwarning("Login Error", "Invalid username or password!")

    # Create a login button
    login_btn = Button(login_window, text="Login", command=login_user)
    login_btn.grid(row=2, column=0, columnspan=2)


def play_menu_sound(option):
    """
    :type option: str
    :return: None
    Plays a sound based on the 'option' argument
    """
    if option == 'menu_bar':
        pygame.mixer.music.load('music/button-11.wav')
        pygame.mixer.music.play()
    elif option == 'quit':
        pygame.mixer.music.load('music/quit.wav')
        pygame.mixer.music.play()
        time.sleep(0.3)
        root.destroy()



def logout():
    tkinter.messagebox.showinfo('Logout Successfull')

def open_popup():
    tkinter.messagebox.showinfo('How it Works?', 'Using Cosine Similarity on IMDb dataset!')


def update_values():
    """
    :return: None
    Updates the content in the dropdown menu based on the keyword entered in the text field.
    """
    pygame.mixer.music.load('music/button-3.wav')
    pygame.mixer.music.play()
    filter_str = combo1.get().lower()
    filter_str = ' '.join([word for word in re.split(r'\s+', filter_str) if word != ''])  # handling white space
    # if no input is provided show the entire database
    if filter_str == '':
        combo1['values'] = movie_data
    # else filter based on the input
    else:
        filtered_list_1 = []  # holds values that starts with the input string
        filtered_list_2 = []  # holds values that matches the input pattern in the database
        for value in movie_data:
            if value.lower().startswith(filter_str):
                filtered_list_1.append(value)
            elif filter_str in value.lower():
                filtered_list_2.append(value)
        combo1['values'] = filtered_list_1 + filtered_list_2  # so that values of filtered_list_1 appear first


def open_link(my_url):
    """
    :param my_url: URL
    :type my_url: str
    :return: None
    Opens the provided URL in your default browser.
    """
    pygame.mixer.music.load('music/open_browser.wav')
    pygame.mixer.music.play()
    webbrowser.open_new(url=my_url)


def get_text(event=None):
    """
    :param event: None
    :return: None
    Gets the recommendations and shows it in a text widget.
    """
    pygame.mixer.music.load('music/button-3.wav')
    pygame.mixer.music.play()
    text_widget = Text(frame, font='Courier 13 italic', cursor='arrow', bg='#E7F2F8', height=11, width=60)
    hyperlink = HyperlinkManager(text_widget)
    text_widget.tag_configure('tag-center', justify='center')
    text_widget.tag_configure('tag-left', justify='left')
    query = combo1.get()  # get input from combo widget
    query = ' '.join([word for word in re.split(r'\s+', query) if word != ''])
    # query = ' '.join([word for word in re.split(r'\s+', query) if word != ''])  # handling white space
    text = ims.get_recommendations(query)
    print(text)
    
    


    if text is None:  # if the movie/tv show not found print some tips
        text = "Item not found!\n"
        text_widget.insert(1.0, text, 'tag-center')
        text_widget.insert(END, '\nYou can try the following:\n\n 1. Enter keywords and choose from dropdown menu.\n '
                                '2. Check for typos.', 'tag-left')
    else:  # if found iterate over the DataFrame to create hyperlinks in the text widget
        text_widget.delete(1.0, END)  # clear previous entries
        for idx, title, imdb_url in text.itertuples():  # iterating over the DataFrame as tuples
            text_widget.insert(END, title, hyperlink.add(partial(open_link, imdb_url)))  # insert hyperlinks in the

            with open("history.txt", 'a') as f:
                f.writelines(title)
                f.writelines('\n')

            # widget
            if idx != 9:  # if not the last index, insert a new line after the previous entry
                text_widget.insert(END, '\n')
                text_widget.insert(END, '\n')
    text_widget.config(highlightcolor='black', highlightbackground="black", highlightthickness=2)
    text_widget.place(x=185, y=310)
    # adding scrollbar to the text widget
    scroll_y = Scrollbar(text_widget, orient='vertical', command=text_widget.yview)
    scroll_y.place(x=185*3 + 30, relheight=1)
    text_widget.configure(state='disabled', yscrollcommand=scroll_y.set)  # making the text widget un-editable


# initialize master window
root = Tk()  # creates a window in which we work our gui
root.title("What2Watch")
root.geometry('960x720')  # width x height
root.resizable(False, False)  # restricts window size




# creating menu widget
menu = Menu(root)
helpMenu = Menu(menu, tearoff=0, postcommand=partial(play_menu_sound, 'menu_bar'), font='Courier 11', bg='#E7F2F8',
                activebackground='black', activeforeground='white')
menu.add_cascade(label='Menu', menu=helpMenu)
helpMenu.add_command(label='How it Works?', command=open_popup)
helpMenu.add_separator()
helpMenu.add_separator()
helpMenu.add_command(label='Exit', command=partial(play_menu_sound, 'quit'))

# setting background image for our app
bg_image = PhotoImage(file=r'images/new_bg_image.png')
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# creating a frame to place the widgets
frame = Frame(root, height=500, width=750, bg='white').place(x=150, y=75)
frame_bg_image = PhotoImage(file=r'images/new_bg_image.png')
# resize automatically
frame_label = Label(frame, image=bg_image)
frame_label.pack()




# creating widgets
label1 = Label(frame, font='Helvetica 13 italic', text='Select a Movie/TV Show/Documentary!', height=2, width=65,
               bg='#E7F2F8', highlightthickness=2, highlightbackground="black")
movie_data = ims.get_movie_data()  # get the database of all the movies/tv shows
combo1 = ttk.Combobox(frame, width=55, font=("Courier", 13), postcommand=update_values, values=movie_data)
button1 = Button(frame, text='SEARCH', font='Arial 13 bold italic', bg='#FBE7C6', width=35, command=get_text)
button2 = Button(frame, text='Signup', font = 'Arial 13 bold', bg='#FBE7C6', width=10, command=register)
button3 = Button(frame, text='Login', font = 'Arial 13 bold', bg='#FBE7C6', width=10, command=login)
button4 = Button(frame, text='Logout', font = 'Arial 13 bold', bg='#FBE7C6', width=10, command=logout)



instructions_text = Text(frame, font='Times 13 ', cursor='arrow', bg='#E7F2F8', height=11, width=60)

# print instructions in the text widget
instructions_text.tag_configure('tag-center', justify='center')
instructions_text.tag_configure('tag-center-underline', justify='center', underline=1)
instructions_text.tag_configure('tag-left', justify='left')
instructions_text.insert(1.0, 'Welcome to What2Watch!\n', 'tag-center')
instructions_text.insert(END, "\nInstructions\n", 'tag-center-underline')
instructions_text.insert(END, "\n 1. Enter the name of a TV Show/ Movie/ Documentary. \n 2. Select from the dropdown menu. \n 3. Press ENTER search. \n 4. Click on the movie that interests you to redirect you to the IMDb website.", 'tag-left')
# placing widgets
instructions_text.config(highlightcolor='black', highlightbackground="black", highlightthickness=2)
instructions_text.place(x=185, y=310)
instructions_text.configure(state='disabled')
label1.place(x=150, y=150)
root.option_add('*TCombobox*Listbox.font', ("Times", 13))
root.config(menu=menu)
combo1.place(x=200, y=213, height=32)
button1.place(x=300, y=260)
# register button
button2.place(x=100, y=100)
# login button
button3.place(x=200, y=100)
# logout button
button4.place(x=300, y=100)

combo1.bind('<Return>', get_text)


register_btn = Button(root, text="Register", command=register)
login_btn = Button(root, text="Login", command=login)
register_btn.pack(pady=10)
login_btn.pack(pady=10)

# main loop
if __name__ == '__main__':
    pygame.mixer.init()
    root.mainloop()

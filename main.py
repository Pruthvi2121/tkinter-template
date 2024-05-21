import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
from sqlalchemy.orm import sessionmaker
from database import engine, User, Base

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

primary = "#0E1525"
secondary = "#151C2C"
tirnary = "#1C2333"  # Example color



class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.current_user = None 
        # Create a container to hold all frames and sidebar
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Initialize dictionary to hold different frames
        self.frames = {}

        # Create and add frames to the dictionary
        for F in (LoginPage, RegisterPage, HomePage, Task1Page, Task2Page, Task3Page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=1, column=1, sticky="nsew")

        # Show the login page by default
        self.show_frame(LoginPage)

        # Create navigation navbar
        self.navbar_frame = tk.Frame(container, height=50, bg=primary)
        self.navbar_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Configure grid columns for navbar
        self.navbar_frame.grid_columnconfigure(0, weight=1)
        self.navbar_frame.grid_columnconfigure(1, weight=1)
        self.navbar_frame.grid_columnconfigure(2, weight=0)

        # Add content to navbar
        self.label = tk.Label(self.navbar_frame, bg=secondary, fg="#FF6600", text="CakeVilla", font=("Helvetica", 14))
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Add user label to navbar
        self.user_label = tk.Label(self.navbar_frame, bg=secondary, fg="#000000", font=("Helvetica", 12))
        self.user_label.grid(row=0, column=1, pady=10, padx=10, sticky="e")

        # Add logout button to navbar
        self.logout_button = tk.Button(self.navbar_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=0, column=2, pady=10, padx=10, sticky="e")

        # Create navigation sidebar but don't add it to the grid yet
        self.sidebar_frame = tk.Frame(container, bg=primary, width=200)

        # Add buttons to sidebar
        self.buttons = [
            ("Home", HomePage),
            ("Records", Task1Page),
            ("Analysis", Task2Page),
            ("Export", Task3Page)
        ]

        google_font = Font(size=10)

        for text, page in self.buttons:
            btn = tk.Button(self.sidebar_frame, text=text, bg=tirnary, fg="#4AE60C", font=google_font, command=lambda page=page: self.show_frame(page))
            btn.pack(fill="x", padx=10, pady=5, ipady=2, ipadx=60)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def login(self, username, password):
        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            self.show_frame(HomePage)
            self.current_user = user.username
            self.user_label.config(text=f"Welcome, {self.current_user}", fg="#4AE60C")
            self.sidebar_frame.grid(row=1, column=0, sticky="ns")  # Show sidebar after successful login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def logout(self):
        self.show_frame(LoginPage)
        self.current_user = None
        self.user_label.config(text="")
        self.sidebar_frame.grid_forget()  # Hide sidebar on logout

    def register(self, username, password):
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            messagebox.showerror("Registration Failed", "Username already exists")
        else:
            new_user = User(username=username, password=password)
            session.add(new_user)
            session.commit()
            messagebox.showinfo("Registration Success", "Account created successfully")
            self.show_frame(LoginPage)

# Define the LoginPage class
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Login Page", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        self.username_label = tk.Label(self, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.check_login)
        self.login_button.pack()

        self.register_button = tk.Button(self, text="Don't have an account? Register", command=lambda: controller.show_frame(RegisterPage))
        self.register_button.pack()

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.controller.login(username, password)

# Define the RegisterPage class
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Register Page", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        self.username_label = tk.Label(self, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack()

        self.register_button = tk.Button(self, text="Register", command=self.check_register)
        self.register_button.pack()

        self.back_to_login_button = tk.Button(self, text="Back to Login", command=lambda: controller.show_frame(LoginPage))
        self.back_to_login_button.pack()

    def check_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.controller.register(username, password)

# Define other pages as classes
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Home Page", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)
        label = tk.Label(self, text="Today's Order", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

class Task1Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Task 1 Page", font=("Helvetica", 18))
        label.pack(pady=10, padx=10, anchor="e")

class Task2Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Task 2 Page", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

class Task3Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Task 3 Page", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

if __name__ == "__main__":
    app = MainApplication()
    app.geometry("800x600")
    app.mainloop()

import tkinter as tk
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from database import engine, User

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")

        self.username_label = tk.Label(root, text="Username")
        self.username_label.pack()

        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password")
        self.password_label.pack()

        self.password_entry = tk.Entry(root, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

        self.logout_button = tk.Button(root, text="Logout", command=self.logout, state=tk.DISABLED)
        self.logout_button.pack()

        self.current_user = None

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = session.query(User).filter_by(username=username, password=password).first()

        if user:
            self.current_user = user
            messagebox.showinfo("Login Info", f"Welcome {username}")
            self.login_button.config(state=tk.DISABLED)
            self.logout_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Login Info", "Invalid Username or Password")

    def logout(self):
        self.current_user = None
        messagebox.showinfo("Logout Info", "You have successfully logged out")
        self.login_button.config(state=tk.NORMAL)
        self.logout_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

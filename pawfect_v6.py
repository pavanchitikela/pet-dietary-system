from functools import partial
import csv
import tkinter
#import python ,tkinter, mysql and other libraries
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
                              
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk
import re
import tkinter as tk
from tkinter import ttk
import webbrowser
from RAG import RAG

#For SMTP
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#connecting to the database
pdsdb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pavan",
    database="pawfect"
)

#creating table user query userid,first_name,last_name,email,mobile,password
create_user_table = """
CREATE TABLE IF NOT EXISTS user_info (  
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100)  NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    mobile VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
    )
"""

#pettable
create_pet_table= """
CREATE TABLE IF NOT EXISTS pet_info (
    pet_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pet_type VARCHAR(100) NOT NULL DEFAULT 'dog',
    pet_name VARCHAR(100) NOT NULL,
    pet_breed VARCHAR(100) NOT NULL,
    pet_gender VARCHAR(100) NOT NULL,
    pet_color VARCHAR(100) NOT NULL,
    pet_weight VARCHAR(100) NOT NULL,
    pet_year VARCHAR(100) NOT NULL,
    pet_month VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user_info(user_id)
    )
"""

# Define the SQL command to create the pet info table
create_pet_image_urls_table = """
CREATE TABLE IF NOT EXISTS pet_image_urls (
    pet_info_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_type VARCHAR(3) NOT NULL,
    breed VARCHAR(40) NOT NULL,
    image_path VARCHAR(200) NOT NULL
)
"""

#executing the query
cursor = pdsdb.cursor()
cursor.execute(create_user_table)
cursor.execute(create_pet_table)
cursor.execute(create_pet_image_urls_table)
cursor.close()


#class Pawfect Portions as pp
class PawfectPortions:
    #initializing the class
    def __init__(self, root):
        self.root = root
        self.root.title("Pawfect Portions")
        self.root.geometry("1200x750")
        self.root.config(bg="white")
        self.rag = RAG()

        
        
        
        #self.welcomeScreen()
        self.loginScreen()
    

    #login screen
    def loginScreen(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
            
        #create a frame for the login screen
        self.login_frame = Frame(self.root, bg="white")
        self.login_frame.place(x=0, y=0, width=1300, height=750)
        
        self.show_pass_var = tk.IntVar()
        self.password_visible = False
        # adding Logindogpage1 image
        self.bg = Image.open("images/Logindogpage1.jpg")
        self.bg = self.bg.resize((1300, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.login_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        #adding Welcome text on the top
        self.welcome_label = Label(self.login_frame, text="Welcome", font=("calibri", 70, "bold"), bg="black", fg="WHITE")
        self.welcome_label.place(x=100, y=70)
        
        self.title = Image.open("txtImages/title.png")
        self.title = self.title.resize((170, 70), Image.LANCZOS)
        self.title = ImageTk.PhotoImage(self.title)
        self.title_image = Label(self.login_frame, image=self.title, bg="white")
        self.title_image.config(highlightthickness=0, bd=0, relief="ridge")
        self.title_image.place(x=760, y=100)
        
        #adding username label
        self.username_label = Label(self.login_frame, text="__________________________", font=("calibri", 18, "bold"), bg="black", fg="WHITE") 
        self.username_label.place(x=760, y=270)
        #adding password label
        self.password_label = Label(self.login_frame, text="__________________________", font=("calibri", 18, "bold"), bg="black", fg="WHITE")
        self.password_label.place(x=760, y=340)
        
        #adding password entry
        self.password_entry = Entry(self.login_frame,font=("calibri", 18), bg="black", width=28, bd=0,fg="white", relief="ridge",insertbackground="white")
        self.password_entry.place(x=765, y=325)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind('<FocusIn>', self.removepasswordtext)
        self.password_entry.bind('<FocusOut>', self.removepasswordtext)
    
        #adding username entry
        self.username_entry = Entry(self.login_frame,font=("calibri", 18), bg="black", width= 28, bd=0,fg="white", relief="ridge",insertbackground="white")
        self.username_entry.place(x=765, y=260)
        self.username_entry.insert(0, "Email")
        #self.username_entry.bind("<Key>", self.removeusernametext)
        self.username_entry.bind('<FocusIn>', self.removeusernametext)
        self.username_entry.bind('<FocusOut>', self.removeusernametext)
        
        #adding show password icon
        show_icon_image = Image.open("images/show.png")
        show_icon_resized = show_icon_image.resize((30, 30), Image.Resampling.LANCZOS)  
        self.show_icon = ImageTk.PhotoImage(show_icon_resized)

        # Open and resize the hide icon
        hide_icon_image = Image.open("images/hide.png")
        hide_icon_resized = hide_icon_image.resize((30, 30), Image.Resampling.LANCZOS)  
        self.hide_icon = ImageTk.PhotoImage(hide_icon_resized)


        # Create a button to toggle password visibility
        self.toggle_button = tk.Button(self.login_frame, image=self.show_icon, command=self.toggle_password_visibility, borderwidth=0,highlightthickness=0, bg="black", activebackground="black")
        self.toggle_button.place(x=1050, y=330)
        
        
       #adding login button
        self.login_button = Button(self.login_frame, text="Login", font=("calibri",18,"bold"), bg="midnight blue", fg="white", bd=1, cursor="hand2",activebackground="black",activeforeground="grey", command=self.login_validation)
        self.login_button.place(x=880, y=420)

        #text for signup button
        self.text = Label(self.login_frame, text="Don't have an account?", font=("calibri", 14), bg="#080808", fg="WHITE")
        self.text.place(x=780, y=500)

        #adding signup button
        self.signup_button = Button(self.login_frame, text="sign up", font=("calibri",14,"underline"), bg="black", fg="light blue", bd=0, cursor="hand2",activebackground="black",activeforeground="grey",command=self.signupScreen)
        self.signup_button.place(x=970, y=495)

        #adding forgot password button
        self.login_forgot_password_button = Button(self.login_frame, text="Forgot Password?", font=("calibri",10,"bold"), bg="black", fg="light blue", bd=0, cursor="hand2",activebackground="black",activeforeground="grey")
        self.login_forgot_password_button.place(x=960, y=380)
        self.login_forgot_password_button.config(command=self.forgotPasswordScreen)
    
    #method for show and hide password icon
    def toggle_password_visibility(self):
        if self.password_visible:
            # Hide the password and update the button icon
            self.password_entry.config(show="*")
            self.toggle_button.config(image=self.show_icon)
            self.password_visible = False
        else:
            # Show the password and update the button icon
            self.password_entry.config(show="")
            self.toggle_button.config(image=self.hide_icon)
            self.password_visible = True
    
    #creating entry lable inside the username entry
    def removeusernametext(self, event):
        if self.username_entry.get() == "Email":
            self.username_entry.delete(0, "end")
            self.username_entry.config(fg="white")
        elif self.username_entry.get() == "":
            self.username_entry.insert(0, "Email")
            self.username_entry.config(fg="white") 
    
    def removepasswordtext(self, event):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, "end")
            self.password_entry.config(fg="white")
            self.password_entry.config(show="*")
        elif self.password_entry.get() == "":
            self.password_entry.insert(0, "Password")
            self.password_entry.config(show="")
            self.password_entry.config(fg="white") 

    #creating signup screen
    def signupScreen(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
            
        #create a frame for the signup screen
        self.signup_frame = Frame(self.root, bg="white")
        self.signup_frame.place(x=0, y=0, width=1300, height=750)
        # adding Logindogpage1 image
        self.bg = Image.open("images/signtupcat.jpg")
        self.bg = self.bg.resize((1300, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.signup_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        self.signup_label = Label(self.signup_frame, text="Register Your Account Here", font=("calibri", 40, "bold"), bg="#080808", fg="WHITE")
        self.signup_label.place(x=300, y=50)
        
        #adding first name label
        self.first_name_label = Label(self.signup_frame, text="First Name", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.first_name_label.place(x=40, y=200)
        #addling line under the first name label
        self.first_name_label = Label(self.signup_frame, text="_______________________", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.first_name_label.place(x=158, y=206)
        #adding first name entry
        self.first_name_entry = Entry(self.signup_frame,font=("calibri", 15), bg="#080808", width=28, bd=0,fg="white", relief="ridge",insertbackground="white")
        self.first_name_entry.place(x=160, y=206)
        #adding last name label 
        self.last_name_label = Label(self.signup_frame, text="Last Name", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.last_name_label.place(x=450, y=206)
        #addling line under the last name label
        self.last_name_label = Label(self.signup_frame, text="____________________", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.last_name_label.place(x=565, y=205)
        #adding last name entry
        self.last_name_entry = Entry(self.signup_frame,font=("calibri",15), bg="#080808", bd=0,fg="white", relief="ridge",insertbackground="white")
        self.last_name_entry.place(x=570, y=206)
        #adding email label
        self.email_label = Label(self.signup_frame, text="Email", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.email_label.place(x=50, y=275)
        #addling line under the email label
        self.email_label = Label(self.signup_frame, text="_______________________", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.email_label.place(x=158, y=280)
        #adding email entry
        self.email_entry = Entry(self.signup_frame,font=("calibri", 15), width=28, bg="#080808", bd=0,fg="white", relief="ridge",insertbackground="white")
        self.email_entry.place(x=160, y=280)
        #adding mobile label
        self.mobile_label = Label(self.signup_frame, text="Mobile", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.mobile_label.place(x=50, y=350)
        #addling line under the mobile label
        self.mobile_label = Label(self.signup_frame, text="_______________________", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.mobile_label.place(x=160, y=350)
        #adding mobile entry
        self.mobile_entry = Entry(self.signup_frame,font=("calibri", 15), bg="#080808", bd=0,fg="white", relief="ridge",insertbackground="white")
        self.mobile_entry.place(x=160, y=350)
        #adding password label
        self.password_label = Label(self.signup_frame, text="Password", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.password_label.place(x=50, y=425)
        #addling line under the password label
        self.password_label = Label(self.signup_frame, text="_______________________", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.password_label.place(x=160, y=425)
        #adding password entry
        self.password_entry = Entry(self.signup_frame,font=("calibri", 15), width= 28, bg="#080808", bd=0,fg="white", relief="ridge",insertbackground="white",show="*")
        self.password_entry.place(x=160, y=425)
        
         # Create a button to toggle password visibility
        self.toggle_button = tk.Button(self.signup_frame, image=self.show_icon, command=self.toggle_password_visibility, borderwidth=0,highlightthickness=0, bg="#080808", activebackground="black")
        self.toggle_button.place(x=425, y=420)
        
        #adding confirm password label
        self.confirm_password_label = Label(self.signup_frame, text="Confirm Password", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.confirm_password_label.place(x=50, y=500)
        #addling line under the confirm password label
        self.confirm_password_label = Label(self.signup_frame, text="_______________________", font=("calibri", 18, "bold"), bg="#080808", fg="WHITE")
        self.confirm_password_label.place(x=250, y=495)
        #adding confirm password entry
        self.confirm_password_entry = Entry(self.signup_frame,font=("calibri", 15), width=28, bg="#080808", bd=0,fg="white", relief="ridge",insertbackground="white",show="*")
        self.confirm_password_entry.place(x=252, y=495)
        #adding signup button
        self.signup_button = Button(self.signup_frame, text="Sign Up", font=("calibri",18,"bold"), bg="midnight blue", fg="white", bd=1, cursor="hand2",activebackground="#080808",activeforeground="grey")
        self.signup_button.place(x=485, y=590)
        self.signup_button.config(command=self.signup_data)
        #adding login button
        self.login_button = Button(self.signup_frame, text="Back to Login", font=("calibri",18,"bold"), bg="#080808", fg="white", bd=0, cursor="hand2",activebackground="#080808",activeforeground="grey",command=self.loginScreen)
        self.login_button.place(x=460, y=650)
        

    def welcomeScreen(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()

        #dsiplay welcome image
        self.bg = Image.open("images/welcome.jpg")
        self.bg = self.bg.resize((1300, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        #display title image on left middle
        self.title = Image.open("txtImages/title.png")
        self.title = self.title.resize((570, 200), Image.LANCZOS)
        self.title = ImageTk.PhotoImage(self.title)
        self.title_image = Label(self.root, image=self.title, bg="white")
        self.title_image.config(highlightthickness=0, bd=0, relief="ridge")
        self.title_image.place(x=20, y=140)
        
        self.bottomNavBar()

        self.home_button.config(bg="white", fg="#242323")

    def bottomNavBar(self):                   
        

        #bottom frame for buttons
        self.bottom_frame = Frame(self.root, bg="#242323")
        self.bottom_frame.place(x=0, y=670, width=1300, height=80)
        #add shadow to the bottom frame
        self.bottom_frame.config(highlightbackground="black", highlightcolor="black", highlightthickness=0)
        
        #add logout image as a button side to home button
        self.logout = Image.open("images/logout.jpg")
        self.logout = self.logout.resize((40, 40), Image.LANCZOS)
        self.logout = ImageTk.PhotoImage(self.logout)
        self.logout_button = Button(self.bottom_frame, image=self.logout, bg="#242323", activebackground="#242323",bd=0, cursor="hand2")
        self.logout_button.place(x=20, y=10)
        self.logout_button.config(command=self.confirm_logout)
        
        #add profile image as a button
        self.profile = Image.open("images/profile.png")
        self.profile = self.profile.resize((40, 40), Image.LANCZOS)
        self.profile = ImageTk.PhotoImage(self.profile)
        self.profile_button = Button(self.bottom_frame, image=self.profile, bg="#242323", activebackground="#242323",bd=0, cursor="hand2")
        self.profile_button.place(x=90, y=10)
        self.profile_button.config(command=self.profileScreen)
        
        # add Petprofile image as a button
        self.petprofile = Image.open("images/Petprofile.jpg")
        self.petprofile = self.petprofile.resize((60, 60), Image.LANCZOS)
        self.petprofile = ImageTk.PhotoImage(self.petprofile)
        self.petprofile_button = Button(self.bottom_frame, image=self.petprofile, bg="#242323", activebackground="#242323",bd=0, cursor="hand2")
        self.petprofile_button.place(x=145, y=0)
        self.petprofile_button.bind("<Button-1>", self.show_dropdown_menu)

        # Create the dropdown menu
        self.dropdown_menu = Menu(self.root, tearoff=0)
        self.dropdown_menu.add_command(label="View My Pet", command=self.view_Profile)
        self.dropdown_menu.add_command(label="Register Cat", command=self. catProfileScreen)
        self.dropdown_menu.add_command(label="Register Dog", command=self.dogProfileScreen)
        self.dropdown_menu.config(font=("calibri", 15), bg="#242323", fg = "white")
        
        #home button    
        self.home_button = Button(self.bottom_frame, text="Home", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.home_button.place(x=400, y=6)
        
        #dogs button
        self.dogs_button = Button(self.bottom_frame, text="Dogs", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        #command to dogs screen
        self.dogs_button.config(command = partial(self.selectPetBreed, "dog"))
        self.dogs_button.place(x=520, y=6)
        
        #cats button
        self.cats_button = Button(self.bottom_frame, text="Cats", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.cats_button.place(x=640, y=6)
        self.cats_button.config(command=partial(self.selectPetBreed, "cat"))
        
        #Pet AI
        self.pet_ai_button = Button(self.bottom_frame, text="Pet AI", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        #command=self.petAiScreen
        self.pet_ai_button.config(command=self.commonPetAiScreen)
        self.pet_ai_button.place(x=760, y=6)
        
        
        #place facebook icon as a button
        self.facebook_icon = Image.open("social/facebook.png")
        self.facebook_icon = self.facebook_icon.resize((25, 25), Image.LANCZOS)
        self.facebook_icon = ImageTk.PhotoImage(self.facebook_icon)
        self.facebook_button = Button(self.bottom_frame, image=self.facebook_icon, bg="#242323", bd=0, cursor="hand2")
        self.facebook_button.place(x=1100, y=13)
        self.facebook_button.config(command=self.selectfacebook)
        
        
        #place instagram icon as a button
        self.instagram_icon = Image.open("social/insta.png")
        self.instagram_icon = self.instagram_icon.resize((25, 25), Image.LANCZOS)
        self.instagram_icon = ImageTk.PhotoImage(self.instagram_icon)
        self.instagram_button = Button(self.bottom_frame, image=self.instagram_icon, bg="#242323", bd=0, cursor="hand2")
        self.instagram_button.place(x=1150, y=15)
        self.instagram_button.config(command=self.selectinstagram)
        
        
        #twitter  icon as a button
        self.twitter_icon = Image.open("social/twitter.png")
        self.twitter_icon = self.twitter_icon.resize((25, 25), Image.LANCZOS)
        self.twitter_icon = ImageTk.PhotoImage(self.twitter_icon)
        self.twitter_button = Button(self.bottom_frame, image=self.twitter_icon, bg="#242323", bd=0, cursor="hand2")
        self.twitter_button.place(x=1200, y=15)
        self.twitter_button.config(command=self.selecttwitter)
    
    
    def topNavBar(self):
      #buttons frame on top
        self.buttons_frame = Frame(self.root , bg="#242323")
        self.buttons_frame.place(x=0, y=0, width=1300, height=60)
        
        #home button
        self.home_button = Button(self.buttons_frame, text="Home", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.home_button.config(command=self.welcomeScreen)
        self.home_button.place(x=400, y=6)
        
        #dogs button
        self.dogs_button = Button(self.buttons_frame, text="Dogs", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.dogs_button.place(x=520, y=6)
        self.dogs_button.config(command=partial(self.selectPetBreed, "dog"))
        
        #cats button
        self.cats_button = Button(self.buttons_frame, text="Cats", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.cats_button.place(x=640, y=6)
        self.cats_button.config(command=partial(self.selectPetBreed, "cat"))
        
        #Pet AI
        self.pet_ai_button = Button(self.buttons_frame, text="Pet AI", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.pet_ai_button.config(command=self.commonPetAiScreen)
        self.pet_ai_button.place(x=760, y=6)
        
        #facebook icon as a button
        self.facebook_icon = Image.open("social/facebook.png")
        self.facebook_icon = self.facebook_icon.resize((25, 25), Image.LANCZOS)
        self.facebook_icon = ImageTk.PhotoImage(self.facebook_icon)
        
        self.facebook_button = Button(self.buttons_frame, image=self.facebook_icon, bg="#242323", bd=0, cursor="hand2")
        self.facebook_button.place(x=1100, y=13)
        self.facebook_button.config(command=self.selectfacebook)
        
        #instagram icon as a button
        self.instagram_icon = Image.open("social/insta.png")
        self.instagram_icon = self.instagram_icon.resize((25, 25), Image.LANCZOS)
        self.instagram_icon = ImageTk.PhotoImage(self.instagram_icon)
        
        self.instagram_button = Button(self.buttons_frame, image=self.instagram_icon, bg="#242323", bd=0, cursor="hand2")
        self.instagram_button.place(x=1150, y=15)
        self.instagram_button.config(command=self.selectinstagram)
        
        #twitter icon as a button
        self.twitter_icon = Image.open("social/twitter.png")
        self.twitter_icon = self.twitter_icon.resize((25, 25), Image.LANCZOS)
        self.twitter_icon = ImageTk.PhotoImage(self.twitter_icon)
        
        self.twitter_button = Button(self.buttons_frame, image=self.twitter_icon, bg="#242323", bd=0, cursor="hand2")
        self.twitter_button.place(x=1200, y=15)
        self.twitter_button.config(command=self.selecttwitter)
        
        #add logoout image as a button 
        self.logout = Image.open("images/logout.jpg")
        self.logout = self.logout.resize((40, 40), Image.LANCZOS)
        self.logout = ImageTk.PhotoImage(self.logout)
        self.logout_button = Button(self.buttons_frame, image=self.logout, bg="#242323", activebackground="#242323",bd=0, cursor="hand2")
        self.logout_button.place(x=20, y=10)
        self.logout_button.config(command=self.confirm_logout)
        
        #add profile image as a button
        self.profile = Image.open("images/profile.png")
        self.profile = self.profile.resize((40, 40), Image.LANCZOS)
        self.profile = ImageTk.PhotoImage(self.profile)
        self.profile_button = Button(self.buttons_frame, image=self.profile, bg="#242323", activebackground="#242323",bd=0, cursor="hand2")
        self.profile_button.place(x=90, y=10)
        self.profile_button.config(command=self.profileScreen)
        
        
         # add Petprofile image as a button
        self.petprofile = Image.open("images/Petprofile.jpg")
        self.petprofile = self.petprofile.resize((60, 60), Image.LANCZOS)
        self.petprofile = ImageTk.PhotoImage(self.petprofile)
        self.petprofile_button = Button(self.buttons_frame, image=self.petprofile, bg="#242323", activebackground="#242323",bd=0, cursor="hand2")
        self.petprofile_button.place(x=145, y=0)
        self.petprofile_button.bind("<Button-1>", self.show_dropdown_menu)

         # Create the dropdown menu
        self.dropdown_menu = Menu(self.root, tearoff=0)
        self.dropdown_menu.add_command(label="View My Pet", command=self.view_Profile)
        self.dropdown_menu.add_command(label="Register Cat", command=self. catProfileScreen)
        self.dropdown_menu.add_command(label="Register Dog", command=self.dogProfileScreen)
        self.dropdown_menu.config(font=("calibri", 15), bg="#242323", fg = "white")
    
      #dropdown menu for the pet profile
    def show_dropdown_menu(self, event):
        """Show the dropdown menu near the button."""
        try:
            self.dropdown_menu.tk_popup(event.x_root, event.y_root)
        finally:
        
            self.dropdown_menu.grab_release()

    def show_dropdown_menu(self, event):
        """Show the dropdown menu near the button."""
        try:
            self.dropdown_menu.tk_popup(event.x_root, event.y_root)
        finally:
        
            self.dropdown_menu.grab_release()
        
    def confirm_logout(self):
        
        result = messagebox.askyesno("Confirmation", "Are you sure you want to logout?")
        print(result)
        if result:
            self.loginScreen()
        else:
            return                         
        
        #creating the social media methods
    def selectfacebook(self):
        webbrowser.open_new("https://www.facebook.com/pawfect.portions/")  

    def selectinstagram(self):
        webbrowser.open_new("https://www.instagram.com/pawfect._portions/")

    def selecttwitter(self):
        webbrowser.open_new("https://twitter.com/PawfectPortions")


    
    #petai screen
    def commonPetAiScreen(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
        
        self.topNavBar()

        self.pet_ai_button.config(bg="white", fg="#242323")
        
        #rest as frame for the rest of the screen with black background
        self.rest_frame = Frame(self.root, bg="black")
        self.rest_frame.place(x=0, y=60, width=1300, height=750)
        
        
        #i'm your pet ai label
        self.pet_ai_label = Label(self.rest_frame, text="I'm your Pet AI", font=("calibri", 30, "bold"), bg="black", fg="white")
        self.pet_ai_label.place(x=500, y=20)
        
        #you can ask me anything about your pet, ask a question label, or ask me to explain the behavior of your pet
        self.ask_label = Label(self.rest_frame, text="You can ask me anything about your pet, ask a question, or ask me to explain the behavior of your pet", font=("calibri", 18), bg="black", fg="white")
        self.ask_label.place(x=120, y=80)
         
        #Example: What are the best foods for my dog?
        self.example_label = Label(self.rest_frame, text="Example: What are the best foods for my dog?", font=("calibri", 18), bg="black", fg="white")
        self.example_label.place(x=400, y=120)
        
        
        #entry box for the question big and wide
        self.question_entry = Entry(self.rest_frame, font=("calibri", 18), bg="white", fg="black", relief="ridge")
        #center the text
        self.question_entry.config(justify="center")
        
        #rounded corners
        self.question_entry.config(highlightthickness=0, bd=0)
        self.question_entry.config(highlightbackground="black", highlightcolor="black")
        self.question_entry.place(x=120, y=180, width=1000, height=50)
        
        
        #Checkbox for use my pet
        self.toggle_var = tk.BooleanVar()
        self.toggle_button = tk.Checkbutton(self.rest_frame, text="Use my pet data", variable=self.toggle_var, font=("calibri", 15), bg="#010101", fg="white", selectcolor="black", command=self.display_pet_type)
        self.toggle_button.place(x=100, y=260)

        #ask button
        self.ask_button = Button(self.rest_frame, text="Ask", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2",command=self.generateResponse)
        # self.ask_button = Button(self.rest_frame, text="Ask", font=("calibri", 18, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2")
        self.ask_button.place(x=600, y=250)

    def getMyPets(self, pet_type):
        cursor = pdsdb.cursor()
        print("EMail is:", self.email)
        print("Pet type is: ", pet_type)
        get_my_pet_query = f"SELECT pet_name FROM pet_info WHERE pet_type= '{pet_type}' AND user_id IN (SELECT user_id FROM user_info WHERE email = '{self.email}');"

        cursor.execute(get_my_pet_query)
        myPets = cursor.fetchall()

        print("My pets from DB", myPets)
        myPetsArray = []
        for pet_tuple in myPets:
            # 'pet_tuple' represents a single tuple in the list
            for pet in pet_tuple:
                myPetsArray.append(pet)
        
        cursor.close()

        return myPetsArray
    
    def display_breeds(self):
        # Destroy widget if already exists
        if hasattr(self, 'my_pet_dropdown'):
             self.my_pet_dropdown.destroy()

        #Take new variable for this
        self.my_pet_type = self.pet_type_var.get()

        print("Pet selected is : ", self.my_pet_type)
        #Get user pets from DB
        myPets = self.getMyPets(self.my_pet_type)
        print(myPets)
        if len(myPets) == 0:
            messagebox.showerror("ERROR", f"You don't have any {self.my_pet_type}")
        else:

            self.my_pet = StringVar()
            self.my_pet.set("select pet")
            self.my_pet_dropdown = OptionMenu(self.rest_frame, self.my_pet, *myPets)
            #self.pet_breed_dropdown = OptionMenu(self.pet_profile_frame, self.pet_breed, "German Shepherd", "Labrador", "Golden Retriever", "French Bulldog", "Siberian Husky")
            self.my_pet_dropdown.config(font=("calibri", 12), bg="#242323", fg = "white")
            self.my_pet_dropdown.place(x=450, y=260)


    def display_pet_type(self):
        if self.toggle_var.get():
             #Checkbox for use my pet
             self.pet_type_var = StringVar(value=" ")
             self.dog_radio = Radiobutton(self.rest_frame,text="Dog", variable=self.pet_type_var,value="Dog", font=("calibri", 13), bg="#010101", fg="white", selectcolor="black", command=self.display_breeds)
             self.dog_radio.place(x=300, y=265)
            
             self.cat_radio = Radiobutton(self.rest_frame,text="Cat", variable=self.pet_type_var,value="Cat",font=("calibri", 13), bg="#010101", fg="white", selectcolor="black", command=self.display_breeds)
             self.cat_radio.place(x=370, y=265)
        else:
            if hasattr(self, 'dog_radio'):
                self.dog_radio.destroy()

            if hasattr(self, 'cat_radio'):
                self.cat_radio.destroy() 

            if hasattr(self, 'my_pet_dropdown'):
                self.my_pet_dropdown.destroy()                           
        
        
        #generate response
    def generateResponse(self):
        #get the question from the entry box
        question = self.question_entry.get()
        my_pet_data = ""
        
        pet_type = self.pet_type_var.get()

        if pet_type==" " or pet_type is None:
            messagebox.showerror("Error", "Please select your pet type (Dog or cat) ")
            return
        else:
            pet_name = self.my_pet.get()

        if pet_name == "select pet":
            messagebox.showerror("Error", "Please select your pet")
            return
        #check if the question is empty
        if question == "":
            messagebox.showerror("Error", "Please enter your question")
            return
        
        print(f'pet type is {pet_type}')
        print(f'My pet is {pet_name}')

        if (pet_type == 'Dog' or pet_type == 'Cat') and pet_name is not None:
            cursor = pdsdb.cursor()
            select_pet_query = f"SELECT pet_breed, pet_gender, pet_weight, pet_year, pet_month, pet_color FROM pet_info WHERE pet_type= '{pet_type}' AND pet_name = '{pet_name}' AND user_id = {self.user_id}"

            cursor.execute(select_pet_query)

            pet = cursor.fetchone()

            cursor.close() 

            print(pet)

            pet_breed = pet[0]
            pet_gender = pet[1]
            pet_weight = pet[2]
            pet_years = pet[3]
            pet_months = pet[4]
            pet_color= pet[5]

            my_pet_data = f"I have a {pet_type} and the breed is {pet_breed}.The weight is {pet_weight}, gender is {pet_gender}, age is {pet_years} years and {pet_months} months, and color is {pet_color} "
            answer = messagebox.askyesno(f"Your {pet_type} data", f"Your pet {pet_name} is a {pet_breed}.\nThe weight is {pet_weight}, gender is {pet_gender}, age is {pet_years} years and {pet_months} months, and color is {pet_color}.\n\nDo you want to continue ?")
            print(answer)

            if answer:
                print(f"Your {pet_type} data", my_pet_data)
                question = f'{my_pet_data}. {question}'
                
                response = self.rag.query(question)
                
                # print(response)
                
                #frame for the response
                self.response_frame = Frame(self.rest_frame, bg="black")
                self.response_frame.place(x=120, y=320, width=1000, height=300)
                
                #with borders
                self.response_frame.config(highlightbackground="white", highlightcolor="white", highlightthickness=1)
                
                #response label
                self.response_label = Label(self.response_frame, text=response, font=("calibri", 18), bg="black", fg="white")
                #if text is long, wrap it
                self.response_label.config(wraplength=950)
                self.response_label.place(x=10, y=10)

                # clear response
                self.clear_response_button = Button(self.rest_frame, text="Clear", font=("calibri", 12, "bold"), bg="#242323", fg="white", bd=0, cursor="hand2", command= self.clear_response)
                self.clear_response_button.place(x=1080, y=280)
            else:
                return   

    def clear_response(self):
        self.response_frame.destroy()
        self.clear_response_button.destroy()


    #dogs screen
    def selectPetBreed(self, pet_type):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
            

        #display selectbreed image full screen
        if pet_type == 'dog' :     
            #dogs button white and load dogbreed image
           
            self.bg = Image.open("images/selectbreed.jpg")
            self.bg = self.bg.resize((1300, 750), Image.LANCZOS)
            self.bg = ImageTk.PhotoImage(self.bg)
            self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1) 
            self.topNavBar() 
            self.dogs_button.config(bg="white", fg="#242323")
        else:
            # Cat button white and load catbreed image
            self.bg = Image.open("images/catbreed.jpeg")
            self.bg = self.bg.resize((1300, 750), Image.LANCZOS)
            self.bg = ImageTk.PhotoImage(self.bg)
            self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1) 
            self.topNavBar() 
            self.cats_button.config(bg="white", fg="#242323")
    
            

        #select dog breed label bg #272727
        self.select_dog_breed_label = Label(self.root, text=f"Explore {pet_type} breed", font=("calibri", 30, ), bg="#272727", fg="white")
        self.select_dog_breed_label.place(x=250, y=120)

        cursor = pdsdb.cursor()
        select_data = f"SELECT breed FROM pet_image_urls WHERE pet_type = '{pet_type}';"

        cursor.execute(select_data)
        breeds = cursor.fetchall()

        # for breed in breeds:
        #     print(row)
        cursor.close()

        #breeds = [("Labrador"), "German Shepherd", "Golden Retriever", "French Bulldog", "Siberian Husky"]

        #logic to display all breed buttons
        x, y = 280, 250
        for breed_tuple in breeds:
            # 'breed' represents a single tuple in the list
            for breed in breed_tuple:
                # 'item' represents each element within the tuple
                self.pet_breed_button = Button(self.root, text=breed, font=("calibri", 18, "bold"), bg="#272727", fg="white", bd=0, cursor="hand2")
                x = 360-len(breed)*4
                self.pet_breed_button.place(x=x, y=y)
                y+=70
                self.pet_breed_button.config(command= partial(self.petAIScreen, pet_type, breed))
        

    def petAIScreen(self, pet_type, breed):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()

        # Getting image_path for the pet type and breed from database

        cursor = pdsdb.cursor()
        select_data = f"SELECT image_path FROM pet_image_urls WHERE pet_type = '{pet_type}' AND breed = '{breed}';"

        cursor.execute(select_data)
        image_path = cursor.fetchone()

        cursor.close()

        #display selectbreed image full screen
        self.bg = Image.open(image_path[0])
        self.bg = self.bg.resize((1300, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        self.breed_label = Label(self.root, text=breed, font=("calibri", 50,"bold"),fg="black")
        self.breed_label.place(x=40, y=80)

        self.back_button = Button(self.root, text="Back", font=("calibri", 18, "bold"), bg="#eef4f4", fg="black", bd=0, cursor="hand2", command=partial(self.selectPetBreed, pet_type))
        self.back_button.place(x=1000, y=650)

        self.topNavBar()
        if pet_type == 'dog' :      
        # #dogs button white
            self.dogs_button.config(bg="white", fg="#242323")
        else:
            self.cats_button.config(bg="white", fg="#242323")

        #ask question about the breed label
        self.ask_breed_label = Label(self.root, text=f"Ask Anything about the {breed}.", font=("calibri", 20,"bold"), bg="#f8f8fa", fg="black")
        self.ask_breed_label.place(x=650, y=300)
        
        #Entry box for the question
        self.question_entry = Entry(self.root, font=("calibri", 18), bg="white", fg="black")
        self.question_entry.place(x=650, y=350, width=400, height=40)
        
        #ask button
        self.ask_button = Button(self.root, text="Ask", font=("calibri", 18, "bold"), bg="#f8f8fa", fg="black", bd=0, cursor="hand2", command= partial(self.askBreedQuestion, pet_type, breed))
        self.ask_button.place(x=1050, y=350)

        if pet_type == "cat":
            self.breed_label.config(fg="#eef4f4", bg="black")
            self.ask_breed_label.config(fg="#eef4f4", bg="black")
            self.question_entry.config(fg="#eef4f4", bg="black")
            self.ask_button.config(fg="#eef4f4", bg="black")
            self.back_button.config(fg="#eef4f4", bg="black")
        
    def askBreedQuestion(self, pet_type, breed):
        question=self.question_entry.get()
        
        #get the answer from the database
        answer=self.rag.getAnswer(pet_type, breed, question)
        
        #a frame to display the answer
        self.answer_frame = Frame(self.root)
        self.answer_frame.place(x=650, y=400, width=600, height=200)

        #display the answer
        self.answer_label = Label(self.answer_frame, text=answer, font=("calibri", 18),fg="black")
        self.answer_label.config(wraplength=450)
        self.answer_label.place(x=0, y=0)

        if pet_type == "cat":
            self.answer_label.config(fg="#eef4f4", bg="black")
            self.answer_frame.config(bg="black")
        
        #clear the entry box
        self.question_entry.delete(0, END)
    
    # adding signup page entry boxes data to the database
    def signup_data(self):
    #get the data from the entry boxes
        self.first_name = self.first_name_entry.get()
        self.last_name = self.last_name_entry.get()
        self.email = self.email_entry.get()
        self.mobile = self.mobile_entry.get()
        self.password = self.password_entry.get()
        self.confirm_password = self.confirm_password_entry.get()
        
         #check if the data is empty
        if self.first_name == "" or self.last_name == "" or self.email == "" or self.mobile == "" or self.password == "" or self.confirm_password == "":
            messagebox.showerror("Error", "All fields are required")
            return
        #email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            messagebox.showerror("Error", "Invalid Email")
            return
        else:
            # checking the user exists or not with email abefore signup
            cursor = pdsdb.cursor()
            select_data = f"SELECT * FROM user_info WHERE email = '{self.email}'"
            cursor.execute(select_data)
            user = cursor.fetchone()
            if user:
                messagebox.showerror("Error", "You already have an account with this email !")
                return
            
        #mobile validation
        if not re.fullmatch(r"^[0-9]{10}$", self.mobile):
            messagebox.showerror("Error", "Invalid Mobile Number")
            return
        #password validation
        if len(self.password) < 8 or not re.search("[a-z]", self.password) or not re.search("[A-Z]", self.password) or not re.search("[0-9]", self.password) or not re.search("[@#$%^&+=]", self.password):
            messagebox.showerror("Error", "Password must contain at least 8 characters, including letters, numbers and a special character")
            return
        #check if the password and confirm password are the same
        if self.password != self.confirm_password:
            messagebox.showerror("Error", "Password and Confirm Password should be the same")
            return
        

        print("Sending OTP to your account to verify you")
        self.user_full_name_for_email = self.first_name + ' ' + self.last_name
        self.sent_OTP = self.send_OTP(self.email)
        self.enterOTPSignupScreen()
        # inserting the data to the database
        

    def enterOTPSignupScreen(self):

        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
        
        #crete a new frame for the forgot password page
        self.enter_otp_signup_frame = Frame(self.root, bg="black")
        self.enter_otp_signup_frame.place(x=0, y=0, width=1300, height=750)

        self.signup_label = Label(self.enter_otp_signup_frame, text="Please finish the SIGNUP by verifying your Account...", font=("calibri", 16, "bold"), bg="#080808", fg="WHITE")
        self.signup_label.place(x=200, y=300)

        self.enter_otp_label = Label(self.enter_otp_signup_frame, text="Enter your OTP:", font=("calibri", 18), bg="black", fg="white")
        self.enter_otp_label.place(x=350, y=350)
        
        #otp entry
        self.otp_entry = Entry(self.enter_otp_signup_frame, font=("calibri", 20), bg="white", fg="black", bd=0)
        self.otp_entry.place(x=550, y=350)

        #submit button
        self.verify_otp_button = Button(self.enter_otp_signup_frame, text="Submit OTP", font=("calibri", 18), bg="midnight blue", fg="white", bd=1, cursor="hand2")
        self.verify_otp_button.place(x=550, y=420)
        self.verify_otp_button.config(command=partial(self.verify_otp_signup))

        # Back
        self.back_button = Button(self.enter_otp_signup_frame, text="Back", font=("calibri", 18, "bold"), bg="#010101", fg="white", bd=0, cursor="hand2",activebackground="Black", activeforeground="white")
        self.back_button.place(x=200, y=650)
        self.back_button.config(command=self.loginScreen)
    
    # Verfify Email with OTP before SIGNUP
    def verify_otp_signup(self):
        entered_OTP = self.otp_entry.get()
        sent_OTP = self.sent_OTP
        print(entered_OTP)
        print(sent_OTP)
        if self.is_otp_match(sent_OTP, entered_OTP) == TRUE:
             self.insert_singup_data_to_DB()
        else:
            messagebox.showerror("ERROR", "Invalid OTP !")
    
    def insert_singup_data_to_DB(self):
       
        cursor = pdsdb.cursor()
        insert_data = f"INSERT INTO user_info (email,first_name,last_name, mobile, password) VALUES ('{self.email}', '{self.first_name}', '{self.last_name}',  '{self.mobile}', '{self.password}')"
        cursor.execute(insert_data)
        pdsdb.commit()
        messagebox.showinfo("Success", "You have successfully registered")
        self.loginScreen()
        
       
    #login page validation with the database
    def login_validation(self):
        #get the data from the entry boxes
        email = self.username_entry.get()
        password = self.password_entry.get()
        
        # checking the email and password with the database
        cursor = pdsdb.cursor()
        select_data = f"SELECT * FROM user_info WHERE email = '{email}' AND password = '{password}'"
        cursor.execute(select_data)
        user = cursor.fetchone()

        if user:
            self.user_id=user[0]
            self.email=user[1]
            self.first_name=user[2]
            self.last_name=user[3]
            self.mobile=user[4]
            self.current_password=user[5]
            self.welcomeScreen()
        elif email == "admin" and password == "admin":
            self.adminScreen()
        else:
            messagebox.showerror("Error", "Invalid Email or Password")
            return
    
       

    def toggle_reset_password_visibility(self):     
        if self.password_visible:
            # Hide the password and update the button icon
            self.new_confirm_password_entry.config(show="*")
            self.toggle_button_for_confirm_password.config(image=self.show_icon)
            self.password_visible = False
        else:
            # Show the password and update the button icon
            self.new_confirm_password_entry.config(show="")
            self.toggle_button_for_confirm_password.config(image=self.hide_icon)
            self.password_visible = True
        
    #forgot password page
    def forgotPasswordScreen(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
        
        #crete a new frame for the forgot password page
        self.forgot_password_frame = Frame(self.root, bg="black")
        self.forgot_password_frame.place(x=0, y=0, width=1300, height=750)
        
         #VERIFY YOUR ACCOUNT
        self.forgot_password_label = Label(self.forgot_password_frame, text="VERIFY YOUR ACCOUNT", font=("calibri", 30, "bold"), bg="#010204", fg="white")
        self.forgot_password_label.place(x=450, y=70)


        #email label
        self.email_label = Label(self.forgot_password_frame, text="Please Enter your Email ID :", font=("calibri", 18), bg="black", fg="white")
        self.email_label.place(x=200, y=270)
        
        
        self.email_underline_label = Label(self.forgot_password_frame, text="_________________________________", font=("calibri", 18), bg="black", fg="white")
        self.email_underline_label.place(x=480, y=270)

        self.verify_email_entry = Entry(self.forgot_password_frame, font=("calibri", 18), bg="black", fg="white", bd=0,relief="ridge",insertbackground="white", width=35)
        self.verify_email_entry.place(x=500, y=268)

        #validate the current password
        self.send_otp_button = Button(self.forgot_password_frame, text="SEND OTP", font=("calibri", 18), bg="midnight blue", fg="white", bd=1, cursor="hand2",activebackground="black", activeforeground="white")
        self.send_otp_button.place(x=600, y=350)
        self.send_otp_button.config(command=partial(self.user_verification))

        # Load the image
        self.image = Image.open("images/back_button_logo.png")
        self.image = self.image.resize((90, 50), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)


        # Create a Button with the image
        # self.back_button = Button(self.forgot_password_frame, image=self.image, command=self.loginScreen, bg="black", bd=0, cursor="hand2",activebackground="black")
        # self.back_button.place(x=200, y=600)
        
            
        #back button
        self.back_button = Button(self.forgot_password_frame, text="BACK", font=("calibri", 18,"bold"), bg="black", fg="white", bd=0, cursor="hand2")
        self.back_button.place(x=250, y=600)
        self.back_button.config(command=self.loginScreen)
    
    # Method to verify user with the email
    def user_verification(self):
        # storing in self.entered_email to access in other screens as well
        self.entered_email = self.verify_email_entry.get()

        entered_email = self.entered_email
        print("You mail is :"+entered_email)
        # validate email criteria
        if self.validate_email(entered_email) == FALSE:
            messagebox.showerror("Error", "Invalid Email")
            return
        
        #checking user exists with this email in DB or not
        user = self.get_user_by_email(entered_email)

        # If user exists, send OTP or else show error
        if user:
            # Combining user first and last name Storing user full name to use name in email body when sending email
            self.user_full_name_for_email = f'{user[2]} {user[3]}' 

            sent_otp = self.send_OTP(entered_email)
            self.enterOTPScreen(sent_otp, entered_email)
        
        else:
            messagebox.showerror("Error", "You don't have an account with this Email, please SIGNUP!")
            self.signupScreen
    
    # Generates and return the OTP
    def generate_otp(self):
        digits = "0123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[random.randint(0, 9)]
        return OTP
    
    #  sends OTP to the Email
    def send_OTP(self, entered_email):
        otp = self.generate_otp()

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # or 465 for SSL
        smtp_username = 'petpawfectportions@gmail.com'
        smtp_password = 'bmpt xwnv lecw jrxy'

        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)

        msg = MIMEMultipart()
        msg['From'] = 'petpawfectportions@gmail.com'
        msg['To'] = entered_email
        msg['Subject'] = 'OTP for Verification'

        body = f'Hi {self.user_full_name_for_email},\n\
        \n\
        Thank you for choosing our platform for your account needs. To ensure the security of your account, we have generated a One-Time Password (OTP) for you to verify your identity.\n\
        \n\
        Your OTP: {otp}\n\nPlease enter this OTP on the verification page to complete the verification process.\nIf you did not request this OTP, please contact our support team immediately.\n\nThank you,\nPawfect portions'

        msg.attach(MIMEText(body, 'plain'))

        smtp.send_message(msg)
        messagebox.showinfo("Success", "OTP sent successfully")

        smtp.quit()
        return otp

    # Verfify OTP for forgot pwd
    def verify_otp_forgot_pwd(self, sent_OTP):
        print(sent_OTP)
        entered_OTP = self.otp_entry.get()
        print(entered_OTP)
        if self.is_otp_match(sent_OTP, entered_OTP):
             messagebox.showinfo("success", "You have been verified !")
             self.enterResetPasswordScreen()
        else:
             messagebox.showerror("ERROR", "Invalid OTP !")

    def is_otp_match(self, sent_OTP, entered_OTP):
        print(sent_OTP)
        if sent_OTP == entered_OTP:
            return TRUE
        else:
            return FALSE

    def enterOTPScreen(self, sent_otp, entered_email):

        for i in self.forgot_password_frame.winfo_children():
            i.destroy()
        
        self.text_label = Label(self.forgot_password_frame, text=f"Please verify your account with the OTP that we sent to {entered_email} !", font=("calibri", 16), bg="#080808", fg="WHITE")
        self.text_label.place(x=200, y=300)

        #otp label
        self.enter_otp_label = Label(self.forgot_password_frame, text="Enter your OTP:", font=("calibri", 18), bg="black", fg="white")
        self.enter_otp_label.place(x=350, y=350)
        
        #otp entry
        self.otp_entry = Entry(self.forgot_password_frame, font=("calibri", 20), bg="white", fg="black", bd=0)
        self.otp_entry.place(x=550, y=350)

        #submit button
        self.verify_otp_button = Button(self.forgot_password_frame, text="Submit", font=("calibri", 18), bg="midnight blue", fg="white", bd=1, cursor="hand2")
        self.verify_otp_button.place(x=580, y=420)
        self.verify_otp_button.config(command=partial(self.verify_otp_forgot_pwd, sent_otp))

        # Back
        self.back_button = Button(self.forgot_password_frame, text="Back", font=("calibri", 18, "bold"), bg="#010101", fg="white", bd=0, cursor="hand2",activebackground="Black", activeforeground="white")
        self.back_button.place(x=200, y=650)
        self.back_button.config(command=self.loginScreen)

    def enterResetPasswordScreen(self):

        # Destroying all widgets that are already on the forgot password frame
        for i in self.forgot_password_frame.winfo_children():
                i.destroy()

        self.new_password_label = Label(self.forgot_password_frame, text="Enter New Password", font=("calibri", 20), bg="#010204", fg="white")
        self.new_password_label.place(x=460, y=140)
        
        self.new_password_underline_label = Label(self.forgot_password_frame, text="______________________", font=("calibri", 18), bg="white", fg="white")
        self.new_password_underline_label.place(x=450, y=200)

        self.new_password_entry = Entry(self.forgot_password_frame, font=("calibri", 20), bg="black", fg="white", bd=0,insertbackground="white")
        self.new_password_entry.place(x=450, y=198)

        #Confirm Password labelS
        self.new_confirm_password_label = Label(self.forgot_password_frame, text="Confirm Password", font=("calibri", 20), bg="#010204", fg="white")
        self.new_confirm_password_label.place(x=470, y=260)
        
        self.new_confirm_password_underline_label = Label(self.forgot_password_frame, text="______________________", font=("calibri", 18), bg="white", fg="white") 
        self.new_confirm_password_underline_label.place(x=450, y=320)

        self.new_confirm_password_entry = Entry(self.forgot_password_frame, font=("calibri", 20), bg="#010204", fg="white", bd=0,insertbackground="white", show="*")
        self.new_confirm_password_entry.place(x=450, y=318)

        self.password_visible = False
        # Create a button to toggle password visibility
        self.toggle_button_for_confirm_password = tk.Button(self.forgot_password_frame, image=self.show_icon, command=self.toggle_reset_password_visibility, borderwidth=0,highlightthickness=0, bg="black", activebackground="black")
        self.toggle_button_for_confirm_password.place(x=720, y=318)

        #reset password button
        self.reset_password_button = Button(self.forgot_password_frame, text="Reset Password", font=("calibri", 18), bg="midnight blue", fg="white", bd=0, cursor="hand2",activebackground="#010204", activeforeground="white")
        self.reset_password_button.place(x=500, y=500)

        self.reset_password_button.config(command= self.update_password_to_DB)

        # Back
        self.back_button = Button(self.forgot_password_frame, text="Back", font=("calibri", 18, "bold"), bg="#010101", fg="white", bd=0, cursor="hand2",activebackground="Black", activeforeground="white")
        self.back_button.place(x=200, y=650)
        self.back_button.config(command=self.forgotPasswordScreen)


    #after submitting the email, check if the email is in the database
    def get_user_by_email(self, entered_email):

        # Print the entered email address
        print("Entered Email Address:", entered_email)
        
        #check if the email is in the database
        cursor = pdsdb.cursor()
        select_data = f"SELECT * FROM user_info WHERE email = '{entered_email}'"
        cursor.execute(select_data)
        user = cursor.fetchone()


        return user
    
    def validate_email(self, entered_email):
        #email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", entered_email) or entered_email == "":
            return FALSE

    def validate_password(self):
    #password validation
        if len(self.new_password_entry.get()) < 8 or not re.search("[a-z]", self.new_password_entry.get()) or not re.search("[A-Z]", self.new_password_entry.get()) or not re.search("[0-9]", self.new_password_entry.get()) or not re.search("[@#$%^&+=]", self.new_password_entry.get()):
            messagebox.showerror("Error", "Password must contain at least 8 characters, including letters, numbers and a special character")
            return FALSE
        #check if the password and confirm password are the same
        if self.new_password_entry.get() != self.new_confirm_password_entry.get():
            messagebox.showerror("Error", "Password and Confirm Password should be the same")
            return FALSE
        else:
            return TRUE
        
    def update_password_to_DB(self):
        #password validation
        if self.validate_password() == TRUE:
            new_password = self.new_confirm_password_entry.get()
            email = self.entered_email
            cursor = pdsdb.cursor()
            update_data = f"UPDATE user_info SET password = '{new_password}' WHERE email = '{email}'"
            cursor.execute(update_data)
            pdsdb.commit()
            messagebox.showinfo("Success", "Password Updated, Redirecting to the Login Screen")
            self.loginScreen()
    
   
    #creating a profile page window and displaying the user details that are stored in the database for the signed in user
    def profileScreen(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
            
        #creating a new frame for the profile page
        self.profile_frame = Frame(self.root, bg="black")
        self.profile_frame.place(x=0, y=0, width=1300, height=750)

        # self.background_profile_image = Image.open("images/black-background-with-focus-spot-light.jpg")
        # self.background_profile_image = self.background_profile_image.resize((1300, 750), Image.LANCZOS)
        # self.background_profile_image = ImageTk.PhotoImage(self.background_profile_image)
        # self.background_profile_image_label = Label(self.profile_frame, image=self.background_profile_image).place(x=0, y=0, relwidth=1, relheight=1)
        

        self.userprofile = Image.open("images/profile_logo.png")
        self.userprofile = self.userprofile.resize((500, 500), Image.LANCZOS)
        self.userprofile = ImageTk.PhotoImage(self.userprofile)

        self.userprofile_image = Label(self.profile_frame, image=self.userprofile, bg="black").place(x=0, y=50)

        y = 200
        for i in range (0,4):
            self.colon_label = Label(self.profile_frame, text=":", font=("calibri", 18), bg="#010204", fg="white")
            self.colon_label.place(x=620, y=y)
            y = y+50
            
    
        #profile label
        self.profile_label = Label(self.profile_frame, text="My Profile", font=("calibri", 30), bg="#010204", fg="white")
        self.profile_label.place(x=550, y=20)
        
        #First Name label
        self.first_name_label = Label(self.profile_frame, text="First Name", font=("calibri", 18), bg="#010204", fg="white")
        self.first_name_label.place(x=450, y=200)
        
        #Last Name label
        self.last_name_label = Label(self.profile_frame, text="Last Name", font=("calibri", 18), bg="#010204", fg="white")
        self.last_name_label.place(x=450, y=250)
        
        #Email label
        self.email_label = Label(self.profile_frame, text="Email", font=("calibri", 18), bg="#010204", fg="white")
        self.email_label.place(x=450, y=300)
        
        #Mobile label
        self.mobile_label = Label(self.profile_frame, text="Mobile", font=("calibri", 18), bg="#010204", fg="white")
        self.mobile_label.place(x=450, y=350)

        # full_name = f'{self.first_name} {self.last_name}'
        # self.last_name_label = Label(self.profile_frame, text=full_name, font=("calibri", 18), bg="#010204", fg="white")
        # self.last_name_label.place(x=500, y=250)

        # display data as label
        self.first_name_label = Label(self.profile_frame, text=self.first_name, font=("calibri", 18), bg="#010204", fg="white")
        self.first_name_label.place(x=650, y=200)

        self.last_name_label = Label(self.profile_frame, text=self.last_name, font=("calibri", 18), bg="#010204", fg="white")
        self.last_name_label.place(x=650, y=250)

        self.email_label = Label(self.profile_frame, text=self.email, font=("calibri", 18), bg="#010204", fg="white")
        self.email_label.place(x=650, y=300)

        self.mobile_label = Label(self.profile_frame, text=self.mobile, font=("calibri", 18), bg="#010204", fg="white")
        self.mobile_label.place(x=650, y=350)

        
        #back button
        self.back_button = Button(self.profile_frame, text="Back", font=("calibri", 18), bg="#010204", fg="white", bd=0, cursor="hand2",activebackground="#010204", activeforeground="white")
        self.back_button.place(x=400, y=500)
        self.back_button.config(command=self.welcomeScreen)

        #update password button
        self.update_password_button = Button(self.profile_frame, text="Update Password", font=("calibri", 18), bg="midnight blue", fg="white", bd=1, cursor="hand2",activebackground="#010204", activeforeground="white")
        self.update_password_button.place(x=700, y=500)
        self.update_password_button.config(command=self.updatePassword)
        
       #view my pet profile
        
    #updatePassword
    def updatePassword(self):
        #clear profile_frame
        for i in self.profile_frame.winfo_children():
            i.destroy()
        
        #Enter your current password
        self.current_password_label1 = Label(self.profile_frame, text="Enter Current Password", font=("calibri", 20), bg="#010204", fg="white")
        self.current_password_label1.place(x=480, y=100)
        
        self.current_password_label = Label(self.profile_frame, text="_____________________", font=("calibri", 18), bg="white", fg="white")
        self.current_password_label.place(x=480, y=170)

        self.current_password_entry = Entry(self.profile_frame, font=("calibri", 20), bg="black", fg="white", bd=0,relief="ridge",insertbackground="white")
        self.current_password_entry.place(x=480, y=168)

        #validate the current password
        self.validate_password_button = Button(self.profile_frame, text="Validate Password", font=("calibri", 18), bg="#010204", fg="white", bd=0, cursor="hand2",activebackground="black", activeforeground="white")
        self.validate_password_button.place(x=520, y=240)
        self.validate_password_button.config(command=self.profile_updatePassword)

        #back button
        self.back_button = Button(self.profile_frame, text="BACK", font=("calibri", 18,"bold"), bg="black", fg="white", bd=0, cursor="hand2")
        self.back_button.place(x=250, y=600)
        self.back_button.config(command=self.profileScreen)                                                    
    #update the password form user profile screen
    def profile_updatePassword(self):
        #check if password is correct
        current_password = self.current_password_entry.get()
        

        if current_password!=self.current_password:

            #passwords donot match
            messagebox.showerror("Error", "Incorrect Password")
            return
        else:
            self.current_password_label1.destroy()
            self.current_password_entry.destroy()
            self.validate_password_button.destroy()
            self.current_password_label.destroy()
            #New Password label
            self.new_update_password_label = Label(self.profile_frame, text="Enter New Password", font=("calibri", 20), bg="#010204", fg="white")
            self.new_update_password_label.place(x=450, y=100)
            
            self.new_update_password_label = Label(self.profile_frame, text="______________________", font=("calibri", 18), bg="white", fg="white")
            self.new_update_password_label.place(x=450, y=170)

            self.new_update_password_entry = Entry(self.profile_frame, font=("calibri", 20), bg="black", fg="white", bd=0,insertbackground="white")
            self.new_update_password_entry.place(x=450, y=168)

            #Confirm Password labelS
            self.confirm_update_password_label = Label(self.profile_frame, text="Confirm Password", font=("calibri", 20), bg="#010204", fg="white")
            self.confirm_update_password_label.place(x=470, y=240)
            
            self.confirm_update_password_label = Label(self.profile_frame, text="______________________", font=("calibri", 18), bg="white", fg="white") 
            self.confirm_update_password_label.place(x=450, y=280)

            self.confirm_update_password_entry = Entry(self.profile_frame, font=("calibri", 20), bg="#010204", fg="white", bd=0,insertbackground="white")
            self.confirm_update_password_entry.place(x=450, y=278)

            #update password button
            self.update_password_button = Button(self.profile_frame, text="Update Password", font=("calibri", 18), bg="#010204", fg="white", bd=0, cursor="hand2",activebackground="#010204", activeforeground="white")
            self.update_password_button.place(x=490, y=350)

            self.update_password_button.config(command= self.updatePassword_db_via_profile)

            #cancel button
            self.cancel_button = Button(self.profile_frame, text="Cancel", font=("calibri", 18), bg="#010204", fg="white", bd=0, cursor="hand2",activebackground="#010204", activeforeground="white")
            self.cancel_button.place(x=540, y=390)

            self.cancel_button.config(command=self.profileScreen)

    #updatePassword_db
    def updatePassword_db_via_profile(self):
        #get the new password
        new_password = self.new_update_password_entry.get()
        confirm_password = self.confirm_update_password_entry.get()

        print(new_password)
        print(confirm_password)

        #password validation
        if len(new_password) < 8 or not re.search("[a-z]", new_password) or not re.search("[A-Z]", new_password) or not re.search("[0-9]", new_password) or not re.search("[@#$%^&+=]", new_password):
            messagebox.showerror("Error", "Password must contain at least 8 characters, including letters, numbers and a special character")
            return
        #check if the password and confirm password are the same
        if new_password != confirm_password:
            messagebox.showerror("Error", "Password and Confirm Password should be the same")
            return
        else:
            #update the password
            cursor = pdsdb.cursor()
            print(self.email)
            update_data = f"UPDATE user_info SET password = '{new_password}' WHERE email = '{self.email}'"
            cursor.execute(update_data)
            pdsdb.commit()
            cursor.close()
            messagebox.showinfo("Success", "Password Updated!")
            # redirecting to home screen after password update
            self.welcomeScreen()
  
    #Dog pet profile page
    def dogProfileScreen(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
        
        #creating a new frame for the pet profile page
        self.pet_profile_frame = Frame(self.root, bg="black")
        self.pet_profile_frame.place(x=0, y=0, width=1300, height=750)
        
        self.dogbg =Image.open("images/dogprofile.jpg")
        self.dogbg = self.dogbg.resize((1300, 750), Image.LANCZOS)
        self.dogbg = ImageTk.PhotoImage(self.dogbg)
        self.dogbg_image = Label(self.pet_profile_frame, image=self.dogbg).place(x=0, y=0, relwidth=1, relheight=1)
        
        
        #create a back button to go back to the home page
        self.back_button = Button(self.pet_profile_frame, text="Back", font=("calibri", 18, "bold"), bg="#010101", fg="white", bd=0, cursor="hand2",activebackground="black", activeforeground="white")
        self.back_button.place(x=1000, y=650)
        self.back_button.config(command=self.welcomeScreen)
        
        #pet profile label 
        self.pet_profile_label = Label(self.pet_profile_frame, text="Add Your Dog Profile", font=("calibri", 40), bg="#010101", fg="white")
        self.pet_profile_label.place(x=430, y=30)

        # place colon
        y=150
        for i in range(0,5): 
            self.colon_lebel = Label(self.pet_profile_frame, text=":", bg="#010101", fg="white", font=("calibri", 20))
            self.colon_lebel.place(x=620, y=y)
            y = y+50
        
        #pet name label
        self.pet_name_label = Label(self.pet_profile_frame, text="Pet Name", font=("calibri", 20), bg="#010101", fg="white")
        self.pet_name_label.place(x=470, y=150)
        
        #pet name label
        self.pet_name_label = Label(self.pet_profile_frame, text="_____________________", font=("calibri", 20), bg="#010101", fg="white")
        self.pet_name_label.place(x=650, y=150)
        
        #pet name entry box
        self.pet_name_entry = Entry(self.pet_profile_frame, font=("calibri", 20),bg="#010101", bd=0,fg="white",relief="ridge",insertbackground="white")
        self.pet_name_entry.place(x=650, y=146)


        #pet breed dropdown menu below the pet name to select the breed German Shepherd, Labrador, French Bulldog, Golden Retriever, Siberian husky
        self.pet_breed_label = Label(self.pet_profile_frame, text="Pet Breed", font=("calibri", 20), bg="#010101", fg="white")
        self.pet_breed_label.place(x=470, y=200)
        self.pet_breed = StringVar()
        self.pet_breed.set("Select Breed")

        #get dog breeds from database
        breeds = self.getPetBreeds('dog')
        
        self.pet_breed_dropdown = OptionMenu(self.pet_profile_frame, self.pet_breed, *breeds)
        #self.pet_breed_dropdown = OptionMenu(self.pet_profile_frame, self.pet_breed, "German Shepherd", "Labrador", "Golden Retriever", "French Bulldog", "Siberian Husky")
        self.pet_breed_dropdown.config(font=("calibri", 15), bg="#242323", fg = "white")
        self.pet_breed_dropdown.place(x=670, y=205)
        
        
        #pet gender label
        self.pet_gender_label = Label(self.pet_profile_frame, text="Gender", font=("calibri", 20), bg="black", fg="white")
        self.pet_gender_label.place(x=470, y=250)  
        
        #radio buttons for pet gender male or female
        self.gender = StringVar(value=" ")
        self.male_radio = Radiobutton(self.pet_profile_frame,text="Male", variable=self.gender,value="Male", font=("calibri", 20), bg="#010101", fg="white", selectcolor="black")
        self.male_radio.place(x=650, y=247)
        
        self.female_radio = Radiobutton(self.pet_profile_frame,text="Female", variable=self.gender,value="Female",font=("calibri", 20), bg="#010101", fg="white", selectcolor="black")
        self.female_radio.place(x=750, y=247)
        
        #pet age label
        self.pet_age_label = Label(self.pet_profile_frame, text="Pet Age", font=("calibri", 20), bg="#010101", fg="white")
        self.pet_age_label.place(x=470, y=300)

        #pet age in months and years
        self.months = StringVar()
        self.years = StringVar()
        self.weight = StringVar()

        #create dropdown menu for years
        self.years_label = Label(self.pet_profile_frame, text="Years", font=("calibri", 20), bg="#010101", fg="white")
        self.years_label.place(x=650, y=300) 
        self.years_dropdown = OptionMenu(self.pet_profile_frame, self.years, *range(0, 25))
        self.years_dropdown.config(bg="#010101", fg="white")
        self.years_dropdown.place(x=730, y=303) 
        #create dropdown menu for months
        self.months_label = Label(self.pet_profile_frame, text="Months", font=("calibri", 20), bg="#010101", fg="white")
        self.months_label.place(x=790, y=300)  
        self.months_dropdown = OptionMenu(self.pet_profile_frame, self.months, *range(0, 12))
        self.months_dropdown.config(bg="#010101", fg="white")
        self.months_dropdown.place(x=890, y=303)  
         #dropdown menu for weight beside months
        # self.weight_label = Label(self.pet_profile_frame, text="Weight(lbs):", font=("calibri", 20), bg="#010101", fg="white")
        # self.weight_label.place(x=910, y=300)
        # self.weight_dropdown = OptionMenu(self.pet_profile_frame, self.weight, *range(1, 60))
        # self.weight_dropdown.config(bg="#010101", fg="white")
        # self.weight_dropdown.place(x=1010, y=303)                                                                                                                      
        #pet color label
        self.pet_color_label = Label(self.pet_profile_frame, text="Pet Color", font=("calibri", 20), bg="#010101", fg="white")
        self.pet_color_label.place(x=470, y=350)  
        
        #pet color label
        self.pet_color_label = Label(self.pet_profile_frame, text="_____________________", font=("calibri", 20), bg="#010101", fg="white")
        self.pet_color_label.place(x=650, y=350)
        
        #pet color entry box
        self.pet_color_entry = Entry(self.pet_profile_frame, font=("calibri", 20),bg="#010101", bd=0,fg="white",relief="ridge",insertbackground="white")
        self.pet_color_entry.place(x=650, y=346)

        #weight color label
        self.weight_label = Label(self.pet_profile_frame, text="Weight", font=("calibri", 20), bg="#010101", fg="white")
        self.weight_label.place(x=470, y=400)  

        #weight color label
        self.pet_color_label = Label(self.pet_profile_frame, text="_______ (in lbs)", font=("calibri", 20), bg="#010101", fg="white")
        self.pet_color_label.place(x=650, y=400)

        self.weight_entry = Entry(self.pet_profile_frame, font=("calibri", 20),bg="#010101", bd=0,fg="white",relief="ridge",insertbackground="white", width=6)
        self.weight_entry.place(x=650, y=397)
        
        
        # if(self.selected_pet):
        #     #use the selected pet data to fill the form
        #     self.pet_name_entry.insert(0, self.selected_pet[3])
        #     self.pet_breed.set(self.selected_pet[4])
        #     self.gender.set(self.selected_pet[5])
        #     self.years.set(self.selected_pet[7])
        #     self.months.set(self.selected_pet[8])
        #     self.weight.set(self.selected_pet[9])
        #     self.pet_color_entry.insert(0, self.selected_pet[6])
            #submit button
        self.pet_profile_submit_button = Button(self.pet_profile_frame, text="Submit", font=("calibri", 20), bg="midnight blue", fg="white", bd=1, cursor="hand2",activebackground="black", activeforeground="white")
        self.pet_profile_submit_button.place(x=650, y=485)
        self.pet_profile_submit_button.config(command=self.insertDogProfileData)
        
    #adding the dog pet profile data to the database
    def getPetBreeds(self, pet_type):
        #Get Dog breeds from database
        cursor = pdsdb.cursor()
        select_query = f"SELECT breed FROM pet_image_urls WHERE pet_type = '{pet_type}';"

        cursor.execute(select_query)
        breeds = cursor.fetchall()

        cursor.close()

        #
        breedsArray = []

        # Iterating through the list of tuples
        for breed_tuple in breeds:
            # Iterating through the tuple
            # 'breed' represents a single tuple in the list
            for breed in breed_tuple:
                breedsArray.append(breed)

        return breedsArray

    #dogpetProfileData

    def insertDogProfileData(self):
        #take data
        pet_name = self.pet_name_entry.get()
        pet_breed = self.pet_breed.get()
        pet_gender = self.gender.get()
        years = self.years.get()
        months = self.months.get()
        #pet_age = years+'Y,'+months+'M'
        pet_year = self.years.get()
        pet_month = self.months.get()
        pet_weight = self.weight_entry.get()
        #print(pet_age)
        pet_color = self.pet_color_entry.get()
        
        #duplication check for pet name
        cursor = pdsdb.cursor()
        select_query = f"SELECT pet_name FROM pet_info WHERE pet_name = '{pet_name}' AND user_id = '{self.user_id}' AND pet_type = 'Dog'"
        cursor.execute(select_query)
        pet = cursor.fetchone()
        cursor.close()
        if pet:
            messagebox.showerror("Error", "A dog with same name already exists !")
            return
        
        #check if the data is empty
        if pet_name == "" or pet_breed == "Select Breed" or pet_gender == " " or years == "" or months == "" or pet_color == "" or pet_weight == "":
            messagebox.showerror("Error", "All fields are required")
            return
        # check for numeric or decimal, and weight should be less than 500lb for dog(No dog weigh more than 400lb till now)
        if self.is_weight_valid(pet_weight, 'Dog'):
            # Insert into database if all validation passes
            cursor = pdsdb.cursor()
            insert_data = f"INSERT INTO pet_info (user_id, pet_type, pet_name,pet_breed, pet_gender, pet_color, pet_weight, pet_year, pet_month) VALUES ({self.user_id}, 'Dog', '{pet_name}', '{pet_breed}', '{pet_gender}', '{pet_color}', '{pet_weight}', '{pet_year}', '{pet_month}')"
            cursor.execute(insert_data)
            pdsdb.commit()
            messagebox.showinfo("Success", "Dog Profile Created !")
            self.welcomeScreen()
        


    
    
    def catProfileScreen(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
        
        #creating a new frame for the pet profile page
        self.pet_profile_frame = Frame(self.root, bg="black")
        self.pet_profile_frame.place(x=0, y=0, width=1300, height=750)
        
        self.dogbg =Image.open("images/catprofile.jpg")
        self.dogbg = self.dogbg.resize((1300, 750), Image.LANCZOS)
        self.dogbg = ImageTk.PhotoImage(self.dogbg)
        self.dogbg_image = Label(self.pet_profile_frame, image=self.dogbg).place(x=0, y=0, relwidth=1, relheight=1)
        
        
        #create a back button to go back to the home page
        self.back_button = Button(self.pet_profile_frame, text="Back", font=("calibri", 18, "bold"), bg="#010101", fg="white", bd=0, cursor="hand2",activebackground="Black", activeforeground="white")
        self.back_button.place(x=1000, y=650)
        self.back_button.config(command=self.welcomeScreen)
        
        #pet profile label 
        self.pet_profile_label = Label(self.pet_profile_frame, text="Add Your Cat Profile", font=("calibri", 40), bg="#010101", fg="white")
        self.pet_profile_label.place(x=430, y=30)

        # place colon
        y=150
        for i in range(0,6): 
            self.colon_lebel = Label(self.pet_profile_frame, text=":", bg="#010101", fg="white", font=("calibri", 20))
            self.colon_lebel.place(x=620, y=y)
            y = y+50
        
        #pet name label
        self.pet_name_label = Label(self.pet_profile_frame, text="Pet Name", font=("calibri", 20), bg="#010101", fg="white")
        self.pet_name_label.place(x=470, y=150)
        
        #pet name label
        self.pet_name_label = Label(self.pet_profile_frame, text="_____________________", font=("calibri", 20), bg="#010101", fg="white")
        self.pet_name_label.place(x=650, y=150)
        
        #pet name entry box
        self.pet_name_entry = Entry(self.pet_profile_frame, font=("calibri", 20),bg="#010101", bd=0,fg="white",relief="ridge",insertbackground="white")
        self.pet_name_entry.place(x=650, y=146)


        #pet breed dropdown menu below the pet name to select the breed
        self.pet_breed_label = Label(self.pet_profile_frame, text="Pet Breed", font=("calibri", 20), bg="#010101", fg="white")
        self.pet_breed_label.place(x=470, y=200)
        self.pet_breed = StringVar()
        self.pet_breed.set("Select Breed")

        #get dog breeds from database
        cat_breeds = self.getPetBreeds('cat')

        self.pet_breed_dropdown = OptionMenu(self.pet_profile_frame, self.pet_breed, *cat_breeds)
        self.pet_breed_dropdown.config(font=("calibri", 15), bg="#242323", fg = "white")
        self.pet_breed_dropdown.place(x=670, y=205)

              
        #pet gender label
        self.pet_gender_label = Label(self.pet_profile_frame, text="Gender", font=("calibri", 20), bg="black", fg="white")
        self.pet_gender_label.place(x=470, y=250)  
        
        #radio buttons for pet gender male or female
        self.gender = StringVar(value=" ")
        self.male_radio = Radiobutton(self.pet_profile_frame,text="Male", variable=self.gender,value="Male", font=("calibri", 20), bg="#010101", fg="white", selectcolor="black")
        self.male_radio.place(x=650, y=247)
        
        self.female_radio = Radiobutton(self.pet_profile_frame,text="Female", variable=self.gender,value="Female",font=("calibri", 20), bg="#010101", fg="white", selectcolor="black")
        self.female_radio.place(x=750, y=247)
        
        #pet age label
        self.pet_age_label = Label(self.pet_profile_frame, text="Pet Age", font=("calibri", 20), bg="#010101", fg="white")
        self.pet_age_label.place(x=470, y=300)

        #pet age in months and years
        self.months = StringVar()
        self.years = StringVar()
        self.weight = StringVar()
        #create dropdown menu for years
        self.years_label = Label(self.pet_profile_frame, text="Years", font=("calibri", 20), bg="#010101", fg="white")
        self.years_label.place(x=650, y=300) 
        self.years_dropdown = OptionMenu(self.pet_profile_frame, self.years, *range(0,30))
        self.years_dropdown.config(bg="#010101", fg="white")
        self.years_dropdown.place(x=730, y=303) 
        #create dropdown menu for months
        self.months_label = Label(self.pet_profile_frame, text="Months", font=("calibri", 20), bg="#010101", fg="white")
        self.months_label.place(x=790, y=300)  
        self.months_dropdown = OptionMenu(self.pet_profile_frame, self.months, *range(0, 12))
        self.months_dropdown.config(bg="#010101", fg="white")
        self.months_dropdown.place(x=890, y=303)  
        #dropdown menu for weight beside months
        # self.weight_label = Label(self.pet_profile_frame, text="Weight(lbs):", font=("calibri", 20), bg="#010101", fg="white")
        # self.weight_label.place(x=960, y=300)
        # self.weight_dropdown = OptionMenu(self.pet_profile_frame, self.weight, *range(0, 60))
        # self.weight_dropdown.config(bg="#010101", fg="white")
        # self.weight_dropdown.place(x=1060, y=303)                                                                                                                       
        
        #pet color label
        self.pet_color_label = Label(self.pet_profile_frame, text="Pet Color", font=("calibri", 20), bg="#010101", fg="white")
        self.pet_color_label.place(x=470, y=350)  
        

        #pet color label
        self.pet_color_label = Label(self.pet_profile_frame, text="_____________________", font=("calibri", 20), bg="#010101", fg="white")
        self.pet_color_label.place(x=650, y=350)
        
        #pet color entry box
        self.pet_color_entry = Entry(self.pet_profile_frame, font=("calibri", 20),bg="#010101", bd=0,fg="white",relief="ridge",insertbackground="white")
        self.pet_color_entry.place(x=650, y=346)

        #weight label
        self.weight_label = Label(self.pet_profile_frame, text="Weight", font=("calibri", 20), bg="#010101", fg="white")
        self.weight_label.place(x=470, y=400)  

        #weight underline
        self.weight_label = Label(self.pet_profile_frame, text="_______ (in lbs)", font=("calibri", 20), bg="#010101", fg="white")
        self.weight_label.place(x=650, y=400)

        self.weight_entry = Entry(self.pet_profile_frame, font=("calibri", 20),bg="#010101", bd=0,fg="white",relief="ridge",insertbackground="white", width=6)
        self.weight_entry.place(x=650, y=397)
        
        #submit button
        self.pet_profile_submit_button = Button(self.pet_profile_frame, text="Submit", font=("calibri", 20), bg="midnight blue", fg="white", bd=1, cursor="hand2",activebackground="black", activeforeground="white")
        self.pet_profile_submit_button.place(x=650, y=485)
        self.pet_profile_submit_button.config(command=self.insertCatPetProfileData)

        
    def insertCatPetProfileData(self):
        #take data
        pet_name = self.pet_name_entry.get()
        pet_breed = self.pet_breed.get()
        pet_gender = self.gender.get()
         #pet_age = years+'Y,'+months+'M'
        pet_year = self.years.get()
        pet_month = self.months.get()
        pet_weight = self.weight_entry.get()
        #print(pet_age)
        pet_color = self.pet_color_entry.get()
        
        #duplication check for pet name
        cursor = pdsdb.cursor()
        select_query = f"SELECT pet_name FROM pet_info WHERE pet_name = '{pet_name}' AND user_id = '{self.user_id}' AND pet_type = 'Cat'"
        cursor.execute(select_query)
        pet = cursor.fetchone()
        cursor.close()
        if pet:
            messagebox.showerror("Error", "Pet already exists with the same name!")
            return
        #check if the data is empty
        if pet_name == "" or pet_breed == "Select Breed" or pet_gender == " " or pet_year == "" or pet_month == "" or pet_color == "" or pet_weight == "":
            messagebox.showerror("Error", "All fields are required")
            return
        if self.is_weight_valid(pet_weight, 'Cat'):
            #insert the data to the database
            cursor = pdsdb.cursor()
            insert_data = f"INSERT INTO pet_info (user_id, pet_type, pet_name,pet_breed, pet_gender, pet_color, pet_weight, pet_year, pet_month) VALUES ({self.user_id}, 'Cat', '{pet_name}', '{pet_breed}', '{pet_gender}', '{pet_color}', '{pet_weight}', '{pet_year}', '{pet_month}')" 
            cursor.execute(insert_data)
            pdsdb.commit()
            messagebox.showinfo("Success", "Cat Profile Created !")
            self.welcomeScreen()                         
  


    #pet profile screen
    def view_Profile(self):
        for i in self.root.winfo_children():
            i.destroy()
        self.pet_profile_frame = Frame(self.root, bg="black")
        self.pet_profile_frame.place(x=0, y=0, width=1300, height=750)

        # self.userprofile = Image.open("images/profile_logo.png")
        # self.userprofile = self.userprofile.resize((500, 500), Image.LANCZOS)
        # self.userprofile = ImageTk.PhotoImage(self.userprofile)

        # self.userprofile_image = Label(self.profile_frame, image=self.userprofile, bg="black").place(x=0, y=50)
        
        # Loading the edit logo
        self.edit_logo = Image.open("images/edit_logo.png")
        self.edit_logo = self.edit_logo.resize((30, 30), Image.LANCZOS)
        self.edit_logo = ImageTk.PhotoImage(self.edit_logo)

        # Loading the delete logo
        self.delete_logo = Image.open("images/delete_logo.png")
        self.delete_logo = self.delete_logo.resize((30, 30), Image.LANCZOS)
        self.delete_logo = ImageTk.PhotoImage(self.delete_logo)
        
        # Title label My Pet Profile
        self.pet_profile_title = Label(self.pet_profile_frame, text="My Pet Profiles", font=("calibri", 30), bg="black", fg="white")
        self.pet_profile_title.place(x=500, y=20)

        # Get data from pets table with user id
        cursor = pdsdb.cursor()
        select_data = f"SELECT * FROM pet_info WHERE user_id = {self.user_id}"
        cursor.execute(select_data)
        pets = cursor.fetchall()

         

        # Initial y position for pet information labels
        y_position = 100

         # Define labels
        pet_name_label = Label(self.pet_profile_frame, text="Pet Name", font=("calibri", 20), bg="black", fg="light blue")
        pet_name_label.place(x=50, y=y_position)

        pet_type_label = Label(self.pet_profile_frame, text="Pet Type", font=("calibri", 20), bg="black", fg="light blue")
        pet_type_label.place(x=200, y=y_position)

        pet_breed_label = Label(self.pet_profile_frame, text="Breed", font=("calibri", 20), bg="black", fg="light blue")
        pet_breed_label.place(x=350, y=y_position)

        pet_color_label = Label(self.pet_profile_frame, text="Pet color", font=("calibri", 20), bg="black", fg="light blue")
        pet_color_label.place(x=500, y=y_position)

        pet_year_label = Label(self.pet_profile_frame, text="Year", font=("calibri", 20), bg="black", fg="light blue")
        pet_year_label.place(x=650, y=y_position)
        
        pet_month_label = Label(self.pet_profile_frame, text="Month", font=("calibri", 20), bg="black", fg="light blue")
        pet_month_label.place(x=750, y=y_position)
        
        pet_weight_label = Label(self.pet_profile_frame, text="Weight(lbs)", font=("calibri", 20), bg="black", fg="light blue")
        pet_weight_label.place(x=850, y=y_position)

        pet_gender_label = Label(self.pet_profile_frame, text="Gender", font=("calibri", 20), bg="black", fg="light blue")
        pet_gender_label.place(x=1000, y=y_position)

        # Increment y position for the values
        y_position += 50  # Adjust this value based on your preference for spacing between labels and values

         # Iterate through the pets and display the data
        for pet in pets:
            pet_name_value = Label(self.pet_profile_frame, text=pet[3], font=("calibri", 18), bg="black", fg="white")
            pet_name_value.place(x=50, y=y_position)
                                                                                                                                                                                 
            pet_type_value = Label(self.pet_profile_frame, text=pet[2], font=("calibri", 18), bg="black", fg="white")
            pet_type_value.place(x=200, y=y_position)
                                                                                                                                                                                              
            pet_breed_value = Label(self.pet_profile_frame, text=pet[4], font=("calibri", 18), bg="black", fg="white")
            pet_breed_value.place(x=330, y=y_position)

            pet_color_value = Label(self.pet_profile_frame, text=pet[6], font=("calibri", 18), bg="black", fg="white")
            pet_color_value.place(x=530, y=y_position)

            pet_year_value = Label(self.pet_profile_frame, text=pet[8], font=("calibri", 18), bg="black", fg="white")
            pet_year_value.place(x=650, y=y_position)

            pet_month_value = Label(self.pet_profile_frame, text=pet[9], font=("calibri", 18), bg="black", fg="white")
            pet_month_value.place(x=750, y=y_position)
            
            pet_weight_value = Label(self.pet_profile_frame, text=pet[7], font=("calibri", 18), bg="black", fg="white")
            pet_weight_value.place(x=860, y=y_position)

            pet_gender_value = Label(self.pet_profile_frame, text=pet[5], font=("calibri", 18), bg="black", fg="white")
            pet_gender_value.place(x=1000, y=y_position)

             
            self.edit_logo_image_button = Button(self.pet_profile_frame, image=self.edit_logo, bg ="black", cursor="hand2", bd=0)
            self.edit_logo_image_button.place(x=1130, y=y_position)         
            self.edit_logo_image_button.config(command= partial(self.update_pet_data_new, pet))

            self.delete_logo_image_button = Button(self.pet_profile_frame, image=self.delete_logo, bg ="black", cursor="hand2", bd=0)
            self.delete_logo_image_button.place(x=1200, y=y_position)         
            self.delete_logo_image_button.config(command= partial(self.delete_pet, pet))

            # Increment y position for the next pet's information
            y_position += 50  # Adjust this value based on your preference for spacing between pet information
   
        
        # Back button
        self.back_button = Button(self.pet_profile_frame, text="Back", font=("calibri", 18), bg="black", fg="white", bd=0, cursor="hand2")
        self.back_button.place(x=50, y=650)
        self.back_button.config(command=self.welcomeScreen)
        
        # # Update pet data button
        # self.update_pet_data_button = Button(self.pet_profile_frame, text="Update Pet Data", font=("calibri", 18), bg="black", fg="white", bd=0, cursor="hand2")
        # self.update_pet_data_button.place(x=650, y=400)
        # self.update_pet_data_button.config(command=self.update_pet_data)
        
        # # Delete pet data button
        # self.delete_pet_data_button = Button(self.pet_profile_frame, text="Delete Pet Data", font=("calibri", 18), bg="black", fg="white", bd=0, cursor="hand2")
        # self.delete_pet_data_button.place(x=850, y=400)
        # self.delete_pet_data_button.config(command=self.delete_pet_data)

    def update_pet_data_new(self, pet):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
        
        #creating a new frame for the pet profile page
        self.update_pet_profile_frame = Frame(self.root, bg="black")
        self.update_pet_profile_frame.place(x=0, y=0, width=1300, height=750)
        
       
        pet_type = pet[2]

        if pet_type == 'Cat':
            self.cat_bg =Image.open("images/catprofile.jpg")
            self.cat_bg = self.cat_bg.resize((1300, 750), Image.LANCZOS)
            self.cat_bg = ImageTk.PhotoImage(self.cat_bg)
            self.cat_bg_image = Label(self.update_pet_profile_frame, image=self.cat_bg).place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.dog_bg =Image.open("images/dogprofile.jpg")
            self.dog_bg = self.dog_bg.resize((1300, 750), Image.LANCZOS)
            self.dog_bg = ImageTk.PhotoImage(self.dog_bg)
            self.dog_bg_image = Label(self.update_pet_profile_frame, image=self.dog_bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        #pet profile label 
        self.pet_profile_label = Label(self.update_pet_profile_frame, text="Update Your Pet Profile", font=("calibri", 40), bg="#010101", fg="white")
        self.pet_profile_label.place(x=430, y=30)

        # place colon
        y=150
        for i in range(0,4): 
            self.colon_lebel = Label(self.update_pet_profile_frame, text=":", bg="#010101", fg="white", font=("calibri", 18))
            self.colon_lebel.place(x=620, y=y)
            y = y+30
        
        #pet name label
        self.pet_name_label = Label(self.update_pet_profile_frame, text="Pet Name", font=("calibri", 16), bg="#010101", fg="white")
        self.pet_name_label.place(x=470, y=150)
        
        #pet name
        self.pet_name_value = Label(self.update_pet_profile_frame, text=pet[3], font=("calibri", 16), bg="#010101", fg="white")
        self.pet_name_value.place(x=650, y=150)

        # pet type label
        pet_type_label = Label(self.update_pet_profile_frame, text="Pet Type", font=("calibri", 16), bg="#010101", fg="white")
        pet_type_label.place(x=470, y=180)

        # pet type
        pet_type_value = Label(self.update_pet_profile_frame, text=pet[2], font=("calibri", 16), bg="#010101", fg="white")
        pet_type_value.place(x=650, y=180)

        #pet breed 
        self.pet_breed_label = Label(self.update_pet_profile_frame, text="Pet Breed", font=("calibri", 16), bg="#010101", fg="white")
        self.pet_breed_label.place(x=470, y=210)

        # Pet Breed value
        self.pet_breed_value = Label(self.update_pet_profile_frame, text=pet[4], font=("calibri", 16), bg="#010101", fg="white")
        self.pet_breed_value.place(x=650, y=210)
              
        #pet gender label
        self.pet_gender_label = Label(self.update_pet_profile_frame, text="Gender", font=("calibri", 16), bg="black", fg="white")
        self.pet_gender_label.place(x=470, y=240)  
        
        #pet gender value
        self.pet_gender_value = Label(self.update_pet_profile_frame, text=pet[5], font=("calibri", 16), bg="#010101", fg="white")
        self.pet_gender_value.place(x=650, y=240)

        #pet gender value
        self.pet_gender_value = Label(self.update_pet_profile_frame, text="You can update the following:", font=("calibri", 18), bg="#010101", fg="white")
        self.pet_gender_value.place(x=470, y=350)

        # place colon
        y=400
        for i in range(0,3): 
            self.colon_lebel = Label(self.update_pet_profile_frame, text=":", bg="#010101", fg="white", font=("calibri", 18))
            self.colon_lebel.place(x=620, y=y)
            y = y+50
        
        #pet age label
        self.pet_age_label = Label(self.update_pet_profile_frame, text="Pet Age", font=("calibri", 18), bg="#010101", fg="white")
        self.pet_age_label.place(x=470, y=400)

        #pet age in months and years
        self.months = StringVar(self.update_pet_profile_frame, pet[9])
        self.years = StringVar(self.update_pet_profile_frame, pet[8])
        #create dropdown menu for years
        self.years_label = Label(self.update_pet_profile_frame, text="Years", font=("calibri", 18), bg="#010101", fg="white")
        self.years_label.place(x=650, y=400) 
        self.years_dropdown = OptionMenu(self.update_pet_profile_frame, self.years, *range(0,30))
        self.years_dropdown.config(bg="#010101", fg="white")
        self.years_dropdown.place(x=730, y=403) 
        #create dropdown menu for months
        self.months_label = Label(self.update_pet_profile_frame, text="Months", font=("calibri", 18), bg="#010101", fg="white")
        self.months_label.place(x=790, y=400)  
        self.months_dropdown = OptionMenu(self.update_pet_profile_frame, self.months, *range(0, 12))
        self.months_dropdown.config(bg="#010101", fg="white")
        self.months_dropdown.place(x=890, y=403)                                                                                                                     
        
        #pet color label
        self.pet_color_label = Label(self.update_pet_profile_frame, text="Pet Color", font=("calibri", 18), bg="#010101", fg="white")
        self.pet_color_label.place(x=470, y=450)  
        
        #pet color label
        self.pet_color_label = Label(self.update_pet_profile_frame, text="_____________________", font=("calibri", 18), bg="#010101", fg="white")
        self.pet_color_label.place(x=650, y=450)

        #pet color entry box
        self.pet_color_entry = Entry(self.update_pet_profile_frame, font=("calibri", 18),bg="#010101", bd=0,fg="white",relief="ridge",insertbackground="white")
        self.pet_color_entry.place(x=650, y=446)
        self.pet_color_entry.insert(0, pet[6])

        #weight label
        self.weight_label = Label(self.update_pet_profile_frame, text="Weight", font=("calibri", 18), bg="#010101", fg="white")
        self.weight_label.place(x=470, y=500)  

        #weight underline
        self.weight_label = Label(self.update_pet_profile_frame, text="_______ (in lbs)", font=("calibri", 18), bg="#010101", fg="white")
        self.weight_label.place(x=650, y=500)

        self.weight_entry = Entry(self.update_pet_profile_frame, font=("calibri", 18),bg="#010101", bd=0,fg="white",relief="ridge",insertbackground="white", width=6)
        self.weight_entry.place(x=650, y=497)
        self.weight_entry.insert(0, pet[7])
        
        #create a back button to go back to the home page
        self.back_button = Button(self.update_pet_profile_frame, text="Back", font=("calibri", 18, "bold"), bg="#010101", fg="white", bd=0, cursor="hand2",activebackground="Black", activeforeground="white")
        self.back_button.place(x=470, y=650)
        self.back_button.config(command=self.view_Profile)

        #submit button
        self.pet_profile_submit_button = Button(self.update_pet_profile_frame, text="Update", font=("calibri", 20), bg="midnight blue", fg="white", bd=1, cursor="hand2",activebackground="black", activeforeground="white")
        self.pet_profile_submit_button.place(x=600, y=550)
        self.pet_profile_submit_button.config(command=partial(self.updatePetData,pet))
    
    def is_weight_valid(self, pet_weight, pet_type):
        try:
            weight_float = float(pet_weight)
            if pet_type == 'Cat' and weight_float>= 100:
                messagebox.showerror("Error",f"Please enter correct weight of your {pet_type}, Weight should be less than 100lb.\n\
                Entered weight: {pet_weight} lb")
                return FALSE
            if pet_type == 'Dog' and weight_float>= 400:
                messagebox.showerror("Error",f"Please enter correct weight of your {pet_type}, Weight should be less than 400lb.\n\
                Entered weight: {pet_weight} lb")
                return FALSE
            else:
                return TRUE
        except ValueError:
            messagebox.showerror("Error","Weight should be only number or decimal.")
            return FALSE  

    def updatePetData(self, pet):
        pet_name = pet[3]
        pet_type = pet[2]
        pet_gender = pet[5]    
        pet_color = self.pet_color_entry.get() 
        pet_year = self.years.get()
        pet_month = self.months.get() 
        pet_weight = self.weight_entry.get() 

        #check if the data is empty
        if pet_color == "" or pet_year == "" or pet_month == "" or pet_weight == "":
            messagebox.showerror("Error", "All fields are required")
            return
        if self.is_weight_valid(pet_weight, pet_type):
            #update the data to the database
            cursor = pdsdb.cursor()
            update_data = f"UPDATE pet_info SET pet_color = '{pet_color}', pet_year = '{pet_year}', pet_month = '{pet_month}', pet_weight = '{pet_weight}' WHERE user_id = {self.user_id} AND pet_name = '{pet_name}'"
            cursor.execute(update_data)
            pdsdb.commit()
            messagebox.showinfo("Success", f"{pet_type} Profile Updated")
            self.view_Profile()
    

            
    def delete_pet(self, pet):
        pet_id = pet[0]
        #Show the ALERT message box to confirm the deletion
        confirm = messagebox.askyesno("Delete Pet Profile", "Are you sure you want to delete this pet profile?")
        if not confirm:
            return
        cursor = pdsdb.cursor()
        delete_query = f"DELETE FROM pet_info WHERE pet_id = {pet_id}"
        cursor.execute(delete_query)
        pdsdb.commit()
        cursor.close()
        messagebox.showinfo("Success", "Pet Profile Deleted")
        self.view_Profile()

        
    #delete pet data button
    # def delete_pet_data(self):
    #     #clear the window
    #     for i in self.root.winfo_children():
    #         i.destroy()
    #     #creating a new frame for the pet profile page        
                                                      
    #     self.pet_profile_frame = Frame(self.root, bg="black")
    #     self.pet_profile_frame.place(x=0, y=0, width=1200, height=750)
        
        
    #     self.dogbg =Image.open("images/dogprofile.jpg")
    #     self.dogbg = self.dogbg.resize((1200, 750), Image.LANCZOS)
    #     self.dogbg = ImageTk.PhotoImage(self.dogbg)
    #     self.dogbg_image = Label(self.pet_profile_frame, image=self.dogbg).place(x=0, y=0, relwidth=1, relheight=1)
        
    #     #create a back button to go back to the home page
    #     self.back_button = Button(self.pet_profile_frame, text="Back", font=("calibri", 18, "bold"), bg="#010101", fg="white", bd=0, cursor="hand2",activebackground="black", activeforeground="white")
    #     self.back_button.place(x=1000, y=650)
    #     self.back_button.config(command=self.welcomeScreen)
        
    #     #pet profile label 
    #     self.pet_profile_label = Label(self.pet_profile_frame, text="Delete Your Pet Profile", font=("calibri", 40), bg="#010101", fg="white")
    #     self.pet_profile_label.place(x=430, y=30)
        
    #     # username name label
    #     self.pet_name_label = Label(self.pet_profile_frame, text="Hello! " + self.first_name, font=("calibri", 20), bg="#010101", fg="white")
    #     self.pet_name_label.place(x=650, y=110)
        
    #     #fetch the pet names from the database
    #     cursor = pdsdb.cursor()
    #     select_query = f"SELECT pet_name FROM pet_info WHERE user_id = {self.user_id}"
    #     cursor.execute(select_query)
    #     pet_names = cursor.fetchall()
    #     pet_name_list = []
    #     for pet_name in pet_names:
    #         pet_name_list.append(pet_name[0])
    #     self.petname = StringVar()
    #     self.petname.set("Select Pet Name")
    #     self.petname_dropdown = OptionMenu(self.pet_profile_frame, self.petname, *pet_name_list)
    #     self.petname_dropdown.config(font=("calibri", 15), bg="#242323", fg = "white")
    #     self.petname_dropdown.place(x=590, y=205)
    #     #call a method when selecting the pet name
    #     self.petname.trace("w", self.del_pet_name_selected)
        
    # def del_pet_name_selected(self, *args):
    #     pet_name = self.petname.get()
    #     if pet_name:
    #         cursor = pdsdb.cursor()
    #         select_query = f"SELECT * FROM pet_info WHERE pet_name = '{pet_name}'"
    #         cursor.execute(select_query)
    #         pet = cursor.fetchone()
    #         self.selected_pet = pet
    #         #Create a button to delete the pet data
    #         self.delete_pet_data_button = Button(self.pet_profile_frame, text="Delete Pet Data", font=("calibri", 18), bg="black", fg="white", bd=0, cursor="hand2")
    #         self.delete_pet_data_button.place(x=650, y=300)
    #         self.delete_pet_data_button.config(command=self.delete_pet)
            
        
                
    
                
        
        
        
        
        
        # #pet name label
        # self.pet_name_label = Label(self.pet_profile_frame, text="_____________________", font=("calibri", 20), bg="#010101", fg="white")                          
        # self.pet_name_label.place(x=590, y=150)
        
        # #pet name entry box
        # self.pet_name_entry = Entry(self.pet_profile_frame, font=("calibri", 20),bg="#010101", bd=0,fg="white",relief="ridge",insertbackground="white")
        # self.pet_name_entry.place(x=590, y=146)
        #fetch the pet name from the database and show it as a dropdown menu
        # cursor = pdsdb.cursor()
        # select_query = f"SELECT pet_name FROM pet_info WHERE user_id = {self.user_id}"
        # cursor.execute(select_query)
        # pet_names = cursor.fetchall()
        # pet_name_list = []
        # for pet_name in pet_names:
        #     pet_name_list.append(pet_name[0])
        # self.pet_name = StringVar()
        # self.pet_name.set("Select Pet Name")
        # self.pet_name_dropdown = OptionMenu(self.pet_profile_frame, self.pet_name, *pet_name_list)
        # self.pet_name_dropdown.config(font=("calibri", 15), bg="#242323", fg = "white")
        # self.pet_name_dropdown.place(x=590, y=150)
        
        # #set the on select action method for the pet name dropdown menu
        # self.pet_name.trace("w", self.pet_name_on_select)

        #pet breed dropdown menu below the pet name to
        # self.pet_breed_label = Label(self.pet_profile_frame, text="Pet Breed:", font=("calibri", 20), bg="#010101", fg="white")
        # self.pet_breed_label.place(x=470, y=200)
        # self.pet_breed = StringVar()
        # self.pet_breed.set("Select Breed")
        # self.pet_breed_dropdown = OptionMenu(self.pet_profile_frame, self.pet_breed, "German Shepherd", "Labrador", "Golden Retriever", "French Bulldog", "Siberian Husky")
        # self.pet_breed_dropdown.config(bg="#010101", fg="white")
        # self.pet_breed_dropdown.place(x=607, y=205)
        
        
            
    # def pet_name_on_select(self, *args):
    #     #based on the pet name selected, fetch the pet data from the database
    #     pet_name = self.pet_name.get()
    #     cursor = pdsdb.cursor()
    #     select_query = f"SELECT * FROM pet_info WHERE user_id = {self.user_id} AND pet_name = '{pet_name}'"
    #     cursor.execute(select_query)
    #     pet = cursor.fetchone()
    #     #display the pet data in the entry boxes
    #     #iterate through the pets and display the data
    #     if pet:
    #         self.selected_pet = pet
    #         print(self.selected_pet)
    #         if(pet[2] == 'Dog'):
    #             self.dogProfileScreen()
    #         elif(pet[2] == 'Cat'):
    #             self.catProfileScreen()                      
            
    
    
    # #reports 
    def Application_Data(self):
        # Open the CSV file in write mode
        print("Application Data Downloaded Successfully.")

        # Get file path from user
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        # fetch user details along with number of pets
        cursor = pdsdb.cursor()
        select_data = f"SELECT u.user_id,u.first_name,u.last_name,u.email,u.mobile,COUNT(p.pet_id) AS pet_count FROM user_info u LEFT JOIN pet_info p ON u.user_id = p.user_id GROUP BY u.user_id"
        cursor.execute(select_data)
        users_data = cursor.fetchall()
        

        if file_path:

            # Write data to CSV file
            with open(file_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["","","","","","","","Application Data"])
                writer.writerow([""])
                column_headers = ["User ID", "Email", "First Name", "Last Name", "Mobile","Total Pets"]
                writer.writerow(column_headers)
                for row in users_data:
                    writer.writerow(row)

            print("CSV file saved successfully.")
            messagebox.showinfo("Success", "File Downloaded.")

        
        #back button
        self.back_button = Button(self.pet_profile_frame,text="Back",font=("calibri",18),bg="black",fg="white",bd=0,cursor="hand2")
        self.back_button.place(x=600,y=400)
        self.back_button.config(command=self.welcomeScreen)

  
        
            
        
   #show table in admin page
    def show_table(self):
        self.user_table = ttk.Treeview(self.admin_frame)
        self.user_table['columns'] =("User ID", "Email", "First Name", "Last Name", "Mobile","Total Pets")
        self.user_table.heading("#0", text='S.No')  # ID column
        self.user_table.column("#0", anchor='center', width=40)
        for col in self.user_table['columns']:
            self.user_table.heading(col, text=col)  # Set column headings
            self.user_table.column(col, anchor='center', width=100)  # Set column widths
        self.user_table.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Load the transaction logs for the current user
        self.load_users()

        
 
    def load_users(self):

        self.user_table.delete(*self.user_table.get_children())

        cursor = pdsdb.cursor()
        select_data = f"SELECT u.user_id,u.first_name,u.last_name,u.email,u.mobile,COUNT(p.pet_id) AS pet_count FROM user_info u LEFT JOIN pet_info p ON u.user_id = p.user_id GROUP BY u.user_id"
        cursor.execute(select_data)
        users_data = cursor.fetchall()
        self.income_data = users_data

        for idx, row in enumerate(self.income_data, start=1):
            self.user_table.insert(parent='', index='end', iid=idx, text=idx, values=row)
    
        
    
    #admin page
    def adminScreen(self):
        #clear the window
        for i in self.root.winfo_children():
            i.destroy()
            
        #creating a new frame for the admin page
        self.admin_frame = Frame(self.root, bg="white")
        self.admin_frame.place(x=0, y=0, width=1300, height=750)
        
        #admin label
        self.admin_label = Label(self.admin_frame, text="Admin Page", font=("calibri", 30), bg="white", fg="black")
        self.admin_label.place(x=500, y=20)
        
        #Application Data label
        self.application_data_label = Label(self.admin_frame, text="Application Data", font=("calibri", 20), bg="white", fg="black")
        self.application_data_label.place(x=500, y=100)
        
        self.show_table()
        
        #back button
        self.back_button = Button(self.admin_frame, text="Back", font=("calibri", 18), bg="white", fg="black", bd=0, cursor="hand2")
        self.back_button.place(x=500, y=600)
        self.back_button.config(command=self.loginScreen)
        
        #button to print reports  
        self.print_report_button = Button(self.admin_frame, text="Print Report", font=("calibri", 18), bg="white", fg="black", bd=0, cursor="hand2")
        self.print_report_button.place(x=600, y=600)
        self.print_report_button.config(command=self.Application_Data)

#starter code
if __name__ == "__main__":

    root = Tk()
    app = PawfectPortions(root)
    root.mainloop()
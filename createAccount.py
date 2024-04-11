# CREATE ACCOUNT PAGE 
import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import requests
import json
import pandas as pd
import base64
import ast
import time

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
partner_db = client.partner
collection = partner_db.partner
username_collection = partner_db.login


usernames = [doc['username'] for doc in username_collection.find()]

usernames = [user for user in usernames if user != "admin"]

if 'logged_in' not in st.session_state:
   st.session_state.logged_in = False

if 'accountCreated' not in st.session_state:
   st.session_state.accountCreated = False

def export_to_excel():
   """
   Export MongoDB collection data to an Excel file.


   Returns:
       str: File path of the exported Excel file.
   """
   # Retrieve data from MongoDB collection
   cursor = collection.find({})


   # Convert cursor to DataFrame
   df = pd.DataFrame(list(cursor))


   # Define the file path
   file_path = "mongodb_data.xlsx"


   # Write DataFrame to Excel file
   df.to_excel(file_path, index=False)


   return file_path


def convert_to_list(s):
   """
   Convert a string representation of a list to an actual list.


   Args:
       s (str): String representation of a list.


   Returns:
       list or str: Converted list or the original string if conversion fails.
   """
   try:
       # Attempt to evaluate the string as a list
       return ast.literal_eval(s)
   except ValueError:
       # Return the original string if conversion fails
       return s


def get_binary_file_downloader_html(bin_file, file_label='File'):
   """
   Generate HTML code for downloading a binary file.


   Args:
       bin_file (str): Path to the binary file.
       file_label (str, optional): Label for the download link. Defaults to 'File'.


   Returns:
       str: HTML code for the download link.
   """
   # Read binary data from the file
   with open(bin_file, 'rb') as f:
       data = f.read()


   # Encode the binary data as base64
   b64 = base64.b64encode(data).decode()


   # Generate HTML code for the download link
   return (f'<a href="data:application/octet-stream;base64,{b64}" '
           f'download="{bin_file}">{file_label}</a>')
def createAccount():
   """
   Creates a new user account.


   Returns:
       bool: True if the account is successfully created, False otherwise.
   """
   # Check if the "Sign Up" button is clicked
   if st.button("Sign Up"):
       # Define user input data
       add_input = {
           'username': input_user,
           'password': input_pwd,
           'acc_type': input_type
       }
       # Check if the username already exists in the database
       if username_collection.find_one(add_input):
           # Display error message if the username is taken
           st.error("Sorry, your username is already taken.")
       else:
           # Insert the new user data into the database
           username_collection.insert_one(add_input)
           # Validate user input and display success or error messages accordingly
           if len(input_user) > 0 and len(input_pwd) > 8 and input_user not in usernames:
               st.success("Your account has successfully been created!")
               st.subheader("Account Successfully Created!")
               msg = st.text_area("", f"Username: {input_user}  \n\n"
                                f"Password: {input_pwd}  \n\n"
                                f"Type: {input_type}", height=150)
               return True
           elif len(input_user) > 0 and len(input_pwd) < 8:
               st.error("Please make sure that your password is at least 8 characters long.")
               return False
           elif input_user in usernames:
               st.error("Username already exists")
               return False
           else:
               st.warning("Please create your username and password.")
               return False

def reset_password():
   if st.button("Reset Password"):
       update = {}
       reset_user ={'username': user_to_reset}
       query_doc = collection.find_one(reset_user)
       update["$set"] = {"password": new_password}
       username_collection.update_one(reset_user, update)


st.title("Administrator Priveleges")


tab1, tab2, tab3 = st.tabs(["Create New Account", "Reset Password", "Backup/Export Database"])
# Display content for the first tab - Create Account
with tab1:
   # Title for the tab
   st.title("Create Account")


   # Text input for new username
   input_user = st.text_input("New Username:")


   # Text input for new password with password type
   input_pwd = st.text_input("New Password:", type="password" )


   # Dropdown selection for account type
   input_type = st.selectbox("Account Type:", options=['Viewer', 'Administrator', 'Editor'])


   # Create an account and store the result in session state
   st.session_state.accountCreated = createAccount()
   if st.session_state.accountCreated:
       time.sleep(5)
       st.rerun()


# Display content for the second tab - Reset password
with tab2:
   # Title for the tab
   st.title("Reset password")


   # Dropdown selection for username
   user_to_reset = st.selectbox("Username", usernames)


   # Text input for new password with a unique key
   new_password = st.text_input("New Password:", key="new_password", type = "password")


   # Reset the password
   reset_password()


# Display content for the third tab - Database Backup/Export
with tab3:
   # Subheader for the section
   st.subheader("Database Backup/Export")


   # Information about backup and restore options
   st.write("To backup your database, you can export it as an excel file. To restore a backup, select an excel file to restore.")

   # Text input for file name
   file_to_use = st.text_input("Enter your file name here")

   # Layout for buttons using columns
   col1, col2 = st.columns([13,50])


   # Button to restore backup
   restore_backup = col1.button("Restore Backup")


   # Button to backup the database
   backup = col2.button("Backup Database")


   # Attempt to restore backup from the selected file
   try:
       if restore_backup:
           # Read the excel file and convert resources column to list
           df = pd.read_excel(f"{file_to_use}")
           df['resources'] = df['resources'].apply(convert_to_list)
           data = df.to_dict(orient='records')
           # Clear the current collection and insert the restored data
           collection.delete_many({})
           collection.insert_many(data)
           st.success("Database Restored!")
   except FileNotFoundError as e:
       # Error message if the file is not found
       st.error("Please enter a valid file path above")


   # If backup button is clicked, export database to excel
   if backup:
       # Export the database to excel and get the file path
       file_path = export_to_excel()
       # Display success message with file path and provide download link
       st.success(f"Data exported to Excel: [{file_path}]")
       st.markdown(get_binary_file_downloader_html(file_path, 'Excel file'), unsafe_allow_html=True)

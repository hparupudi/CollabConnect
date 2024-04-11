# LOGIN PAGE


import streamlit as st
from pymongo import MongoClient
import requests
from streamlit_lottie import st_lottie
from st_pages import Page, show_pages, add_page_title


# Connection to local MongoDB server, accessing partner and login collections.
connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
partner_db = client.partner
collection = partner_db.partner
username_collection = partner_db.login


# Initialize 'logged_in' and 'account_type' in streamlit session state
if 'logged_in' not in st.session_state:
   st.session_state.logged_in = False


if 'account_type' not in st.session_state:
   st.session_state.account_type = " "


def load_lottieurl(url: str):
   """
   Load gifs and animations from URL
   :param url: URL of the specified gif
   :return: JSON data if successful, otherwise None
   """
   r = requests.get(url)
   if r.status_code != 200:
       return None
   return r.json()


def login():
   """
   Function to handle user login
   """
   if st.button("Log in"):
       user_query = {'username': input_user}
       login_doc = username_collection.find_one(user_query)


       if login_doc and input_password == login_doc.get('password'):
           st.success("Logged in successfully!")
           st.session_state.account_type = login_doc.get('acc_type')
           st.session_state.logged_in = True
           pick_pages()
           st.rerun()  # Manual rerun after login
       else:
           st.error("Incorrect username or password.")


def pick_pages():
   """
   Function to handle page navigation based on account type
   """
   if st.session_state.account_type == " ":
       show_pages([Page("Login.py")])
   elif st.session_state.account_type == "Viewer":
       show_pages([Page("Login.py"), Page("pages/View Organizations.py"), Page("pages/Chatbot.py")])
   elif st.session_state.account_type == "Admin":
       show_pages([Page("Login.py"), Page("pages/Admin Page.py"), Page("pages/View Organizations.py"),
                   Page("pages/Edit Organizations.py"), Page("pages/Add Organizations.py"), Page(
               "pages/Remove Organizations.py"),
                   Page("pages/Chatbot.py")])
   elif st.session_state.account_type == "Editor":
       show_pages([Page("Login.py"), Page("pages/View Organizations.py"), Page("pages/Edit Organizations.py"),
                   Page("pages/Add Organizations.py"), Page("pages/Remove Organizations.py"), Page("pages/Chatbot.py")])


# If not logged in, show a Login screen
if not st.session_state.logged_in:
   pick_pages()
   st.title("Login")
   st.subheader("Welcome to CollabConnect!!")
   input_user = st.text_input("Username:")
   input_password = st.text_input("Password:", type="password")
   login()


elif st.session_state.logged_in:
   gif = load_lottieurl("https://lottie.host/2c14656b-941b-4faa-afe2-328b50571ab6/IhnT2jxA4M.json")
   st.empty()
   st.title("Home")
   st.subheader("Welcome to the organization manager!")
   st.write("Welcome to the CollabConnect Department's cutting-edge database management system, "
            "designed specifically to streamline your interactions with business partners and associated entities. "
            "Our platform offers intuitive tools for adding, editing, viewing, and removing organizations, "
            "putting you in control of your partnerships with unprecedented ease.")
   st_lottie(gif, height=400, width=600)
   st.subheader("Convenient and Simple")
   st.write("Our website goes to lengths to provide you with the tools you need to manage your circle of organizations. "
            "On CollabConnect, simplicity is our priority. Different pages are there for you to navigate, "
            "so you never find anything difficult to locate.")
   st.subheader("Chatbot Functionality")
   st.write("In case you have any questions, you can connect with our chatbot! Our chatbot can help you with "
            "questions regarding the use of our webpages, or direct you toward where you want to find something. "
            "If you have any more questions, feel free to contact an administrator!")
   log_out = st.button("Log out")


   if log_out:
       st.session_state.logged_in = False
       st.session_state.account_type = " "
       st.rerun()

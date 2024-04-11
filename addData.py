# CODE FOR ADD DATA PAGE

import streamlit as st
from streamlit_modal import Modal
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import requests
import json

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
partner_db = client.partner
collection = partner_db.partner
username_collection = partner_db.login


def load_lottieurl(url: str):
   r = requests.get(url)
   if r.status_code != 200:
       return None
   return r.json()


if 'logged_in' not in st.session_state:
   st.session_state.logged_in = False


orgs_names = [doc['name'] for doc in collection.find()]


# Set the title of the Streamlit app page
st.title("Add Organizations")


# Input fields for organization details
name = st.text_input("Organization Name")
org_type = st.selectbox(label="Type of Organization", options=['Non-profit', 'Small business', 'Corporation'])
resources = []
num_resources = st.number_input("Resource amount", value=1, min_value=1)


# Loop to collect multiple resources
for i in range(num_resources):
   resource_entry = st.text_input(f'Resource {i+1}')
   resources.append(resource_entry)


description = st.text_input("Description")
email = st.text_input('Email')


# Button to submit the form
submit = st.button('Submit')


# When the submit button is clicked
if submit:
   # Check if the organization name is not already in the database
   if name not in orgs_names:
       # Create a dictionary representing the organization
       organization_to_add = {
           "name": name,
           "type": org_type,
           "resources": resources,
           "email": email,
           "description": description,
       }
       # Insert the organization into the database
       collection.insert_one(organization_to_add)
       # Display success message
       st.success("Organization successfully added!")
   else:
       # Display error message if the organization already exists
       st.error("Organization already in database: Please edit or remove the organization")

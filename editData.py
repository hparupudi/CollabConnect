# CODE FOR EDIT DATA PAGE


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


if 'logged_in' not in st.session_state:
   st.session_state.logged_in = False


if 'account_type' not in st.session_state:
   st.session_state.account_type = " "


def load_lottieurl(url: str):
   r = requests.get(url)
   if r.status_code != 200:
       return None
   return r.json()


orgs_names = [doc['name'] for doc in collection.find()]


# Check if the user is already logged in


st.title("Edit Organizations")
if orgs_names:
   orgs_select = st.selectbox("Select organization", orgs_names)
   user_query = {'name': orgs_select}
   query_doc = collection.find_one(user_query)
   type_selected = query_doc.get('type')
   resource_selected = query_doc.get('resources')
   if isinstance(resource_selected, str):
       resource_selected = [resource_selected]


   if len(resource_selected) == 1:
       formatted_resources = resource_selected[0]
   else:
       formatted_resources = ', '.join(str(resource) for resource in resource_selected)
   description_selected = query_doc.get('description')
   email_selected = query_doc.get('email')
   edit = st.selectbox("Field to edit:", ["Name", "Type", "Resources", "Description", "Contact"])
else:
   st.error("No organizations available. Did you delete them all?")
# Check if the field to edit is not "Resources" or "Type"
if edit != "Resources" and edit != "Type":
   # Input field for the new value of the selected field
   new_field = st.text_input(f"New {edit}:")
# If the field to edit is "Resources"
elif edit == "Resources":
   # Initialize an empty list to store resources
   resources = []
   # Input field to specify the number of resources
   num_resources = st.number_input("Resource amount", value=1, min_value=1)
   try:
       # Loop to collect multiple resources
       for i in range(num_resources):
           resource_entry = st.text_input(f'Resource {i+1}')
           resources.append(resource_entry)
       # Convert the list of resources to a formatted string
       formatted_resources = ', '.join(str(resource) for resource in resources)
   except Exception as e:
       # Display error message if there's an exception
       st.error(e)
# If the field to edit is "Type"
elif edit == "Type":
   # Dropdown menu to select the type of organization
   type_of_org = st.selectbox(label="Type of Organization",
                              options=['Non-profit', 'Small business', 'Corporation'])


# Display the current information of the selected organization
st.text_area("Information", f"Organization name: {orgs_select}  \n\n"
                           f"Organization type: {type_selected}  \n\n"
                           f"Organizations resources: {formatted_resources}  \n\n"
                           f"Organization description: {description_selected}  \n\n"
                           f"Organization contact: {email_selected}", height=225)


# Prepare the update query based on the field to edit
update = {}
if edit == "Resources":
   update["$set"] = {"resources": resources}
elif edit == "Type":
   update["$set"] = {"type": type_of_org}
elif edit == "Name":
   update["$set"] = {"name": new_field}
elif edit == "Description":
   update["$set"] = {"description": new_field}
elif edit == "Contact":
   update["$set"] = {"email": new_field}


# When the Submit button is clicked
if st.button("Submit"):
   # Update the organization information in the database
   collection.update_one(user_query, update)
   st.rerun()

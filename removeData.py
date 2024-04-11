# CODE FOR REMOVE DATA PAGE


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


# Display the title for the removal section
st.title("Remove Organizations")


# Retrieve the names of all organizations from the database
orgs_names = [doc['name'] for doc in collection.find()]


# Check if there are organizations available for removal
if orgs_names:
   # Dropdown menu to select an organization for removal
   org_selected = st.selectbox("Select an Organization to remove:", orgs_names)


   # Query to find the selected organization in the database
   user_query = {'name': org_selected}
   delete_doc = collection.find_one(user_query)


   # Retrieve information about the selected organization
   delete_type = delete_doc.get('type')
   delete_resources = delete_doc.get('resources')


   # Format the resources for display
   if isinstance(delete_resources, str):
       delete_resources = [delete_resources]
   if len(delete_resources) == 1:
       formatted_resources = delete_resources[0]
   elif len(delete_resources) > 1:
       formatted_resources = ', '.join(resource for resource in delete_resources)


   delete_description = delete_doc.get('description')
   delete_email = delete_doc.get('email')


   # Display the information of the organization to be deleted
   st.text_area("This organization will be deleted", f"Organization name: {org_selected}  \n\n"
                                                     f"Organization type: {delete_type}  \n\n"
                                                     f"Resources offered: {formatted_resources}  \n\n"
                                                     f"Description: {delete_description}  \n\n"
                                                     f"Organization contact: {delete_email}", height=240)


   # Button to confirm the deletion of the organization
   if st.button("Delete Organization"):
       # Delete the selected organization from the database
       collection.delete_one(user_query)
       # Reload the page to reflect the changes
       st.rerun()
else:
   # Error message if there are no organizations available for removal
   st.error("No organizations available. Did you delete them all?")

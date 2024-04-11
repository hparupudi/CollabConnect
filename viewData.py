#Updated Code for View Data page


import streamlit as st
from streamlit_modal import Modal
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from streamlit_tags import st_tags
import pandas as pd
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
if 'resources_formatted' not in st.session_state:
   st.session_state.resources_formatted = True
def load_lottieurl(url: str):
   r = requests.get(url)
   if r.status_code != 200:
       return None
   return r.json()








def create_lines(col, lines):
   for i in range(lines):
       col.write(" \n\n")


orgs_names = [doc['name'] for doc in collection.find()]
orgs_names_display = orgs_names[:]
orgs_names_display.insert(0, 'All')
orgs_types = [doc['type'] for doc in collection.find()]
orgs_resources = [doc['resources'] for doc in collection.find()]
orgs_emails = [doc['email'] for doc in collection.find()]
orgs_descriptions = [doc['description'] for doc in collection.find()]

size = 1
showType = True
st.title("View Organizations")
col1, col2 = st.columns([20,5])
create_lines(col2, 1)
with col1:
   filters = st_tags(
       label = ' ',
       text = 'Search by organization name, type, resources, etc...',
       maxtags = 20,
       key = 'filtersKey'
   )
   enter_filters = col2.button("Submit Filters")
col1, col2, col3 = st.columns([20, 20, 20])
org_select = col1.selectbox("Search by Name", orgs_names_display, key="name")
types = ['All', 'Non-profit', 'Small business', 'Corporation']
resources = ['All']
for i in range(len(orgs_resources)):
   new_orgs_resources = orgs_resources[i]
   for j in range(len(new_orgs_resources)):
       if (new_orgs_resources[j] not in resources):
           resources.append(new_orgs_resources[j])

if (org_select != "All"):
   showType = False

if showType == True:
   type_select = col2.selectbox("Search by Type", types, key="type")
   resource_select = col3.selectbox("Search by Resource", resources)

if (org_select != "All"):
   org_query = {'name': org_select}
   org_doc = collection.find_one(org_query)
   org_type = org_doc.get('type')
   org_resources = org_doc.get('resources', [])
   if isinstance(org_resources, str):
       org_resources = [org_resources]
   org_description = org_doc.get('description')
   org_email = org_doc.get('email')
   if len(org_resources) == 1:
       formatted_resources = org_resources[0]
   else:
       formatted_resources = ', '.join(str(resource) for resource in org_resources)
   data = [org_select, org_type, formatted_resources, org_description, org_email]
   df = pd.DataFrame(index=range(1), columns=range(5))
   df.loc[0] = data

elif (type_select != "All"):
   if (resource_select == "All"):
        org_query = {'type': type_select}
   else:
       org_query = {'type': type_select,
                    'resources': resource_select}
   org_names = [doc['name'] for doc in collection.find(org_query)]
   org_resources = [doc['resources'] for doc in collection.find(org_query)]
   org_descriptions = [doc['description'] for doc in collection.find(org_query)]
   org_emails = [doc['email'] for doc in collection.find(org_query)]
   size = len(org_names)
   if isinstance(org_resources, str):
       orgs_resources = [org_resources]
   if (size != 0):
       df = pd.DataFrame(index=range(size), columns=range(5))
       for i in range(size):
           data = [org_names[i], type_select,  ', '.join(org_resources[i]), org_descriptions[i], org_emails[i]]
           df.loc[i] = data
   else:
       st.warning("None of the items match given filters. Please try again.")
elif (resource_select != "All"):
   if (type_select == "All"):
       org_query = {'resources': resource_select}
   else:
       org_query = {'type': type_select,
                    'resources': resource_select}
   org_names = [doc['name'] for doc in collection.find(org_query)]
   orgs_types = [doc['type'] for doc in collection.find(org_query)]
   org_resources = [doc['resources'] for doc in collection.find(org_query)]
   org_descriptions = [doc['description'] for doc in collection.find(org_query)]
   org_emails = [doc['email'] for doc in collection.find(org_query)]
   if isinstance(org_resources, str):
       orgs_resources = [org_resources]
   size = len(org_resources)
   if (size != 0):
       df = pd.DataFrame(index=range(size), columns=range(5))
       for i in range(size):
           data = [org_names[i], orgs_types[i],  ', '.join(org_resources[i]), org_descriptions[i], org_emails[i]]
           df.loc[i] = data
   else:
       st.warning("None of the items match given filters. Please try again.")
elif enter_filters:
   if isinstance(filters, str):
       filters = [filters]
   try:
       # Initialize a list to store matching documents
       matching_documents = []


       # Iterate over filters
       for i in range(len(filters)):
           # User regex filters to find close matches in every field, and return matches.
           regex_pattern = f".*{filters[i]}.*"  # Creating a regex pattern to match any part of the string
           name_found = collection.find({"name": {"$regex": regex_pattern, "$options": "i"}})
           type_found = collection.find({"type": {"$regex": regex_pattern, "$options": "i"}})
           resources_found = collection.find({"resources": {"$regex": regex_pattern, "$options": "i"}})
           description_found = collection.find({"description": {"$regex": regex_pattern, "$options": "i"}})
           email_found = collection.find({"email": {"$regex": regex_pattern, "$options": "i"}})


           # Add the document to the list of matching documents
           matching_documents.extend(name_found)
           matching_documents.extend(type_found)
           matching_documents.extend(resources_found)
           matching_documents.extend(description_found)
           matching_documents.extend(email_found)


       # Display matching documents
       if matching_documents:
           data_list = []
           doc_list = []
           for doc in matching_documents:
               # Ensure the same document is not displayed twice
               if doc not in doc_list:
                   resources = doc.get('resources', [])
                   if isinstance(resources, str):
                       resources = [resources]
                   doc_list.append(doc)
                   data_list.append([doc.get('name'), doc.get('type'), ', '.join(resources), doc.get('description'), doc.get('email')])
           # Display data
           df = pd.DataFrame(data_list, columns=['Name', 'Type', 'Resources', 'Description', 'Email'])
       else:
           st.warning("None of the items match given filters. Please try again.")
   except Exception as e:
       st.warning("None of the items match given filters. Please try again.")
else:
   size = len(orgs_types)
   df = pd.DataFrame(index=range(size), columns=range(5))
   if isinstance(orgs_resources, str):
       orgs_resources = [orgs_resources]
   for i in range(size):
       data = [orgs_names[i], orgs_types[i], ', '.join(orgs_resources[i]), orgs_descriptions[i], orgs_emails[i]]
       df.loc[i] = data


try:
   if (size != 0):
       df.columns = ['Name', 'Type', 'Resources', 'Description', 'Email']
       st.table(df)
except Exception as e:
   pass

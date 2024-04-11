# CODE FOR CHATBOT PAGE


import streamlit as st


st.title("Chatbot Assistant")


if "messages" not in st.session_state:
   st.session_state.messages = []


if "play_msg_shown" not in st.session_state:
   st.session_state.play_msg_shown = False


if not st.session_state.play_msg_shown:
   response = "Hello! Ask me any questions about this website that you may have. Please contact an administrator if you have any additional questions."
   with st.chat_message("assistant"):
       st.markdown(response)
       st.session_state.messages.append({"role": "assistant", "content": response})
   st.session_state.play_msg_shown = True


else:
   for message in st.session_state.messages:
       with st.chat_message(message["role"]):
           st.markdown(message["content"])


# Function to find a keyword in user input
def findKeyword(userInput, keyWord):
   strInput = repr(userInput)
   strInput = strInput.lower()
   keywordIndex = strInput.find(keyWord)
   return keywordIndex


userInput = st.chat_input()


if userInput is not None:
   with st.chat_message("user"):
       st.markdown(userInput)
       st.session_state.messages.append({"role": "user", "content": userInput})


       # Chatbot response logic
   if findKeyword(userInput, "account") >= 0 or findKeyword(userInput, "access") >= 0:
       response = ("To gain access to certain pages, different levels of authorization are required."
                   "For example, viewers can only access view organizations and chatbot pages."
                   "If you would like to access more pages, you need to contact an administrator for a new account with a different level of access\n"
                   "\n If you're experiencing issues with your account, such as forgetting the password, please contact an administrator to reset it.")
   elif findKeyword(userInput, "login") >= 0 or findKeyword(userInput, "password") >= 0:
       response = ("If you're experiencing login issues, please contact an admin. Administrators can reset your password if you've forgotten it, and create new accounts if you want a different level of authorization.")
   elif findKeyword(userInput, "accident")>=0:
       response = ("If you've deleted something on accident, or are experiencing any other issues, contact an administrator. They can reset your password if youve forgotten it, and restore the database if you've made any accidental changes.")
   elif findKeyword(userInput, "hello") >= 0 or findKeyword(userInput, "hi") >= 0:
       response = "Hi, how may I assist you?"
   elif findKeyword(userInput, "add") >= 0 or findKeyword(userInput, "insert") >= 0:
       response = ("The add organizations page allows users to create new organizations one at a time. Only "
                   "editors and admins can access this feature.\n"
                   "\nTo add organizations:\n"
                   "1. Fill out organization name\n"
                   "2. Select the type of organization (ex. Non-profit)\n"
                   "2. Specify the number of resources\n"
                   "4. Fill out the individual resource fields\n"
                   "5. Add a description for any important notes, or additional information (optional)\n"
                   "6. Enter contact information\n"
                   "7. Submit once all desired fields have been filled out.")
   elif findKeyword(userInput, "remove") >= 0 or findKeyword(userInput, "delete") >= 0:
       response = ("The remove organizations page allows users to delete organizations one at a time. Only "
                   "editors and admins can access this feature.\n"
                   "\nTo remove organizations:\n"
                   "1. Select the organization, via name. If you need help, visit the view organizations page to confirm name.\n"
                   "2. Review organization information.\n"
                   "2. Delete organization once ready. THIS ACTION CANNOT BE UNDONE!!\n")
   elif findKeyword(userInput, "view") >= 0 or findKeyword(userInput, "see") >= 0:
       response = ("The view organizations page allows users to query organizations. All users have access to this page."
                   "\nTo view organizations:\n"
                   "1.  Filters: Select any filter, such as name, type, or resources.\n"
                   "\n\tSearch: Search by any keyword, hit enter to confirm. Select the submit filters button when ready.\n"
                   "2. Review the results, and change any information which is not up to date through the edit organizations page.")
   elif findKeyword(userInput, "edit") >= 0 or findKeyword(userInput, "change") >= 0:
       response = ("The edit organizations page allows users to edit organization information, one field at a time. Only editors and admins have access to this page\n"
                   "\nTo edit organizations:\n"
                   "\n1. Select the field you want to edit\n"
                   "\n2. Enter the new information\n"
                   "\n3. Submit the information once it is correect\n ")
   elif findKeyword(userInput, "collabconnect is the best") >= 0:
       response = "An admin will give you a prize! Congrats on finding this easter egg!"
   else:
       response = ("Sorry, I don't have the answer to that question. Contact an administrator for more information.\n"
                   "\nFrequently Asked Questions:\n"
                   "\nQuestion: How do I gain access to the pages?\n"
                   "\nAnswer: To view the pages, you need to have an administrator create an account for you.\n"
                   "\nViewers: Access to view organizations, chatbot, and login pages\n"
                   "\nEditors: Access to remove, add, edit, view organizations pages, alongside the login and chatbot pages\n"
                   "\nQuestion: I forgot my password. How do I find it?\n"
                   "\nAnswer: To reset your password, contact an adminstrator.\n")


   with st.chat_message("assistant"):
       st.markdown(response)
       st.session_state.messages.append({"role": "assistant", "content": response})

import streamlit as st
from models import Session, Transaction, Split, Person, Merchant
from datetime import datetime
from sqlalchemy import text
session = Session()
st.set_page_config(layout="wide")

st.title('Data Management')

# Function to add a merchant
def add_merchant(name):
    if not session.query(Merchant).filter_by(name=name).first():
        merchant = Merchant(name=name)
        session.add(merchant)
        session.commit()
        return True
    return False

# Function to delete a merchant by row id
def delete_merchant_by_id(merchant_id):
    statement = text("DELETE FROM merchants WHERE id = :id")
    session.execute(statement, {"id": merchant_id})
    session.commit()

# Function to delete a person by row id
def delete_person_by_id(person_id):
    statement = text("DELETE FROM persons WHERE id = :id")
    session.execute(statement, {"id": person_id})
    session.commit()

def edit_merchant_by_id(merchant_id, merchant_name):
    statement = text("UPDATE merchants SET name = :name WHERE id = :id")
    session.execute(statement, {"name": merchant_name, "id": merchant_id})
    session.commit()

def edit_person_by_id(person_id, person_name):
    statement = text("UPDATE persons SET name = :name WHERE id = :id")
    session.execute(statement, {"name": person_name, "id": person_id})
    session.commit()

# Function to add a person
def add_person(name):
    if not session.query(Person).filter_by(name=name).first():
        person = Person(name=name)
        session.add(person)
        session.commit()
        return True
    return False

def on_add_merchant(merchant_name):
    return add_merchant(merchant_name)

# Merchant management expander
with st.expander("Merchant Management", expanded=True):
    cols_merchant = st.columns([1, 1])

    # left column
    with cols_merchant[0]:
        # Get all merchants
        merchants = session.query(Merchant).all()

        # Create a list of dictionaries for the data editor
        merchant_data = [{
            "ID": merchant.id,
            "Name": merchant.name
        } for merchant in merchants]
        
        cols_merchant_data = st.columns([1, 1])
        
        # inner left column
        with cols_merchant_data[0]:
            st.data_editor(
                merchant_data,
                key="merchant_data",
                num_rows="fixed",
                width=300
            )
            # Save the data in the session state
            st.session_state['merchant_data']['data'] = merchant_data

        # # inner right column
        # with cols_merchant_data[1]:
            # st.subheader("Edit Merchant")
            # edit_merchant_id = st.selectbox("Merchant ID", options=[merchant["ID"] for merchant in merchant_data], key="edit_merchant_id")
            # # edit_merchant_id = st.number_input("Merchant ID", key="edit_merchant_id")
            # edit_merchant_name = st.text_input("New Merchant Name", key="edit_merchant_name")
                    
            # st.button("Save", key="edit_merchant", on_click=edit_merchant_by_id, args=(edit_merchant_id, edit_merchant_name))

        #     if st.button("Save Changes", key="save_merchants"):
        #         st.warning("Not implemented yet. Changes are not saved.")
        #         # edited_rows = st.session_state["merchant_data"]["edited_rows"]
        #         # # {0: {'Name': 'Walmarts'}}
        #         # for row_id, row in edited_rows.items():
        #         #     merchant = session.query(Merchant).get(row_id)
                    
        #         #     merchant.name = row["Name"]
        #         #     session.commit()

        #         # if added_rows := st.session_state["merchant_data"]["added_rows"]:
        #         #     st.error("Error: Adding new rows is not supported. Please use the adding form on the right. New rows are not saved.")


    # right column
    with cols_merchant[1]:
        inner_cols = st.columns([3, 1, 3])
        with inner_cols[0]:
            st.subheader("Add a New Merchant")

            new_merchant_name = st.text_input("Merchant Name", key="new_merchant")

            # Add merchant button
            st.button("Add Merchant",
                      key="add_merchant",
                      on_click=on_add_merchant,
                      args=(new_merchant_name,))
        
        st.divider()
        
        with inner_cols[2]:

            st.subheader("Delete Merchant")
            delete_merchant_id = st.selectbox("Merchant ID", options=[merchant["ID"] for merchant in merchant_data], key="delete_merchant_id")
            st.button("Delete", key="delete_merchant", on_click=delete_merchant_by_id, args=(delete_merchant_id,))

        st.subheader("Edit Merchant")
        inner_cols2 = st.columns([3, 1, 3])
        with inner_cols2[0]:
            edit_merchant_id = st.selectbox("Merchant ID", options=[merchant["ID"] for merchant in merchant_data], key="edit_merchant_id")
        # edit_merchant_id = st.number_input("Merchant ID", key="edit_merchant_id")
        with inner_cols2[2]:
            edit_merchant_name = st.text_input("New Merchant Name", key="edit_merchant_name")
                
        st.button("Save", key="edit_merchant", on_click=edit_merchant_by_id, args=(edit_merchant_id, edit_merchant_name))
        

    # # Delete merchants
    # deleted_rows = st.session_state["merchant_data"]["deleted_rows"]
    # if deleted_rows:
    #     for row in deleted_rows:
    #         delete_merchant_by_row(row)
    #     # Clear the deleted rows
    #     st.session_state["merchant_data"]["deleted_rows"] = []

# Person management expander
with st.expander("People Management", expanded=True):
    cols_person = st.columns([1, 1])

    # left column
    with cols_person[0]:
        # Get all persons
        persons = session.query(Person).all()

        # Create a list of dictionaries for the data editor
        person_data = [{
            "ID": person.id,
            "Name": person.name
        } for person in persons]
        
        cols_person_data = st.columns([1, 1])
        
        # inner left column
        with cols_person_data[0]:
            st.data_editor(
                person_data,
                key="person_data",
                num_rows="fixed",
                width=300
            )
            # Save the data in the session state
            st.session_state['person_data']['data'] = person_data

        # # inner right column
        # with cols_person_data[1]:
            # st.subheader("Edit Person")
            # edit_person_id = st.selectbox("Person ID", options=[person["ID"] for person in person_data], key="edit_person_id")
            # # edit_person_id = st.number_input("Person ID", key="edit_person_id")
            # edit_person_name = st.text_input("New Person Name", key="edit_person_name")
                    
            # st.button("Save", key="edit_person", on_click=edit_person_by_id, args=(edit_person_id, edit_person_name))

        #     if st.button("Save Changes", key="save_persons"):
        #         st.warning("Not implemented yet. Changes are not saved.")
        #         # edited_rows = st.session_state["person_data"]["edited_rows"]
        #         # # {0: {'Name': 'Walmarts'}}
        #         # for row_id, row in edited_rows.items():
        #         #     person = session.query(Person).get(row_id)
                    
        #         #     person.name = row["Name"]
        #         #     session.commit()

        #         # if added_rows := st.session_state["person_data"]["added_rows"]:
        #         #     st.error("Error: Adding new rows is not supported. Please use the adding form on the right. New rows are not saved.")


    # right column
    with cols_person[1]:
        inner_cols = st.columns([3, 1, 3])
        with inner_cols[0]:
            st.subheader("Add a New Person")

            new_person_name = st.text_input("Person Name", key="new_person")

            # Add person button
            st.button("Add Person",
                      key="add_person",
                      on_click=add_person,
                      args=(new_person_name,))
            
        with inner_cols[2]:
                
                st.subheader("Delete Person")
                delete_person_id = st.selectbox("Person ID", options=[person["ID"] for person in person_data], key="delete_person_id")
                st.button("Delete", key="delete_person", on_click=delete_person_by_id, args=(delete_person_id,))

        st.divider()

        st.subheader("Edit Person")
        inner_cols2 = st.columns([3, 1, 3])
        with inner_cols2[0]:
            edit_person_id = st.selectbox("Person ID", options=[person["ID"] for person in person_data], key="edit_person_id")
        # edit_merchant_id = st.number_input("Merchant ID", key="edit_merchant_id")
        with inner_cols2[2]:
            edit_person_name = st.text_input("New Person Name", key="edit_person_name")

        st.button("Save", key="edit_person", on_click=edit_person_by_id, args=(edit_person_id, edit_person_name))



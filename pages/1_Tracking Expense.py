import streamlit as st
import pandas as pd
from models import Session, Transaction, Split, Person, Merchant
from datetime import datetime
from sqlalchemy import text
# Initialize a session
session = Session()
st.set_page_config(layout="wide")
st.title('Bill Tracking App')

if 'show_add' not in st.session_state:
    st.session_state['show_add'] = True

if 'show_edit' not in st.session_state:
    st.session_state['show_edit'] = False

if 'splits' not in st.session_state:
    st.session_state.splits = []

if 'new_splits' not in st.session_state:
    st.session_state.new_splits = []


# Function to add a new split entry
def add_split():
    st.session_state.new_splits.append({'name': '', 'amount': 0.0})

# Function to remove a split entry
def remove_split(index):
    if index < len(st.session_state.splits):
        del st.session_state.splits[index]

# Ensure there's always at least one split entry
if len(st.session_state.new_splits) == 0:
    add_split()


col1, col2 = st.columns([6, 4])


def delete_transaction_by_row(row):
    transaction_id = st.session_state.transactions_data_main_page[row]['ID']
    # using ORM
    # transaction = session.query(Transaction).get(transaction_id)
    # session.delete(transaction)
    # using prepared statement
    statement = text("DELETE FROM transactions WHERE id = :id")
    session.execute(statement, {"id": transaction_id})
    session.commit()

def get_or_create_person(name):
    person = session.query(Person).filter_by(name=name).first()
    if not person:
        person = Person(name=name)
        session.add(person)
        session.commit()
    return person

def load_transactions_into_ss():
    transactions = session.query(Transaction).all()
    data = [{
        "ID": transaction.id,
        "Merchant Name": session.query(Merchant).get(transaction.merchant_id).name,
        "Amount": transaction.amount,
        "Date": transaction.date,
        "Purchaser": session.query(Person).get(transaction.purchaser_id).name
    } for transaction in transactions]
    if 'transactions_data_main_page' not in st.session_state or st.session_state.get('on_change_reload'):
        st.session_state.transactions_data_main_page = data
        st.session_state.on_change_reload = False

def on_delete_button_click(transaction_id):
    transaction = session.query(Transaction).get(transaction_id)
    session.delete(transaction)
    session.commit()
    st.session_state.on_change_reload = True
    load_transactions_into_ss()

load_transactions_into_ss()

# Function to load splits
def load_splits(transaction_id):
    splits = session.query(Split).filter_by(transaction_id=transaction_id).all()
    data = [{
        "ID": split.id,
        "Name": split.person.name,
        "Amount": split.amount
    } for split in splits]
    return data

def search_purchaser(query):
    persons = session.query(Person).filter(Person.name.like(f"%{query}%")).all()
    return [person.name for person in persons]

with col2:
    with st.expander("Add Transaction", expanded=st.session_state['show_add']):
    # if st.session_state['show_add']:
        cols_basics=st.columns([2.5,  1])
        with cols_basics[0]:
            # merchant_name = st.text_input('Merchant Name')
            merchants = session.query(Merchant).all()
            merchant_name = st.selectbox(
                'Merchant Name',
                options=[""] + [merchant.name for merchant in merchants],
                index=0,
                key="add_merchant_name"
            )

        with cols_basics[1]:
            date = st.date_input('Date', key='add_date')
        
        st.divider()

        cols_purchaser = st.columns([1.2, 1])

        with cols_purchaser[0]:
            persons = session.query(Person).all()
            purchaser_name = st.selectbox(
                'Payer',
                options=[''] + [person.name for person in persons],
                index=0,
                key="add_purchase_name"
            )
        with cols_purchaser[1]:
            amount = st.number_input('Amount', key='add_trans_amount', step=0.01)
        #     new_purchaser = st.text_input('Or enter new purchaser name')


        if purchaser_name:
            purchaser = get_or_create_person(purchaser_name)



        st.divider()
        for i, split in enumerate(st.session_state.new_splits):
            cols = st.columns([1, 1, 1])  # Adjust the layout as needed
            with cols[0]:
                # st.session_state.splits[i]['name'] = st.text_input(f"Person {i+1}", key=f"name_{i}")
                st.session_state.new_splits[i]['name'] = st.selectbox(
                    f"Person {i+1}",
                    options=[''] + [person.name for person in session.query(Person).all()],
                    index=0,
                    key=f"add_split_person_{i}"
                )
            with cols[1]:
                st.session_state.new_splits[i]['amount'] = st.number_input(f"Amount {i+1}", min_value=0.0, key=f"add_split_amount_{i}")
            with cols[2]:
                st.button("Remove", key=f"add_split_remove_{i}", on_click=remove_split, args=(i,))
        
        st.button("Add another split", on_click=add_split, key='add_split_button')
        st.divider()
        selected_transaction_id = st.empty()
    
        

        # Add transaction
        if st.button('Add Transaction', key="add_button"):
            if not merchant_name or not purchaser_name or not amount or not date:
                st.error('Please fill in all fields')
            else:
                merchant_id = session.query(Merchant).filter_by(name=merchant_name).first().id

                new_transaction = Transaction(merchant_id=merchant_id,
                                            amount=float(amount),
                                            date=datetime.strptime(date.isoformat(), '%Y-%m-%d'),
                                            purchaser_id=purchaser.id)
                session.add(new_transaction)
                session.commit()
                
                for split in st.session_state.splits:
                    person = get_or_create_person(split['name'])  # Assuming this function is defined
                    new_split = Split(transaction_id=new_transaction.id,
                                    person_id=person.id,
                                    amount=split['amount'])
                    session.add(new_split)
                session.commit()
                # if split_name and split_amount:
                #     new_split = Split(name=split_name, amount=float(split_amount), transaction=new_transaction)
                #     session.add(new_split)
                #     session.commit()
                st.session_state.on_change_reload = True
                load_transactions_into_ss()
                st.success('Transaction added successfully!')

    with st.expander("Edit Transaction", expanded=st.session_state['show_edit']):
        if st.session_state['show_edit']:
            selected_transaction = session.query(Transaction).get(st.session_state.edit_transaction_id)
            st.warning(f"Editing transaction {selected_transaction.id}, with merchant {selected_transaction.merchant.name} and purchaser {selected_transaction.purchaser.name}")
            cols_basics=st.columns([2.5,  1])
            with cols_basics[0]:
                # merchant_name = st.text_input('Merchant Name')
                merchants = session.query(Merchant).all()
                merchant_name = st.selectbox(
                    'Merchant Name',
                    options=[f"{selected_transaction.merchant.name}"] + [merchant.name for merchant in merchants],
                    index=0,
                    key="edit_merchant_name",
                )

            with cols_basics[1]:
                date = st.date_input('Date', key='edit_date', value=selected_transaction.date)
            
            st.divider()

            cols_purchaser = st.columns([1.2, 1])

            with cols_purchaser[0]:
                persons = session.query(Person).all()
                purchaser_name = st.selectbox(
                    'Purchaser',
                    options=[f"{selected_transaction.purchaser.name}"] + [person.name for person in persons],
                    index=0
                )
            with cols_purchaser[1]:
                amount = st.number_input('Amount', key='trans_amount', step=0.01, value=selected_transaction.amount)


            if purchaser_name:
                purchaser = get_or_create_person(purchaser_name)

            st.divider()
            st.session_state.splits = load_splits(selected_transaction.id)


            # st.warning(f"transaction {selected_transaction.id} has {len(selected_transaction.splits)} splits")
            for i, split in enumerate(st.session_state.splits):
                # st.warning(f"split {i} has name {split['Name']} and amount {split['Amount']}")
                cols = st.columns([1, 1, 1])
                with cols[0]:
                    # Example modification of split name, you'd replace this with your actual logic
                    st.session_state.splits[i]['Name'] = st.selectbox(
                        f"Person {i+1}",
                        options=[split['Name']] + [person.name for person in session.query(Person).all()],
                        index=0,
                        key=f"name_{i}"
                    )
                with cols[1]:
                    st.session_state.splits[i]['Amount'] = st.number_input("Amount", min_value=0.0, value=split['Amount'], key=f"amount_{i}")
                with cols[2]:
                    if st.button("Remove", key=f"remove_{i}"):
                        # Add logic to remove a split
                        pass

            for i, split in enumerate(st.session_state.new_splits):
                cols = st.columns([1, 1, 1])
                with cols[0]:
                    st.session_state.new_splits[i]['name'] = st.selectbox(
                        f"New Person {i+1}",
                        options=[''] + [person.name for person in session.query(Person).all()],
                        index=0,
                        key=f"new_name_{i}"
                    )
                with cols[1]:
                    st.session_state.new_splits[i]['amount'] = st.number_input(f"Amount {i+1}", min_value=0.0, key=f"new_amount_{i}")
                
                def on_remove_button_click(i):
                    del st.session_state.new_splits[i]
                
                cols[2].button("Remove", on_click=on_remove_button_click, args=(i,), key=f"new_remove_{i}")
            

            # Button to add a new split
            st.button("Add another split", on_click=add_split, key='new_split_button')
            st.divider()
            selected_transaction_id = st.empty()
        
            def on_save_button_click():
                transaction_id = st.session_state.edit_transaction_id
                transaction = session.query(Transaction).get(transaction_id)
                transaction.merchant_id = session.query(Merchant).filter_by(name=merchant_name).first().id
                transaction.amount = amount
                transaction.date = date
                transaction.purchaser_id = purchaser.id
                session.commit()

                # Delete all existing splits
                session.query(Split).filter_by(transaction_id=transaction_id).delete()
                
                for split in st.session_state.splits:
                    if split['Name'] == '' or split['Amount'] == 0.0:
                        continue
                    person = get_or_create_person(split['Name'])

                    new_split = Split(transaction_id=transaction_id, person_id=person.id, amount=split['Amount'])
                    session.add(new_split)
                for split in st.session_state.new_splits:
                    if split['name'] == '' or split['amount'] == 0.0:
                        continue
                    person = get_or_create_person(split['name'])
                    new_split = Split(transaction_id=transaction_id, person_id=person.id, amount=split['amount'])
                    session.add(new_split)
                
                st.session_state.new_splits = []
                session.commit()

            st.button('Save Changes', key='save_changes', on_click=on_save_button_click)


with col1:
    load_transactions_into_ss()
    st.write('## Transactions')
    # st.data_editor(st.session_state.transactions_data_main_page,
    #                key='transactions',
    #                num_rows='dynamic', width=800, height=400)

    col_id, col_merchant, col_amount, col_date, col_purchaser, col_edit, col_delete = st.columns([1, 1, 1, 1, 1, 1, 1])
    with col_id:
        st.write('ID')
    with col_merchant:
        st.write('Merchant')
    with col_amount:
        st.write('Amount')
    with col_date:
        st.write('Date')
    with col_purchaser:
        st.write('Payer')
    with col_edit:
        st.write('Edit')
    with col_delete:
        st.write('Delete')

    def on_edit_button_click(transaction_id):
        st.session_state.edit_transaction_id = transaction_id
        st.session_state['show_edit'] = True
        st.session_state['show_add'] = False

    

    for i, transaction in enumerate(st.session_state.transactions_data_main_page):
        col_id, col_merchant, col_amount, col_date, col_purchaser, col_edit, col_delete = st.columns([1, 1, 1, 1, 1, 1, 1])
        col_id.write(transaction['ID'])
        col_merchant.write(transaction['Merchant Name'])
        col_amount.write(transaction['Amount'])
        col_date.write(transaction['Date'])
        col_purchaser.write(transaction['Purchaser']) 
        col_edit.button('Edit', key=f"edit_{transaction['ID']}", on_click=on_edit_button_click, args=(transaction['ID'],))
        col_delete.button('Delete', key=f"delete_{transaction['ID']}", on_click=on_delete_button_click, args=(transaction['ID'],))

            # st.session_state["transactions"]["deleted_rows"].append(i)


    # st.write(st.session_state["transactions"])

    # deleted_rows = st.session_state["transactions"]["deleted_rows"]


    # if deleted_rows:
    #     for row in deleted_rows:
    #         delete_transaction_by_row(row)

    #     st.session_state["transactions"]["deleted_rows"] = []
    load_transactions_into_ss()

    
import streamlit as st
from models import Session, Transaction, Split, Person, Merchant, TransactionList, Item
from datetime import datetime
from sqlalchemy import text
session = Session()
st.set_page_config(layout="wide")

st.title('Adding Details for a Transaction')

if 'show_right_column' not in st.session_state:
    st.session_state.show_right_column = False

# Function to remove an item entry
def remove_item_entry(index):
    if index < len(st.session_state.item_list):
        del st.session_state.item_list[index]

def add_item_entry(name: str, price: float):
    st.session_state.item_list.append({'name': name, 'price': price})

def add_new_item_entry():
    if not 'new_item_list' in st.session_state:
        st.session_state.new_item_list = []
    st.session_state.new_item_list.append({'name': '', 'price': 0.0})

def on_add_button_click():
    add_new_item_entry()
    st.session_state.should_add = True

# st.button("Show Right Column", on_click=lambda: st.session_state.update(show_right_column=not st.session_state.show_right_column))
def on_edit_button_click(transaction_id):
    st.session_state.show_right_column = True
    st.session_state.selected_transaction_id = transaction_id
    st.session_state.item_list = []

def on_save_button_click():
    num_valid = sum(1 for item in st.session_state.item_list if item['name'] != "" and item['price'] != 0.0)
    if num_valid == 0:
        st.session_state.show_save_warning = True
        return
    
    # clear existing records in transaction_list
    session.query(TransactionList).filter_by(transaction_id=st.session_state.selected_transaction_id).delete()
    session.commit()


    for i, item in enumerate(st.session_state.item_list):
        if item['name'] != "" and item['price'] != 0.0:
            # if item exists not in items
            if (item_record := session.query(Item).filter_by(name=item['name']).first()) is None:
                item_record = Item(name=item['name'])
                session.add(item_record)
                session.commit()
            # item_record = session.query(Item).filter_by(name=item['name']).first()
            transaction_list_entry = TransactionList(transaction_id=st.session_state.selected_transaction_id,
                                                    item_id=item_record.id,
                                                    price=item['price'])
            session.add(transaction_list_entry)
            session.commit()
        elif item['name'] == "" and item['price'] == 0.0:
            continue
        else:
            st.warning(f"Item {i+1} is missing name or price")

    if 'new_item_list' in st.session_state:
        for i, item in enumerate(st.session_state.new_item_list):
            if item['name'] != "" and item['price'] != 0.0:
                # if item exists not in items
                if (item_record := session.query(Item).filter_by(name=item['name']).first()) is None:
                    item_record = Item(name=item['name'])
                    session.add(item_record)
                    session.commit()
                else:
                    # item_record = session.query(Item).filter_by(name=item['name']).first()
                    transaction_list_entry = TransactionList(transaction_id=st.session_state.selected_transaction_id,
                                                        item_id=item_record.id,
                                                        price=item['price'])
                    session.add(transaction_list_entry)
            elif item['name'] == "" and item['price'] == 0.0:
                continue
            else:
                st.warning(f"Item {i+1} is missing name or price")

        del st.session_state['new_item_list']

    session.commit()
    st.session_state.show_save_message = True

def on_close_button_click():
    st.session_state.show_right_column = False
    st.session_state.selected_transaction_id = None
    st.session_state.item_list = None
    
left_column, right_column = st.columns([1, 1])

with right_column:
    
    if st.session_state.show_right_column:
        
        
        st.subheader("Transaction Details for ID: " + str(st.session_state.selected_transaction_id))
        transaction = session.query(Transaction).get(st.session_state.selected_transaction_id)
        transaction.items = session.query(TransactionList).filter_by(transaction_id=transaction.id).all()
        st.warning(f"transaction {transaction.id} has {len(transaction.items)} items")
        
        if 'item_list' not in st.session_state:
                # st.session_state.item_list = st.session_state.get('items', [{'name': '', 'price': 0.0}])
            st.session_state.item_list = []

        if transaction.items:
            st.session_state.item_list = []
            for item in transaction.items:
                add_item_entry(item.item.name, item.price)
        
        if 'new_item_list' in st.session_state:
            for item in st.session_state.new_item_list:
                add_item_entry(item['name'], item['price'])
            st.session_state.should_add = False

        # UI for item entries
        for i, item in enumerate(st.session_state.item_list):
            cols = st.columns([3, 2, 1])
            with cols[0]:
                st.session_state.item_list[i]['name'] = st.text_input(f"Item Name {i+1}", key=f"item_name_{i}", value=item['name'])
            with cols[1]:
                st.session_state.item_list[i]['price'] = st.number_input(f"Price {i+1}", min_value=0.0, key=f"item_price_{i}", value=item['price'])
            with cols[2]:
                
                st.button("Remove", key=f"remove_item_{i}", on_click=remove_item_entry, args=(i,))

        if 'show_save_message' in st.session_state:
            st.success("Items saved successfully")
            del st.session_state['show_save_message']
        elif 'show_save_warning' in st.session_state:
            st.warning("No items to save")
            del st.session_state['show_save_warning']
        

        st.divider()

        # Example button to save items to a transaction (adjust according to your app logic)

        save_cols = st.columns([1, 1, 1, 1])
        save_cols[0].button("Add another item", on_click=on_add_button_click)
        save_cols[1].button('Save Items', key='save_items', on_click=on_save_button_click)
        save_cols[3].button("Close", on_click=on_close_button_click)
    else:
        st.write("Select a transaction to view details on the right column")

with left_column:
    all_transactions = session.query(Transaction).all()
    
    transaction_data = [{
        "ID": transaction.id,
        "Merchant": transaction.merchant.name,
        "Amount": transaction.amount,
        "Date": transaction.date,
        "Purchaser": transaction.purchaser.name,
    } for transaction in all_transactions]
    

    cols = st.columns([1, 1, 1, 1, 1, 1])
    for col, field in zip(cols, ["ID", "Merchant", "Amount", "Date", "Buyer", "Edit"]):
        col.write(f"##### {field}")

    for transaction in transaction_data:
        col0, col1, col2, col3, col4, col5= st.columns((1, 1, 1, 1, 1, 1))
        # id
        col0.write(str(transaction["ID"]))
        col1.write(transaction["Merchant"])
        col2.write(f"${transaction['Amount']:.2f}")
        col3.write(transaction["Date"])
        col4.write(transaction["Purchaser"])
        col5.button(f"Edit",
                    key=f"edit_new{transaction['ID']}",
                    on_click=on_edit_button_click,
                    args=(transaction['ID'],))

    st.subheader("Transaction List")
    st.table(transaction_data)

    button_text = "foo", "bar", "foo"
    pairs = zip(button_text, st.columns(len(button_text)))

    if st.session_state.IS_DEBUG:
        st.write(st.session_state)

import streamlit as st
from models import Session, Transaction, Split, Person, Merchant, TransactionList, Item
from datetime import datetime
from sqlalchemy import text
import plotly.express as px
session = Session()
st.set_page_config(layout="wide")

st.title('Report')


st.subheader('Filter')
cols = st.columns([1, 1, 1, 1, 1])

with cols[0]:
    start_date = st.date_input('Start Date', datetime(2023, 3, 1))
with cols[1]:
    end_date = st.date_input('End Date')
with cols[2]:
    person = st.selectbox('Person', ['All'] + [person.name for person in session.query(Person).all()])
with cols[3]:
    merchant = st.selectbox('Merchant', ['All'] + [merchant.name for merchant in session.query(Merchant).all()])
with cols[4]:
    purchaser = st.selectbox('Payer', ['All'] + [purchaser.name for purchaser in session.query(Person).all()])

def load_transactions_into_ss(start_date, end_date, person, merchant, purchaser):

    transactions = session.query(Transaction).filter(Transaction.date >= start_date, Transaction.date <= end_date)
    # statement = text("SELECT * FROM transactions WHERE date >= :start_date AND date <= :end_date")
    # transactions = session.execute(statement, {"start_date": start_date, "end_date": end_date})
    if person != 'All':
        # statement = text("SELECT * FROM persons WHERE name = :name")
        # person_id = session.execute(statement, {"name": person}).first().id
        person_id = session.query(Person).filter_by(name=person).first().id
        transactions = transactions.filter_by(purchaser_id=person_id)
    if merchant != 'All':
        # statement = text("SELECT * FROM merchants WHERE name = :name")
        # merchant_id = session.execute(statement, {"name": merchant}).first().id
        merchant_id = session.query(Merchant).filter_by(name=merchant).first().id
        transactions = transactions.filter_by(merchant_id=merchant_id)
    if purchaser != 'All':
        # statement = text("SELECT * FROM persons WHERE name = :name")
        # purchaser_id = session.execute(statement, {"name": purchaser}).first().id
        purchaser_id = session.query(Person).filter_by(name=purchaser).first().id
        transactions = transactions.filter_by(purchaser_id=purchaser_id)

    data = [{
        "ID": transaction.id,
        "Merchant Name": session.query(Merchant).get(transaction.merchant_id).name,
        "Amount": transaction.amount,
        "Date": transaction.date,
        "Payer": session.query(Person).get(transaction.purchaser_id).name
    } for transaction in transactions]

    st.session_state.transactions = transactions
    st.session_state.transactions_data = data

main_left, main_right = st.columns([4, 6])
load_transactions_into_ss(start_date, end_date, person, merchant, purchaser)
with main_left:
    st.subheader('Transactions')
    st.dataframe(st.session_state.transactions_data)
    st.write(st.session_state.transactions_data)

with main_right:
    # pie chart by merchant
    st.subheader("Visualizations")

    inner_left, inner_right = st.columns([1, 1])
    with inner_left:
        
        merchant_data = {}
        for transaction in st.session_state.transactions:
            merchant_name = session.query(Merchant).get(transaction.merchant_id).name
            if merchant_name in merchant_data:
                merchant_data[merchant_name] += transaction.amount
            else:
                merchant_data[merchant_name] = transaction.amount
        
        
        fig = px.pie(values=list(merchant_data.values()), names=list(merchant_data.keys()), title='Pie chart by merchant', width=400, height=400)
        st.plotly_chart(fig)

        st.write(merchant_data)

    # pie chart by purchaser
    with inner_right:
        purchaser_data = {}
        for transaction in st.session_state.transactions:
            purchaser_name = session.query(Person).get(transaction.purchaser_id).name
            if purchaser_name in purchaser_data:
                purchaser_data[purchaser_name] += transaction.amount
            else:
                purchaser_data[purchaser_name] = transaction.amount
        fig = px.pie(values=list(purchaser_data.values()), names=list(purchaser_data.keys()), title='Pie chart by payer', width=400, height=400)
        st.plotly_chart(fig)

        st.write(purchaser_data)

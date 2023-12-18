import streamlit as st
import pandas as pd
import pymongo
from io import StringIO


#connection to MongoDB database
#client = MongoClient('mongodb://localhost:27017')



@st.cache_resource
def init_connection():
    try:
        return pymongo.MongoClient(**st.secrets['mongo'])
    except pymongo.errors.ServerSelectionTimeoutError as e:
        st.error(f"Failed to connect to MongoDB: {e}")
        raise e

client = init_connection()
db = client['sample_company_db']
employees_collection = db['employees']
wages_collection = db['wages']
#####
#streamlit app
st.title('Wages Streamlit App')

# def get_next_employee_id():
    # sequence_doc = db.counters.find_one_and_update(
    #     {'_id':'employee_id'},
    #     {'$inc':{'seq':1}},
    #     upsert=True,
    #     return_document=True
    # )



#employee information
st.subheader('Register Employees')
emp_name = st.text_input('Name:')
emp_surname = st.text_input('Surname:')
emp_addr =  st.text_input('Address:')
if st.button('Register Employee'):
    emp_data = {'emp_name':emp_name,
                'emp_surname':emp_surname,
                'emp_addr':emp_addr}
    employees_collection.insert_one(emp_data)
    st.success('Employee registered!')

#Upload csv file
uploaded_file = st.file_uploader('Upload CSV file',
                                 type=['csv'])

if uploaded_file is not None:
    
    df = pd.read_csv(uploaded_file)
    
    st.subheader('Uploaded file data:')
    st.write(df)
    
    if st.button('Calculate Wages'):
        #calculate wages
        df['total_wage'] = df['hours'] * df['rate']
        
        st.subheader('Calculated Wages:')
        st.write(df)
        
        for _ , row in df.iterrows():
            wage_data = {
                'employee_id':int(row['employee_id']),
                'hours':int(row['hours']),
                'rate':float(row['rate']),
                'total_wage':float(row['total_wage']),
                'date':row['date']
            }
            wages_collection.insert_one(wage_data)
            
        st.success('Wages calculated and saved to database.')
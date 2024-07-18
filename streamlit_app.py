import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import SnowparkSessionException

# Configurare conexiune Snowflake
connection_parameters = {
    "account": "KVFEXRW.TC40940",
    "user": "crazvan6",
    "password": "Counter6,.",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC"
}

def create_snowflake_session():
    try:
        session = Session.builder.configs(connection_parameters).create()
        return session
    except SnowparkSessionException as e:
        st.error(f"Could not create Snowflake session: {e}")
        return None

# Creează sesiunea
session = create_snowflake_session()

# Verifică dacă sesiunea a fost creată cu succes
if session:
    st.write("Snowflake session created successfully!")
    # Poți continua cu logica aplicației tale folosind `session`
else:
    st.error("Failed to create Snowflake session. Please check the connection parameters.")

# Write directly to the app
st.title(":smoothie: Example Streamlit App :balloon:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

from snowflake.snowpark.functions import col
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
                values ('""" + ingredients_string + """')"""
    
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered!', icon="✅")


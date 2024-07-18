# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.context import get_active_session
import pandas

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """
    choose the fruits you want in your custom smoothie
    """
)


from snowflake.snowpark.functions import col
st.write("debug")
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col("search_on"))

# st.dataframe(data=my_dataframe, use_container_width=True)
pd_df = my_dataframe.to_pandas()


ingredients_list = st.multiselect(
    "What are your favorite fruits",
    my_dataframe
    ,
    max_selections = 5
)

ingredients_string  = ''
if ingredients_list:    
    # st.write("You selected:", ingredients_list)
    # st.text(ingredients_list)
    for fruit in ingredients_list: 
        st.subheader(fruit + " Nutrition Information" )
        
        ingredients_string += fruit + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit,' is ', search_on, '.')
        
        st.write(ingredients_string)
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
        fv_df = st.dataframe(data = fruityvice_response.json(),use_container_width = False)



name_on_order = st.text_input("Your Name")
# st.write("Your name entered is", name_on_order)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """',
            '"""+name_on_order+"""')"""

# st.write(my_insert_stmt)

time_to_insert = st.button("Submit Order")
if time_to_insert: 
    if ingredients_string:
        session.sql(my_insert_stmt).collect()
    st.success(f'Your Smoothie is ordered {name_on_order}!', icon="✅")





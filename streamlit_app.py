# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
Choose up to 5 ingredients.
  """
)

# Input: name on order
name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie:', name_on_order)

# Load fruit options
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))

# Multiselect ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list and name_on_order:
    # Build the string with a loop
    ingredients_string = ""
  
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "
        st.subheader(fruit_chosen + 'Nutrition Infromation')  
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Trim trailing space (optional)
    ingredients_string = ingredients_string.strip()

    # Create insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Button to submit
    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

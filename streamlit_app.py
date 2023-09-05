import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#This is where streamlit is used
streamlit.title ('My Parents New Healthy Diner')

streamlit.header ('BREAKFEAST FAVORITES')
streamlit.text ('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text ('🥗 Kale, Spinach & Rocket Smothie')
streamlit.text ('🐔 Hard-boiled Free-Range Egg')
streamlit.text ('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#This is where pandas is used
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
streamlit.dataframe(fruits_to_show)

#This is where requests is used
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response)

#Create the repeatable code called a function
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)

#New Section to display Fruityvice API Response
streamlit.header ('FruityVice Fruit Advice!')
try: 
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error ("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

#This is where Snowflake is used
streamlit.header("The Fruit Load List Contains:")
#Snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

#Add button to load the fruit
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

#Allow the user to add fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into FRUIT_LOAD_LIST Values ('"+new_fruit+ "')")
        return "Thanks For Adding  " + new_fruit

add_my_fruit = streamlit.text_input("What Fruit would you like to add?")
if streamlit.button ('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

#Don't run anything past this point
streamlit.stop()   
streamlit.text("What Fruit would you like to add?")
add_my_fruit = streamlit.text_input('What Fruit would you like to add?')
streamlit.write('Thanks for adding ', add_my_fruit)


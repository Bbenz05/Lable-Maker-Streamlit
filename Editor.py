import streamlit as st
import pymongo
from faker import Faker
from PIL import Image, ImageFont, ImageDraw, ImageTk
import os
import random
import treepoem
import fitz
import code128
from pyzbar.pyzbar import decode
import random_address
import string
import webbrowser
import xmltodict
import requests
import json
from streamlit_toggle import st_toggle_switch

dir_path = os.path.dirname(os.path.realpath(__file__))

#Extras------------------------------------------------------------------------------------------
#    st_toggle_switch(
        #label="Custome Return Address",
        #key="custom_return_address",
        #default_value=True,
        #label_after=False)

#---UPS Functions---
auto_tracking_number = "1Z"


fake = Faker()
fake_return_name = fake.name()
fake_return_address = fake.street_address()
fake_return_city = fake.city()
fake_return_state = fake.state_abbr()
fake_return_zip = fake.zipcode()

fake_ship_name = fake.name()
fake_ship_address = fake.street_address()
fake_ship_city = fake.city()
fake_ship_state = fake.state_abbr()
fake_ship_zip = fake.zipcode()
#Extras------------------------------------------------------------------------------------------

#---Global Funtions---
def selectOriginalLabelUPS():
    return
    #This was subbed out for the file uploader and collectTrackingNumberUPS(original_label)

def collectTrackingNumberUPS(file):
    global tracking_number
    tracking_number = []
    file_name, file_extension = os.path.splitext(file.name)
    doc = fitz.open(stream=file.read(), filetype=file_extension)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=150)
    pix.save("temp.png")
    for bar in decode(Image.open("temp.png")):
        if bar.data.decode("utf-8").upper().startswith(('1Z')):
            tracking_number.append((bar.data.decode("utf-8")))
    os.remove("temp.png")
    try:
        auto_tracking_number = tracking_number[0]
        return auto_tracking_number
        #reverseTrackingLookup()
    except:
        st.warning(
            "Can't find a tracking number in this file. If this continues you'll need to manually enter it.",
            icon="⚠️")
        




def ups_main():
    blank_label = Image.open(dir_path + "/resources/master.png")

    return_address_font = ImageFont.truetype(
        dir_path + '/resources/fonts/DroidSans.ttf', 15)
    shipping_address_font = ImageFont.truetype(
        dir_path + '/resources/fonts/DroidSans.ttf', 25)
    shipping_address_city_font = ImageFont.truetype(
        dir_path + '/resources/fonts/DroidSans-Bold.ttf', 35)
    big_state_and_numbers_font = ImageFont.truetype(
        dir_path + '/resources/fonts/DroidSans-Bold.ttf', 66)
    big_h = ImageFont.truetype(
        dir_path + '/resources/fonts/DroidSans-Bold.ttf', 225)
    
    return_text_name = ups_return_name_input.upper()
    return_text_address_1 = ups_return_address_input.upper()
    return_text_address_2 = ups_return_city_input.upper() + " " + \
    ups_return_state_input.upper() + " " + ups_return_zip_input.upper()

    ship_to_name = ship_to_name_input.upper()
    ship_to_address_1 = ship_to_address1_input.upper()
    ship_to_city = ship_to_city_input.upper()
    ship_to_state = ship_to_state_input.upper()
    ship_to_zip = ship_to_zip_input.upper()

    ship_to_address_2 = ship_to_city + " " + ship_to_state + " " + ship_to_zip

    #if (len(ups_region_input.get()) < 4):
    #    ups_region = "9-01"
    #else:
    ups_region = ups_region_input.upper()

    image_editable = ImageDraw.Draw(blank_label)

    tracking_number = ups_tracking_number_input
    tracking_number = tracking_number.upper()
    tracking_number = tracking_number.replace(" ", "")
    tracking_number_with_spaces = tracking_number[:2] + " " + tracking_number[2:5] + " " + tracking_number[5:8] + \
        " " + tracking_number[8:10] + " " + \
        tracking_number[10:14] + " " + tracking_number[14:18]
    modified_tracking_number = tracking_number_with_spaces[:-9] + \
        tracking_number_with_spaces[19:] + tracking_number_with_spaces[13:18]

    big_barcode = code128.image(tracking_number, height=160)
    new_random_address2 = random_address.real_random_address()

    if edit_type == "LIT":
        tracking_number = "1Z" + random.choice(string.ascii_letters).upper() + str(random.randint(
            1, 9)) + random.choice(string.ascii_letters).upper() + str(random.randint(1000000000001, 9999999999999))
        tracking_number_with_spaces = tracking_number[:2] + " " + tracking_number[2:5] + " " + tracking_number[5:8] + \
            " " + tracking_number[8:10] + " " + \
            tracking_number[10:14] + " " + tracking_number[14:18]
        big_state_number = new_random_address2["state"].upper(
        ) + " " + str(random.randint(111, 999)) + "  " + ups_region
        small_barcode_text = "420" + str(random.randint(10001, 99999))
        small_barcode = code128.image(small_barcode_text, height=90)
        global file_name
        file_name = dir_path + "/resources/maxi/" + \
            str(random.randint(1, 8)) + ".png"
        weird_file_name = file_name
        weird_barcode = Image.open(weird_file_name)
        blank_label.paste(weird_barcode.resize((177, 168)), (16, 350))

    else:
        big_state_number = ship_to_state + " " + \
            ship_to_zip[0:3] + "  " + ups_region
        small_barcode_text = "420" + str(ship_to_zip)
        small_barcode = code128.image(small_barcode_text, height=90)

        # RETURN ADDRESS
    image_editable.text((15, 10), return_text_name,
                        (0, 0, 0), font=return_address_font)
    image_editable.text((15, 25), return_text_address_1,
                        (0, 0, 0), font=return_address_font)
    image_editable.text((15, 40), return_text_address_2,
                        (0, 0, 0), font=return_address_font)

    # SHIP TO ADDRESS
    image_editable.text((60, 135), ship_to_name, (0, 0, 0),
                        font=shipping_address_font)
    image_editable.text((60, 160), ship_to_address_1,
                        (0, 0, 0), font=shipping_address_font)
    image_editable.text((60, 185), ship_to_address_2,
                        (0, 0, 0), font=shipping_address_city_font)

    # TRACKING NUMBER
#    if (ups_scramble_tracking.get() == True):
#        image_editable.text((155, 583), modified_tracking_number,
#                           (0, 0, 0), font=shipping_address_font)
#    else:
    image_editable.text((155, 583), tracking_number_with_spaces,
                        (0, 0, 0), font=shipping_address_font)
    
    # STATE + 6 NUMBERS
    image_editable.text((220, 343), big_state_number,
                        (0, 0, 0), font=big_state_and_numbers_font)

    # SMALL BARCODE
    blank_label.paste(small_barcode, (230, 425))

    w, h = big_barcode.size
    big_barcode_cropped = big_barcode.crop((15, 0, w-10, h))
    big_barcode_resized = big_barcode_cropped.resize((490, 160))
    blank_label.paste(big_barcode_resized, (50, 645))

    st.sidebar.image(blank_label, use_column_width=False, width=400)
    








#----------------------------------------------------------------------------Page Setup------------------------------------------------------------------------------------------------
#Affects the tab name, icon, and layout of the page
st.set_page_config(
    page_title="UPS", 
    page_icon=None,
    layout="centered",
    initial_sidebar_state="auto",)
#---Header--- 

#---Body---
original_label = st.file_uploader(
    "Upload Original Label",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=False,
    help="Upload only the label. Do not upload the instructions.",
)

if original_label is not None:
    collectTrackingNumberUPS(original_label)


Carrier = st.selectbox("Carrier:", ["UPS", "FedEx", "USPS"])

#UPS
if Carrier == "UPS":
    edit_type = st.selectbox(
        "Edit Type:",
        ["LIT", "FTID"],
        help="FTID: You are responsible for knowing where the send the label.\n LIT: This is very beginner friendly. Just drop the Label and it will be lost after 2 scans.")
    if edit_type == "FTID":         
        with st.expander("Shipping Information"):
            ship_to_name_input = st.text_input("Name")
            ship_to_address1_input = st.text_input("Address")
            ship_to_city_input = st.text_input("City")
            ship_to_state_input = st.selectbox("State", ["-","AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])
            ship_to_zip_input = st.text_input("Zip")
            ups_region_input = st.text_input("UPS Region Code")
            ups_tracking_number_input = st.text_input("Tracking Number", value=auto_tracking_number)
            ups_scramble_tracking_input = st.checkbox("Scramble Tracking Number", value=False)

        with st.expander("Return Information"):
            if st.checkbox("Generate Random"):
                ups_return_name_input = st.text_input("Name", key="ups_fake_return_name_input", value=fake_return_name)
                ups_return_address_input = st.text_input("Address", key="ups_fake_return_address_input",value=fake_return_address)
                ups_return_city_input = st.text_input("City", key="ups_fake_return_city_input",value=fake_return_city)
                ups_return_state_input = st.text_input("State", key="ups_fake_return_state_input",value=fake_return_state)
                ups_return_zip_input = st.text_input("Zip", key="ups_fake_return_zip_input",value=fake_return_zip)
            else:
                ups_return_name_input = st.text_input("Name", key="ups_return_name_input")
                ups_return_address_input = st.text_input("Address", key="ups_return_address_input")
                ups_return_city_input = st.text_input("City", key="ups_return_city_input")
                ups_return_state_input = st.text_input("State", key="ups_return_state_input")
                ups_return_zip_input = st.text_input("Zip", key="ups_return_zip_input")
    else:
        with st.expander("Shipping Information"):

            new_region = str(random.randint(0, 9)) + "-" + \
            str(random.randint(10, 99))
                    
            ship_to_name_input = st.text_input("Name", disabled=True, value=fake_ship_name)
            ship_to_address1_input = st.text_input("Address", disabled=True, value=fake_ship_address)
            ship_to_city_input = st.text_input("City", disabled=True, value=fake_ship_city)
            ship_to_state_input = st.text_input("State", disabled=True, value=fake_ship_state)
            ship_to_zip_input = st.text_input("Zip", disabled=True, value=fake_ship_zip)
            ups_region_input = st.text_input("UPS Region Code", disabled=True, value=new_region)
            ups_tracking_number_input = st.text_input("Tracking Number", value=auto_tracking_number, disabled=False, help="You might want to change the tracking number up a bit incase it actually reaches the store. This way they can't match up the label to your order.")
        with st.expander("Return Information"):
            ups_return_name_input = st.text_input("Name", key="ups_return_name_input", disabled=True, value=fake_return_name)
            ups_return_address_input = st.text_input("Address", key="ups_return_address_input", disabled=True, value=fake_return_address)
            ups_return_city_input = st.text_input("City", key="ups_return_city_input", disabled=True, value=fake_return_city)
            ups_return_state_input = st.text_input("State", key="ups_return_state_input", disabled=True, value=fake_return_state)
            ups_return_zip_input = st.text_input("Zip", key="ups_return_zip_input", disabled=True, value=fake_return_zip)



    with st.expander("Key"):
        st.text_input("Key Not Needed", disabled=True)

    st.button('Generate Label', key="generate_label", on_click=ups_main, )

#fedex
elif Carrier == "FedEx":
    st.write("Coming Soon")
#usps
elif Carrier == "USPS":
    st.write("Coming Soon")
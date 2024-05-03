import streamlit as st
import openai
import os

from openai import AsyncOpenAI
from openai import OpenAI
import time

client = AsyncOpenAI(
    api_key=os.getenv("API_key")
    )

context = """This app assists users in finding information about specific medications 
based on their symptoms. Please follow the prompts to proceed."""

async def split_comma_separated_string(string):
    """Splits a string containing comma-separated items into a list.
    Args:
        string: The string to split.
    Returns:
        A list containing the individual items from the string.
    """
    # Split the string by comma, handling potential spaces around commas
    return string.split(", ")


async def generate_response(question, context):
    model = "gpt-4-0125-preview"
    completion = await client.chat.completions.create(model=model, 
        messages=[{"role": "user", "content": question}, 
                {"role": "system", "content": context}])
    return completion.choices[0].message.content


async def app():
    if "current_form" not in st.session_state:
        st.session_state["current_form"] = 1    

    if "symptoms" not in st.session_state:
        st.session_state["symptoms"] = None
    
    if "selected_option" not in st.session_state:
        st.session_state["selected_option"] = None
    
    if "possible_medications" not in st.session_state:
        st.session_state["possible_medications"] = None
        

    # Display the appropriate form based on the current form state
    if st.session_state["current_form"] == 1:
        await display_symptoms_form1()
    elif st.session_state["current_form"] == 2:
        await display_medication_form2()
    elif st.session_state["current_form"] == 3:
        await display_information3()


async def display_symptoms_form1():
    form1 = st.form("Introduction")
    form1.subheader("Medication Information Lookup")
    
    text = """Cherry Mirra Calisnao     BSCS 3A \n
    CCS 229 - Intelligent Systems \n
    Final Project in Intelligent Systems \n
    College of Information and Communications Technology
    West Visayas State University"""
    form1.text(text)

    form1.image("med_ai.png", caption="Medication Information App", use_column_width=True)
    text = """An AI powered research co-pilot designed to assist students in finding research problems for their undergraduate thesis."""
    form1.write(text)
    
    # Prompt user for course inp
    symptoms = form1.text_input("Enter your symptoms (comma-separated):", key="symptoms")
    possible_medications = form1.text_input("Enter possible medications (comma-separated):", key="possible_medications")
    
    submit1 = form1.form_submit_button("Submit")
    if submit1:
        if symptoms:
            st.session_state["symptoms"] = symptoms
            if possible_medications:
                st.session_state["possible_medications"] = possible_medications
            st.session_state["current_form"] = 2
        else:
            form1.warning("Please enter your symptoms.")       

#Error starts here
async def display_medication_form2():
    symptoms = st.session_state["symptoms"]
    possible_medications = st.session_state["possible_medications"]
    st.session_state["current_form"] = 2
    form2 = st.form("Medication Selection")
    prompt = f"What are your symptoms? \n Based on your symptoms ({symptoms}) and possible medications ({possible_medications}), here are some medication options:"
    medications = await generate_response(prompt, context)
    options = await split_comma_separated_string(medications)
    selected_medication = form2.selectbox(
        label="Choose a medication:",
        options=options,    
    )
        
    submit2 = form2.form_submit_button("Get Information")
    
    if submit2:
        st.session_state["selected_option"] = selected_medication
        st.session_state["current_form"] = 3
        display_information3()

def display_information3():
    form3 = st.form("Medication Information")
    selected_medication = st.session_state["selected_option"]
    symptoms = st.session_state["symptoms"]
    
    question = f"For the symptoms {symptoms} and the selected medication {selected_medication}, provide information such as indications, contraindications, and side effects."
    response = generate_response(question, context)
    
    form3.write("Medication Information:")
    form3.write(response)
            

# Run the app
if __name__ == "__main__":
    import asyncio
    asyncio.run(app())



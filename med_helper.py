import streamlit as st
import openai
import os
import time
import asyncio

from openai import AsyncOpenAI

# Create AsyncOpenAI instance
client = AsyncOpenAI(api_key=os.getenv("API_key"))

context = """This app assists users in finding information about specific medications 
based on their symptoms. Please follow the prompts to proceed."""

async def generate_response(question, context):
    model = "gpt-3.5-turbo-0613"
    completion = await client.chat.completions.create(model=model, 
        messages=[{"role": "user", "content": question}, 
                {"role": "system", "content": context}])
    return completion.choices[0].message.content

async def app():
    if "current_form" not in st.session_state:
        st.session_state["current_form"] = 1    

    if "symptoms" not in st.session_state:
        st.session_state["symptoms"] = None
    
    if "age" not in st.session_state:
        st.session_state["age"] = None
    
    if "selected_medication" not in st.session_state:
        st.session_state["selected_medication"] = None
        
    # Display the appropriate form based on the current form state
    if st.session_state["current_form"] == 1:
        await display_symptoms_form1()
    elif st.session_state["current_form"] == 2:
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
    
    # Prompt user for symptoms
    symptoms = form1.text_input("Enter your symptoms (comma-separated):", key="symptoms")

    # Prompt user for age
    age = form1.number_input("Enter your age:", min_value=0, max_value=150, key="age")
    
    submit1 = form1.form_submit_button("Submit")

    if submit1:
        if symptoms:
            if "symptoms" not in st.session_state:
                st.session_state["symptoms"] = symptoms
            if "age" not in st.session_state:
                st.session_state["age"] = age
            # Generate a question based on symptoms and age
            question = f"What medication would you recommend for a {age}-year-old with {symptoms.strip()}?"
            # Generate possible medications based on the question
            response = await generate_response(question, context)
            possible_medications = response.splitlines()
            if possible_medications:
                st.session_state["possible_medications"] = possible_medications
                st.session_state["current_form"] = 2  # Move to the next form
                await display_information3()  # Call the display_information3 function directly
            else:
                form1.warning("No medications found for the entered symptoms.")       
        else:
            form1.warning("Please enter your symptoms.")       

async def display_information3():
    form3 = st.form("Medication Information")
    symptoms = st.session_state["symptoms"]
    possible_medications = st.session_state["possible_medications"]
    age = st.session_state["age"]
    
    form3.write(f"Symptoms: {symptoms}")
    form3.write(f"Age: {age}")
    form3.write("Possible Medications:")
    for medication in possible_medications:
        form3.write(f"- {medication}")
    
    question = f"Provide information about the medication {possible_medications[0]} for a {age}-year-old, including indications, contraindications, common and potential side effects, usage instructions (e.g., dosage and frequency of administration), and any other important considerations."
    progress_bar = form3.progress(0, text="The AI co-pilot is processing the request, please wait...")
    response = await generate_response(question, context)
    form3.write("Medication Information:")
    form3.write(response)

    # update the progress bar
    for i in range(100):
        # Update progress bar value
        progress_bar.progress(i + 1)
        # Simulate some time-consuming task (e.g., sleep)
        time.sleep(0.01)
    # Progress bar reaches 100% after the loop completes
    form3.success("AI research co-pilot task completed!") 

    submit3 = form3.form_submit_button("Submit")  # Add the submit button
    if submit3:
        form3.write("Would you like to ask another question?")  
        form3.write("If yes, please refresh the browser.") 

# Run the app
if __name__ == "__main__":
    asyncio.run(app())

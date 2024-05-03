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
    
    submit1 = form1.form_submit_button("Submit")

    if submit1:
        if symptoms:
            if "symptoms" not in st.session_state:
                st.session_state["symptoms"] = symptoms
            st.session_state["current_form"] = 2
            await display_medication_form2()
        else:
            form1.warning("Please enter your symptoms.")       

#Error starts here
async def display_medication_form2():
    symptoms = st.session_state["symptoms"]
    st.session_state["current_form"] = 2
    form2 = st.form("Medication Selection")
    prompt = f"What are your symptoms? \n Based on your symptoms ({symptoms}), here are some medication options:"
    medications = await generate_response(prompt, context)
    options = await split_comma_separated_string(medications)
    # selected_medication = form2.selectbox(
    #     label="Choose a medication:",
    #     options=medication_list,    
    # )
        
    submit2 = form2.form_submit_button("Get Information")
    
    if submit2:
        st.session_state["selected_medication"] = options
        await display_information3()

async def display_information3():
    st.session_state["current_form"] = 3
    form3 = st.form("Medication Information")
    selected_medication = st.session_state["selected_medication"]
    symptoms = st.session_state["symptoms"]
    
    # Create the combobox (selectbox) with a descriptive label
    selected_option = form3.selectbox(
        label="Choose the Medicine:",
        options=selected_medication,    
    )

    
    submit3 = form3.form_submit_button("Medication Information")
    if submit3:
        question = f"For the symptoms {symptoms} and the research area {selected_option}, give me 3 research problems.  Provide the title, abstract and research objectives for each research problem."
        if question:
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
            form3.write("Would you like to input another symptoms?")  
            form3.write("If yes, please refresh the browser.")  
        else:
            form3.error("Please enter a prompt.")
            

# Run the app
if __name__ == "__main__":
    import asyncio
    asyncio.run(app())




# import streamlit as st
# import openai
# import os

# from openai import AsyncOpenAI
# from openai import OpenAI
# import time

# client = AsyncOpenAI(api_key=os.getenv("API_key"))

# context = """This app assists users in finding information about specific medications based on their symptoms. Please follow the prompts to proceed."""

# async def generate_response(question, context):
#     model = "gpt-4-0125-preview"
#     completion = await client.chat.completions.create(model=model, 
#         messages=[{"role": "user", "content": question}, 
#                 {"role": "system", "content": context}])
#     return completion.choices[0].message.content


# async def app():
#     if "current_form" not in st.session_state:
#         st.session_state["current_form"] = 1    

#     if "symptoms" not in st.session_state:
#         st.session_state["symptoms"] = None
    
#     if "selected_medication" not in st.session_state:
#         st.session_state["selected_medication"] = None
        

#     # Display the appropriate form based on the current form state
#     if st.session_state["current_form"] == 1:
#         await display_symptoms_form()
#     elif st.session_state["current_form"] == 2:
#         await display_medication_form()
#     elif st.session_state["current_form"] == 3:
#         await display_information()


# async def display_symptoms_form():
#     form = st.form("Symptoms Selection")
#     form.subheader("Select Your Symptoms")

#     symptoms = form.text_input("Enter your symptoms (comma-separated):", key="symptoms")
    
#     submit = form.form_submit_button("Submit")

#     if submit:
#         if symptoms:
#             st.session_state["symptoms"] = symptoms
#             st.session_state["current_form"] = 2
#             await display_medication_form()
#         else:
#             form.warning("Please enter your symptoms.")       


# async def display_medication_form():
#     symptoms = st.session_state["symptoms"]
#     st.session_state["current_form"] = 2
#     form = st.form("Medication Selection")
#     prompt = f"Based on your symptoms ({symptoms}), here are some medication options:"
#     medications = await generate_response(prompt, context)
#     medication_list = await split_comma_separated_string(medications)

#     selected_medication = form.selectbox(
#         label="Choose a medication:",
#         options=medication_list,    
#     )
        
#     submit = form.form_submit_button("Get Information")
#     if submit:
#         st.session_state["selected_medication"] = selected_medication
#         st.session_state["current_form"] = 3
#         await display_information()

# async def display_information():
#     st.session_state["current_form"] = 3
#     form = st.form("Medication Information")
#     selected_medication = st.session_state["selected_medication"]

#     question = f"Provide information about the medication {selected_medication}, including indications, contraindications, side effects, and nursing considerations."
#     progress_bar = form.progress(0, text="Processing your request, please wait...")
#     response = await generate_response(question, context)
#     form.write("Medication Information:")
#     form.write(response)

#     for i in range(100):
#         progress_bar.progress(i + 1)
#         time.sleep(0.01)
#     form.success("Information retrieved successfully!") 

# # Run the app
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(app())

import streamlit as st
import PyPDF2
from openai import OpenAI
from lastmileai import LastMile
import pandas as pd 
import os

Lastmile_API = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..AovYeCL9Ip-nUbaO.JlmY8Rbhivhs63sFt3kwR8YTXPFH_K_RjmCin5dYFOMOgigiHopTmriGOjzTxm8a3EOaY3ztuuhnQmsZxi03a4oVPl0Xb2v2gizSnknbtwopNjwiOLOYagM1xCU6FEbTnj8CJQzXv-QYqRlydRhXC_SSItCrsoJfY4CHPsRG3M8WyzLzYrsP_8pwZyRa7hdjiv22JqTZMR-yM6WTyLUCwZMGoLI6xnl4lQWwBHJai4a8tRg.mjWnBW4pECgGkUcjMQWz_w"
lastmile = LastMile(api_key=Lastmile_API)

# Saving the user questions
if 'UserQA.csv' in os.listdir():
    userQA = pd.read_csv("UserQA.csv")
else:
    userQA = pd.DataFrame (columns=["User", "Bot"])
    print("Dataframe created")

def get_chatGPT_response(prompt, pdf_content, job_description):
    # Assume integration with an AI service like OpenAI's ChatGPT or similar
    response = lastmile.create_openai_chat_completion(
        completion_params={
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt.format(pdf_content, job_description)}]}
            ],
        }
    )

    return response['completionResponse']['choices'][0]['message']['content']


def input_pdf_setup(file):
    if file is not None:
        resume_text = ""
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            resume_text += page.extract_text()

        return resume_text
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
job_desc = st.text_area("Job Description:", key="input")
file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if 'history' not in st.session_state:
    st.session_state['history'] = []

# Creating buttons
AboutButton = st.button("Analyze the resume against the job description")
RatingButton = st.button("Rate the match and provide feedback")

st.header("Ask questions about your resume or job description")
# Using st.text_input with on_change
user_question = st.text_input("Enter your question here:", key="chat", on_change=None, args=None, kwargs=None,)

ask_button = st.button("Ask")

if AboutButton:
    if file:
        pdf_content = input_pdf_setup(file)
        FeedbackPrompt = """
        You are an experienced Technical Human Resource Manager, your task is to review the provided Resume : {0} against the job description {1}. 
        Please share your professional evaluation on whether the candidate's profile aligns. 
        Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
        """
        response = get_chatGPT_response(FeedbackPrompt, pdf_content, job_desc)
        st.write(response)
    else:
        st.error("Please upload the resume.")

elif RatingButton:
    if file:
        pdf_content = input_pdf_setup(file)
        RatingPrompt = """
        You are an ATS (Applicant Tracking System) scanner which is designed to scan resume {0} for specific keywords and phrases. 
        Your task is to evaluate the resume against the provided job description {1}. Rate the resume between 1 - 10 where 1 being the lowest match and 10 being the highest match with the job description. 
        The output should come as the rating / highest score, explain the reason for the score, missing keywords, lastly final thoughts with the list of best resources with links to learn missing skills better if they are provided from the same company or suggest from top resources in the according to the job title.
        """
        response = get_chatGPT_response(RatingPrompt, pdf_content, job_desc)
        st.write(response)
    else:
        st.error("Please upload the resume.")

elif ask_button:
    if file and job_desc and user_question:  # Ensure all necessary inputs are provided
        pdf_content = input_pdf_setup(file)
        QuestionPrompt = "You're a helpful bot. Given the resume {0} and job description {1} answer the user query." + user_question
        response = get_chatGPT_response(QuestionPrompt, pdf_content, job_desc)
        
        # Save conversation to history
        st.session_state['history'].append(("You", user_question))
        st.session_state['history'].append(("Bot", response))

        userQA.loc[len(userQA)]= [user_question, response]
        userQA.to_csv("UserQA.csv", index=False)
        
        # Display conversation history with emojis
        for speaker, text in st.session_state['history']:
            if speaker == "You":
                # Adding user emoji
                st.markdown(f"👤 **{speaker}**: {text}")
            else:  # Bot
                # Adding bot emoji
                st.markdown(f"🤖 **{speaker}**: {text}")
    elif not file:
        st.error("Please upload the resume.")
    elif not job_desc:
        st.error("Please enter a job description.")
    elif not user_question:
        st.error("Please enter a question.")

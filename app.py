import streamlit as st
import PyPDF2
from lastmileai import LastMile

Lastmile_API = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..pmrV6W5j6CPKG31L.liGQlJroWTrTAVIqLj_3qfGhKIo2uu5WELTbSEOa3CL5QLYCKmrEKF0eOiycPDwJQNggJbjw1wmwU_4zkeKFwAl21Ob4d9cCILNDaEi_0jjnDu2G83LB9wsWHv3TMoXQ5au-msLr5VcDCS8Q5Vp8bynQyAExPl0PIPSa_mbHDAFC3AMkGo1VoxOTwcS57QgO_wZaAaAmaBMUpBkt2D0tH6tpyQAenldpX6SQuooq5NPgkFhSEwlFPcRcFkJWYm3Gvk1XjWKxT_faXTQ9eBdE0yk2FLucEsSI9EJ06OjEaaBBGPEINQMAhvc6Lcas2grQ_1dmW54hRRMR_Pa2LgpUNOQkZ1OCXPEjaiCWJIsI3SqHpiJuFKRmwhbjMX06COXxceE.M1xNvsKpBjcr2dvjueKVxA"
lastmile = LastMile(api_key=Lastmile_API)

def get_chatGPT4_response(input,pdf_content,prompt):
    completion = lastmile.create_openai_chat_completion(
    completion_params = {
        "model": "gpt-3.5-turbo",
        "messages": [
        {
        "role": "user",
        "content": [
            {"type": "text", "text": input + prompt + pdf_content},
        ],
        }
    ],
    }
    )
    return completion['completionResponse']['choices'][0]['message']['content']

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        resume_text = ""
        pdf = PyPDF2.PdfReader(uploaded_file)
        for page in pdf.pages:
            resume_text += page.extract_text()

        return resume_text
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
job_desc=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_chatGPT4_response(input_prompt1,pdf_content,job_desc)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_chatGPT4_response(input_prompt3,pdf_content,job_desc)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please upload the resume")



   






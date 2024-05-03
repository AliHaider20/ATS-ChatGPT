from flask import Flask, request, jsonify
import PyPDF2
from lastmileai import LastMile

app = Flask(__name__)

# Initialize the LastMile API with your key
lastmile_api_key = "your_lastmile_api_key_here"
lastmile = LastMile(api_key=lastmile_api_key)

@app.route('/upload', methods=['POST'])
def upload_pdf_and_analyze():
    if 'pdf_file' not in request.files:
        return jsonify({"error": "missing file"}), 400
    
    pdf_file = request.files['pdf_file']
    job_description = request.form.get('job_description', '')

    if pdf_file:
        pdf_content = extract_text_from_pdf(pdf_file)
        prompt = request.form.get('prompt', '')
        
        response = get_chatGPT4_response(prompt, pdf_content, job_description)
        return jsonify({"response": response}), 200
    else:
        return jsonify({"error": "No file uploaded"}), 400

def extract_text_from_pdf(uploaded_file):
    resume_text = ""
    pdf = PyPDF2.PdfReader(uploaded_file.stream)
    for page in pdf.pages:
        resume_text += page.extract_text() or ""
    return resume_text

def get_chatGPT4_response(prompt, pdf_content, job_desc):
    completion = lastmile.create_openai_chat_completion(
        completion_params = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": [ {"type": "text", "text": prompt + job_desc + pdf_content} ]},
            ],
        }
    )
    return completion['completionResponse']['choices'][0]['message']['content']

if __name__ == '__main__':
    app.run(debug=True)

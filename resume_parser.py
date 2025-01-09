import os
import re
import docx
import PyPDF2
import json

# Define the folder path where the resumes are stored
resume_folder = r'C:\Users\Keerthi\OneDrive\Desktop\New folder'

# Supported file types (docx, pdf)
supported_formats = ['.docx', '.pdf']

# Required skills
required_skills = {'.net', 'java', 'llm','python','c#'}

# Function to extract contact information (email and phone number)
def extract_contact_info(text):
    # Email regex
    email_regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    email = re.search(email_regex, text)



    # Phone number regex
    phone_regex = r"\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}"
    phone = re.search(phone_regex, text)
     

    return (email.group(0) if email else "No email found", phone.group(0) if phone else "No phone number found")

# Function to extract skills from the resume text
def extract_skills(text):
    # Sample list of skills, replace this with a more robust skill extraction logic
    skills_list = ['.net', 'java', 'llm', 'python', 'c++', 'javascript', 'html', 'css', 'sql', 'aws','c#']
    found_skills = {skill for skill in skills_list if skill.lower() in text.lower()}
    return found_skills 

# Function to analyze resumes in the folder
def analyze_resumes_in_folder(folder_path):
    total_resumes = 0
    selected_resumes = []

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        # Skip temporary files (files starting with ~$)
        if filename.startswith('~$'):
            continue
        
        # Process only supported formats
        if any(filename.endswith(ext) for ext in supported_formats):
            total_resumes += 1
            file_path = os.path.join(folder_path, filename)

            try:
                # Read DOCX file
                if filename.endswith('.docx'):
                    doc = docx.Document(file_path)
                    text = '\n'.join([para.text for para in doc.paragraphs])

                # Read PDF file
                elif filename.endswith('.pdf'):
                    with open(file_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        text = ''
                        for page in pdf_reader.pages:
                            text += page.extract_text()

                # Extract skills from resume
                found_skills = extract_skills(text)
                email, phone = extract_contact_info(text)

                # Check if required skills are present
                if required_skills & found_skills:  # Check if there is an intersection of skills
                    status = "selected"
                    # Store the analysis result for each selected resume
                    selected_resumes.append({
                        'filename': filename,
                        'skills_found': list(found_skills),
                        'required_skills': list(required_skills),
                        'email': email,
                        'phone': phone,
                        'status': status
                    })

                    # Print result for this selected resume
                    print(f"------Resume: {filename} NLP Parser Output-------")
                    print(f"Skills Found: {found_skills}")
                    print(f"Required Skills: {required_skills}")
                    print(f"Email: {email}")
                    print(f"Phone: {phone}")
                    print(f"Status: selected\n")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    # Save the selected resumes to a JSON file
    with open('selected_resume_analysis_output.json', 'w') as json_file:
        json.dump(selected_resumes, json_file, indent=4)

    print(f"Total resumes analyzed: {total_resumes}")
    print(f"Total selected resumes: {len(selected_resumes)}")

# Call the function to analyze the resumes in the folder
analyze_resumes_in_folder(resume_folder)

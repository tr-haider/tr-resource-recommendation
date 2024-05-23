import streamlit as st
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Set your OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found. Please set it in the environment variables.")
    st.stop()

client = OpenAI(api_key=api_key)
current_dir = Path(__file__).parent
projects_path = current_dir / 'projects.json'
resources_path = current_dir / 'resource.json'

# Load the datasets
def load_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        st.stop()
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from file: {file_path}")
        st.stop()

projects = load_json(projects_path)
resources = load_json(resources_path)

# Function to query OpenAI GPT-4
def query_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error querying OpenAI: {e}")
        return ""

# Function to recommend projects for a resource
def recommend_projects(resource, projects):
    resource_skills = resource['Skills']
    matched_projects = []
    for project in projects:
        project_technologies = project['Technologies']
        match = any(tech in resource_skills and resource_skills[tech] in ['Intermediate', 'Advanced'] for tech in project_technologies)
        if match:
            matched_projects.append(project['Project Name'])
    
    if matched_projects:
        response = f"Projects that match the resource's skills:\n- " + "\n- ".join(matched_projects)
    else:
        response = "No matching projects found for the resource's skills."
    
    return response

def run_resourcerec():
    st.title("Resource and Project Recommendation Chatbot")

    # Enter a new resource
    st.header("Enter New Resource")
    new_resource_name = st.text_input("Enter a new resource name")

    skill_options = ["React", "NestJS", "ExpressJS", "MySQL", "PostgreSQL", "TensorFlow", "Machine Learning", "React Native", "DevOps", "Solution Architect"]
    level_options = ["Beginner", "Intermediate", "Advanced"]

    new_resource_skills = {}
    if new_resource_name:
        st.write("Select skills for the new resource:")
        for skill in skill_options:
            level = st.selectbox(f"Select level for {skill}", [""] + level_options, key=f"{new_resource_name}_{skill}")
            if level:
                new_resource_skills[skill] = level

    if st.button("Get Recommendations"):
        if new_resource_name and new_resource_skills:
            new_resource = {
                "Resource Name": new_resource_name,
                "Skills": new_resource_skills,
                "Project Preferences": []
            }
            recommendations = recommend_projects(new_resource, projects)
            st.write("Project Recommendations for the Resource:")
            st.write(recommendations)
        else:
            st.error("Please enter a resource name and select skills.")

if __name__ == "__main__":
    run_resourcerec()

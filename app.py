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

# Function to recommend resources based on user problem
def recommend_resources(problem, resources):
    prompt = f"Based on the following problem description, recommend the best resources along with their skills and levels:\n\nProblem: {problem}\n\nResources:\n{json.dumps(resources, indent=2)}"
    return query_openai(prompt)

# Streamlit application
def run_resourcerec():
    st.title("Resource Recommendation Application")

    st.header("Enter Your Problem")
    user_problem = st.text_area("Describe your problem (e.g., 'I want someone to implement the login signup form')")

    if st.button("Get Recommendations"):
        if user_problem:
            recommendations = recommend_resources(user_problem, resources)
            st.write("Recommended Resources for your problem:")
            st.write(recommendations)
        else:
            st.error("Please enter a problem description.")

if __name__ == "__main__":
    run_resourcerec()

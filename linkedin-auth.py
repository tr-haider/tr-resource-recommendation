# import requests
# from requests.auth import HTTPBasicAuth
# import os
# from dotenv import load_dotenv
# load_dotenv()
#
# def get_linkedin_token():
#     url = 'https://www.linkedin.com/oauth/v2/accessToken'
#     data = {
#         'grant_type': 'authorization_code',
#         'client_id': os.getenv('LINKEDIN_CLIENT_ID'),
#         'client_secret': os.getenv('LINKEDIN_SECRET_KEY')
#     }
#     response = requests.post(url, data=data)
#     return response.json().get('access_token')
# token = get_linkedin_token()
# print(token)
import requests
from bs4 import BeautifulSoup

# LinkedIn credentials
linkedin_username = 'khanshahab3855@gmail.com'
linkedin_password = 'khan12345'

# Profile URL to scrape
profile_url = 'https://www.linkedin.com/in/muhammad-haider-shahab-a4773a1b4/'

# Start a session
session = requests.Session()

# LinkedIn login URL
login_url = 'https://www.linkedin.com/login'

# Get login page to retrieve CSRF token
login_page = session.get(login_url)
print(login_page)
soup = BeautifulSoup(login_page.content, 'html.parser')

csrf_token = soup.find('input', {'name': 'loginCsrfParam'})['value']
print(csrf_token)
# Login payload
login_payload = {
    'session_key': linkedin_username,
    'session_password': linkedin_password,
    'loginCsrfParam': csrf_token,
}

# Perform login
login_response = session.post(login_url, data=login_payload)
print(login_response)

# Check if login was successful
if login_response.status_code != 200:
    print("Login failed!")
else:
    print("Login successful!")

# Fetch the profile page
profile_response = session.get(profile_url)

# Check if fetching the profile was successful
if profile_response.status_code != 200:
    print("Failed to fetch the profile!")
else:
    print("Profile fetched successfully!")

# Parse the profile page content
soup = BeautifulSoup(profile_response.content, 'html.parser')

# Extract skills section (this may need adjustment based on LinkedIn's HTML structure)
skills_section = soup.find('section', {'id': 'skills-section'})

skills_list = []
if skills_section:
    skills_elements = skills_section.find_all('span', {'class': 'pv-skill-category-entity__name-text'})
    for skill in skills_elements:
        skills_list.append(skill.get_text(strip=True))

print(skills_list)

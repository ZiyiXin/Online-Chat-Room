# Online Chat Room 

## Execution

1. Create Virtual Environment to support program
`python -m venv <venv_name>`

2. Activate virtual environment
`source venv/bin/activate`

3. Install support packages listed in the requirement to support program
`pip install -r requirements.txt`

4. Execute the program
Locally: `uvicorn app:app --reload`

On server: `python3 -m uvicorn app:app --host 0.0.0.0`

## Introduction

The Online Chatroom allows you to 

1. Login with your chosen Username

2. Chat in the public chatting room with all the other users

3. Check current online users on the leftside bar
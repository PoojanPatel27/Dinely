
## Project Overview

In this project, we configured a chatbot using Dialogflow for natural language understanding. We built a backend server using Python and FastAPI to interact with a MySQL database for order placement and retrieval. The chatbot was integrated with a food website to enable seamless user interactions and efficient order management.

## Tech Stacks Involved

- **Natural Language Processing (NLP):** Dialogflow
- **Backend Development:** Python, FastAPI
- **Database Management:** MySQL
- **Frontend Development:** HTML, CSS, JavaScript
- **HTTPS Tunneling:** Ngrok

## Directory Structure

```
DineBot/
├── backend/              # Contains Python FastAPI backend code
├── db/                   # Contains the dump of the MySQL database
├── dialogflow_assets/    # Contains training phrases and intents for Dialogflow
└── frontend/             # Contains the website code
```

## Installation

First, clone the repository:

```bash
git clone REPO_URL
cd DineBot
```

Next, install the necessary Python modules:

```bash
pip install mysql-connector-python
pip install "fastapi[all]"
```

Alternatively, you can install all required modules with one command:

```bash
pip install -r backend/requirements.txt
```

## Backend Server Setup

To start the FastAPI backend server, follow these steps:

1. Navigate to the `backend` directory in your command prompt:

    ```bash
    cd backend
    ```

2. Run the following command to start the server:

    ```bash
    uvicorn main:app --reload
    ```

## Ngrok for HTTPS Tunneling

To expose your local server to the internet using Ngrok, follow these steps:

1. Download and install Ngrok from [here](https://ngrok.com/download) for your operating system.
2. Extract the zip file and place `ngrok` in a folder.
3. Open the command prompt, navigate to that folder, and run this command:

    ```bash
    ngrok http 8000
    ```

**Note:** Ngrok sessions can expire, so you may need to restart the session if you see a session expired message.

## Usage

Once the backend server and Ngrok are set up, you can interact with the DineBot through your food website. The chatbot will handle order placement and retrieval seamlessly.

## Conclusion

DineBot aims to revolutionize the way users place food orders online, offering a seamless and efficient experience through advanced NLP and robust backend services. We look forward to your contributions and feedback to make this project even better.

## References

- [Dialogflow Documentation](https://cloud.google.com/dialogflow/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Ngrok Documentation](https://ngrok.com/docs)

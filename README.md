# Description
FastAPI fundamentals. Examples explained in the official documentation


## Requirements
- Python 3.8
- FastAPI
- Uvicorn server (ASGI)
- Pydantic


## Instructions to run
1. Clone the project repository

2. Create a new virtual environment from Python with the command ``python -m virtualenv /path/name_of_virtualenv``

3. Activate the virtualenv. The command is: ``source /path/name_of_virtualenv/bin/activate``

4. Install the project requirements with the command ``pip install -r requirements.txt``.\
  **PS**: You must be at the same level as the `requirements.txt` file

5. Run the uvicorn server with the command: ``uvicorn app.main:app --host 0.0.0.0 --port=6700 --reload``\
  **PS**: This command will run the server at the port 6700. If you want to use another port, change the ``--port`` parameter

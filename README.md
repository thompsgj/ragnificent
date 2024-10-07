## Introduction
Style guides help people collaborate together by fostering a shared understanding of rules and best practices.  They help raise awareness and reminder people of important considerations.  Organizations may have style guides for specific purposes, such as coding, marketing, instructional design, and other business areas.

However, it can be hard to find what one needs in a style guide, particularly when that guide doesn't have search functionality.  The time spent looking through contents, indexes, and individual pages can take one "out of the zone".  

RAG-nificient Styles helps make the specialized knowledge within style guides easily accessible to their audience by providing quick, relevant answers.


## Getting Started

### Preparation
You will need to prepare some accounts to make full use of this project.  This system uses a postgresl database, such as [Supabase](https://supabase.com/), to log message interactions and user ratings. Add the database url to the .env file.  Note that SQLAlchemy necessitates using "postgresql" instead of just "postgres".

[Langfuse](https://langfuse.com) is used for observability.  Create an account there.  Make a project.  Then, add the public key, secret key, and host url to your .env file.

The .env-copy file shows the values your .env file needs.

For `GENERATIVE_MODEL_NAME`, you can choose one of [the models Ollama offers](https://ollama.com/library) that best fits within your system resources.  `qwen2:0.5b` is a small model that is useful for testing.

Additionally, you can choose one or more style guides for the RAG system to draw from.  [Google Style Guides](https://github.com/google/styleguide) offer guides for different programming languages.  This project tested with the `pyguide.md`.  Put your selected guide(s) in `data/style`.

### Start up: Using Docker Compose
Ensure you have [Docker installed on your computer](https://docs.docker.com/engine/install/).

Build the images first.
```shell
docker compose build --no-cache
```

Then, start the services.
```shell
docker compose up
```

Four separate services will start up.  The API (`rag_api`) should be last.  Once you see the following in your terminal, the initial service set up should be finished.
```
rag_api        | INFO:     Started server process [1]
rag_api        | INFO:     Waiting for application startup.
rag_api        | INFO:     Application startup complete.
rag_api        | INFO:     Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)
```

To use the RAG service, you will need to add a style guide to the `data/style` folder.  You can add one or more files to this folder.
From the project root folder, run the ingestion script.
```shell
python -m backend.utils.ingest
```

Create the models in your postgres database.
```shell
python -m backend.utils.models
```



### Start up: Using manual steps
#### Set up the environment

Create a virtual environment
```shell
python -m virtualenv .venv
```

Activate your virtual environment
```shell
# Linux
source .venv/bin/activate

# Windows
source .venv/scripts/activate
```
#### Set up the vector database and load documents
Pull the Qdrant vector database
```shell
docker pull qdrant/qdrant
```

Run the Qdrant vector database
```shell
docker run -p 6333:6333 qdrant/qdrant
```

[Install Ollama](https://ollama.com/download) to your computer.

To use the RAG service, you will need to add a style guide to the `data/style` folder.  You can add one or more files to this folder.
From the root folder, run the ingestion script.
```shell
python -m backend.utils.ingest
```

#### Set up the database
This system uses a postgresl database, such as [Supabase](https://supabase.com/), to log message interactions and user ratings. Add the database url to the .env file.  Note that SQLAlchemy necessitates using "postgresql" instead of just "postgres".
```shell
python -m backend.utils.models
```

#### Set up the API
Start the FastAPI application.
```shell
uvicorn app:app --host localhost --port 7860
```

Send a sample request to test the API.
```shell
>>> ipython
>>> import requests
>>> resp = requests.post(url="http://localhost:7860/queries", data=b'{"message": "hi"}')
>>> resp.json()
{'answer': 'The context does not provide any information about the current job, what the person is doing, or any other relevant details. Therefore, I cannot answer this question from the provided context.', 'query_id': 1}
```

#### Set up the frontend
Start the Streamlit application
```shell
streamlit run app.py
```


## Folder Structure
```bash
├── backend
│   ├── utils # Folder of RAG support functions
│       ├── ingest.py # Reads files, processes content, and creates index
│       ├── message_logging.py # Logs messages and feedback to postgres database
│       ├── models.py # Database schema
│       ├── prompts.py # Library of custom prompts
│       ├── query.py # Build the query_engine for answering user's query
│   ├── constants.py # The file that contains configuration variables
│   ├── main.py # The core API file with FastAPI and endpoints
│   ├── requirements.txt # Backend dependencies
│   ├── schemas.py # The models for the request and response objects
│   data # Folder of test data
│   ├── style # Folder of style guides
│   ├── testsets # Manual and LLM created evaluation datasets
├── experiments # Folder of notebooks and scripts for testing RAG strategies
├── frontend
│   ├── app.py # A minimal Streamlit chat interface
│   ├── requirements.txt # Frontend dependencies
├── app.py # The main file where endpoint reside
├── .env-copy # An example of the ENV variables you should set
├── requirements.txt # Package dependencies for the project
├── compose.yaml # Start all components via Docker
```





## Resources


* [Local Qdrant Setup](https://qdrant.tech/documentation/quickstart/#)
* [LlamaIndex-Qdrant](https://qdrant.tech/documentation/frameworks/llama-index/)
## Sales App
#### _a test assignment_

This is a simple FastAPI project with a single endpoint, showcasing industry practices and SOLID test driven design.

This readme contains instructions for *development* and *testing*.

### Prerequisites

#### Invoke
Invoke is a simple CLI tool, used throughout the project
to automate tasks like finding todo comments, running the server, veryfing code etc.
More info can be found on their page: https://www.pyinvoke.org/ .

Install via pip: `pip install invoke`

#### Poetry

Poetry is a Python packaging and dependency management tool.
More info can be found on their page: https://python-poetry.org/ .

Install via pip: `pip install poetry`


### Development

1. Insert the sales_data.csv file into the main root of the project. Make sure the file is well formated and not empty.
2. Run `poetry shell`.
3. Run `poetry install` to install dependencies.
4. Run `invoke server`.
5. Access `127.0.0.1:8080/` in the browser to access index and use the `/docs` endpoint for API docs.
6. Running the local build (OPTIONAL): in order to test out changes locally before
   pushing, always run `invoke build-local`.

### Testing

In order for testing to work you will need docker installed.
https://docs.docker.com/desktop/

1. Run `docker compose up` to create an docker-compose environment.
2. Access docs on `http://0.0.0.0:8080/docs`


### Troubleshooting

- **Error: 'docker compose' command not found**  
  Make sure Docker is installed and the Docker service is running on your machine.

- **Error: 'poetry' command not found**  
  Ensure Poetry is installed globally or within your virtual environment. You can check if it's installed by running `poetry --version`.



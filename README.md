## Sales App
#### _a test assignment_

This is a simple FastAPI project with a single endpoint, showcasing industry practices and SOLID design.

This readme contains instructions for *development* and *testing*.

### Prerequisites

#### Invoke
Invoke is a simple CLI tool, used throughout the project. 
More info can be found on their page: https://www.pyinvoke.org/ .

Install via pip: `pip install invoke`

#### Poetry

Poetry is a Python packaging and dependency management tool.
More info can be found on their page: https://python-poetry.org/ .

Install via pip: `pip install poetry`


### Development

1. Insert the sales_data.csv file into the main root of the project.
2. Run `poetry shell`.
3. Run `invoke server`.
4. Access `127.0.0.1:8080/docs` in the browser to view documentation.
5. Running the local build (OPTIONAL), in order to test out changes locally before
   pushing, always run `invoke build-local`.

## Testing

In order for testing to work you will need docker installed.
https://docs.docker.com/desktop/

1. Run `invoke buildup` to create an docker-compose environment.
2. Access docs on `http://0.0.0.0:8080/docs`


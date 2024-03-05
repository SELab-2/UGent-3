# Project pigeonhole backend
## Prerequisites
If you want the development environment run both commands if you only need to deploy only run the Deploment command.

The dev-requirements.txt contains everything for writing tests and linters for maintaining quality code.
On the other hand the regular requirements.txt install the packages needed for 
the regular base application.

- Deployment
```sh
  pip install -r requirments.txt
```
- Development
```sh
  pip install -r dev-requirments.txt
```

## Installation
1. Clone the repo
   ```sh
   git clone git@github.com:SELab-2/UGent-3.git
   ```
2. If you want to development run both commands, if you want to deploy only run deployment command.
   - Deployment
   ```sh
   pip install -r requirments.txt
   ```
   - Development
   ```sh
   pip install -r dev-requirments.txt
   ``` 

## Setting up the environment variables
The project requires a couple of environment variables to run,
these should be located in your own .env file if you want to develop on this codebase.

| Variable          | Description                                                    |
|-------------------|----------------------------------------------------------------|
| DB_HOST           | Url of where the database is located                           |
| POSTGRES_USER     | Name of the user, needed to login to the postgres database     |
| POSTGRES_PASSWORD | Password of the user, needed to login to the postgres database |
| POSTGRES_HOST     | IP adress of the postgres database                             |
| POSTGRES_DB       | Name of the postgres database                                  |
| API_HOST          | Location of the API root                                       |

All the variables except the last one are for the database setup,
these are needed or else you can't make a valid connection.
The last one is for keeping the API restfull since the location of the recourse should be located.

## Running the project
Once all the setup is done you can start the development server by
navigating to the backend directory and running:
```sh
python project
``` 
The server should now be located at localhost:5000 and you can
start developping.

## Maintaining the codebase
### Writing tests
When writing new code it is important to maintain the right functionality so 
writing tests is mandatory for this, the test library used in this codebase is pytest.

- pytest documentation: https://docs.pytest.org/en/8.0.x/

If you want to write tests we highly advise to read the pytest documentation on how
to write tests, so they are kept conventional.

For executing the tests and testing you're newly added functionality (and to test if you broke nothing from earlier working code)
you can run:
```sh
sudo ./run_tests.sh
``` 

Located in the backend directory.
### Running the linter
This codebase is kept by the pylint linter.
- pylint docutmentation: https://pypi.org/project/pylint/

If you want to execute the linter on all .py files in the project it can simply be done
with the command:
```sh
find . -type f -name "*.py" | xargs pylint
``` 
The code needs to get a 10/10 score to get pushed to the repository.

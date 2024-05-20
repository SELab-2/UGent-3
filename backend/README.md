# Project pigeonhole backend
![tests](https://github.com/SELab-2/UGent-3/actions/workflows/ci-test-backend.yaml/badge.svg)
![linter](https://github.com/SELab-2/UGent-3/actions/workflows/ci-linter-backend.yaml/badge.svg)
## Prerequisites
**1. Clone the repo**
   ```sh
   git clone git@github.com:SELab-2/UGent-3.git
   ```
**2. Installing required packages**

   If you want the development environment: run both commands. If you only need to deploy, run the deployment command.

   The [dev-requirements.txt](dev-requirements.txt) contains everything for writing tests and linters for maintaining quality code.
On the other hand the regular [requirements.txt](requirements.txt) installs the packages needed for 
the regular base application.

   - Deployment
   ```sh
   pip install -r requirements.txt
   ```
   - Development
   ```sh
   pip install -r dev-requirements.txt
   ```

## Setting up the environment variables
The project requires a couple of environment variables to run, if you want to develop on this codebase.
Setting values for these variables can be done with a method to your own liking.

| Variable                               | Description                                                                                                                                                                                                                                                                                                                       |
|----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POSTGRES_USER                          | Name of the user, needed to login to the postgres database                                                                                                                                                                                                                                                                        |
| POSTGRES_PASSWORD                      | Password of the user, needed to login to the postgres database                                                                                                                                                                                                                                                                    |
| POSTGRES_HOST                          | Location of the postgres database                                                                                                                                                                                                                                                                                                 |
| POSTGRES_DB                            | Name of the postgres database                                                                                                                                                                                                                                                                                                     |
| API_HOST                               | Location of the API root                                                                                                                                                                                                                                                                                                          |
| CLIENT_ID                              | [Client id](https://learn.microsoft.com/nl-nl/entra/identity-platform/v2-protocols)                                                                                                                                                                                                                                               |
| CLIENT_SECRET                          | Client's secret is your personal secret key for authentication, this can be found at the [Entra ID admin center](https://entra.microsoft.com/)                                                                                                                                                                                                                |
| JWT_SECRET_KEY                         | JWT secret key is the key used to encode the JWT's and should be kept secret, because otherwise everyone can create "valid" JWT's for our application. Variable should be a random 32 characters long string, if you need more information please refer to the [RDF documentation](https://www.rfc-editor.org/rfc/rfc4868#page-3) |                       
| TENANT_ID                              | [Tenant id](https://learn.microsoft.com/nl-nl/entra/fundamentals/whatis), an ID that is used to identify yourself to the microsoft servic                                                                                                                                                                                         |                     
| HOMEPAGE_URL                           | URL of where the website's homepage is located                                                                                                                                                                                                                                                                                    |

All the variables except the last one are for the database setup,
these are needed to make a connection with the database.
The last one is for keeping the API restful since the location of the resource should be located.

## Running the project
Once all the setup is done you can start the development server by
navigating to the backend directory and running:
```sh
python project
``` 
The server should now be located at `localhost:5000` and you can
start developing.

## Maintaining the codebase
### Writing tests
When writing new code it is important to maintain the right functionality so 
writing tests is mandatory for this, the test library used in this codebase is [pytest](https://docs.pytest.org/en/8.0.x/).

If you want to write tests we highly advise to read the pytest documentation on how
to write tests, so they are kept conventional.

For executing the tests and testing your newly added functionality
you can run:
```sh
sudo ./run_tests.sh
``` 

Located in the backend directory.
### Running the linter
This codebase is kept clean by the [pylint](https://pypi.org/project/pylint/) linter.

If you want to execute the linter on all .py files in the project it can simply be done
with the command:
```sh
find . -type f -name "*.py" | xargs pylint
``` 
The code needs to get a 10/10 score to get pushed to the repository.

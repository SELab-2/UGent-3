# Project pigeonhole frontend
![tests](https://github.com/SELab-2/UGent-3/actions/workflows/ci-test-frontend.yaml/badge.svg?branch=development)
![linter](https://github.com/SELab-2/UGent-3/actions/workflows/ci-linter-frontend.yaml/badge.svg?branch=development)
## Prerequisites
**1. Clone the repo**
   ```sh
   git clone git@github.com:SELab-2/UGent-3.git
   ```

**2. Installing required packages**
Run the command below to install the needed dependencies.
   ```sh
   cd frontend
  npm install
   ```
After this you can run the development or the production build with one of the following command
  - Deployment
  ```sh
   npm run build
   ```
After running this command the build can be found in the `dist` directory.
You can choose your own preferred webserver like for example `nginx`, `serve` or something else.
  
  - Development
   ```sh
   npm run dev
   ```

## Maintaining the codebase
### Writing tests
When writing new code it is important to maintain the right functionality so 
writing tests is mandatory for this, the test library used in this codebase is [cypres e2e](https://www.cypress.io/).

If you want to write tests we highly advise to read the cypres e2e documentation on how
to write tests, so they are kept conventional.

For executing the tests and testing your newly added functionality
you can run:
```sh
npm run dev
``` 
After the development build is running, you can run the following command on another terminal:
```sh
npm run test
``` 
### Running the linter
This codebase is kept clean by the [eslint](https://eslint.org) linter.

If you want to execute the linter on all files in the project it can simply be done
with the command:
```sh
npm run lint
``` 


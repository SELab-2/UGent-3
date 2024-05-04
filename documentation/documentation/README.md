# UGent-3 project peristerónas user guide

## Introduction
Project peristerónas has a lot of features, therefor a detailed user guide is available to consult.

## Usage
### Development
If you want to develop on the site, run the following command:
  ```sh
   npm run start
   ```
This creates a lightweight version of the site, if you want to test a certain language version of the site you can use the command:
  ```sh
    npm run start -- --locale [language]
  ```

  ### Deployment
  When you're ready to deploy run the following command to run the proper version of the site:
  ```sh
  npm run build
  ```

  A static version will be build that you can acces in the directory `build/`, you can then run the static site by using the command:

  ```sh
  npm run serve
  ```

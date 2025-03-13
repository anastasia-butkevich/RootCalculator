# Numeric Polynomial Root Calculator

## Overview
The Numeric Polynomial Root Calculator is a Django-based application designed to compute the roots of polynomial equations using numerical methods such as bisection and Newton's method. Additionally, the app integrates with the public Desmos API to visually plot the polynomial functions. The app includes four endpoints: an index route `/`, `manual/`, `from_db/`, and `results/`. 

## Features
- **Numerical Root-Finding:** Utilizes bisection and Newton's methods.
- **Desmos Integration:** Plots functions using the Desmos API.
- **Multiple Endpoints:** Supports both database-driven and manual inputs.
- **UI:** Styled using Bootstrap.
- **Django Framework:** Ensures scalability and maintainability.

## Endpoints

### 1. Index (GET) 
- **Route:** `/`
- **Purpose:** Serves as a main page, providing a menu for navigating other endpoints. 
### 2. From Database (GET)
- **Route:** `/from_db/`
- **Purpose:** Retrieves polynomial data from the database and displays previously computed results. 
### 3. Manual Input (POST)
- **Route:** `/manual/`
- **Purpose:** Accepts manual input of polynomial equations for root calculations and saves the data into a database to be able to get precalculated data and display them.
### 4. Results (GET)
- **Route:** `/results/`
- **Purpose:** Displays the computed results, including any plots generated via the Desmos API.

## Environment Variables
Before running the application, ensure you create a .env file in the project's root directory. This file should include the following variables:

- `SECRET_KEY:` A unique Django secret key (required for security).
- `DEBUG:` Set to True or False (required to control debug mode).
- `DATABASE_ENGINE:` The engine for your database (e.g., django.db.backends.sqlite3).
- `DATABASE_NAME:` The name of your database.  
  
> **Important:** The application will not work without these environment variables, especially without a valid `SECRET_KEY`.

## Installation
To install and run the application using Docker, follow the steps below:  
**1. Clone the repository:**  
Firstly, navigate to the target directory using `cd` where you want to store the repository. Then run `git clone`:
``` 
git clone <repository-url>
cd <repository-folder>
```
**2. Create the `.env` file:**  
Create a `.env` file in the project's root directory and add the necessary variables:
```
SECRET_KEY=your_django_secret_key
DEBUG=True  # or False, depending on your environment
DATABASE_ENGINE=django.db.backends.sqlite3  # or your preferred engine
DATABASE_NAME=your_database_name
```
**3. Build the Docker Image:**  
In the terminal, from the repository's root directory, run:
```
docker buildx build -t rootcalc -f docker/Dockerfile .
```
**3. Run the Docker Container**  
Start the container:
```
docker run -p 8000:8000 rootcalc
```
Or, to specify .env file, run (assuming .env is present):
```
docker run --env-file .env -p 8000:8000 chat_app
```
**4. Access the Application:**  
After running the container, you can access the application by navigating to `http://localhost:8000` in your web browser.

**5. Stopping the Application:**  
Stop the container by running:
```
docker stop <container-id>
```
To find container id you can either run:
```
docker ps 
```
or look it up in Docker desktop.
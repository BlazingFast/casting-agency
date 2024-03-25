The Casting Agency
-----

## Introduction

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.


## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack includes the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework

## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. It includes the REST API endpoints
  ├── models.py *** Includes your SQLAlchemy models.
  ├── config.py *** Database URLs & JWT Tokens (fetched from environment variables), App Configs etc
  ├── error.log
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── render.yml *** The blueprint for Render deployment
  ├── test_app.py *** Contains the test cases
  ├── enums.py *** Contains the enums required by the application
  ├── auth.py *** Contains the logic for auth required by the application

  
  ```

Overall:
* Models are located in the `MODELS` section of `models.py`.
* Controllers are located in `app.py`.
* Authentication & Authorization logic is located in `auth.py`
* Application configuration is located in `config.py`


## Development Setup
1. **Download the project starter code locally**
```
git clone https://github.com/BlazingFast/casting-agency
cd casting-agency
```

2. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

3. **Install the dependencies:**
```
pip3 install -r requirements.txt
```

4. **Run the development server:**
```
export FLASK_APP=app
export FLASK_ENV=development # enables debug mode
python3 app.py
```

5. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

## Endpoints:

```python
GET /actors & /movies & /actors/<int:id> & /movies/<int:id>

DELETE /actors/<int:id> & /movies/<int:id>

POST /actors/create & /movies/create & /actors/search & /movies/search

PATCH /actors/<int:id>/edit & /movies/<int:id>/edit
```

All below Endpoints have been created, please refer `app.py` file.

## Auth0 Setup:

**AUTH0_DOMAIN**, **ALGORITHMS** and **API_AUDIENCE** are all available in the `auth.py` file for reference.
Json Web Tokens: You can find **JWTs** for each role and **DATABASE_URI** in the `.env` file to run the app locally.
To run the app locally, you can set the environment variables in the .env file

**Roles**: All 3 roles have been defined in Auth0 and following permissions as shown for each role below are also defined in Auth0.

- **Casting Assistant** \* get:actors and get:movies
- **Casting Director**
  _ All permissions a Casting Assistant has and
  _ post:actors and delete:actors \* patch:actors and patch:movies
- **Executive Producer**
  _ All permissions a Casting Director has and
  _ post:movies and delete:movies

## Deployment Details:

- Click [here](https://casting-agency-nlmg.onrender.com/) to access the app deployed to Render.
- URL: https://casting-agency-nlmg.onrender.com/


## Testing:

- We can import the postman collection - **casting-agency.postman_collection.json** in Postman to test the remote app.

- For testing locally, we need to update the `config.py` file with values from `.env` file which contains JWTs and Database URL.
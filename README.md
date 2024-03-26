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
  ├── README.md *** Contains the project documentation
  ├── app.py *** the main driver of the app. It includes the controllers and error handling logic
  ├── models.py *** Includes your SQLAlchemy models
  ├── forms.py *** Includes the forms and validation
  ├── config.py *** Fetches App Configuration properties like Database URLs and JWT Tokens
  ├── setup.sh *** Setup file for quick setup of the environment related variables such as Auth0, Database URL and JWT Tokens
  ├── .env *** Same as setup.sh. Just different in the way that it is used for Render deployment
  ├── error.log *** Contains error stack traces of the running application
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── render.yml *** The blueprint for Render deployment
  ├── test_app.py *** Contains the test cases
  ├── enums.py *** Contains the enums required by the application
  ├── auth.py *** Contains the logic for auth required by the application
  ├── test_app.py *** Contains the application unit tests

  ```


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


## Auth0 Setup:

### Auth0 Setup

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:movies`
   - `get:actors`
   - `post:movies`
   - `post:actors`
   - `patch:movies`
   - `patch:actors`
   - `delete:movies`
   - `delete:actors`


**AUTH0_DOMAIN**, **ALGORITHMS** and **API_AUDIENCE** are all available in the `auth.py` file for reference.
Json Web Tokens: You can find **JWTs** for each role and **DATABASE_URI** in the `.env` file to run the app locally.
To run the app locally, you can set the environment variables in the .env file

**Roles**: All 3 roles have been defined in Auth0 and following permissions as shown for each role below are also defined in Auth0.

- **Casting Assistant**
  - get:actors
  - get:movies
- **Casting Director**
  _ All permissions a Casting Assistant has and
  - post:actors
  - delete:actors
  - patch:actors
  - patch:movies
- **Executive Producer**
  _ All permissions a Casting Director has and
  - post:movies
  - delete:movies

## Deployment Details:

- Click [here](https://casting-agency-nlmg.onrender.com/) to access the app deployed to Render.
- URL: https://casting-agency-nlmg.onrender.com/


## API Reference

### Endpoints


`GET '/'`

- Root endpoint
- Request Arguments: None
- Role: Public endpoint
- Response Body: `The Casting Agency is up and running!!`

  Example response:

  ```json
  `The Casting Agency is up and running!!`
  ```


`GET '/movies'`

- Fetches all the movies present in the database.
- Request Arguments: None
- Role: Casting Assistant, Casting Director or Executive Producer
- Response Body: 
  - `movies`: `<JSON Array>` An object containing a list of movies with - id, title and release_date.
  - `movies_count`: `<Integer>` Count of total movies
  - `success`: `<Boolean>` Status of the request

  Example response:

  ```json
  {
    "movies": [
        {
            "id": 2,
            "name": "New Movie",
            "release_date": "Sun, 24 Mar 2024 00:00:00 GMT"
        },
        {
            "id": 3,
            "name": "New Movie",
            "release_date": "Sun, 24 Mar 2024 00:00:00 GMT"
        },
        {
            "id": 4,
            "name": "New Movie",
            "release_date": "Sun, 24 Mar 2024 00:00:00 GMT"
        },
    ],
    "movies_count": 3,
    "success": true
  }
  ```

`GET '/actors'`

- Fetches all the actors present in the database.
- Request Arguments: None
- Role: Casting Assistant, Casting Director or Executive Producer
- Response Body: 
  - `actors`: `<JSON Array>` An object containing a list of movies with - id, name, gender and age.
  - `actors_count`: `<Integer>` Count of total actors
  - `success`: `<Boolean>` Status of the request

  Example response:

  ```json
  {
    "actors": [
        {
            "age": 34,
            "gender": "MALE",
            "id": 2,
            "name": "Actor 1"
        },
        {
            "age": 24,
            "gender": "MALE",
            "id": 3,
            "name": "Actor 2"
        },
        {
            "age": 45,
            "gender": "MALE",
            "id": 4,
            "name": "Actor 3"
        }
    ],
    "actors_count": 3,
    "success": true
  }
  ```

`GET '/movies/<int:movie_id>'`

- Get Movie by ID.
- Request Arguments: None
- Role: Casting Assistant, Casting Director or Executive Producer
- Response Body: 
  - `movie`: `<JSON Object>` An object containing actor object with - id, name and release_date.

  Example response:

  ```json
  {
    "movie": {
        "id": 2,
        "name": "New Movie",
        "release_date": "Sun, 24 Mar 2024 00:00:00 GMT"
    }
  }
  ```

`GET '/actors/<int:actor_id>'`

- Get Actor by ID.
- Request Arguments: None
- Role: Casting Assistant, Casting Director or Executive Producer
- Response Body: 
  - `actor`: `<JSON Object>` An object containing actor object with - id, name, gender and age.

  Example response:

  ```json
  {
    "actor": {
        "age": 34,
        "gender": "MALE",
        "id": 2,
        "name": "New Actor"
    }
  }
  ```

`POST '/movies/create'`

- Creates a new movie with the required details sent in the body.
- Role: Executive Producer
- Request Body: 
  - `name`: `<String>` Movie title
  - `release_date`: `<Date>` Movie Release date

  Example request:

  ```json
  {
    "name": "New Movie",
    "release_date": "2024-03-24 21:37:56"
  }
  ```

- Response Body: 

  - `created`: `<Integer>` Movie id of new movie
  - `success`: `<Boolean>` Status of request

Example response:

  ```json
  {
    "created": 10,
    "success": true
  }
  ```

`POST '/movies/search'`

- Searches for a search string in all movies names and returns movies with matching results.
- Role: Casting Assistant, Casting Director or Executive Producer
- Request Body: 
  - `search_term`: `<String>` Text to be searched in all movies names

Example request:

  ```json
  {
    "search_term": "movie"
  }
  ```

- Response Body: 

  - `data`: `<Array>` JSON array of movies.
  - `count`: `<Integer>` Count of movies matching search criteria

Example response:

  ```json
  {
    "count": 3,
    "data": [
        {
            "id": 2,
            "name": "New Movie",
            "release_date": "Sun, 24 Mar 2024 00:00:00 GMT"
        },
        {
            "id": 3,
            "name": "New Movie",
            "release_date": "Sun, 24 Mar 2024 00:00:00 GMT"
        },
        {
            "id": 4,
            "name": "New Movie",
            "release_date": "Sun, 24 Mar 2024 00:00:00 GMT"
        }
    ]
}
  ```


`POST '/actors/create'`

- Creates a new actor with the required details sent in the body.
- Role: Casting Director or Executive Producer
- Request Body: 
  - `name`: `<String>` Actor name
  - `age`: `<Integer>` Actor age
  - `gender`: `<Integer>` Actor gender

  Example request:

  ```json
  {
    "name": "New Actor",
    "age": 56,
    "gender": "MALE",
  }
  ```

- Response Body: 

  - `created`: `<Integer>` Actor id of new Actor
  - `success`: `<Boolean>` Status of request

Example response:

  ```json
  {
    "created": 10,
    "success": true
  }
  ```

`POST '/actors/search'`

- Searches for a search string in all actors names and returns actors with matching results.
- Role: Casting Assistant, Casting Director or Executive Producer
- Request Body: 
  - `search_term`: `<String>` Text to be searched in all actors names

Example request:

  ```json
  {
    "search_term": "actor"
  }
  ```

- Response Body: 

  - `data`: `<Array>` JSON array of actors.
  - `count`: `<Integer>` Count of actors matching search criteria

Example response:

  ```json
  {
    "count": 2,
    "data": [
        {
            "age": 34,
            "gender": "MALE",
            "id": 2,
            "name": "New Actor"
        },
        {
            "age": 34,
            "gender": "MALE",
            "id": 3,
            "name": "New Actor"
        }
    ]
  }
  ```


`PATCH '/actors/<int:actor_id>/edit'`

- Update Actor by ID.
- Request Arguments: None
- Role: Casting Director or Executive Producer
- Request Body: 
  - `name`: `<String>` Actor name
  - `age`: `<Integer>` Actor age
  - `gender`: `<String>` Actor gender

  Example request:

  ```json
  {
    "name": "New Actor Modified",
    "age": 56,
    "gender": "MALE",
  }
  ```

  Example response:

  ```json
  {
    "actor": {
        "age": 34,
        "gender": "MALE",
        "id": 2,
        "name": "New Actor modified"
    }
  }
  ```


`PATCH '/movies/<int:movie_id>/edit'`

- Update Movie by ID.
- Request Arguments: None
- Role: Casting Director or Executive Producer
- Response Body: 
  - `movie`: `<JSON Object>` JSON Object containing Movie id, name/title and release_date
  - `success`: `<Date>` Status of the request

  Example request:

  ```json
  {
    "name": "New Movie modified",
    "release_date": "2024-06-30 21:37:56"
  }
  ```

  Example response:

  ```json
  {
    "movie": {
        "id": 2,
        "name": "New Movie modified",
        "release_date": "Sun, 30 Jun 2024 00:00:00 GMT"
    },
    "success": true
  }
  ```


`DELETE '/movies/<int:movie_id>'`

- Delete a movie with given `movie_id`
- Request Arguments: Path parameter - `movie_id` of type integer.
- Role: Executive Producer
- Response Body: 
  - `deleted`: `< Integer>` Movie id of deleted movie
  - `success`: `<Boolean>` Status of request

  Example response:

  ```json
  {
    "deleted": 4,
    "success": true
  }
  ```

`DELETE '/actors/<int:actor_id>'`

- Delete a actor with given `actor_id`
- Request Arguments: Path parameter - `actor_id` of type integer.
- Role: Casting Director or Executive Producer
- Response Body: 
  - `deleted`: `< Integer>` Actor id of deleted actor
  - `success`: `<Boolean>` Status of request

  Example response:

  ```json
  {
    "deleted": 4,
    "success": true
  }
  ```


### Error Handling

  - 404: 'Not Found'
  - 401: 'unauthorized'
  - 422: 'unprocessible'
  - 500: 'Something went wrong'


## Testing:

- We can import the postman collection - **casting-agency.postman_collection.json** in Postman to test the remote app.

- For testing locally, we can use the `setup.sh` which contains Auth0 configuration, JWTs and Database URL.
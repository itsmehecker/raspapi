# Documentation for avavado's game
-- Total 2 POST & 14 GET

## Endpoints

### Get API Key

- **Endpoint:** `/get-api-key`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "name": "your_name"
    }
    ```
- **Response:**
    ```json
    {
      "api_key": "generated_api_key"
    }
    ```
### Update Level

- **Endpoint:** `/update-level`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "api_key": "your_api_key",
      "level": 2
    }
    ```

### Get Level

- **Endpoint:** `/level`
- **Method:** `GET`
- **Query Parameter:** `api_key`
- **Response:**
    ```json
    {
      "level": 1
    }
    ```


### Root

- **Endpoint:** `/`
- **Method:** `GET`
- **Query Parameter:** `api_key`, `choice`
- **Response:**
    ```json
    {
      "message": "You are a fresh avocado now that you have been checked by the store keeper.",
      "stage": "You've been accused of salt by a flower you once hooked up with. She thinks you made her gain weight.",
      "choices": {
        "1": "Fight the accusation in court.",
        "2": "Flee the country."
      }
    }
    ```

### Mexico

- **Endpoint:** `/mexico`
- **Method:** `GET`
- **Query Parameter:** `api_key`, `choice`
- **Response:**
    ```json
    {
      "choices": {
        1: "Sell fertilizers to kids",
        2: "Become a shopkeeper's show item"
      }
    }
    ```

### Jail

- **Endpoint:** `/jail`
- **Method:** `GET`
- **Query Parameter:** `api_key`
- **Response:**
    ```json
    {
      "message": "You see some rotten veggies in the jail cell. They seem to be looking at you and saying something.",
      "level": 4,
      "mission": "go to /rotten_veggies?apikey=YOURAPIKEY"
    }
    ```

### Rotten Veggies

- **Endpoint:** `/rotten_veggies`
- **Method:** `GET`
- **Query Parameter:** `api_key`, `choice`
- **Response:**
    ```json
    {
      "message": "they tell you to do something for them",
      "choices": {
        1: "do what they say",
        2: "dont do what they say"
      }
    }
    ```

### Do What They Say

- **Endpoint:** `/do_what_they_say`
- **Method:** `GET`
- **Query Parameter:** `api_key`
- **Response:**
    ```json
    {
      "message": "they tell you to smuggle some synthetic fertilizer in",
      "TO DO:": "do a POST req to /smuggle_fertilizer with an argument of this famous riddle",
      "riddle": "Guac is my fame, but what is my name?",
      "instruction": "go to terminal and type curl -X POST http://127.0.0.1:8000/smuggle_fertilizer -H \"Content-Type: application/json\" -d '{\"answer\": \"avocado\"}'"
    }
    ```

### The Mafia Gets Her Killed

- **Endpoint:** `/the_mafia_gets_her_killed`
- **Method:** `GET`
- **Query Parameter:** `api_key`
- **Response:**
    ```json
    {
      "message": "you see the flower's sister and immediately flirt with her and she flirts back and asks you to come to her place",
      "level": 5,
      "mission": "go to /enjoy_hybridisation_with_the_flowers_sister"
    }
    ```

### Jury Flower

- **Endpoint:** `/jury_flower`
- **Method:** `GET`
- **Query Parameter:** `api_key`
- **Response:**
    ```json
    {
      "message": "you go to jail no matter due to the speciest laws",
      "waitaminute": "The guard comes in and tells you someone bailed you out",
      "level": 2,
      "mission": "go to /bailout_j to meet the person who bailed you out"
    }
    ```

### Enjoy Hybridisation With The Flower's Sister

- **Endpoint:** `/enjoy_hybridisation_with_the_flowers_sister`
- **Method:** `GET`
- **Query Parameter:** `api_key`
- **Response:**
    ```json
    {
      "message": "The mafia was her (the flower) she killed you and cut you and also threw your seed in the fire",
      "level": 6
    }
    ```

### Bailout J

- **Endpoint:** `/bailout_j`
- **Method:** `GET`
- **Query Parameter:** `api_key`
- **Response:**
    ```json
    {
      "message": "Jonhny Pepp (pepper) bails you out and tells you he can help you fight the flower with the help of his lawyer",
      "test": "to test you he puts a jar of powdered sugar on the table",
      "level": 2,
      "mission": "go to /do_a_jar_of_powdered_sugar or to /dont_do_the_jar_of_powdered_sugar"
    }
    ```

### Do A Jar Of Powdered Sugar

- **Endpoint:** `/do_a_jar_of_powdered_sugar`
- **Method:** `GET`
- **Query Parameter:** `api_key`
- **Response:**
    ```json
    {
      "message": "you're cool you get to fight the flower the false accusation has been dealt with",
      "vision": "JOHNNY DEPP tells you be proud of who you are you know what you would do and not do but sometimes you gotta prove it to some rich and nasty people. Believe in yourself",
      "status": "Game Over (ik its a lame game)",
      "level": 1,
      "reset": "game has been reset try going to /"
    }
    ```

### Don't Do The Jar Of Powdered Sugar

- **Endpoint:** `/dont_do_the_jar_of_powdered_sugar`
- **Method:** `GET`
- **Query Parameter:** `api_key`
- **Response:**
    ```json
   
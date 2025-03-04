## Avacado 
Story of game: Avocado is on a journey to legally fight in court because a Flower charged him with assault falsely and for making her gain weight.

A game made inside an API.
its a choice based game and the outcomes are manually made by me so it's a short and random game
might actually make this a game without the choices part in unity as my first game(wait for that)

It's choice-based and short. It utilizes GET and POST protocols and also uses PostgreSQL to store your API keys and progress. It uses `secrets` to give you a secure generation of your API key and tracks your progress using the API key.

## How to Use
use your terminal or your browser (you need to use the terminal atleast once to get the api key)
### Prerequisites

- Python 3.13
- PostgreSQL
- `pip` (Python package installer)

### Installation

1. Clone the repository:
```bash
   git clone https://github.com/itsmehecker/raspapi.git
   cd raspapi
```
Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate
```
3.Install the required packages
```bash
pip install wheel
pip install --upgrade setuptools pip
pip install -r requirements.txt
```
4.Create .env file so your db is secure
```
DATABASE_URL=postgresql://username:pass@host
```

5.Running The Application
```bash
uvicorn main:app --reload
```
The API will be available at http://127.0.0.1:8000.


## API Endpoints (ONLY A FEW ARE NOTED HERE)
Get API Key

- Endpoint: /get-api-key
- Method: POST
- Request Body:
```json
{
  "name": "your_name"
}
```
- Response:
```json
{
  "api_key": "generated_api_key"
}
```
Get Level
- Endpoint: /level
- Method: GET
- Query Parameter: api_key
- Response:
```json
{
  "level": 1
}
```
Use choices
```json
curl -X GET "http://127.0.0.1:8000/?api_key=your_generated_api_key"
```
Update Level
Endpoint: /update-level
Method: POST
Request Body:
```json
{
  "api_key": "your_api_key",
  "level": 2
}
```

## Example curl Commands
Get API Key:
```bash
curl -X POST "http://127.0.0.1:8000/get-api-key" -H "Content-Type: application/json" -d '{"name": "your_name"}'
```
Get Level:
```bash
curl -X GET "http://127.0.0.1:8000/level?api_key=your_api_key"
```
curl -X POST "http://127.0.0.1:8000/update-level" -H "Content-Type: application/json" -d '{"api_key": "your_api_key", "level": 2}'

Replace your_name and your_api_key with the appropriate values.
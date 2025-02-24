cd raspapi
python -m venv .venv
source .venv/bin/activate
pip install wheel
pip install --upgrade setuptools pip
pip install -r requirements.txt
touch .env
nano .env
uvicorn main:app --reload

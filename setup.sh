VIRTUAL_ENV=".env_fuzzy"
if [ -d "$VIRTUAL_ENV" ]; then
  source "$VIRTUAL_ENV/bin/activate"
else
  python3 -m venv $VIRTUAL_ENV
  source "$VIRTUAL_ENV/bin/activate"
  pip install -r requirements/requirements.txt
fi

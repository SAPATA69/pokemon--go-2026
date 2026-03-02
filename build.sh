#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python -c "
from main import app
from pokemon.extensions import db
with app.app_context():
    db.create_all()
    print('Tables created successfully!')
"
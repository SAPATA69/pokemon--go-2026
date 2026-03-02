#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python -c "
import os
print('DATABASE_URL =', os.environ.get('DATABASE_URL', 'NOT FOUND'))
"
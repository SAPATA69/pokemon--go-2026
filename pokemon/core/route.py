from flask import Blueprint, render_template, request
from pokemon.extensions import db
from pokemon.models import Pokemon, Type

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
  page = request.args.get('page', type=int)
  pokemons = db.paginate(db.select(Pokemon), per_page=4, page=page)
  return render_template('core/index.html',
                         title='Home Page',
                         pokemons=pokemons)
from flask import Blueprint, render_template, request
from pokemon.extensions import db
from pokemon.models import Pokemon, Type

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
  page = request.args.get('page')
  pokemons = db.paginate(db.select(Pokemon), per_page=4, page=page)
  return render_template('core/index.html',
                         title='Home Page',
                         pokemons=pokemons)

@core_bp.route('/<int:id>/detail')
def detail(id):
  pokemon = db.session.get(Pokemon, id)
  return render_template('core/pokemon_detail.html',
                         title='Pokemon Detail Page',
                         pokemon=pokemon)
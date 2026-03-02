from flask import Blueprint, render_template, request
from pokemon.extensions import db
from pokemon.models import Pokemon, Type
import sqlalchemy as sa

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
    # แก้ไข: เพิ่ม type=int และ default=1
    page = request.args.get('page', type=int, default=1)
    pokemons = db.paginate(sa.select(Pokemon), per_page=4, page=page)
    return render_template('core/index.html',
                         title='Home Page',
                         pokemons=pokemons)

# เพิ่ม route สำหรับ detail ที่ขาดหายไป
@core_bp.route('/pokemon/<int:id>')
def detail(id):
    pokemon = db.session.get(Pokemon, id)
    if pokemon is None:
        return "ไม่พบโปเกมอนนี้", 404
    return render_template('core/pokemon_detail.html',
                         title=f'รายละเอียด {pokemon.name}',
                         pokemon=pokemon)

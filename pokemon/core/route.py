from flask import blueprints ('core',__name__,template_folder='templates'

core_bdp = blueprints('core',__name__,template_folder='templates')

@core_bdp.route('/')
 def index():
 query = db select(pokemon)
 pokemons = db
 
                                return render_template('core/index.html', title='Home')

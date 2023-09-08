from flask import  Blueprint

from scores.src.Models.model import init_db


# Crear el Blueprint para el calculo del score
scores_blueprint = Blueprint('scores', __name__)

init_db()

@scores_blueprint.route('/score', methods=['POST'])
def score_operation():
    # document why this method is empty
    pass
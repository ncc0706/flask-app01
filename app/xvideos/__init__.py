from flask import Blueprint

# template_folder 有问题, 貌似跟 __name__有关.
# xvideos = Blueprint('xvideos', __name__, template_folder=path.join('templates/xvideos'))
xvideos = Blueprint('xvideos', __name__)

from . import views, errors

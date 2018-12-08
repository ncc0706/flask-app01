from . import xvideos
from flask import render_template


@xvideos.route('/index', methods=['GET'])
def index():
    return render_template('xvideos/xindex.html')

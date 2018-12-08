from flask import Blueprint

video = Blueprint('video', __name__)


@video.route('/')
def index_video():
    return 'index video'

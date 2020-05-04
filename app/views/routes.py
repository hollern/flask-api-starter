from app.views import blueprint


@blueprint.route('/', methods=['GET'])
def index():
    return 'app entry point'

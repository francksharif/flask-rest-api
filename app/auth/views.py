from . import auth 


@auth.get('/test')
def index():
    return 'test success'
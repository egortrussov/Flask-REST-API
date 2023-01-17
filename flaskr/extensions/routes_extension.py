from ..routes import auth 
from ..routes import users 
from ..routes import orders
from ..routes import reviews

def register_blueprints(app):
    """
    Registers all blueprints in flask application 
    :return: None
    """
    app.register_blueprint(auth.bp) 
    app.register_blueprint(users.bp) 
    app.register_blueprint(orders.bp) 
    app.register_blueprint(reviews.bp)
    
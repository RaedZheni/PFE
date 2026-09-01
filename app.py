from flask import Flask
from extensions import db, login_manager
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."

    from routes.auth import auth
    from routes.employees import employees
    from routes.departments import departments
    from routes.contracts import contracts
    from routes.projects import projects
    from routes.dashboard import dashboard

    app.register_blueprint(auth)
    app.register_blueprint(employees)
    app.register_blueprint(departments)
    app.register_blueprint(contracts)
    app.register_blueprint(projects)
    app.register_blueprint(dashboard)

    with app.app_context():
        db.create_all()
        from models.user import User
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
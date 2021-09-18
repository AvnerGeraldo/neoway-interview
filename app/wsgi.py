from app import create_app

app = create_app()

with app.app_context():
    import database
    import database.redis
    import routes
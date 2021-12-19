from flask.cli import FlaskGroup
from app import app

cli = FlaskGroup(app)
# per avere client sul docker

if __name__ == "__main__":
    cli()
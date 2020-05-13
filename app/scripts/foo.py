import click

from app import app

@app.cli.command()
def historical_records():
    print 'hi'

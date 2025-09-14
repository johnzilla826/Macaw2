import click

@click.group()
def account():
    """Account commands"""

@account.command()
def setup():
    """Create an account."""
    print("account created")
import click
from macaw2.models.database import init_db


@click.group(
    help="Macaw2. A simple, reliable command-line interface for personal and small-business accounting.",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def cli():
    db = init_db()
    db.connect()
    # db.create_tables([Account])
    pass

# Commands
from macaw2.commands.account import account

cli.add_command(account)

if __name__ == "__main__":
    cli()
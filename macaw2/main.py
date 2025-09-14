import click
from macaw2.models.database import init_db, Account, Transaction, Entry


@click.group(
    help="Macaw2. A simple, reliable command-line interface for personal and small-business accounting.",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def cli():
    db = init_db()
    db.connect()
    db.create_tables([Account, Transaction, Entry], safe=True)
    pass

# Commands
from macaw2.commands.account import account
from macaw2.commands.entry import entry

cli.add_command(account)
cli.add_command(entry)

if __name__ == "__main__":
    cli()
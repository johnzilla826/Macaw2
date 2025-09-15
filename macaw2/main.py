import click
from macaw2.models.database import init_db, Account, Transaction, Entry


@click.group(
    help="\033[34mMacaw2: A simple, reliable command-line interface for personal and small-business accounting.\033[0m",
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
from macaw2.commands.reverse import reverse

cli.add_command(account)
cli.add_command(entry)
cli.add_command(reverse)

if __name__ == "__main__":
    cli()
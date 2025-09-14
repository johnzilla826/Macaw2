import click

@click.group(
    help="Macaw2. A simple, reliable command-line interface for personal and small-business accounting.",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def cli():
    pass

# Commands
from macaw2.commands.account import account

cli.add_command(account)

if __name__ == "__main__":
    cli()
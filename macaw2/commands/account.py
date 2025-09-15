import click
import pandas as pd
from macaw2.models.database import Account

@click.group()
def account():
    """Commands to manage the chart of accounts."""

@account.command()
def setup():
    """Create an account."""
    click.echo(
        "Please enter your desired account id. It is recommended to follow the standard naming convention. https://www.accountingtools.com/articles/chart-of-accounts-numbering.html")
    account_id = click.prompt("Account id", type=int)
    click.echo("Please enter your desired account name. Example: 'mybank:checking', 'fuel', 'salary'.")
    account_name = click.prompt("Account name", type=str)
    account_type = click.prompt(
        "Account type",
        type=click.Choice(["asset", "liability", "equity", "income", "expense"], case_sensitive=False)
    )

    created_acc = Account.create(id=account_id, name=account_name, type=account_type)

    click.secho(f"Successfully created: {created_acc.id}, {created_acc.name}, {created_acc.type}", fg="green")

@account.command()
def info():
    """Lists all account information."""
    if not Account.select().exists():
        click.echo("No accounts found.")
    else:
        acc = Account.select().order_by(Account.id.asc()).dicts()
        df = pd.DataFrame(list(acc))
        print(df)

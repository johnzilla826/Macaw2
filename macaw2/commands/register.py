import click
import pandas as pd
from peewee import DoesNotExist
from macaw2.models.database import Account, Entry

@click.command()
@click.option("--all", "show_all", is_flag=True, help="Show all entries")
@click.option("--account", "account_token", type=str, help="Filter by account name or id")
def register(show_all, account_token):
    """Show entries from the register."""

    if not show_all and not account_token:
        account_token = click.prompt("Account name or id")

    if account_token:
        try:
            acc = Account.get((Account.name == account_token) | (Account.id == account_token))
            query = Entry.select().where(Entry.account == acc)
        except DoesNotExist:
            click.echo(f"Account not found: {account_token}")
            return
    else:
        query = Entry.select()

    rows = [{
        "transaction_id": e.transaction.id,
        "date": e.transaction.date,
        "memo": e.transaction.memo,
        "account": e.account.name,
        "debit": float(e.debit),
        "credit": float(e.credit),
    } for e in query]

    if rows:
        df = pd.DataFrame(rows)
        click.echo(df.to_string(index=False))
    else:
        click.echo("No entries found.")

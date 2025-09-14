import click
from peewee import DoesNotExist
from decimal import Decimal

from macaw2.models.database import Account, Transaction, Entry, db_proxy

@click.command()
def entry():
    date_entry = click.prompt(
        "Date",
        type=click.DateTime(formats=["%Y-%m-%d"]),
    )
    memo_entry = click.prompt("Memo/description")

    submitted_lines = []
    while True:
        line_entry = click.prompt("Line")

        # Submit
        if line_entry == "done":
            break

        # Splitting up "dr acc amt"
        parts = line_entry.split()
        if len(parts) != 3:
            raise click.BadParameter("Line must have exactly 3 parts: dr account amount")

        # account_token is either the acc name or acc id
        side, account_token, amount = parts

        # Checking if it is dr or cr
        if side not in ("dr", "cr"):
            raise click.BadParameter("Line must start with 'dr' or 'cr'")

        # Checking if the account exists
        try:
            account = Account.get((Account.name == account_token) | (Account.id == account_token))
        except DoesNotExist:
            raise click.BadParameter("Account not found.")

        # Checking the amount is a number
        try:
            amount = Decimal(amount).quantize(Decimal("0.01"))
        except ValueError:
            raise click.BadParameter("Amount must be a number")

        submitted_lines.append([side, account, amount])

    # If all else is good, submit it to the database
    if submitted_lines:
        with db_proxy.atomic():
            txn = Transaction.create(
                date=date_entry.date(),
                memo=memo_entry
            )
            for side, account, amount in submitted_lines:
                debit = amount if side == "dr" else Decimal("0.00")
                credit = amount if side == "cr" else Decimal("0.00")
                Entry.create(
                    transaction=txn,
                    account=account,
                    debit=debit,
                    credit=credit
                )

        click.echo(f"Transaction #{txn.id} saved with {len(submitted_lines)} entries.")

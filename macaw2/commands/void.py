import click
from click import ClickException

from macaw2.models.database import Entry, Transaction

@click.command()
@click.argument("transaction_id")
def reverse(transaction_id):
    transaction = Transaction.get_or_none(Transaction.id == transaction_id)

    entry = Entry.get_or_none(Entry.transaction_id == transaction_id)

    if transaction:
        if entry:
            pass
            # This is for deleting, but this project is append only. figure out how to reverse and do the opposite of the transaction
            # entries_deleted = Entry.delete().where(Entry.transaction_id == transaction_id).execute()
            # transaction.delete_instance()
            # click.echo(f"Transaction deleted. {entries_deleted} entries removed.")
        else:
            click.echo("Entry does not exist.")
    else:
        click.echo("Transaction does not exist.")

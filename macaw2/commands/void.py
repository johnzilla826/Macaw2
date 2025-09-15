import click
from click import ClickException
from peewee import IntegrityError
from macaw2.models.database import Entry, Transaction, db_proxy

@click.command()
@click.argument("transaction_id", type=int)
def reverse(transaction_id):

    tx = Transaction.get_or_none(Transaction.id == transaction_id)
    if not tx:
        raise ClickException("Transaction does not exist.")
    if tx.reversal_transaction:
        raise ClickException(f"Transaction #{tx.id} is already a reversal.")

    entries = list(Entry.select().where(Entry.transaction == tx))
    if not entries:
        raise ClickException("No entries for this transaction.")

    with db_proxy.atomic():
        try:
            rev_tx = Transaction.create(
                date=tx.date,
                memo=f"Reversal of transaction #{tx.id}",
                reversal_transaction=True,
                reversed_of=tx
            )
        except IntegrityError:
            raise ClickException(f"Transaction #{tx.id} has already been reversed.")

        for e in entries:
            Entry.create(
                transaction=rev_tx,
                account=e.account,
                debit=e.credit,
                credit=e.debit,
            )

    click.echo(f"Reversal created. New transaction id: #{rev_tx.id}")

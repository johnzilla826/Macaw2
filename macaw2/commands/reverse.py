import click
from click import ClickException
from peewee import IntegrityError
from macaw2.models.database import Entry, Transaction, db_proxy

@click.command()
@click.argument("transaction_id", type=int)
def reverse(transaction_id):
    """
    Appends a reversal transaction to the database.

    """
    tx = Transaction.get_or_none(Transaction.id == transaction_id)
    if not tx:
        raise ClickException(f"There is no transaction with id #{transaction_id}.")
    if tx.reversal_transaction:
        raise ClickException(f"Transaction #{tx.id} is already a reversal.")

    reversal_note = click.prompt("Reversal note")

    entries = list(Entry.select().where(Entry.transaction == tx))
    if not entries:
        raise ClickException("No entry has been found that matches this transaction number.")

    with db_proxy.atomic():
        try:
            rev_tx = Transaction.create(
                date=tx.date,
                memo=f"Reversal of transaction #{tx.id}. Note: '{reversal_note}'",
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
    click.secho(f"Reversal of transaction #{tx.id} is successful. The original transaction was:", fg="green")
    click.echo(f"{tx.date} {tx.memo}")

    for e in entries:
        if e.debit and e.debit > 0:
            click.echo(f"dr {e.account.name:<30} {e.debit:,.2f}")
    for e in entries:
        if e.credit and e.credit > 0:
            click.echo(f"    cr {e.account.name:<27} {e.credit:,.2f}")

    click.echo(f"\nThe new transaction id: #{rev_tx.id}. Below is the reversed transaction that has been entered:")
    click.echo(f"{rev_tx.date} {rev_tx.memo}")

    rev_entries = list(Entry.select().where(Entry.transaction == rev_tx))

    for e in rev_entries:
        if e.debit and e.debit > 0:
            click.echo(f"dr {e.account.name:<30} {e.debit:,.2f}")
    for e in rev_entries:
        if e.credit and e.credit > 0:
            click.echo(f"    cr {e.account.name:<27} {e.credit:,.2f}")

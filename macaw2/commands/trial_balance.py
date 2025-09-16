import click
import pandas as pd
from pathlib import Path
from datetime import date
from macaw2.models.database import Account, Entry

@click.command()
@click.option("--csv", is_flag=True, default=False)
def trial_balance(csv):
    """Current balances of all accounts."""
    entries = pd.DataFrame(list(Entry.select().dicts()))
    if entries.empty:
        print("No entries yet.")
        return

    rows = []
    for acc in Account.select():
        acc_entries = entries[entries["account"] == acc.id]
        net = acc_entries["debit"].sum() - acc_entries["credit"].sum()

        if net > 0:
            rows.append({"Account": acc.name, "Debit": f"{net:.2f}", "Credit": ""})
        elif net < 0:
            rows.append({"Account": acc.name, "Debit": "", "Credit": f"{-net:.2f}"})

    df = pd.DataFrame(rows)

    totals = {
        "Account": "Total",
        "Debit": f"{df['Debit'].replace('', 0).astype(float).sum():.2f}",
        "Credit": f"{df['Credit'].replace('', 0).astype(float).sum():.2f}",
    }
    df.loc[len(df)] = totals

    if csv:
        downloads = Path.home() / "Downloads"
        downloads.mkdir(exist_ok=True)
        csv_path = downloads / f"trial-balance {date.today()}.csv"
        df.to_csv(csv_path, index=False)
        print(f"\nSaved to {csv_path}")
    else:
        print(df.to_string(index=False))

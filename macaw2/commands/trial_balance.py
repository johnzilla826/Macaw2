import click
import pandas as pd
from pathlib import Path
from datetime import date
from macaw2.models.database import Account, Entry, Transaction

@click.command()
@click.option("--csv", is_flag=True, default=False)
def trial_balance(csv):
    """Trial balance with optional date range."""
    start_s = click.prompt("Enter start date (YYYY-MM-DD) or leave blank", default="", show_default=False)
    end_s   = click.prompt("Enter end date (YYYY-MM-DD) or leave blank",   default="", show_default=False)

    entries = pd.DataFrame(list(
        Entry.select(
            Entry.id, Entry.account, Entry.debit, Entry.credit,
            Transaction.date.alias("tdate")
        ).join(Transaction).dicts()
    ))
    if entries.empty:
        print("No entries yet.")
        return

    entries["tdate"] = pd.to_datetime(entries["tdate"]).dt.date
    start = pd.to_datetime(start_s).date() if start_s else None
    end   = pd.to_datetime(end_s).date()   if end_s   else None

    if start:
        entries = entries[entries["tdate"] >= start]
    if end:
        entries = entries[entries["tdate"] <= end]
    if entries.empty:
        print(f"No transactions found between {start_s or 'beginning'} and {end_s or 'end'}.")
        return

    rows = []
    for acc in Account.select():
        acc_entries = entries[entries["account"] == acc.id]
        net = acc_entries["debit"].sum() - acc_entries["credit"].sum()
        if net > 0:
            rows.append({"Account": acc.name, "Debit": f"{net:.2f}", "Credit": ""})
        elif net < 0:
            rows.append({"Account": acc.name, "Debit": "", "Credit": f"{-net:.2f}"})

    if not rows:
        print("No non-zero balances in that range.")
        return

    df = pd.DataFrame(rows).sort_values("Account").reset_index(drop=True)

    df.loc[len(df)] = {
        "Account": "Total",
        "Debit":  f"{df['Debit'].replace('', 0).astype(float).sum():.2f}",
        "Credit": f"{df['Credit'].replace('', 0).astype(float).sum():.2f}",
    }

    if csv:
        downloads = Path.home() / "Downloads"
        downloads.mkdir(exist_ok=True)
        suffix = f"_{start_s or 'beginning'}_to_{end_s or 'end'}".replace(" ", "")
        csv_path = downloads / f"trial-balance{suffix}.csv"
        df.to_csv(csv_path, index=False)
        print(f"\nSaved to {csv_path}")
    else:
        print(df.to_string(index=False))

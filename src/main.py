from transaction import Transaction, Journal
from visual import Visualization
from data import Data


def embed_transactions(transactions: dict, journal):
    txn_list: list = []

    for key, value in transactions.items():
        txn = Transaction(date=value['date'], description=value['description'])
        txn.add_entry(debit_category=value['debit_category'], debit_account_name=value['debit_account_name'],
                      debit_amount=value['debit_amount'],
                      credit_category=value['credit_category'], credit_account_name=value['credit_account_name'],
                      credit_amount=value['credit_amount'])
        journal.add_transaction(txn)
        txn_list.append(txn)

    return txn_list


def main():
    journal = Journal(journal_name='Company XYZ', start_date='2025-10-01', end_date='2025-10-31')

    data = Data()
    data.get_transactions_from_excel()
    transactions = data.transactions

    embed_transactions(transactions, journal=journal)

    journal.adjust_journal_entry(
        adjustment_date='2025-10-31',
        description='Adjustment: Recognize earned revenue from unearned revenue contract',  # txn6 $4,800/6 (1/6 months)
        debit_category='Liability',
        debit_account_name='Unearned revenue',
        debit_amount=800,
        credit_category='Equity',
        credit_account_name='Service revenue',
        credit_amount=800
    )

    exporter = Visualization(transactions=journal.transactions, journal=journal)
    exporter.export_to_excel(f"{journal.journal_name}.xlsx")


if __name__ == '__main__':
    main()

from transaction import Transaction, Journal


def transactions() -> list:
    # Transaction 1: Owner investment
    txn1 = Transaction(description='2025-10-04', date='Owner invested $100,000 cash')
    txn1.add_entry(debit_category='asset', debit_account_name='Cash', debit_amount=100000,
                   credit_category='equity', credit_account_name='Owners Capital', credit_amount=100000)

    # Transaction 2: Buying land
    txn2 = Transaction(description='2025-10-05', date='Buying land for $40,000')
    txn2.add_entry(debit_category='asset', debit_account_name='Land', debit_amount=40000,
                   credit_category='asset', credit_account_name='Cash', credit_amount=40000)

    # Transaction 3: Service revenue invoice
    txn3 = Transaction(description='2025-11-05', date='Service revenue invoice of $5,000')
    txn3.add_entry(debit_category='asset', debit_account_name='Cash', debit_amount=5000,
                   credit_category='equity', credit_account_name='Service revenue', credit_amount=5000)

    # Transaction 4: Receive a payable bill for the performed service
    txn4 = Transaction(description='2025-11-05', date='Payable bill of $1,200')
    txn4.add_entry(debit_category='equity', debit_account_name='Service expense', debit_amount=1200,
                   credit_category='liability', credit_account_name='Accounts payable', credit_amount=1200)

    # Transaction 5: Pay the bill
    txn5 = Transaction(description='2025-12-05', date='Pay the payable bill of $1,200')
    txn5.add_entry(debit_category='liability', debit_account_name='Accounts payable', debit_amount=1200,
                   credit_category='asset', credit_account_name='Cash', credit_amount=1200)

    return [txn1, txn2, txn3, txn4, txn5]


def main():
    # Transactions
    txn_list: list = transactions()

    # Journal
    journal = Journal(journal_name="Company XYZ", start_date="2025-10-01", end_date="2025-10-30")

    for txn in txn_list:
        journal.add_transaction(txn)

    print(f"{journal.get_entries_by_account("Accounts payable")}")


if __name__ == '__main__':
    main()

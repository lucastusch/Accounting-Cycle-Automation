from transaction import Transaction, Journal
from visual import Visualization


def transactions() -> list:
    # Transaction 1: Owner investment
    txn1 = Transaction(date='2025-10-04', description='Owner invested $100,000 cash')
    txn1.add_entry(debit_category='asset', debit_account_name='Cash', debit_amount=100000,
                   credit_category='equity', credit_account_name='Owners Capital', credit_amount=100000)

    # Transaction 2: Buying land
    txn2 = Transaction(date='2025-10-05', description='Buying land for $40,000')
    txn2.add_entry(debit_category='asset', debit_account_name='Land', debit_amount=40000,
                   credit_category='asset', credit_account_name='Cash', credit_amount=40000)

    # Transaction 3: Service revenue invoice
    txn3 = Transaction(date='2025-10-06', description='Service revenue invoice of $5,000')
    txn3.add_entry(debit_category='asset', debit_account_name='Cash', debit_amount=5000,
                   credit_category='equity', credit_account_name='Service revenue', credit_amount=5000)

    # Transaction 4: Receive a payable bill for the performed service
    txn4 = Transaction(date='2025-10-07', description='Payable bill of $1,200')
    txn4.add_entry(debit_category='equity', debit_account_name='Service expense', debit_amount=1200,
                   credit_category='liability', credit_account_name='Accounts payable', credit_amount=1200)

    # Transaction 5: Pay the bill
    txn5 = Transaction(date='2025-10-08', description='Pay the payable bill of $1,200')
    txn5.add_entry(debit_category='liability', debit_account_name='Accounts payable', debit_amount=1200,
                   credit_category='asset', credit_account_name='Cash', credit_amount=1200)

    # Transaction 6: Unearned revenue (contract for 6 months)
    txn6 = Transaction(date='2025-10-09', description='Record unearned revenue of $4,800')
    txn6.add_entry(debit_category='asset', debit_account_name='Cash', debit_amount=4800,
                   credit_category='liability', credit_account_name='Unearned revenue', credit_amount=4800)

    # Transaction 7: Pay salary
    txn7 = Transaction(date='2025-10-30', description='Pay a salary of $2,300')
    txn7.add_entry(debit_category='equity', debit_account_name='Salary Expense', debit_amount=2300,
                   credit_category='asset', credit_account_name='Cash', credit_amount=2300)

    # Transaction 8: Pay tax
    txn8 = Transaction(date='2025-10-30', description='Pay tax of $40')
    txn8.add_entry(debit_category='equity', debit_account_name='Tax expense', debit_amount=40,
                   credit_category='asset', credit_account_name='Cash', credit_amount=40)

    return [txn1, txn2, txn3, txn4, txn5, txn6, txn7, txn8]


def main():
    # Transactions
    txn_list: list = transactions()

    # Journal
    journal = Journal(journal_name='Company XYZ', start_date='2025-10-01', end_date='2025-10-30')

    for txn in txn_list:
        journal.add_transaction(txn)

    print(f"{journal.get_account_balances()}")
    print(f"{journal.get_category_balances()}")
    print(f"{journal.get_trial_balance()}")

    journal.adjust_journal_entry(
        adjustment_date='2025-10-31',
        description='Adjustment: Recognize earned revenue from unearned revenue contract',  # txn6 $4,800/6 (1/6 months)
        debit_category='liability',
        debit_account_name='Unearned revenue',
        debit_amount=800,
        credit_category='equity',
        credit_account_name='Service revenue',
        credit_amount=800
    )

    print(f"{journal.get_account_balances()}")
    print(f"{journal.get_category_balances()}")
    print(f"{journal.get_trial_balance()}")
    print(f"{repr(journal)}")

    exporter = Visualization(transactions=txn_list, journal=journal)
    exporter.export_to_excel(f"{journal.journal_name}.xlsx")


if __name__ == '__main__':
    main()

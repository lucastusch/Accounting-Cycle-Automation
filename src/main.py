from transaction import Transaction


def main():
    # Transaction 1: Owner investment
    txn1 = Transaction('2025-11-04', 'Owner invested $100,000 cash')
    txn1.add_entry(debit_account_name='Cash', debit_amount=100000, credit_account_name='Owners Capital', credit_amount=100000)

    # Transaction 2: Buying land
    txn2 = Transaction('2025-11-04', 'Buying land for $40,000')
    txn2.add_entry(debit_account_name='Land', debit_amount=40000, credit_account_name='Cash', credit_amount=40000)

    print(f"{txn1.entry}\n{txn2.entry}")


if __name__ == '__main__':
    main()

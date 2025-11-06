class Transaction:
    """
    Represents a single business transaction following the accounting equation (Assets = Liabilities + Equity)
    """
    transaction_counter: int = 0

    def __init__(self, date, description):
        Transaction.transaction_counter += 1

        self.transaction_id: int = Transaction.transaction_counter  # Unique identifier for the transaction
        self.date: str = date  # Transaction date in YYYY-MM-DD format
        self.description: str = description  # Description of the transaction
        self.entry: dict = {}  # List of journal entries (account, type, amount)

    def add_entry(self, debit_category: str, debit_account_name: str, debit_amount: int,
                  credit_category: str, credit_account_name: str, credit_amount: int):
        """
        Add a journal entry (debit or credit) to the transaction
        """
        if debit_amount < 0 or credit_amount < 0:
            raise ValueError(f"Amount must be positive, got {debit_amount} and {credit_amount}.")

        if debit_amount != credit_amount:
            raise ValueError(f"Debit must match credit, got {debit_amount} and {credit_amount}.")

        if debit_category not in ["asset", "liability", "equity"] or credit_category not in ["asset", "liability",
                                                                                             "equity"]:
            raise ValueError(f"Category must be eiter 'asset', 'liability', or 'equity'.")

        self.entry = {
            'id': self.transaction_id,
            'debit_category': debit_category,
            'debit_account': debit_account_name,
            'debit': debit_amount,
            'credit_category': credit_category,
            'credit_account': credit_account_name,
            'credit': credit_amount
        }


class Journal:
    """
    Represents a Journal - records all business transactions
    """
    adjustment_counter = 0

    def __init__(self, journal_name: str, start_date: str, end_date: str):
        self.journal_name: str = journal_name
        self.transactions: list = []  # List to store Transaction objects
        self.journal_entries: list = []  # List to store formatted journal entries

        self.start_date: str = start_date
        self.end_date: str = end_date

    def _check_balance(self):
        """
        Checks if debits match credits
        """
        sum_debit_entries: int = sum(entry['debit_amount'] for entry in self.journal_entries)
        sum_credit_entries: int = sum(entry['credit_amount'] for entry in self.journal_entries)
        if sum_debit_entries != sum_credit_entries:
            raise ValueError(
                f"Debit must match credit, got sum of debit entries={sum_debit_entries} and sum of credit entries={sum_credit_entries}"
            )

    def add_transaction(self, transaction: Transaction):
        """
        Add a Transaction object to the journal (journal entry)
        """
        if not isinstance(transaction, Transaction):
            raise TypeError(f"Only Transaction objects can be added to the Journal.")

        if not transaction.entry:
            raise ValueError(f"Transaction {transaction.transaction_id} has no entry recorded.")

        self.transactions.append(transaction)

        # Create formatted journal entry
        journal_entry = {
            'transaction_id': transaction.transaction_id,
            'date': transaction.date,
            'description': transaction.description,
            'debit_category': transaction.entry['debit_category'],
            'debit_account': transaction.entry['debit_account'],
            'debit_amount': transaction.entry['debit'],
            'credit_category': transaction.entry['credit_category'],
            'credit_account': transaction.entry['credit_account'],
            'credit_amount': transaction.entry['credit']
        }
        self.journal_entries.append(journal_entry)

    def get_all_entries(self) -> list:
        """
        Get all journal entries in chronological order
        """
        return self.journal_entries

    def get_entries_by_date(self, date: str) -> list:
        """
        Retrieve all journal entries for a specific date "YYYY-MM-DD"
        """
        return [entry for entry in self.journal_entries if entry['date'] == date]

    def get_single_account_entries(self, account_name: str) -> list:
        """
        Retrieve all journal entries involving a specific account
        """
        return [entry for entry in self.journal_entries
                if entry['debit_account'] == account_name or entry['credit_account'] == account_name]

    def get_single_account_balance(self, account_name: str) -> int:
        """
        Calculate the balance of the specified account
        """
        self._check_balance()

        debits_balance: int = sum(
            entry['debit_amount'] for entry in self.journal_entries if entry['debit_account'] == account_name)
        credits_balance: int = sum(
            entry['credit_amount'] for entry in self.journal_entries if entry['credit_account'] == account_name)

        return debits_balance - credits_balance

    def get_account_balances(self) -> dict[str, {str, int}]:
        """
        Calculate all account balances and sorts data by category (ledger and unadjusted account trial balances in one)
        """
        self._check_balance()

        balances: dict = {}
        for entry in self.journal_entries:
            for key in ['debit', 'credit']:
                category = entry[f'{key}_category']
                account = entry[f'{key}_account']

                balances.setdefault(category, {})[account] = self.get_single_account_balance(account)

        return balances

    def get_category_balances(self) -> dict[str, int]:
        """
        Calculate the category balances
        """
        self._check_balance()

        balances: dict = self.get_account_balances()
        return {category: sum(items.values()) for category, items in balances.items()}

    def adjust_journal_entry(self, adjustment_date: str, description: str,
                             debit_category: str, debit_account_name: str, debit_amount: int,
                             credit_category: str, credit_account_name: str, credit_amount: int):

        Journal.adjustment_counter += 1

        if debit_amount < 0 or credit_amount < 0:
            raise ValueError(f"Amount must be positive, got {debit_amount} and {credit_amount}.")

        if debit_amount != credit_amount:
            raise ValueError(f"Debit must match credit, got {debit_amount} and {credit_amount}.")

        adjustment_txn = Transaction(date=adjustment_date, description=description)
        adjustment_txn.add_entry(
            debit_category=debit_category,
            debit_account_name=debit_account_name,
            debit_amount=debit_amount,
            credit_category=credit_category,
            credit_account_name=credit_account_name,
            credit_amount=credit_amount
        )

        self.add_transaction(adjustment_txn)

    def get_trial_balance(self):
        """
        Calculates unadjusted or (after "adjust_journal_entry") adjusted trial balance
        """
        self._check_balance()

        category_balances: dict = self.get_category_balances()
        return category_balances["asset"]

    def __len__(self):
        return len(self.transactions) - self.adjustment_counter

    def __repr__(self):
        return (f"Journal {self.journal_name} for operating range {self.start_date} to {self.end_date}.\n"
                f"Transactions: {len(self.transactions) - self.adjustment_counter}, "
                f"adjustments: {self.adjustment_counter}")

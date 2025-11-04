class Transaction:
    """
    Represents a single business transaction following the accounting equation (Assets = Liabilities + Equity)
    """

    transaction_counter = 0

    def __init__(self, date, description):
        Transaction.transaction_counter += 1

        self.transaction_id: int = Transaction.transaction_counter  # Unique identifier for the transaction
        self.date: str = date  # Transaction date in YYYY-MM-DD format
        self.description: str = description  # Description of the transaction
        self.entry: dict = {}  # List of journal entries (account, type, amount)

    def add_entry(self, debit_account_name: str, debit_amount: int, credit_account_name: str, credit_amount: int):
        """
        Add a journal entry (debit or credit) to the transaction
        """
        if debit_amount < 0 or credit_amount < 0:
            raise ValueError(f"Amount must be positive, got {debit_amount} and {credit_amount}.")

        if debit_amount != credit_amount:
            raise ValueError(f"Debit must match credit, got {debit_amount} and {credit_amount}.")

        self.entry = {
            'debit_account': debit_account_name,
            'debit': debit_amount,
            'credit_account': credit_account_name,
            'credit': credit_amount
        }

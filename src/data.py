import pandas as pd


class Data:
    def __init__(self):
        self.transactions: dict = {}
        self.journal: dict = {}

    def get_transactions_from_excel(self, filename: str = "Transactions.xlsx"):
        """
        Import transactions from Excel worksheet "Transactions"
        """
        df = pd.read_excel(filename, sheet_name='Transactions')
        self.transactions = {}

        for _, row in df.iterrows():
            date_str: str = row['Date'].strftime('%Y-%m-%d') if hasattr(row['Date'], 'strftime') else str(row['Date'])

            transaction: dict = {
                "date": date_str,
                "description": str(row['Description']),
                "debit_category": str(row['Debit Category']) if pd.notna(row['Debit Category']) else "",
                "debit_account_name": str(row['Debit Account']) if pd.notna(row['Debit Account']) else "",
                "debit_amount": float(row['Debit Amount']) if pd.notna(row['Debit Amount']) else 0.0,
                "credit_category": str(row['Credit Category']) if pd.notna(row['Credit Category']) else "",
                "credit_account_name": str(row['Credit Account']) if pd.notna(row['Credit Account']) else "",
                "credit_amount": float(row['Credit Amount']) if pd.notna(row['Credit Amount']) else 0.0
            }

            # Use Transaction ID or date+description as key to avoid overwriting
            key: int = row.get('Transaction ID', date_str + '_' + transaction['description'][:20])
            self.transactions[key] = transaction

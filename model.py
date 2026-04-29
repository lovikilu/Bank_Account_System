import json
from datetime import datetime
from collections import deque

class Account:
    """"Базовый класс для всех счетов"""
    def __init__(self, account_number, owner_name, balance=0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False
    
    def withdraw (self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return True
        return False
    
    def to_dict (self):
        return {
            'type': self.__class__.__name__,
            'account_number': self.account_number,
            'owner_name': self.owner_name,
            'balance': self.balance
        }
    
    @staticmethod
    def from_dict(data):
        account_type = data.get('type')
        if account_type == 'CheckingAccount':
            return CheckingAccount(data['account_number'], data['owner_name'], data['balance'])
        elif account_type == 'SavingsAccount':
            return SavingsAccount(data['account_number'], data['owner_name'], data['balance'])
        elif account_type == 'CreditAccount':
            return CreditAccount(data['account_number'], data['owner_name'], data['balance'])
        return None
    
class CheckingAccount(Account):
    """Текущий счет"""
    pass

class SavingsAccount(Account):
    """Сберегательный счет"""
    pass

class CreditAccount(Account):
    """Кредитный счет"""
    def __init__(self, account_number, owner_name, balance = 0, credit_limit = 100000):
        super().__init__(account_number, owner_name, balance)
        self.credit_limit = credit_limit

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance + self.credit_limit:
            self.balance -= amount
            return True
        return False
    
    def to_dict(self):
        data = super().to_dict()
        data['credit_limit'] = self.credit_limit
        return data
    
    @staticmethod
    def from_dict(data):
        return CreditAccount(data['account_number'], data['owner_name'], data['balance'], data.get('credit_limit', 100000))

class Transaction:
    """Класс транзакции"""
    def __init__(self, transaction_id, from_account, to_account, amount, transaction_type, date = None):
        self.transaction_id = transaction_id
        self.from_account= from_account
        self.to_account = to_account
        self.amount= amount
        self.transaction_type = transaction_type
        self.date = date if date else datetime.now().strftime("%Y-%m-%D %H:%M:%S")

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'from_account': self.from_account,
            'to_account': self.to_account,
            'amount': self.amount,
            "transaction_type": self.transaction_type,
            'date': self.date
        }
    
    @staticmethod
    def from_dict(data):
        return Transaction(
            data['transaction_id'],
            data['from_account'],
            data['to_account'],
            data['amount'],
            data['transaction_type'],
            data['date'],
        )

    def __str__(self):
        return f"[{self.date}] {self.transaction_type}: {self.amount}руб. ({self.from_account} -> {self.to_account})"
    
class TransactionHistoryQueue:
    """Очередь истори транзакций"""
    def __init__(self, max_size = 100):
        self.queue = deque(maxlen=max_size)

    def add_transaction(self, transaction):
        self.queue.append(transaction)

    def get_all(self):
        return list(self.queue)
    
    def filter_by_date(self, date_str):
        return [t for t in self.queue if date_str in t.date]
    
    def filter_by_type(self, transaction_type):
        return [t for t in self.queue if t.transaction_type == transaction_type]
    
    def clear(self):
        self.queue.clear()

    def from_list_dict(self, transaction_data):
        self.queue.clear()
        for t_data in transaction_data:
            self.queue.append(Transaction.from_dict(t_data))

    def to_list_dict(self):
        """Преобразует очередь транзакций в список словарей для JSON"""
        return [t.to_dict() for t in self.queue]

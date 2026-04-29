import json
import os
from model import *

class BankController:
    def __init__(self):
        self.accounts = []
        self.transaction_history = TransactionHistoryQueue()
        self.next_account_number = 1
        self.next_transaction_id = 1
    
    def create_account(self, account_type, owner_name, initial_balance=0):
        """Создание нового счета"""
        try:
            if initial_balance < 0:
                raise ValueError("Начальный баланс не может быть отрицательным")
            
            account_number = str(self.next_account_number).zfill(6)
            self.next_account_number += 1
            
            if account_type == '1':
                account = CheckingAccount(account_number, owner_name, initial_balance)
            elif account_type == '2':
                account = SavingsAccount(account_number, owner_name, initial_balance)
            elif account_type == '3':
                account = CreditAccount(account_number, owner_name, initial_balance)
            else:
                return None
            
            self.accounts.append(account)
            
            # Записываем транзакцию создания счета (как пополнение)
            if initial_balance > 0:
                transaction = Transaction(
                    str(self.next_transaction_id),
                    "SYSTEM",
                    account_number,
                    initial_balance,
                    "deposit"
                )
                self.next_transaction_id += 1
                self.transaction_history.add_transaction(transaction)
            
            return account
        except Exception as e:
            print(f"Ошибка создания счета: {e}")
            return None
    
    def find_account(self, account_number):
        """Поиск счета по номеру"""
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None
    
    def deposit(self, account_number, amount):
        """Пополнение счета"""
        try:
            account = self.find_account(account_number)
            if not account:
                raise ValueError("Счет не найден")
            
            if amount <= 0:
                raise ValueError("Сумма должна быть больше 0")
            
            if account.deposit(amount):
                transaction = Transaction(
                    str(self.next_transaction_id),
                    "EXTERNAL",
                    account_number,
                    amount,
                    "deposit"
                )
                self.next_transaction_id += 1
                self.transaction_history.add_transaction(transaction)
                return True, f"Счет {account_number} пополнен на {amount} руб. Новый баланс: {account.balance} руб."
            else:
                return False, "Ошибка пополнения"
        except Exception as e:
            return False, str(e)
    
    def withdraw(self, account_number, amount):
        """Снятие денег со счета"""
        try:
            account = self.find_account(account_number)
            if not account:
                raise ValueError("Счет не найден")
            
            if amount <= 0:
                raise ValueError("Сумма должна быть больше 0")
            
            if account.withdraw(amount):
                transaction = Transaction(
                    str(self.next_transaction_id),
                    account_number,
                    "EXTERNAL",
                    amount,
                    "withdraw"
                )
                self.next_transaction_id += 1
                self.transaction_history.add_transaction(transaction)
                return True, f"Со счета {account_number} снято {amount} руб. Новый баланс: {account.balance} руб."
            else:
                return False, f"Недостаточно средств. Доступно: {account.balance} руб."
        except Exception as e:
            return False, str(e)
    
    def transfer(self, from_account_num, to_account_num, amount):
        """Перевод между счетами"""
        try:
            from_account = self.find_account(from_account_num)
            to_account = self.find_account(to_account_num)
            
            if not from_account:
                raise ValueError("Счет отправителя не найден")
            if not to_account:
                raise ValueError("Счет получателя не найден")
            
            if amount <= 0:
                raise ValueError("Сумма должна быть больше 0")
            
            if from_account.withdraw(amount):
                to_account.deposit(amount)
                transaction = Transaction(
                    str(self.next_transaction_id),
                    from_account_num,
                    to_account_num,
                    amount,
                    "transfer"
                )
                self.next_transaction_id += 1
                self.transaction_history.add_transaction(transaction)
                return True, f"Переведено {amount} руб. с {from_account_num} на {to_account_num}"
            else:
                return False, f"Недостаточно средств. Доступно: {from_account.balance} руб."
        except Exception as e:
            return False, str(e)
    
    def save_to_json(self, filename="data.json"):
        """Сохранение данных в JSON"""
        try:
            data = {
                'accounts': [acc.to_dict() for acc in self.accounts],
                'transactions': self.transaction_history.to_list_dict(),
                'next_account_number': self.next_account_number,
                'next_transaction_id': self.next_transaction_id
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True, "Данные сохранены"
        except Exception as e:
            return False, f"Ошибка сохранения: {e}"
    
    def load_from_json(self, filename="data.json"):
        """Загрузка данных из JSON"""
        try:
            if not os.path.exists(filename):
                return False, "Файл не найден"
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Загружаем счета
            self.accounts = []
            for acc_data in data.get('accounts', []):
                account = Account.from_dict(acc_data)
                if account:
                    self.accounts.append(account)
            
            # Загружаем транзакции
            self.transaction_history.from_list_dict(data.get('transactions', []))
            
            # Загружаем счетчики
            self.next_account_number = data.get('next_account_number', 1)
            self.next_transaction_id = data.get('next_transaction_id', 1)
            
            return True, f"Загружено {len(self.accounts)} счетов и {len(self.transaction_history.get_all())} транзакций"
        except Exception as e:
            return False, f"Ошибка загрузки: {e}"
    
    def get_all_accounts(self):
        return self.accounts
    
    def get_transaction_history(self):
        return self.transaction_history.get_all()
    
    def filter_transactions_by_date(self, date_str):
        return self.transaction_history.filter_by_date(date_str)
    
    def filter_transactions_by_type(self, transaction_type):
        return self.transaction_history.filter_by_type(transaction_type)

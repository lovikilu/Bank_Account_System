class ConsoleView:
    """Консольный интерфейс пользователя"""
    
    @staticmethod
    def show_menu():
        print("\n" + "="*50)
        print("        БАНКОВСКАЯ СИСТЕМА")
        print("="*50)
        print("1. Создать новый счет")
        print("2. Показать все счета")
        print("3. Пополнить счет")
        print("4. Снять деньги со счета")
        print("5. Перевести деньги между счетами")
        print("6. Показать историю транзакций")
        print("7. Фильтровать историю транзакций")
        print("8. Сохранить данные")
        print("9. Загрузить данные")
        print("0. Выход")
        print("-"*50)
    
    @staticmethod
    def get_input(prompt):
        return input(prompt)
    
    @staticmethod
    def show_message(message, is_error=False):
        if is_error:
            print(f"❌ ОШИБКА: {message}")
        else:
            print(f"✅ {message}")
    
    @staticmethod
    def show_accounts(accounts):
        if not accounts:
            print("📭 Нет открытых счетов")
            return
        
        print("\n" + "="*60)
        print("СПИСОК СЧЕТОВ:")
        print("-"*60)
        for acc in accounts:
            print(f"🔹 {acc.__class__.__name__}: №{acc.account_number}")
            print(f"   Владелец: {acc.owner_name}")
            print(f"   Баланс: {acc.balance} руб.")
            if hasattr(acc, 'credit_limit'):
                print(f"   Кредитный лимит: {acc.credit_limit} руб.")
            print("-"*40)
    
    @staticmethod
    def show_transactions(transactions):
        if not transactions:
            print("📭 Нет транзакций")
            return
        
        print("\n" + "="*60)
        print("ИСТОРИЯ ТРАНЗАКЦИЙ:")
        print("-"*60)
        for t in transactions:
            print(t)
        print("="*60)
    
    @staticmethod
    def show_filter_menu():
        print("\n--- ФИЛЬТРАЦИЯ ТРАНЗАКЦИЙ ---")
        print("1. По дате")
        print("2. По типу транзакции")
        print("0. Отмена")
        return ConsoleView.get_input("Выберите фильтр: ")
    
    @staticmethod
    def get_date_filter():
        return ConsoleView.get_input("Введите дату (ГГГГ-ММ-ДД): ")
    
    @staticmethod
    def get_type_filter():
        print("Типы транзакций: deposit, withdraw, transfer")
        return ConsoleView.get_input("Введите тип транзакции: ")
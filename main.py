from controller import BankController
from view import ConsoleView

def main():
    controller = BankController()
    view = ConsoleView()
    
    view.show_message("Добро пожаловать в банковскую систему!", False)
    
    while True:
        view.show_menu()
        choice = view.get_input("Выберите действие: ")
        
        if choice == '1':  # Создать счет
            print("\n--- СОЗДАНИЕ СЧЕТА ---")
            print("1. Текущий счет")
            print("2. Сберегательный счет")
            print("3. Кредитный счет")
            acc_type = view.get_input("Выберите тип счета: ")
            
            owner_name = view.get_input("Введите имя владельца: ")
            initial_balance = float(view.get_input("Введите начальный баланс (0 по умолчанию): ") or "0")
            
            account = controller.create_account(acc_type, owner_name, initial_balance)
            if account:
                view.show_message(f"Счет создан! Номер счета: {account.account_number}")
            else:
                view.show_message("Неверный тип счета", True)
        
        elif choice == '2':  # Показать все счета
            view.show_accounts(controller.get_all_accounts())
        
        elif choice == '3':  # Пополнить счет
            acc_num = view.get_input("Введите номер счета: ")
            amount = float(view.get_positive_number_input("Введите сумму пополнения: "))
            success, message = controller.deposit(acc_num, amount)
            view.show_message(message, not success)
        
        elif choice == '4':  # Снять деньги
            acc_num = view.get_input("Введите номер счета: ")
            amount = float(view.get_positive_number_input("Введите сумму снятия: "))
            success, message = controller.withdraw(acc_num, amount)
            view.show_message(message, not success)
        
        elif choice == '5':  # Перевести деньги
            from_acc = view.get_input("Введите номер счета отправителя: ")
            to_acc = view.get_input("Введите номер счета получателя: ")
            amount = float(view.get_positive_number_input("Введите сумму перевода: "))
            success, message = controller.transfer(from_acc, to_acc, amount)
            view.show_message(message, not success)
        
        elif choice == '6':  # История транзакций
            view.show_transactions(controller.get_transaction_history())
        
        elif choice == '7':  # Фильтрация
            filter_choice = view.show_filter_menu()
            if filter_choice == '1':
                date_str = view.get_date_filter()
                filtered = controller.filter_transactions_by_date(date_str)
                view.show_transactions(filtered)
            elif filter_choice == '2':
                type_str = view.get_type_filter()
                filtered = controller.filter_transactions_by_type(type_str)
                view.show_transactions(filtered)
            elif filter_choice == '0':
                continue
            else:
                view.show_message("Неверный выбор", True)
        
        elif choice == '8':  # Сохранить
            success, message = controller.save_to_json()
            view.show_message(message, not success)
        
        elif choice == '9':  # Загрузить
            filename = view.get_input("Введите имя файла (data.json по умолчанию): ") or "data.json"
            success, message = controller.load_from_json(filename)
            view.show_message(message, not success)
        
        elif choice == '0':  # Выход
            save_choice = view.get_input("Сохранить перед выходом? (да/нет): ")
            if save_choice.lower() == 'да':
                controller.save_to_json()
            view.show_message("До свидания!")
            break
        
        else:
            view.show_message("Неверный выбор. Попробуйте снова.", True)

if __name__ == "__main__":
    main()

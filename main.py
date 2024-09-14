from src.utils import create_database, create_tables, insert_data
from src.db_manager import DBManager


def main():
    """Точка запуска программы"""
    db_name = "course_work3"
    create_database("course_work3")
    create_tables("course_work3")
    insert_data("course_work3")

    db_manager = DBManager(db_name)

    print("""
    Введите цифру для получения нужной Вам информации:
    1 - получить список всех компаний и количество вакансий у каждой компании.\n
    2 - получить список всех вакансий с указанием  компании, вакансии и зарплаты и ссылки на вакансию. \n
    3 - получить среднюю зарплату по вакансиям. \n
    4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям. \n
    5 - получить список всех вакансий, в названии которых содержатся переданные в метод слова\n""")
    while True:
        user_input = input()
        if user_input == "1":
            list_employer = db_manager.get_companies_and_vacancies_count()
            print("Список всех компаний и количество вакансий у каждой компании:")
            for i in list_employer:
                print(i)
        elif user_input == "2":
            list_vacancy_full = db_manager.get_all_employers()
            print("Список всех вакансий с указанием  компании, вакансии и зарплаты и ссылки на вакансию:")
            for i in list_vacancy_full:
                print(i)
        elif user_input == "3":
            list_vacancy_avg_salary = db_manager.get_avg_salary()
            print("Список всех вакансий co средней зарплатой по вакансиям:")
            for i in list_vacancy_avg_salary:
                print(i)
        elif user_input == "4":
            list_vacancy_avg_salary = db_manager.get_vacancies_with_higher_salary()
            print("Список всех вакансий с зарплатой выше средней:")
            for i in list_vacancy_avg_salary:
                print(i)
        elif user_input == "5":
            keyword = input("Введите слово, по которому хотите отфильтровать вакансии: \n").lower()
            list_vacancy_keyword = db_manager.get_vacancies_with_keyword(keyword)
            print("Список всех вакансий в названии которых содержатся переданные в метод слова:")
            for i in list_vacancy_keyword:
                print(i)
        else:
            print("Работа программы завершена")
            break


if __name__ == "__main__":
    main()

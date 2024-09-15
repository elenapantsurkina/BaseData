import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DBManager:
    """Класс, который подключается к базе данных"""
    def __init__(self, db_name):
        self.__db_name = db_name

    def __execute_query(self, query):
        """Метод , который подключается в базе данных"""
        conn = psycopg2.connect(dbname=self.__db_name, user=os.getenv("user"), password=os.getenv("password"),
                                host=os.getenv("host"), port=os.getenv("port"))
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        """Метод, получает список всех компаний и количество вакансий у каждой компании"""
        query = ("SELECT employer.id, employer.name, COUNT(vacancy.id) AS vacancy_count "
                 "FROM employer "
                 "LEFT JOIN vacancy ON employer.id = vacancy.employer_id "
                 "GROUP BY employer.id, employer.name "
                 "ORDER BY employer.name")
        return self.__execute_query(query)

    def get_all_employers(self):
        """Метод, получает список всех вакансий с указанием  компании, вакансии и зарплаты и ссылки на вакансию """
        return self.__execute_query("SELECT * FROM vacancy")

    def get_avg_salary(self):
        """Метод, получает среднюю зарплату по вакансиям"""
        return self.__execute_query("SELECT AVG(salary_from) FROM vacancy")

    def get_vacancies_with_higher_salary(self):
        """Метод,получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        return self.__execute_query("SELECT name, salary_from, url FROM vacancy "
                                    "WHERE salary_from > (SELECT AVG(salary_from) FROM vacancy)")

    def get_vacancies_with_keyword(self, keyword):
        """Метод, получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        query = f"SELECT * FROM vacancy WHERE name LIKE '%{keyword}%'"
        return self.__execute_query(query)

import os
import psycopg2
from dotenv import load_dotenv
from src.hh_parser import HHParser


load_dotenv()


def create_database(db_name):
    """Создание базы данных"""
    conn = psycopg2.connect(dbname="postgres", user=os.getenv("user"), password=os.getenv("password"),
                            host=os.getenv("host"), port=os.getenv("port"))
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name} WITH (FORCE)")
    cur.execute(f"CREATE DATABASE {db_name}")
    cur.close()
    conn.close()


def create_tables(db_name):
    """Создание таблиц employer(работодатели) и vacancy(вакансии)"""
    conn = psycopg2.connect(dbname=db_name, user=os.getenv("user"), password=os.getenv("password"),
                            host=os.getenv("host"), port=os.getenv("port"))
    with conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE employer (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE)""")

            cur.execute("""CREATE TABLE vacancy (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            url VARCHAR(255),
            employer_id INTEGER REFERENCES employer(id) NOT NULL)""")
    conn.close()


def insert_data(db_name):
    """Функция заполнения таблиц"""
    conn = psycopg2.connect(dbname=db_name, user=os.getenv("user"), password=os.getenv("password"),
                            host=os.getenv("host"), port=os.getenv("port"))
    with conn:
        with conn.cursor() as cur:
            hh = HHParser()
            employers = hh.get_employers()
            for employer in employers:
                employer_id = employer["id"]
                cur.execute("INSERT INTO employer VALUES (%s, %s)", (employer_id, employer["name"]))
                vacansies = hh.get_vacancies(employer_id)
                for vacancy in vacansies:
                    if not vacancy["salary"]:        # Если зарплата не указана, заполняем нули
                        salary_from = 0
                        salary_to = 0
                    else:
                        salary_from = vacancy["salary"]["from"] if vacancy["salary"]["from"] else 0
                        salary_to = vacancy["salary"]["to"] if vacancy["salary"]["to"] else 0

                    cur.execute("INSERT INTO vacancy VALUES (%s, %s, %s, %s, %s, %s)", (vacancy["id"], vacancy["name"],
                                                                                        salary_from, salary_to,
                                                                                        vacancy["alternate_url"],
                                                                                        employer_id))
    conn.close()


# create_database("course_work3")
# create_tables("course_work3")
# insert_data("course_work3")

from src.utils import create_database, create_tables, insert_data
from src.db_manager import DBManager


db_name = "course_work3"
create_database("course_work3")
create_tables("course_work3")
insert_data("course_work3")

db_manager = DBManager(db_name)
print(db_manager.get_all_employers())
print(db_manager.get_avg_salary())
print(db_manager.get_vacancies_with_higher_salary())

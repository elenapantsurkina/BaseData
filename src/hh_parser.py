import requests


class HHParser:
    def __init__(self):
        self.__url = None
        self.__params = None

    def __get_request(self):
        """приватный метод подключения к АРI"""
        response = requests.get(self.__url, self.__params)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            raise Exception(f"Ошибка {response.status_code}: {response.text}")

    def get_employers(self):
        """Метод получения 10-ти работодателей, у которых есть открытые вакансии"""
        self.__url = "https://api.hh.ru/employers"
        self.__params = {
            "sort_by": "by_vacancies_open",
            "per_page": 10
        }
        return self.__get_request()

    def get_vacancies(self, employer_id):
        """Метод получения 50-ти вакансий для заданного работодателя"""
        self.__url = "https://api.hh.ru/vacancies"
        self.__params = {
            "employer_id": employer_id,
            "per_page": 50
        }
        return self.__get_request()


# hh = HHParser()
# print(hh.get_employers())
# comp_id = hh.get_employers()[0]["id"]
# print(hh.get_vacancies(comp_id))
# print(len(hh.get_vacancies(comp_id)))

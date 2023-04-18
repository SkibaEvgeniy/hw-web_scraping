# <a class="serp-item__title" data-qa="serp-item__title" target="_blank" 
# href="https://spb.hh.ru/vacancy/79482696?from=vacancy_search_list&amp;query=python"

# <span data-qa="vacancy-serp__vacancy-compensation" class="bloko-header-section-3">120 000 – 130 000 руб.</span>

# <a data-qa="vacancy-serp__vacancy-employer" class="bloko-link bloko-link_kind-tertiary" href="/employer/3306967?hhtmFrom=vacancy_search_list">ООО&nbsp;Mind&amp;Machine</a>

# <div data-qa="vacancy-serp__vacancy-address" class="bloko-text">Санкт-Петербург</div>

import requests
import lxml as lxml
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

def parsed(response_text):
    soup = BeautifulSoup(response_text, features='lxml')
    link = soup.find_all(class_="serp-item__title")
    city = soup.find_all(attrs={'class': "bloko-text", 'data-qa': "vacancy-serp__vacancy-address"})
    sallary = soup.find_all(attrs={'data-qa': "vacancy-serp__vacancy-compensation"})
    name_company = soup.find_all(attrs={'data-qa': "vacancy-serp__vacancy-employer"})
    
    processed_data = list()

    for (link_,city_,sallary_,name_company_) in zip(link,city,sallary,name_company):
        processed_data.append(
            {
                'link' : link_['href'],
                'city' : city_.text,
                'sallary': sallary_.text,
                'company' : name_company_.text
            }
        )
    return processed_data

if __name__ == "__main__":

    def get_headers():
        headers = Headers(browser='firefox', os='win')
        return headers.generate()
    
    response_text = requests.get(
        'https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=description&only_with_salary=true&text=Python+' \
        'django+flask&from=suggest_post&ored_clusters=true&enable_snippets=true', headers=get_headers()).text
    processed_data = parsed(response_text)

    with open("hh.json", 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, indent=5, ensure_ascii=False)

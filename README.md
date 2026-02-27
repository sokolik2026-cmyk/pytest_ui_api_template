# pytest_ui_api_template

## Шаблон для автоматизации тестирования на python

## Описание проекта 

Дипломный проект по автоматицации тестирования сервиса доставки(Яндекс/Магнит).

В проекте реализваны:
- UI-тесты авторизации, поиск товара и оформления заказа (Selenium + Page Object)
- API-тесты поиск магазинов и товаров (requests).
- Генерация отчетов в Allure
- Проверка качества кода линтером flake8 

### Шаги
1. Склонировать проект "git clone https://github.com/sokolik2026-cmyk/pytest_ui_api_template.git"
2. Установить все зависимости "pip install -r requirements.txt"
3. Запустить тесты "pytest"
4. Сгенирировать отчет "--alluredir=allure-results -s -v"
5. Открыть отчет " allure serve allure-results"
6. Проверить код flake8   .venv\Scripts\activate  ,  flake8 .

### Запуск тестов
- Все тесты:
  ```bash
  pytest --alluredir=allure-results -s -v
  ```
- Только UI-тесты:
  ```bash
  pytest -m "ui"-s --alluredir=allure-results -s -v
  ```
- Только API-тесты: 
  ```bash
  pytest -m "api" --alluredir=allure-results -s -v
  ```
- Сгенерировать и посмотреть отчет в браузере:
  ```bash
  allure serve allure-results
  ```
  
### Стек:
- pytest
- selenium
- webdriver manager
- requests
- _sqlalchemy_
- allure
- configparser
- json
- flake8

### Структура:
- ./test - тесты
     - test_api.py - API-тесты
     - test_ui.py - UI-тесты
- ./page - описание страницы
    - AuthPage.py - класс авторизации
    - CartPage.py - класс корзины
    - HomePage.py - класс главной страницы
    - SearchPage.py - класс страницы поиска
- ./api - хелперы по работе с API
    - YandexSearchAPI.py - класс для работы с API поиска Яндекса
- ./setup.cfg - настройки flake8
- ./utils — провайдер конфигурационных
    - config_reader.py — модуль для загрузки настроек UI и API тестов из файла conf.ini
- ./conf.ini — файл настроек (UI-URL, URL авторизации, логин, пароль, base_url для API)

### Полезные ссылки 
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore)
- [Про pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/.)
  
### Финальный проект по ручному тестированию 
- [Ссылка на проект](https://github.com/sokolik2026-cmyk/pytest_ui_api_template.git)
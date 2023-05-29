# wardrobe_organizer

    Wardrobe_organizer - приложение для систематизации вещей в гардеробе.
В нем можно хранить информацию о предметах и их использовании, объединять вещи 
в комплекты, фильтровать по разным категориям. Предусмотрена регистрация и авторизация.
    Проект реализован с помощью django templates, с использованием django-filters.
### _Запуск проекта в dev-режиме_

* Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:elenaindenbom/wardrobe_organizer.git
```
* Перейти в папку с проектом:
```
cd wardrobe_organizer
```
* Создать и активировать виртуальное окружение

для Linux или MacOS:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
для Windows:
```
python -m venv venv
```
```
source venv/Script/activate
```
* Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
* Перейти в папку wardrobe_organizer, и выполнить миграции:
```
cd wardrobe_organizer
```
python3 manage.py migrate
```
Создайте суперюзера 
```
python3 manage.py createsuperuser.
```
* Запустить проект:
```
python3 manage.py runserver
```
Для корректного создания предметов через фронт, надо создать несколько типов 
предметов в базе через админку.
```
_*  в Windows вместо команды "python3" использовать "python"_

### _Автор проекта_
Инденбом Елена

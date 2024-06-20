AAA Logo-detection Application
========================

Описание
========

В этом репозитории находятся файлы для веб приложения для курсового проекта в Академии Аналитиков Авито.

Приложение позволяет загрузить изображение, детектировать на нём логотипы и распознать их.

Название команды:

Состав команды:
* Миронов Андрей (капитан)
* Омар Ханкишиев
* Олег Фатеев
* Илья Ломоносов

Проект: Детекция и распознавание логотипов

Цели: см. purpose.md

Требования
==========

Для работы сервиса используется Docker.

Установка
=========

Соберите образ для докера:

    make build

Этот шаг будет выполняться автоматически при каждом запуске.

Запуск
======

Для запуска приложения в продакшн режиме:

    make run


Тестирование
============

Для запуска тестов::

    make test


Прохождение тестов является обязательными критерием приёмки домашнего задания.


Линтеры
=======

Для запуска линтеров:

    make lint

или каждый по отдельности:

    make black
    make flake8
    make pycodestyle
    make pylint
    
Удаление
=======

Для удаления Docker образа, используйте команду:

    make clean

Опиcание
========
Для получения описания команд:

    make help

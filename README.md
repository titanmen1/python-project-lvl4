### Hexlet tests and linter status:
[![Actions Status](https://github.com/titanmen1/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/titanmen1/python-project-lvl4/actions)
[![Actions Status](https://github.com/titanmen1/python-project-lvl4/workflows/CI/badge.svg)](https://github.com/titanmen1/python-project-lvl4/actions)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a3cce188b07a0ff172fd/test_coverage)](https://codeclimate.com/github/titanmen1/python-project-lvl4/test_coverage)

Приложение развернуто на Heroku: https://aqueous-plateau-38045.herokuapp.com/

## Функциональные возможности
- приложение настроено на работу с базой данных PostgreSQL;
- реализована авторизация пользователей;
- в системе может быть зарегистрировано множество пользователей;
- пользователь после авторизации может создавать себе задачу, указав для этого ее название, описание, статус, назначить 
исполнителя из списка зарегистрированных пользователей и при необходимости выбрать один или несколко тегов из списка;
- пользователь может редактировать содержимое любой своей или чужой задачи;
- пользователь может удалить любую из ранее созданных задач;
- пользователь может вывести список задач с возможностью фильтрации по статусу, автору, исполнителю, а также по тегам;
- пользователь может может добавлять, редактировать и изменять статусы, а также добавлять теги.

## Запуск приложения
Активируйте виртуальное окружение и установите необходимые зависимости, выполнив команду:
    
    poetry install
    
Замениете название файла .env.example на .env и задайте свои значения переменных внутри этого файла.

После этого сделайте и примените миграции командой:

    make migrations
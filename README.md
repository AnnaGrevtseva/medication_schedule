**Расписание приема лекарств**

Запуск АПИ осуществляется командой python main.py из директории app.

По умолчанию АПИ запускается на http://localhost:8000/. Сваггер доступен на http://{host}:{port}/docs

До запуска АПИ необходимо:

1) Создать виртуальное окружение и установить зависимости, используя файл requirements.txt.

   Например, для Windows: python venv -m venv - создаем виртуальное окружение, pip install -r requirements.txt - устанавливаем зависимости
2) Скопировать файл .env.example, переименовать его в .env и заполнить все настройки. 
**Внимание**, переменная NEXT_TAKINGS задает ближайший период времени для приема лекарств **в минутах** и является **целым числом**!
3) АПИ использует в качестве БД PostgreSQL, необходимо установить на ПК или использовать Docker-контейнер с данной БД.

   
Краткое описание:

Сервис позволяет добавлять расписание приема лекарств. 
По указанным данным рассчитывается график приема таблеток для каждого пользователя. 
По указанному пользователю можно запросить идентификаторы всех его расписаний, график приема препарата для каждого расписания.
Также предоставляется информация о ближайшем приеме лекарств (период задается в настройках сервиса)
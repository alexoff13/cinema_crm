# cinema_crm
## Ссылки на информацию, которая может пригодится в процессе разработки + заметки
1. Документация по бутстрапу:
   1. https://bootstrap-flask.readthedocs.io/en/stable/macros/#render-table
   2. https://bootstrap-table.com/docs/api/table-options/
2. Нав-бар для пользователей
   1. https://stackoverflow.com/questions/70010059/how-do-i-dynamically-extend-in-jinja2-to-render-different-nav-bars

3. Использование SQL - представлений в flask-sqlalchemy
   1. Создаем представление в самой базе данных
   2. Создаем класс, наследуемый от db.Model, где __tablename__=<название представления в базе данных>
   3. Прописываем типы колонок как в обычной таблице, при этом указываем первичный ключ
   4. Пишем запросы также как к обычой таблице
# cinema_crm
1. Миграции:
   ```sh
    flask db init  #запускается один раз для инициализации бд
    flask db migrate -m "<message>"  
    flask db upgrade
   ```
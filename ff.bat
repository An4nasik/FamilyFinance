@echo off
REM setup_project.bat — создаёт структуру проекта FamilyFinance

echo Создаём папки...
mkdir app
mkdir app\models
mkdir app\schemas
mkdir app\repositories
mkdir app\services
mkdir app\api
mkdir app\middleware
mkdir tests

echo Создаём файлы...

REM корневые модули
type NUL > app\config.py
type NUL > app\database.py
type NUL > app\logging_config.py
type NUL > app\main.py

REM модели
type NUL > app\models\__init__.py
type NUL > app\models\base.py
type NUL > app\models\entities.py

REM схемы
type NUL > app\schemas\__init__.py
type NUL > app\schemas\family.py
type NUL > app\schemas\user.py
type NUL > app\schemas\transaction.py

REM репозитории
type NUL > app\repositories\__init__.py
type NUL > app\repositories\family_repo.py
type NUL > app\repositories\user_repo.py
type NUL > app\repositories\transaction_repo.py

REM сервисы
type NUL > app\services\__init__.py
type NUL > app\services\family_service.py
type NUL > app\services\user_service.py
type NUL > app\services\transaction_service.py

REM роутеры
type NUL > app\api\__init__.py
type NUL > app\api\families.py
type NUL > app\api\users.py
type NUL > app\api\transactions.py

REM middleware
type NUL > app\middleware\__init__.py
type NUL > app\middleware\logging.py

REM тесты
type NUL > tests\__init__.py
type NUL > tests\test_families.py

echo Структура проекта создана успешно!
pause
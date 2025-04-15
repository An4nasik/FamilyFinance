# Как это чудо-юдо запустить
Ну тут дело такое, относительно не сложное:
  * Устанавливаем docker и docker-compose
  * Скачиваем дирректорию [app](https://github.com/An4nasik/FamilyFinance/tree/for-docker/app)
  * Заходим в нее в терминале
  * Прописываем:
  *  ```
     docker-compose build
     docker-compose up
     ```
  * Верим что все собралось правильно и запускаем контейнер
    
PS. Я конечно выложил образ на [dockerhub](https://hub.docker.com/r/an4nasik/famiyfinance/tags), а вот образ [БД](https://hub.docker.com/_/mongo), но че дальше делать, я не особо понял

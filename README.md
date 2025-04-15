# Версия для немного скучных:

## Как это чудо-юдо запустить
Ну тут дело такое, относительно не сложное:
  1. Устанавливаем docker и docker-compose
  2. Скачиваем дирректорию [app](https://github.com/An4nasik/FamilyFinance/tree/for-docker/app)
  3. Заходим в нее в терминале
  4. Прописываем:
      ```bash
     docker-compose build
     docker-compose up
     ```
  5. Верим что все собралось правильно и запускаем контейнер
    
P.S. Я конечно выложил образ на [dockerhub](https://hub.docker.com/r/an4nasik/famiyfinance/tags), а вот образ [БД](https://hub.docker.com/_/mongo), но че дальше делать, я не особо понял

# Версия для нормальных людей:

## 🐳 Как запустить это чудо-юдо? (Да, это проще, чем кажется!)  

**🚀 Шаги для победы над технологиями:**  

1. **📦 Установите Docker и Docker Compose**  
   - Если вдруг не установлено — [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/) вам в помощь.  
   - *«Но я уже всё установил(а)!»* — тогда переходим дальше! ✅  

2. **💾 Скачайте волшебную папку [app](https://github.com/An4nasik/FamilyFinance/tree/for-docker/app)**  
   ```bash
   git clone https://github.com/An4nasik/FamilyFinance.git --branch for-docker
   ```  

3. **📂 Зайдите в папку через терминал**  
   ```bash
   cd FamilyFinance/app  # Там, где живёт docker-compose.yml 🗂️
   ```  

4. **🌀 Выполните магические заклинания:**  
   ```bash
   # Собираем образы (кофе? печеньки? ждём... ☕)
   docker-compose build  

   # Запускаем всё это великолепие! 🎉
   docker-compose up -d  # Флаг -d — чтобы не залипать в терминале
   ```  

5. **🔮 Проверяем, что всё работает:**  
   ```bash
   docker ps  # Должны быть два счастливых контейнера 🐋
   ```  

---

**🌟 Важные нюансы:**  
- **🐋 Образы уже на Docker Hub:**  
  - [an4nasik/famiyfinance](https://hub.docker.com/r/an4nasik/famiyfinance/tags) — ваш шедевр.  
  - [mongo](https://hub.docker.com/_/mongo) — база данных (она подтянется сама из композа! 🧙).  

- **💡 А что дальше?**  
  - Если контейнеры запустились — открывайте браузер и проверяйте `http://localhost:8000` (порт смотрите в `docker-compose.yml`).  
  - Хотите посмотреть логи? → `docker-compose logs -f`.  

---

**📌 P.S.**  
*«Че дальше делать?»* — а дальше можно:  
- 🎨 Радоваться, что всё работает.  
- 🐞 Если не работает — кричать «ААА!» и звать меня в телегу.  
- ☕ Или просто пить кофе, пока Docker делает всю работу.  

**Удачи! И да пребудет с вами Сила (и контейнеры)!** 🚀  

--- 

*P.P.S. Если что-то пошло не так — проверьте, не съел ли ваш кот кабель интернета. 🐱*  

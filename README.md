# Скрипт по созданию коротких ссылок и проверки количества переходов
Скрипт формирует краткую ссылку для адреса сайта с использованием сервиса [bitly.com](https://bitly.com), с возможностью вывода информации по количеству переходов для краткой ссылки.


### Требования
- Для работы необходим Python 3.6+
- Подключение к сети Интернет

### Как установить и использовать
- Скачиваем скрипт с [github](https://github.com/dumbturtle/api2)
- Устанавливаем необходимые пакеты: 

```$pip install -r requirements.txt```
- Переименовываем `.env_template` в `env`
- В файле `.env` необходимо прописать свой BITLY_API_TOKEN полученный на сайте [bitly.com](https://bitly.com) 
- Запускаем скрипт:  

```$python bitly.py https://google.com``` 
- Запускаем скрипт для проверки количества переходов: 

```$python bitly.py https://bit.ly/39sujsV```

Если при запуске возникнет ошибка, будет выведено соответствующее сообщение в консоли.
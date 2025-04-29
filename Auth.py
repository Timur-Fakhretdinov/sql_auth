import mysql.connector
import cfg
import requests
import random
import hashlib
# подключаемся к дб
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1"
)
# print(mydb)
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE if not exists ABC_USERS")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1",
  database="ABC_USERS"
)
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, phone VARCHAR(255), password VARCHAR(255), firstname VARCHAR(25), lastname VARCHAR(25))")



# проверка существования номера в бд
phone = input('Введите ваш телефон: ')

mycursor = mydb.cursor()
mycursor.execute(f"SELECT phone FROM users WHERE phone = '{phone}'")
myresult = mycursor.fetchone()

if myresult:
    password = hashlib.sha256(input('Введите ваш пароль: ').encode()).hexdigest()
    mycursor.execute(f"SELECT COUNT(*) FROM users WHERE password = '{password}' and phone = '{phone}'")
    myresultP = mycursor.fetchone()

    if myresultP[0] == 1:
        temp = random.choice(cfg.fruits_and_vegetables)
        for i in range(1):
            params = {
                'key': cfg.key,
                'phone': phone,
                'message': temp,
                'device': cfg.device,
                'sim': '1',
            }

            resp = requests.post('https://smstel.ru/api/send', params=params)
            # print(resp.text)
        confirm = input('введите код из смс: ')
        if confirm == temp:
            print('вы авторизованы')
        else:
            print('код не верный')
    else:
        print('Неверный пароль.')


# регистрация
else:
    print('Номер не найден в базе данных.пройдите регистрацию')
    mycursor = mydb.cursor()
    sql = "INSERT INTO users (phone, password, firstname, lastname) VALUES (%s, %s, %s, %s)"
    val = (f'{phone}', hashlib.sha256(input('Придумайте ваш пароль: ').encode()).hexdigest(), input('ввдедите ваше имя: '), input('ввдедите вашу фамилию: '))
    mycursor.execute(sql, val)
    mydb.commit()
    print("вы Варегестрированы, теперь залогиньтесь.")


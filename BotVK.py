import vk_api, sqlite3, requests, json
from datetime import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

class BotVK:
    """
    Класс BotVK.
    """
    def __init__(self):
        """
        Инициализирует переменные.

        Атрибуты
        --------
        Token_weather : string
            Токен openweathermap. (Значение '')
        """
        self.Token_weather = ''
    
    def get_weather(self):
        """
        Делает запрос к openweathermap.

        Возврат
        -------
        string
            Температура.
        bool
            Возвращает False.

        Ошибки
        ------
        requests.exceptions.RequestException
            Возникает при отправке get запроса.
        Exception
            Возникает при обращении по ключю в словаре.
        response.status_code
            Возникает если запрос выполнен не успешно.
        """
        url = f'http://api.openweathermap.org/data/2.5/weather?lat=55.15&lon=61.43&appid={self.Token_weather}&units=metric'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                try:
                    data = response.json()
                    temp = data['main']['temp']
                    return f"{temp} °C"
                except Exception as err:
                    print(err)
                    return False
            else:
                print(response.text)
                return False
        except requests.exceptions.RequestException as e:
            print(e)
            return False

       
    def query_to_db(self, id_user=None, date=None):
        """
        Делает запрос к базе данных.

        Параметры
        ---------
        id_user : string
            id пользователя.
        date : date_time
            Время обращения.
        
        Возврат
        -------
        items : array_like
            Массив с выборкой из БД.
        bool
            Возвращает True при вставке в БД.
        bool
            Возвращает False при ошибке.

        Ошибки
        ------
        sqlite3.Error
            Возникает при создании, подключении или чтении БД.
        """
        try:
            conn = sqlite3.connect('SQL/data.db')        
            c = conn.cursor()
            if id_user==None:
                c.execute('''CREATE TABLE if not exists users (id int auto_increment primary key,id_user int, date datetime)''')
                c.execute("SELECT id_user,date  FROM users")
                items = c.fetchall()
            else:
                c.execute("INSERT INTO users (id_user,date) VALUES (?,?)",(id_user,date,))
                conn.commit()
            c.close()
            conn.close()
            if id_user==None:
                return items
            else:
                return True
        except sqlite3.Error as err:
            print(err)
            return False

    def print_data(self):
        """
        Выводит информацию из БД.

        Возврат
        -------
        bool
            Возвращает True.
        bool
            Возвращает False при ошибке.
        """
        arr = self.query_to_db()
        if arr == False:
            return False
        else:
            for item in arr:
                print('Пользователь с id:', item[0], 'Время:',item[1])
            return True

    def main(self):
        """
        Основная функция, которая вызывает все остальные.

        Ошибки
        ------
        vk_api.VkApiError
            Возникает если не существует метода или сообщение не было отправлено пользователю.
        vk_api.AuthError
            Возникает если произошла ошибка при авторизации.
        OSError
            Возникает если произошла сетевая ошибка.
        IOError
            Возникает если не существует файла конфигурации.
        """
        tokens = {}
        try:
            exec(open("tokens.py").read(),tokens)
            vk = vk_api.VkApi(token = tokens['token'])
            longpoll = VkLongPoll(vk)
            vk = vk.get_api()
            self.Token_weather = tokens['tokenWeather']
        except (vk_api.AuthError,OSError,IOError) as err:
            print(err)
            return
        
        if not self.print_data():
            return
        try:  
            while True:
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                        if event.text == 'Погода':
                            info = self.query_to_db(event.user_id, datetime.now())
                            if not info:
                                return
                            weather = self.get_weather()
                            if weather:
                                vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = f'Температура в Челябинске {weather}' )
                                print('id пользователя: ', event.user_id, 'Время:', datetime.now())
                            else:
                                print(info)
                                return
                    continue
        except (vk_api.VkApiError) as err:
            print(err)
            return

if __name__ == '__main__':
    bot = BotVK()
    bot.main()
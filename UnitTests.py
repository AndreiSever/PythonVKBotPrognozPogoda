import unittest
from BotVK import BotVK
from datetime import datetime
import tokens

class Test(unittest.TestCase):
    """
    Класс тестирования методов класса BotVK.
    """
    def test_get_weather(self):
        """
        Проверяет запрос к openweathermap.
        """
        bot = BotVK()
        bot.Token_weather = tokens.tokenWeather
        res = bot.get_weather()
        self.assertEqual(isinstance(res, str), True)
        
    def test_query_to_db_insert(self):
        """
        Проверяет запрос insert.
        """
        bot = BotVK()
        res = bot.query_to_db(1, datetime.now())
        self.assertEqual(res, True)
    
    def test_query_to_db_select(self):
        """
        Проверяет запрос select.
        """
        bot = BotVK()
        res = bot.query_to_db()
        ls = isinstance(res, list)
        self.assertEqual(ls, True)
        
if __name__ == '__main__':
    unittest.main()

#импортируем необходимые нам библиотеки:
#библиотеку дла работы с телеграмом
import telebot as tb
from telebot import types
#библиотеку для работы с моделями
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import sessionmaker
#библиотеку для работы с браузером
import webbrowser as wb


#создаем соединение с нашей базой данных
engine = db.create_engine('sqlite:///events.db')
#создаем объект таблицы из базы данных
events_database = declarative_base()
events_database.metadata.create_all(engine)
#подтягиваем наши данные из таблицы
events_database.metadata.bind = engine
#создаем сессию
DBSession = sessionmaker(bind=engine)
session = DBSession()

#создаем объект для работы с данными для добавления в бд
class Events(events_database):
    #присваиваем название таблице
    __tablename__ = 'events'

    #создаем столбцы как в нашей таблице в бд для дальнейшего добавления данных
    #для названия мероприятия
    event_name = db.Column(db.Text, primary_key=True, nullable=False)
    #для его места
    event_place = db.Column(db.Text, nullable=False)
    #для его описания
    description = db.Column(db.Text, nullable=False)
    #для его даты
    date = db.Column(db.Text, nullable=False)

#создаем словарь в котоый мы будем записывать данные чтобы в дальнешем добавить их в бд
event_info = {"event_name": "",
              "event_place": "",
              "description": "",
              "date": ""}

#создаем соединение с нашим ботом с помощью его токена
bot = tb.TeleBot("6353187958:AAGkofC11wkjhiymqjtnSDxJAwAj2M44bhQ")

#создаем словарь для определения месяцев
months = {"1": "янв",
        "2": "февр",
        "3": "март",
        "4": "апр",
        "5": "май",
        "6": "июн",
        "7": "июл",
        "8": "авг",
        "9": "сент",
        "10": "окт",
        "11": "нояб",
        "12": "дек"
}

#создаем функцию срабатывающую при комманде старт
@bot.message_handler(commands=['start'])
def greet(message):
    #создаем объект класса для отображения кнопок под полем ввода пользователя
    markup = types.ReplyKeyboardMarkup()
    #создаем наши кнопки
    create_event = types.KeyboardButton("Создать событие✍")
    see_events = types.KeyboardButton("Ближайшие события👀")
    open_site = types.KeyboardButton("Открыть сайт🔍")
    #размещаем их в определенном порядке
    markup.row(create_event, see_events)
    markup.row(open_site)
    #отправляем приветсвенное сообщение и отображаем кнопки
    bot.send_message(message.chat.id, f"<b>Здравствуйте {message.from_user.first_name}👋</b>", parse_mode="html", reply_markup=markup)
    bot.send_message(message.chat.id, "🦉Рады приветствовать вас в нашем телеграм-боте 🔍<b>Найди в 36</b>🔍\n"
                        "🦉Он является дополнением к <b>сайту</b> Найди в 36\n"
                        "🦉Здесь вы сможете <b>посмотреть</b> ближайшие мероприятия и <b>создать</b> свои собственные🎫\n"
                        "🦉Для того, чтобы посмотреть весь список комманд используйте <a>/commands</a>", parse_mode="html")


#создаем функцию срабатывающую при команде коммандс
@bot.message_handler(commands=['commands'])
def command(message):
    #выводим список комманд
    bot.reply_to(message, "Вот список комманд, которые вы можете использовать\n"
                 "🦉Создать мероприятие <a>/createevent</a>\n"
                 "🦉Посмотреть ближайшие мероприятия <a>/upcomingevents</a>\n"
                 "🦉Получить ссылку на сайт <a>/getlink</a>\n"
                 "🦉Сразу открыть сайт <a>/opensite</a>", parse_mode="html")


#создаем функцию для отображения ближайших событий
@bot.message_handler(commands=['upcomingevents'])
def upcoming_events(message):
    #создаем объект класса для кнопок под сообщением
    markup = types.InlineKeyboardMarkup()
    #создаем 12 кнопок для каждого названия месяца с одинаковым началок callback_data для упрощенной работы
    m1 = types.InlineKeyboardButton("Январь", callback_data="watch_1")
    m2 = types.InlineKeyboardButton("Февраль", callback_data="watch_2")
    m3 = types.InlineKeyboardButton("Март", callback_data="watch_3")
    m4 = types.InlineKeyboardButton("Апрель", callback_data="watch_4")
    m5 = types.InlineKeyboardButton("Май", callback_data="watch_5")
    m6 = types.InlineKeyboardButton("Июнь", callback_data="watch_6")
    m7 = types.InlineKeyboardButton("Июль", callback_data="watch_7")
    m8 = types.InlineKeyboardButton("Август", callback_data="watch_8")
    m9 = types.InlineKeyboardButton("Сентябрь", callback_data="watch_9")
    m10 = types.InlineKeyboardButton("Октябрь", callback_data="watch_10")
    m11 = types.InlineKeyboardButton("Ноябрь", callback_data="watch_11")
    m12 = types.InlineKeyboardButton("Декабрь", callback_data="watch_12")
    #размещаем их в определенном порядке
    markup.add(m1, m2, m3)
    markup.add(m4, m5, m6)
    markup.add(m7, m8, m9)
    markup.add(m10, m11, m12)
    #открываем файл с фотографией
    photo = open("upcomingevents.jpg", "rb")
    #выводим ее
    bot.send_photo(message.chat.id, photo)
    #выводим сообщение и отображаем кнопки
    bot.reply_to(message, "🦉Для того, чтобы посмотреть ближайшие события, выберите интересующий вас месяц", parse_mode="html", reply_markup=markup)


#создаем функцию для создания событий
@bot.message_handler(commands=['createevent'])
def createevent(message):
    #выводим пользователю сообщение с подробными инструкциями по добавлению названия
    bot.reply_to(message, "<b>🦉Отлично, давайте добавим событие</b>\n Вводите все пожалуйста по шаблону, иначе события не будут корректно отображаться", parse_mode="html")
    bot.send_message(message.chat.id, "Для начала введите его название в следующем формате \n"
                     "Название: (ваше название)\n", parse_mode="html")
    #применяем следующую функцию
    bot.register_next_step_handler(message, add_event_name)


#создаем функцию в которой мы будем добавлять название события и запрашивать его место
def add_event_name(message):
    #делаем переменную глобальной для ее изменения
    global event_info
    try:
        id = message.chat.id
        text = message.text
        #берем все символы идущие после "Название: "
        event_name = text[10:]
        #добавляем в словарь
        event_info["event_name"] = event_name
        #отправляем пользователю сообщение с инструкцией по добавлению места
        bot.send_message(id, "🦉Прекрасно! Давайте добавим место, чтобы ребята знали куда идти, в следующей форме\n" "Место: (место *подробно корпус этаж или кабинет при наличии)")
        #применяем нашу следующую функцию
        bot.register_next_step_handler(message, add_event_place)
    #обрабатываем неккоректный ввод пользователя и даем возможность начать заново
    except Exception:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Начать сначала", callback_data="again"))
        bot.reply_to(message, 'Ой, что-то пошло не так\n'
                              "Попробуйте сначала", reply_markup=markup)


#создаем функцию для добавления места события
def add_event_place(message):
    global event_info
    try:
        id = message.chat.id
        text = message.text
        #берем все символы после "Место: "
        event_place = text[7:]
        #добавляем место в словарь
        event_info["event_place"] = event_place
        #отправляем сообщение с инструкцией по добавлению описания
        bot.send_message(id,
                     "🦉Теперь давайте добавим краткое описание события в следующей форме\n" "Описание: (опишите кратко это мероприятие, что нужно с собой взять)")
        #применяем следующую функцию
        bot.register_next_step_handler(message, add_description)
    #обрабатываем неккоректный ввод
    except Exception:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Начать сначала", callback_data="again"))
        bot.reply_to(message, 'Ой, что-то пошло не так\n'
                              "Попробуйте сначала", reply_markup=markup)

def add_description(message):
    global event_info
    try:
        id = message.chat.id
        text = message.text
        #берем все символы после "Описание: "
        description = text[10:]
        #добавляем в словарь
        event_info['description'] = description
        bot.send_message(id, event_info["event_name"])
        #отправляем сообщение с инструкцией по добавлению даты
        bot.send_message(id,
                     "🦉Ну и наконец давайте добавим дату и время в следующем виде\n" "Дата: (число) (месяц словом в именительном падеже) в (время начала)")
        #применяем следующую функцию
        bot.register_next_step_handler(message, add_time)
    #обрабатываем исключение
    except Exception:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Начать сначала", callback_data="again"))
        bot.reply_to(message, 'Ой, что-то пошло не так\n'
                              "Попробуйте сначала", reply_markup=markup)


#создаем функцию для добавления времени
def add_time(message):
    global event_info
    try:
        #создаем объект поля кнопки
        markup = types.InlineKeyboardMarkup()
        #создаем кнопку при нажатии на которую событие добавится в бд
        markup.add(types.InlineKeyboardButton("Готово!", callback_data="add_event"))
        id = message.chat.id
        text = message.text
        #берем все символы после "Дата: "
        time = text[6:]
        #добавляем их в словарь
        event_info['date'] = time
        #отправляем сообщение о завершении заполнения данных с кнопкой
        bot.send_message(id,
                     "🦉Ура! Мы все заполнили! Теперь обязательно нажмите на кнопку внизу, иначе ваше событие не добавится", reply_markup=markup)
    #обрабатываем ошибки
    except Exception:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Начать сначала", callback_data="again"))
        bot.reply_to(message, 'Ой, что-то пошло не так\n'
                              "Попробуйте сначала", reply_markup=markup)


#создаем функцию срабатывающую при нажатии кнопок под сообщениями
@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    global event_info
    #обрабатываем случай нажатия на кнопку "Готово!"
    if callback.data == 'add_event':
        #заполняем объект класса события данными из словаря
        event = Events(event_name=event_info['event_name'], event_place=event_info["event_place"], description=event_info['description'], date=event_info['date'])
        #добавляем их в таблицу
        session.add(event)
        #завершаем сессию
        session.commit()
        bot.edit_message_text("🦉Ваше событие добавлено!", callback.message.chat.id, callback.message.message_id)
    #обрабатываем нажатие на кнопку с месяцем
    if "watch" in callback.data:
        #по ключу в словаре берем нужную подстроку
        month = months[callback.data[6:]]
        #сохраняем результат
        results = session.query(Events).filter(db.func.like(f'%{month}%', Events.date)).all()
        #выводим пользователю все события в этом месяце по определенному шаблону
        for event in results:
           bot.send_message(callback.message.chat.id, f"<b>Название</b>: {event.event_name}\n<b>Место</b>: {event.event_place}\n<b>Описание</b>: {event.description}\n<b>Дата</b>: {event.date}", parse_mode="html")
        #если событий нет отправляем седующее
        if len(results) == 0:
            bot.send_message(callback.message.chat.id, "Увы, событий на этот месяц нет")
        #завершаем сессию
        session.commit()
    #обрабатываем нажатие на кнопку "Начать сначала"
    if callback.data == "again":
        #заново запускаем функцию по добавлению события
        bot.edit_message_text("Попробуем еще раз", callback.message.chat.id, callback.message.message_id)
        createevent(message=callback.message)


#создаем функцию для открытия сайта
@bot.message_handler(commands=['opensite'])
def opensite(message):
    wb.open("https://elisbeth.pythonanywhere.com/")


#создаем функцию для отправления ссылки на сайт
@bot.message_handler(commands=['getlink'])
def getsite(message):
    bot.reply_to(message, "🦉Вот ссылка на сайт Найди в 36 <a>https://elisbeth.pythonanywhere.com/</a>\n"
                 "🦉На нем вы сможете посмотреть карту школы и найти кабинет нужного вам учителя или класса", parse_mode="html")


#создаем функцию для обработки простого текста
@bot.message_handler()
def text(message):
    if message.text == "Открыть сайт🔍":
        #открываем сайт
        wb.open("https://elisbeth.pythonanywhere.com/")
    if message.text == "Ближайшие события👀":
        #запускаем функцию для вывода ближайших событий
        upcoming_events(message)
    if message.text == "Создать событие✍":
        #запускаем функцию для создания событий
        createevent(message)


#прописываем непрерывную работу кода
bot.polling(non_stop=True)
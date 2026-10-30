from aiogram import Bot, Dispatcher, executor, types 
import webbrowser
import asyncio
import aiohttp
import requests
from aiogram.types import ParseMode
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
import random
from aiogram.types import ReplyKeyboardRemove



TIMEZONE = ZoneInfo("Europe/Moscow")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

### РАСПИСАНИЕ НА НЕДЕЛЮ ###

schedule = {
    0: (
        "📚 Расписание на понедельник\n\n"
        "1. Разговоры о важном\n"
        "2. Алгебра\n"
        "3. Физическая культура\n"
        "4. Индивидуальный проект\n"
        "5. Английский язык\n"
        "6. Физика\n"
        "7. Вероятность и статистика",
    ),

    1: (
        "📚 Расписание на вторник\n\n"
        "1. ---\n"
        "2. ОБЗР\n"
        "3. Химия\n"
        "4. География\n"
        "5. Английский язык\n"
        "6. История\n"
        "7. Литература\n"
        "8. Геометрия"
    ),

    2: (
        "📚 Расписание на среду\n\n"
        "1. Обществознание(группа соц.эконом) / Информатика(группа тех)\n"
        "2. Русский язык\n"
        "3. Литература\n"
        "4. Алгебра\n"
        "5. Обществознание / Информатика\n"
        "6. Геометрия\n"
        "7. Обществознание(по группам)\n"
        "8. Обществознание(группа соц.эконом) / Информатика(группа тех.)"
    ),

    3: (
        "📚 Расписание на четверг\n\n"
        "1. ---\n"
        "2. Алгебра\n"
        "3. Геометрия\n"
        "4. Физическая культура\n"
        "5. Физика\n"
        "6. История\n"
        "7. Английский язык\n"
        "8. Россия — Мои горизонты"
    ),

    4: (
        "📚 Расписание на пятницу\n\n"
        "1. Обществознание(группа соц.эконом) / Информатика(группа тех)\n"
        "2. Русский язык\n"
        "3. Обществознание(группа соц.эконом) / Информатика(группа тех)\n"
        "4. Литература\n"
        "5. Право(группа соц.эконом) / Инженерная графика(группа тех)\n"
        "6. Биология"
    )
}


UNITS = {
    'мм': ('длина', 0.001),
    'см': ('длина', 0.01),
    'м': ('длина', 1),
    'км': ('длина', 1000),

    'мг': ('масса', 0.000001),
    'г': ('масса', 0.001),
    'кг': ('масса', 1),
    'т': ('масса', 1000),

    'с': ('время', 1),
    'мин': ('время', 60),
    'ч': ('время', 3600),

    "мл": ("объём", 0.001),
    "л": ("объём", 1),
}

def get_users():
    if not os.path.exists('users.txt'):
        return set()

    with open('users.txt', 'r', encoding= 'UTF-8') as file:
        return {
            int(line.strip())
            for line in file
            if line.strip().isdigit()
        }

def save_user(user_id):
    users = get_users()

    if user_id not in users:
        with open('users.txt', 'a', encoding= 'UTF-8') as file:
            file.write(f'{user_id}\n')


def delete_user(user_id):
    users = get_users()

    if user_id not in users:
        return False
    users.remove(user_id)

    with open('users.txt', 'w', encoding = 'UTF-8',) as file:
        for uid in users:
            file.write(f'{uid}\n')

    return True


    



bot = Bot(token = '8806768223:AAE6ytld9_pvFotqvQ3ytom4EQ79B-YkXoU')
dp = Dispatcher(bot)


@dp.message_handler(commands=['notif'])
async def nofif(message: types.Message):
    save_user(message.from_user.id)
    await message.answer('💤 Теперь каждый будний день в 7:00 по МСК тебе будет приходить уведомление с расписанием на сегодняшний день 💤')


@dp.message_handler(commands=['delnotif'])
async def delnotif(message: types.Message):
    user_id = message.from_user.id

    if delete_user(user_id):
        await message.answer('Ты отписался от уведомлений! Что бы подключить их обратно введите команду /notif')
    else:
        await message.answer('Ты не подписывался на уведомления!')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # save_user(message.from_user.id)
    await message.answer('Привет, ты попал в школьного бота, ознакомиться со всеми функциями ты можешь по команде "/info"\n Приятного времяпрепровождения в боте!')

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    await message.answer('<b>Команды и функционал бота:</b>\n\n'
    '👾 /help - Помощь по боту\n'
    '👾 /gdz - ГДЗ ссылки по предметам\n'
    '👾 /rasp - Расписание уроков для 10-го класса\n'
    '👾 /notif - Получение ежедневных напоминаний в 07:00 по мск с расписанием на сегодняшний день\n'
    '👾 /zvonok - Расписание звонков в школе\n'
    '👾 /sredball  - Высчитывание среднего балла, пример ввода: /sredball 5 4 2 5 \n'
    '👾 /coins - Игра в орел или решка\n'
    '👾 /memes - Выдает самую умную(тупую) шутку\n'
    '👾 /delnotif - Отключение уведомлений с расписанием(отключается до момента, пока вновь не введете команду "/notif")\n'
    '👾 /addwork - Добавить предстоящую контрольную/самостоятельную работу -\n Пример: "/addwork История 27.10.2026"\n<b>(ЕСЛИ РАБОТА ДЛЯ СОЦ.ЭКОНОМА ИЛИ ТЕХ, ТО ПОДПИСЫВАЙТЕ В СКОБОЧКАХ)</b> \n'
    '👾 /works - Список всех работ\n'
    '👾 /delwork - Удалить из списка какую-либо работу\n'
    '👾 /percent - высчитывает конкретный процент от конкретного числа. Пример: /percent 20 500 (20% от 500)\n'
    '👾 /convert - конвертация чисел(из кг в г | из ч в мин | и т.д.)' \
    '' \
    '' \
    '' \
    '' \
    '' \
    '' \
    ''
    '', parse_mode='HTML')

    await message.answer('<b>🛑 Мини гайд по командам:</b>\n\n'
    '👾 /notif - Подписываетесь на ежедневные увеломления в 07:00 по МСК с расписанием на день, отключить можно по команде /delnotif\n'
    '👾 /addwork | /works | /delwork - Команды для добавления/списка/удаления работа, убедительная просьба не баловаться этими командами, добавляет один - видят все.Бот создан с целью облегчения по школьным моментам.\n'
    '👾 /memes | /coins - Развлекательные команды, поиграть в орла и решку, пошутить "смешные шутки"\n'
    '👾 /convert - Переводит число из минут в час, из килограмм в граммы, и километров в метры и т.д\n'
    ''
    ''
    ''
    ''
    ''
    ''
    ''
    ''
    ''
    ''
    ''
    ''
    ''
    ''
    '', parse_mode='HTML')

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer('Если у вас случился баг или есть предложения по улучшению бота, то можете обратиться к @zarwexx')




def calculate_average(grades):
    return sum(grades) / len(grades)


@dp.message_handler(commands=['sredball'])
async def sredball(message: types.Message):
    try:
        grades = list(map(int, message.get_args().split()))

        if not grades:
            await message.answer('Укажи оценки через пробел: /sredball 5 5 3 1')
            return()

        average = calculate_average(grades)

        await message.answer(f'Твой средний балл: {average:.2f}')

    except ValueError:
        await message.answer('Вводи только числа /sredball 5 5 3 1')


@dp.message_handler(commands=['zvonok'])
async def zvonok(message: types.Message):
    await message.answer(f'<b> 👽 Расписание звонков: 👽</b>\n\n'
    '1 урок - 08:30 - 9:10\n'
    '🍷 Перемена 10 минут 🍷\n'
    '2 урок - 9:20 - 10:00\n'
    '🍷 Перемена 20 минут 🍷\n'
    '3 урок - 10:20 - 11:00\n'
    '🍷 Перемена 10 минут 🍷\n'
    '4 урок - 11:10 - 11:50\n'
    '🍷 Перемена 10 минут 🍷\n'
    '5 урок - 12:00 - 12:40\n'
    '🍷 Перемена 20 минут 🍷\n' \
    '6 урок - 13:00 - 14:40\n'
    '🍷 Перемена 10 минут 🍷\n' \
    '7 урок - 13:50 - 14:30\n'
    '🍷 Перемена 10 минут 🍷\n' \
    '8 урок - 14:40 - 15:20', parse_mode = ParseMode.HTML)


@dp.message_handler(commands=['rasp'])
async def rasp(message: types.Message):
    await message.answer(f'Вот расписание на неделю:\n\n'
    '<b> 📚 Понедельник 📚 </b>\n' \
    '1. Разговоры о важном\n 2. Алгебра\n 3. Физическая культруа\n 4. Индивидуальный проект\n 5. Английский язык\n 6. Физика\n 7. Вероятность и статистика\n\n'
    '<b> 📚 Вторник 📚 </b>\n'
    '1. ---\n 2. ОБЗР\n 3. Химия\n 4. География\n 5. Английский язык\n 6. История\n 7. Литература\n 8. Геометрия\n\n'
    '<b> 📚 Среда 📚 </b>\n'
    '1. Обществознание(группа соц.эконом) | Информатика(группа тех.)\n 2. Русский язык\n 3. Литература\n 4. Алгебра\n 5. Обществознание(группа соц.эконом) | Информатика(группа тех.)\n 6. Геометрия\n 7. Обществознание(по группам)\n 8. Обществознание(тех) | Информатика(соц.эконом)\n\n'
    '<b> 📚 Четверг 📚 </b>\n'
    '1. ---\n 2. Алгебра\n 3. Геометрия\n 4. Физическая культура\n 5.Физика\n 6. История\n 7. Английский язык\n 8. Россия Мои Горизонты\n\n'
    '<b> 📚 Пятница 📚 </b>\n'
    '1. Обществознание(группа соц.эконом) | Информатика(группа тех.)\n 2. Русский язык\n 3. Обществознание(группа соц.эконом) | Информатика(группа тех.)\n 4. Литература\n 5. Право(группа соц.эконом) | Инженерная графика(группа тех.)\n 6. Биология\n\n', parse_mode = ParseMode.HTML
    )


@dp.message_handler(commands = ['gdz'])
async def gdz(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('10 класс')
    # btn2 = types.KeyboardButton('9 класс')
    # btn3 = types.KeyboardButton('8 класс')
    # btn4 = types.KeyboardButton('7 класс')
    markup.row(btn1)
    # markup.row(btn2)
    # markup.row(btn3)
    # markup.row(btn4)


    await message.answer('Выбери свой класс:', reply_markup=markup)



@dp.message_handler(
    lambda message: message.text is not None
    and message.text.lower() in ['10 класс', '9 класс', '8 класс', '7 класс']
)



async def gdz_fync(message: types.Message):
    text = message.text.lower()
    await message.answer('Ожидайте появления сообщения', reply_markup=ReplyKeyboardRemove())

    if text == '10 класс':


        markup = types.InlineKeyboardMarkup(resize_keyboard=True)
        btn1 = types.InlineKeyboardButton('Алгебра', url = 'https://gdz.ru/class-10/algebra/alimov-15/')
        btn2 = types.InlineKeyboardButton('Геометрия', url = 'https://gdz.ru/class-10/geometria/atanasyan-10-11/')
        btn3 = types.InlineKeyboardButton('Русский Язык', url = 'https://gdz.ru/class-10/russkii_yazik/gusarova/')
        btn4 = types.InlineKeyboardButton('Английский Язык', url = 'https://gdz.ru/class-10/english/reshebnik-spotlight-10-afanaseva-o-v/')
        btn5 = types.InlineKeyboardButton('Биология', url = 'https://gdz.ru/class-10/biologiya/pasechnik-bazovyj-uroven/')
        btn6 = types.InlineKeyboardButton('Физика', url = 'https://gdz.ru/class-10/fizika/myakishev-10-izdanie/')
        btn7 = types.InlineKeyboardButton('Статистика и Вероятность', url = 'https://gdz.ru/class-10/matematika/bunimovich-bazovyj-i-uglublennyj-uroven/')
        btn8 = types.InlineKeyboardButton('Химия', url = 'https://gdz.ru/class-10/himiya/gabrielyan-sladkov-bazovij/')
        btn9 = types.InlineKeyboardButton('География', url = 'https://gdz.ru/class-10/geografiya/gladkij-bazovyj-uglublennyj-uroven/')
        btn10 = types.InlineKeyboardButton('ОБЗР', url = 'https://gdz.ru/class-10/obj/smirnov/')
        markup.row(btn1, btn2, btn3)
        markup.row(btn4, btn5, btn6)
        markup.row(btn7, btn8, btn9)
        markup.row(btn10)
        await message.answer('<b>Ответы могут отличаться из за года издания учебника!!!</b>', parse_mode = ParseMode.HTML)
        await message.answer('👻Выбирай нужный тебе предмет 👻', reply_markup=markup)



@dp.message_handler(commands=['coins'])
async def coins(message: types.Message):
    result = random.choice(["🦅 Орёл!", "🌟 Решка!", "🔪 Ребро!"])
    await message.answer(f'🪙 Монетка решила: {result}')


@dp.message_handler(commands=['memes'])
async def memes(message: types.Message):
    mems = ['Что сказал ноль восьмёрке? Классный ремень!',
    'Почему рыбы не ходят в школу? Потому что они и так на плаву.',
    'Почему компьютер замёрз? Потому что оставили Windows открытым.',
    'Как называется грустный сыр? Сыр-ота.',
    'Почему банан пошёл к врачу? Потому что плохо себя чистил.',
    'Что делает улитка на черепахе? Экстремально медленно едет.',
    'Почему скелет не пошёл на вечеринку? Ему было не с кем потанцевать.',
    'Как называется бумеранг, который не вернулся? Палка.',
    'Почему утка перешла дорогу? Потому что хотела на другую сторону.',
    'Что сказал чайник, когда устал? Я закипаю!',
    'Почему холодильник никогда не спорит? Он сохраняет холодную голову.',
    'Как называют собаку-волшебника? Лабракадабрадор.',
    'Почему книга пошла спать? У неё закончилась глава.',
    'Что делает кот за компьютером? Мышку ловит.',
    'Почему лук никогда не врёт? Потому что его легко раскрыть.',
    'Как называется рыба без глаз? Рба.']

    rans_memes = random.choice(mems)
    await message.answer (f'Вот самая смешная шутка в этом году:\n {rans_memes}')



@dp.message_handler(commands=['addwork'])
async def addwork(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer('🎮 Используй формат:\n "/addwork История 27.09.2026"')
        return
    work = parts[1].strip()

    if os.path.exists('works.txt'):
        with open('works.txt', 'r', encoding='UTF-8') as file:
            works = file.read().splitlines()

    else:
        works = []

    if work in works:
        await message.answer('⛔ Такая работа уже есть в списке!')
        return

    with open('works.txt', 'a', encoding='UTF-8') as file:
        file.write(work + '\n')

    await message.answer(f'🫶 Работа добавлена:\n{work}')


@dp.message_handler(commands=['delwork'])
async def del_work(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer('🪆 Укажи работу, которую надо удалить\n/delwork История 27.09.2026')
        return

    work = parts[1].strip()

    if not os.path.exists('works.txt'):
        await message.answer('🧸 Список работ пуст')
        return

    with open('works.txt', 'r', encoding='UTF-8') as file:
        works = file.read().splitlines()

    if work not in works:
        await message.answer('🧸 Такой работы нету в списке')
        return
    works.remove(work)

    with open('works.txt', 'w', encoding='UTF-8') as file:
        for item in works:
            file.write(item + '\n')
    await message.answer(f'🧸 Работа успешно удалена:\n{work}')


@dp.message_handler(commands=['works'])
async def show_works(message: types.Message):
    if not os.path.exists('works.txt'):
        await message.answer('⛔ Список работ пока-что пуст.')
        return

    with open('works.txt', 'r', encoding='UTF-8') as file:
        works = file.read().splitlines()
        if not works:
            await message.answer('⛔ Список работ пока-что пуст.')
            return

        text = '⛅ Список работ:\n\n'

        for i, work in enumerate(works, start=1):
            text += f'{i}. {work}\n'

        await message.answer(text)


@dp.message_handler(commands=['percent'])
async def percent(message: types.Message):
    args = message.get_args().split()

    if len(args) != 2:
        await message.answer('🔥 Напиши процент и число:\n\n' \
        '/percent 20 500\n' \
        '20% от 500')
        return

    try:
        percent = float(args[0].replace(",", "."))
        number = float(args[1].replace(",", "."))

        if not 0 <= percent <= 1_000_000:
            await message.answer('❌ Процент может быть от 1 до 1.000.000')
            return
        if abs(number) > 1e100:
            await message.answer('❌ Число слишком большое')
            return
        result = number * percent / 100

        await message.answer(f'<b> 🔥 Резульат: </b>\n{percent:g}% от {number:g} = {result:g}', parse_mode='HTML')

    except Exception:
        await message.answer('❌ Введи числа правильно!\n' \
        'Пример: /percent 20 500')




@dp.message_handler(commands=['convert'])
async def convert_units(message: types.Message):

    await message.answer(f'<b> Обозначение единиц: </b>\n' \
    '!! см - сантиметр\n' \
    '!! м - метры\n' \
    '!! км - километр\n' \
    '!! г - грамм\n' \
    '!! кг - килограмм\n' \
    '!! мин - минуты\n' \
    '!! с - секунда\n' \
    '!! ч - час\n' \
    '!! мл - миллилитр\n' \
    '!! л - литр' \
    '', parse_mode='HTML'
        )
    args = message.get_args().lower().split()

    if len(args) != 3:
        await message.answer('Укажи число, исходную и целевую единицу:\n\n' \
        '/convert 150 см м\n' \
        '/convert 5 км м\n' \
        '/convert 2500 г кг\n' \
        '/convert 3 ч мин\n' \
        '/convert 500 мл л\n' \
            )
        return
    try:
        value = float(args[0].replace(",", "."))
        source = args[1]
        target = args[2]

        if not abs(value) < float('inf') or abs(value) > 1e100:
            await message.answer('❌ Число слишком большое или некорректное')
            return

        if source in ('f', "°f") and target in ('c', '°c'):
            result = (value - 32) * 5 / 9
            await message.answer(f'{value:g} °F = {result:g} °C')
            return

        if source not in UNITS or target not in UNITS:
            await message.answer('❌ Неизвестная единица измерения.')
            return

        source_type, source_factor = UNITS[source]
        target_type, target_factor = UNITS[target]

        if source_type != target_type:
            await message.answer('❌ Нельзя перевести эти единицы друг в друга.')
            return

        result = value* source_factor / target_factor

        await message.answer(f'<b> 🪄 Результат перевода: </b> \n\n' \
        f'{value:g} {source} = {result:g} {target}', parse_mode='HTML')

    except ValueError:
        await message.answer('❌ Введи коррктное число.\n' \
        'Пример: /convert 2.5 км м')



        

# @dp.message_handler(commands=['translate'])
# async def translate(message: types.Message):
#     text = message.get_args()

#     if not text:
#         await message.answer('❌ Напишите текст после команды:\n' \
#         '"/translate Hello my friend"')
#         return
#     try:
#         result = GoogleTranslator(
#             source='auto',
#             target='ru'
#         ).translate(text)

#         await message.answer(f'👀 Перевод:\n\n{result}')

#     except Exception:
#         logging.exception("Ошибка переводчика")
#         await message.answer('❌ Не удалось перевести текст, попробуйте позже.')

   







async def dialy_notification():
    today = datetime.now(TIMEZONE).weekday()

    if today not in schedule:
        logging.info('Сегодня выходной')
        return

    text = schedule[today]
    users = get_users()

    logging.info("начинаю рассыдку. пользователей %s", len(users))

    for user_id in users:
        try:
            await bot.send_message(user_id, text)
            await asyncio.sleep(0.005)

        except Exception:
            logging.exception("не удалось отправить расписание пользователю %s", user_id)

    logging.info('рассылка завершена')



scheduler = AsyncIOScheduler(timezone=TIMEZONE)

async def on_startup(dispatcher):

    if not scheduler.running:
        scheduler.add_job(
            dialy_notification,
            trigger='cron',
            hour=7,
            minute=0,
            id = 'daily_schedule',
            replace_existing=True
        )
        scheduler.start()

    logging.info('бот запущен, рассылка назначена на 07:00')


async def on_shutdown(dispatcher):
    if scheduler.running:
        scheduler.shutdown(wait=False)

    await bot.close()


if __name__ == "__main__":
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
        




    




    
    
executor.start_polling(dp)
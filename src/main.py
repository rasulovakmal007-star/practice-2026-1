import telebot
from telebot import types
import random

# Укажите токен вашего телеграм-бота
TOKEN = "8789087980:AAFaJprDF1jCo3u8mgBchWeef7i_qTnTV_8"

bot = telebot.TeleBot(TOKEN)

# Состояния пользователей для викторины и теста цифровой гигиены
user_states = {}

# Вопросы эко-викторины
QUIZ_QUESTIONS = [
    {
        "question": "Какая главная опасность микропластика для организма человека?",
        "options": [
            "Он портит вкусовые качества еды",
            "Он накапливается в органах и может вызывать скрытые воспалительные процессы",
            "Он просто делает воду мутной на вид"
        ],
        "correct": 1,
        "explanation": "Микропластик проникает сквозь защитные барьеры организма, накапливается в тканях и может вызывать хронические воспаления и аллергические реакции."
    },
    {
        "question": "Какое время использования гаджетов перед сном считается безопасным для качественной выработки мелатонина?",
        "options": [
            "Использование гаджетов прямо в постели",
            "За 15 минут до выключения света",
            "Прекращение использования за 1-2 часа до сна"
        ],
        "correct": 2,
        "explanation": "Рекомендуется убирать экраны за 1-2 часа до сна, чтобы организм успел выработать мелатонин — гормон сна, выработку которого блокирует синий свет."
    },
    {
        "question": "Что оказывает наибольшее негативное влияние на качество питьевой воды в городских квартирах?",
        "options": [
            "Изношенные водопроводные трубы и ржавчина",
            "Естественный ил в реках",
            "Разведение рыбы в питьевых водохранилищах"
        ],
        "correct": 0,
        "explanation": "Даже если очистная станция выдает чистую воду, проходя через устаревшие ржавые городские коммуникации, вода собирает вредные примеси и металлы."
    }
]

# Вопросы теста цифровой гигиены
HYGIENE_QUESTIONS = [
    {
        "question": "1/3. Сколько часов в день в среднем вы проводите за экраном смартфона или компьютера?",
        "options": [
            "Менее 3 часов",
            "От 3 до 6 часов",
            "Более 6 часов"
        ],
        "points": [2, 1, 0]
    },
    {
        "question": "2/3. Пользуетесь ли вы смартфоном/планшетом уже находясь в постели перед сном?",
        "options": [
            "Никогда, откладываю устройство за час до сна",
            "Иногда листаю ленту новостей или соцсетей",
            "Да, регулярно использую до момента засыпания"
        ],
        "points": [2, 1, 0]
    },
    {
        "question": "3/3. Используете ли вы встроенный фильтр синего света («ночной режим») на своих устройствах в вечернее время?",
        "options": [
            "Да, он настроен автоматически по расписанию",
            "Иногда включаю вручную, когда устают глаза",
            "Нет, не пользуюсь этой функцией"
        ],
        "points": [2, 1, 0]
    }
]

ECO_TIPS = [
    "💧 *Фильтрация воды*: Пользуйтесь угольными фильтрами или системами обратного осмоса. Это эффективно очистит водопроводную воду от хлора, ржавчины и тяжелых металлов.",
    "🚫 *Микропластик в быту*: Никогда не разогревайте пищу в пластиковых контейнерах в микроволновой печи (даже если на них есть маркировка 'safe'). Под действием тепла пластик выделяет миллионы микрочастиц в еду. Используйте керамику или стекло.",
    "📱 *Световой фильтр*: Установите автоматическое включение режима чтения (фильтра синего спектра) на смартфоне после 19:00. Это снизит нагрузку на глаза и защитит ваш сон.",
    "🥤 *Отказ от одноразового пластика*: Купите многоразовую бутылку для воды из нержавеющей стали или стекла. Это не только уменьшит объем пластиковых отходов, но и обезопасит вас от вымывания токсичных соединений из одноразового ПЭТ-пластика.",
    "🌳 *Проветривание*: Воздух в помещении часто в 2-5 раз более загрязнен, чем на улице, из-за испарений мебели и бытовой химии. Проветривайте комнату минимум 3 раза в день по 10 минут.",
    "💤 *Спальня без гаджетов*: Попробуйте оставлять телефон на зарядку в другой комнате, а для пробуждения использовать обычный аналоговый будильник. Это убережет вас от ночных проверок уведомлений."
]

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_quiz = types.KeyboardButton("📝 Пройти эко-тест")
    btn_tips = types.KeyboardButton("💡 Получить эко-совет")
    btn_hygiene = types.KeyboardButton("💤 Тест цифровой гигиены")
    btn_site = types.KeyboardButton("🌐 О проекте и сайт")
    markup.add(btn_quiz, btn_tips, btn_hygiene, btn_site)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    user_states[chat_id] = {}
    
    welcome_text = (
        "👋 *Приветствуем вас в ЭкоМедиа Боте!*\n\n"
        "Данный бот разработан студентами первого курса Московского Политеха "
        "*Расуловым Акмалом* и *Кенешовым Эламаном* в рамках учебной практики.\n\n"
        "🍀 Наш бот посвящен *экологии человека* — влиянию окружающей и цифровой среды на здоровье.\n\n"
        "С помощью меню ниже вы можете:\n"
        "1. Проверить свои знания в эко-викторине.\n"
        "2. Узнать полезные советы по улучшению качества жизни.\n"
        "3. Проверить свой уровень цифровой гигиены.\n"
        "4. Ознакомиться с сайтом нашего проекта.\n\n"
        "Используйте клавиатуру для навигации!"
    )
    bot.send_message(chat_id, welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda message: message.text == "💡 Получить эко-совет")
def send_random_tip(message):
    tip = random.choice(ECO_TIPS)
    bot.send_message(message.chat.id, f"💡 *Полезный совет:*\n\n{tip}", parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "🌐 О проекте и сайт")
def send_site_info(message):
    info_text = (
        "🌐 *Проект «ЭкоМедиа»*\n\n"
        "Наш проект посвящен популяризации экологической культуры и гигиены среди молодежи. "
        "Мы исследуем такие важные темы, как вред микропластика, качество питьевой воды в мегаполисе "
        "и правила здорового сна в цифровую эпоху.\n\n"
        "🔗 *Посетите наш официальный веб-сайт:* [Перейти на сайт ЭкоМедиа](https://rasulovakmal007-star.github.io/practice-2026-1/site/index.html)\n\n"
        "Разработчики:\n"
        "• Расулов Акмал (Менеджер, Сценарист, SMM)\n"
        "• Кенешов Эламан (Видеограф, Монтажер, Дизайнер)"
    )
    bot.send_message(message.chat.id, info_text, parse_mode="Markdown", disable_web_page_preview=False)

# --- ЛОГИКА ЭКО-ТЕСТА ---
@bot.message_handler(func=lambda message: message.text == "📝 Пройти эко-тест")
def start_quiz(message):
    chat_id = message.chat.id
    user_states[chat_id] = {
        "mode": "quiz",
        "current_question": 0,
        "score": 0
    }
    send_quiz_question(chat_id)

def send_quiz_question(chat_id):
    state = user_states[chat_id]
    q_idx = state["current_question"]
    
    if q_idx >= len(QUIZ_QUESTIONS):
        # Викторина завершена
        score = state["score"]
        total = len(QUIZ_QUESTIONS)
        result_text = (
            f"🎉 *Викторина окончена!*\n\n"
            f"Вы ответили правильно на *{score}* из *{total}* вопросов.\n\n"
        )
        if score == total:
            result_text += "🏆 Отличный результат! Вы прекрасно разбираетесь в экологии человека!"
        elif score >= total / 2:
            result_text += "👍 Хороший результат. Вы знаете основы, но некоторые аспекты стоит изучить подробнее."
        else:
            result_text += "🧐 Есть над чем поработать! Воспользуйтесь разделом *Эко-советы*, чтобы узнать больше полезного."
            
        bot.send_message(chat_id, result_text, parse_mode="Markdown", reply_markup=get_main_keyboard())
        user_states[chat_id] = {}
        return
        
    q_data = QUIZ_QUESTIONS[q_idx]
    markup = types.InlineKeyboardMarkup()
    for idx, opt in enumerate(q_data["options"]):
        markup.add(types.InlineKeyboardButton(text=opt, callback_data=f"quiz_{idx}"))
        
    bot.send_message(chat_id, f"❓ *Вопрос {q_idx + 1}/{len(QUIZ_QUESTIONS)}:*\n\n{q_data['question']}", 
                     parse_mode="Markdown", reply_markup=markup)

# --- ЛОГИКА ТЕСТА ЦИФРОВОЙ ГИГИЕНЫ ---
@bot.message_handler(func=lambda message: message.text == "💤 Тест цифровой гигиены")
def start_hygiene_test(message):
    chat_id = message.chat.id
    user_states[chat_id] = {
        "mode": "hygiene",
        "current_question": 0,
        "score": 0
    }
    send_hygiene_question(chat_id)

def send_hygiene_question(chat_id):
    state = user_states[chat_id]
    q_idx = state["current_question"]
    
    if q_idx >= len(HYGIENE_QUESTIONS):
        # Тест завершен, выводим результаты
        score = state["score"]
        result_text = (
            f"📊 *Результаты теста цифровой гигиены:*\n\n"
            f"Ваш результат: *{score}* баллов из *6* возможных.\n\n"
        )
        if score >= 5:
            result_text += (
                "🟢 *Отличная цифровая гигиена!*\n"
                "Вы разумно используете технологии, успешно контролируете экранное время и бережете свой сон. Так держать!"
            )
        elif score >= 3:
            result_text += (
                "🟡 *Средний уровень.*\n"
                "У вас хорошие привычки, но есть над чем поработать. Постарайтесь откладывать телефон за час до сна и настроить автофильтр синего света."
            )
        else:
            result_text += (
                "🔴 *Критический уровень!*\n"
                "Ваш сон и здоровье могут быть под угрозой из-за избытка экранного времени перед сном. Синий свет подавляет выработку мелатонина. "
                "Рекомендуем жестко ограничить гаджеты в постели и использовать ночной режим на всех устройствах."
            )
            
        bot.send_message(chat_id, result_text, parse_mode="Markdown", reply_markup=get_main_keyboard())
        user_states[chat_id] = {}
        return
        
    q_data = HYGIENE_QUESTIONS[q_idx]
    markup = types.InlineKeyboardMarkup()
    for idx, opt in enumerate(q_data["options"]):
        markup.add(types.InlineKeyboardButton(text=opt, callback_data=f"hygiene_{idx}"))
        
    bot.send_message(chat_id, f"📱 *Тест цифровой гигиены*\n\n{q_data['question']}", 
                     parse_mode="Markdown", reply_markup=markup)

# --- ОБРАБОТКА callback-запросов (кнопки под сообщениями) ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    
    # Защита от устаревших сессий
    if chat_id not in user_states or not user_states[chat_id]:
        bot.answer_callback_query(call.id, text="Сессия устарела. Начните тест заново.")
        return
        
    state = user_states[chat_id]
    
    # Логика викторины
    if call.data.startswith("quiz_") and state.get("mode") == "quiz":
        ans_idx = int(call.data.split("_")[1])
        q_idx = state["current_question"]
        q_data = QUIZ_QUESTIONS[q_idx]
        
        # Убираем клавиатуру у отвеченного вопроса
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
        
        if ans_idx == q_data["correct"]:
            state["score"] += 1
            feedback = "✅ *Правильно!*\n\n"
        else:
            feedback = f"❌ *Неверно.* Правильный ответ: `{q_data['options'][q_data['correct']]}`\n\n"
            
        feedback += q_data["explanation"]
        bot.send_message(chat_id, feedback, parse_mode="Markdown")
        
        # Переход к следующему вопросу
        state["current_question"] += 1
        send_quiz_question(chat_id)
        
    # Логика цифровой гигиены
    elif call.data.startswith("hygiene_") and state.get("mode") == "hygiene":
        ans_idx = int(call.data.split("_")[1])
        q_idx = state["current_question"]
        q_data = HYGIENE_QUESTIONS[q_idx]
        
        # Начисляем баллы
        points_earned = q_data["points"][ans_idx]
        state["score"] += points_earned
        
        # Убираем клавиатуру
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
        
        # Переход к следующему вопросу
        state["current_question"] += 1
        send_hygiene_question(chat_id)
        
    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    print("Бот запускается...")
    bot.infinity_polling()

from multiprocessing.connection import answer_challenge

from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from gpt import ChatGptService
from util import *

async def start(update, cotext):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, cotext,"main")
    await send_text(update, cotext, text)
    await show_main_menu(update, cotext, {
        'start' : 'главное меню бота',
        'profile' : 'генерация Tinder - профиля 😎',
        'opener' : 'сообщение для знакомства 🥰',
        'message' : 'переписка от вашего имени 😈',
        'date' : 'переписка со звездами 🔥',
        'gpt' : 'задать вопрос чату GPT 🧠'
    })

async def gpt(update, cotext):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, cotext,"gpt")
    await send_text(update, cotext, text)

async def gpt_dialog(update, cotext):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, cotext, answer)

async def date(update, cotext):
    dialog.mode = "date"
    text = load_message("date")
    await send_photo(update, cotext,"date")
    await send_text(update, cotext, text)
    await send_text_buttons(update, cotext, "Запустить?", {
        "date_grande": "Ариана Гранде",
        "date_robbie": "Марго Робби",
        "date_zendaya": "Зендея",
        "date_gosling": "Райан Гослинг",
        "date_hardy": "Том Харди",
    })

async def date_dialog(update, cotext):
    text = update.message.text
    my_message = await send_text(update, cotext, "Девушка набирает сообщение...")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)


async def date_button(update, cotext):
    query = update.callback_query.data
    await update.callback_query.answer()
    await send_photo(update, cotext, query)
    await send_text(update, cotext, "Отличный выбор! Пригласите девушку (парня) на свидание за 5 сообщений")

    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)

async def message(update, cotext):
    dialog.mode = "message"
    text = load_message("message")
    await send_photo(update, cotext, "message")
    await send_text_buttons(update, cotext, text, {
        "message_next" : "Следующее сообщение",
        'message_date' : "Пригласить на свидание"
    })
    dialog.List.clear()

async def message_dialog(update, cotext):
    text = update.message.text
    dialog.List.append(text)


async def message_button(update, cotext):
    query = update.callback_query.data
    await update.callback_query.answer()
    prompt = load_prompt(query)
    user_chat_history = "\n\n".join(dialog.List)
    my_message = await send_text(update, cotext, "GhatGPT думает над вариантами ответа...")
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)

async def profile(update, cotext):
    dialog.mode = "profile"
    text = load_message("profile")
    await send_photo(update, cotext, "profile")
    await send_text(update, cotext, text)
    dialog.user.clear()
    dialog.count = 0
    await send_text(update, cotext, "Сколько вам лет?")

async def profile_dialog(update, cotext):
    text = update.message.text
    dialog.count += 1

    if dialog.count == 1:
        dialog.user["age"] =  text
        await send_text(update, cotext, "Кем вы работаете?")
    elif dialog.count == 2:
        dialog.user["occupation"] = text
        await send_text(update, cotext, "У вас есть хобби?")
    elif dialog.count == 3:
        dialog.user["hobby"] = text
        await send_text(update, cotext, "Что вам не нравится в людях?")
    elif dialog.count == 4:
        dialog.user["annoys"] = text
        await send_text(update, cotext, "Цели знакомства?")
    elif dialog.count == 5:
        dialog.user["goals"] = text
        prompt = load_prompt("profile")
        user_info = dialog_user_info_to_str(dialog.user)
        my_message = await send_text(update, cotext, "GhatGPT заниается генерацией вашего профиля. Подождите несколько секунд...")
        answer = await chatgpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)

async def opener(update, cotext):
    dialog.mode = "opener"
    text = load_message("opener")
    await send_photo(update, cotext, "opener")
    await send_text(update, cotext, text)
    dialog.user.clear()
    dialog.count = 0
    await send_text(update, cotext, "Имя девушки?")

async def opener_dialog(update, cotext):
    text = update.message.text
    dialog.count += 1

    if dialog.count == 1:
        dialog.user["name"] =  text
        await send_text(update, cotext, "Сколько ей лет?")
    elif dialog.count == 2:
        dialog.user["age"] = text
        await send_text(update, cotext, "Оцените её внешность: 1-10 баллов")
    elif dialog.count == 3:
        dialog.user["handsome"] = text
        await send_text(update, cotext, "Кем она работает?")
    elif dialog.count == 4:
        dialog.user["occupation"] = text
        await send_text(update, cotext, "Цели знакомства?")
    elif dialog.count == 5:
        dialog.user["goals"] = text
        prompt = load_prompt("opener")
        user_info = dialog_user_info_to_str(dialog.user)
        answer = await chatgpt.send_question(prompt, user_info)
        await send_text(update, cotext, answer)



async def hello(update, cotext):
    if dialog.mode == "gpt":
        await gpt_dialog(update, cotext)
    elif dialog.mode == "date":
        await date_dialog(update, cotext)
    elif dialog.mode == "message":
        await message_dialog(update, cotext)
    elif dialog.mode == "profile":
        await profile_dialog(update, cotext)
    elif dialog.mode == "opener":
        await opener_dialog(update, cotext)
    else:
        await send_text(update, cotext,"Привет")
        await send_text(update, cotext, "_Как дела?_")
        await send_text(update, cotext, "Ты написал:" + update.message.text)
        await send_photo(update, cotext,"avatar_main")
        await send_text_buttons(update, cotext,"Запустить?", {
            "start":"ДА",
            "stop":"НЕТ"
        })

async def hello_button(update, cotext):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, cotext, "Процесс запущен")
    else:
        await send_text(update, cotext, "Процесс остановлен")

dialog = Dialog()
dialog.mode = None
dialog.List = []
dialog.count = 0
dialog.user = {}

chatgpt = ChatGptService("javcgkAld/r/7U60nS8WDUhWeWVYkZbhjQYpKBFGTvoj5842ast7Pxc54epaCxHRBWXa4vjUutckFaoaUmyOdt62mPPZjjrSFzHlklUvRxjKkD54HiY1iMRLus7TxOkcmPElgqCRPBocX6wJsuWbUTuGkgPNjhYwE08Bvau9oVOiaBcWnUrI/ewY+ccVqx7dnAN4A7RhT46B8BjZjVtU/H8jZakz1cJir+37f/KOL/cTVnmJo=")

app = ApplicationBuilder().token("8004869844:AAHoK4kNK9NXxmE7VgtFYQqNEnoIm4CwJb0").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("date", date))
app.add_handler(CommandHandler("message", message))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("opener", opener))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(date_button, pattern ="^date_.*"))
app.add_handler(CallbackQueryHandler(message_button, pattern ="^message_.*"))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()

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

async def hello(update, cotext):
    if dialog.mode == "gpt":
        await gpt_dialog(update, cotext)
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

chatgpt = ChatGptService("javcgkAld/r/7U60nS8WDUhWeWVYkZbhjQYpKBFGTvoj5842ast7Pxc54epaCxHRBWXa4vjUutckFaoaUmyOdt62mPPZjjrSFzHlklUvRxjKkD54HiY1iMRLus7TxOkcmPElgqCRPBocX6wJsuWbUTuGkgPNjhYwE08Bvau9oVOiaBcWnUrI/ewY+ccVqx7dnAN4A7RhT46B8BjZjVtU/H8jZakz1cJir+37f/KOL/cTVnmJo=")

app = ApplicationBuilder().token("8004869844:AAHoK4kNK9NXxmE7VgtFYQqNEnoIm4CwJb0").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()

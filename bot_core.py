
import logging
import maintest as nrn
import button_lists as btns
import datetime
import pyodbc
import win32com.client
import time_things as tt
import telegram

from win32com.client import constants
from win32com.client import gencache

gencache.EnsureModule('{00000201-0000-0010-8000-00AA006D2EA4}',0,2,1)

from telegram.ext.dispatcher import run_async
from telegram import (ReplyKeyboardMarkup,InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                         ConversationHandler, CallbackQueryHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, CONFIRMAR, LOCATION, CANTIDAD, FECHA, HORAINI, HORAFIN, EMAIL, NUMBER, LOCATION_EID, WHAT_ELSE, GUARDAR_RES, OPENING, REGISTER, CHANGEDATA = range(15)

dictreserva = {"location" : str,
"people" : str,
"timest" : str,
"timeend" : str,
"fecha" : str }

#---------------------------------------------------------------------------------------------------------------------------------

def confirm(update, context):
    markup = InlineKeyboardMarkup(btns.build_menu(btns.buttons_confirmacion, n_cols=2))
    context.bot.send_message(chat_id=update.message.chat_id, text="Do you want to reserve a room? ", reply_markup = markup)
    return CONFIRMAR

#---------------------------------------------------------------------------------------------------------------------------------

def accept(update, context):

    query = update.callback_query
    context.bot.send_message(chat_id=query.message.chat_id, text="Ok, tell me in which location you want to reserve the room")

    return LOCATION

#---------------------------------------------------------------------------------------------------------------------------------

def cancel(update, context):
    query = update.callback_query
    user_data = context.user_data
    context.bot.send_message(chat_id=query.message.chat_id, text="See you later!")
    user_data.clear()

    return ConversationHandler.END

# ---------------------------------------------------------------------------------------------------------------------------------

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

#---------------------------------------------------------------------------------------------------------------------------------

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Could you give me your user? ")
    name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    userName = name, last_name
    estado = OPENING
    return estado

#---------------------------------------------------------------------------------------------------------------------------------
def opening(update, context):
    estado = OPENING
    eid = update.message.text
    connStr = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\sharon.gabriela.levy\Desktop\KVN\Chatbot\Chatbot\Smart KVN\KVNEIDs.accdb;"
    )
    cnxn = pyodbc.connect(connStr)
    cursor = cnxn.cursor()
    cursor.execute('select * from EnterpriseIDs')
    counter = 0

    for row in cursor.fetchall():
    	if eid in row:
    		counter = counter + 1
    		break
    	else:
    		counter = counter

    if counter > 0:

        if row.Authorized == "ON":

            if row.Registered == "YES":
                name = update.message.from_user.first_name
                last_name = update.message.from_user.last_name
                userName = name, last_name
                if str(userName) == row.userName:
                    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome! Always nice to see a friend!.")
                    context.bot.send_message(chat_id=update.message.chat_id, text="How can I help you today?")
                    estado = CHOOSING
                else:
                    context.bot.send_message(chat_id=update.message.chat_id, text="It looks like you are using other account, please use yours or communicate with @shar")
                    return ConversationHandler.END

            else:
                context.bot.send_message(chat_id=update.message.chat_id, text="You are not registered yet, could you give me your EID again?")
                estado = CHANGEDATA
                return estado

        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="I'm sorry, you are not authorized to request access, you'll have to talk to @sharon or @Juan. Hope to see you soon!")
            return ConversationHandler.END

    elif counter == 0:
    	context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, you are not in my frinds list, bye bye!.")
    	estado = ConversationHandler.END

    return estado
#---------------------------------------------------------------------------------------------------------------------------------
def changeData(update, context):
    name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    userName = name, last_name
    userEID = update.message.text
    userEID = str(userEID)
    estado = CHANGEDATA
    connStr = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\sharon.gabriela.levy\Desktop\KVN\Chatbot\Chatbot\Smart KVN\KVNEIDs.accdb;"
    )
    cnxn = pyodbc.connect(connStr)
    cursor2 = cnxn.cursor()
    cursor2.execute('select * from EnterpriseIDs')
    counter = 0

    for row in cursor2.fetchall():
        if userEID in row:
            counter = counter + 1
            break
        else:
            counter = counter

    if counter > 0:
        exstr = (" UPDATE [EnterpriseIDs] SET [Registered] = 'YES' WHERE [EID] = ? ")
        params = (userEID)
        cursor2.execute(exstr, params)
        cnxn.commit()
        exstr1 = (" UPDATE [EnterpriseIDs] SET [userName] = ? WHERE [EID] = ? ")
        params1 = (str(userName), userEID)
        cursor2.execute(exstr1, params1)
        cnxn.commit()
        context.bot.send_message(chat_id=update.message.chat_id, text="Thanks for registering, please start the conversation again.")
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="I couldn't find your EID, please try again")
        return ConversationHandler.END

#---------------------------------------------------------------------------------------------------------------------------------

def register(update, context):
	estado = REGISTER

	return 

#---------------------------------------------------------------------------------------------------------------------------------
@run_async
def ai_test(update, context):

    msg =update.message.text
    estado = CHOOSING
    respuesta = nrn.predictive_function(msg)
    if respuesta == 1:
        estado = confirm(update, context)

    elif respuesta == "email":
        context.bot.send_message(chat_id=update.message.chat_id, text="Could you provide a valid ID? ")
        estado = EMAIL

    elif respuesta == "number":
        context.bot.send_message(chat_id=update.message.chat_id, text="Could you provide a valid ID? ")
        estado = NUMBER

    elif respuesta == "location":
        context.bot.send_message(chat_id=update.message.chat_id, text="Could you provide a valid ID? ")
        estado = LOCATION_EID

    elif respuesta == "goodbye":
        context.bot.send_message(chat_id=update.message.chat_id, text="Bye, Bye")
        return ConversationHandler.END

    else:
        update.message.reply_text(respuesta)

    return estado

#---------------------------------------------------------------------------------------------------------------------------------

def yes(update, context):
    estado = WHAT_ELSE
    query = update.callback_query
    context.bot.send_message(chat_id=query.message.chat_id, text="What else would you like to know? ")
    estado = CHOOSING

    return estado

#---------------------------------------------------------------------------------------------------------------------------------

def no(update, context):
    estado = WHAT_ELSE
    query = update.callback_query
    user_data = context.user_data
    context.bot.send_message(chat_id=query.message.chat_id, text="Ok! Bye bye, see you later! ")
    user_data.clear()
    estado = ConversationHandler.END

    return estado

#---------------------------------------------------------------------------------------------------------------------------------

def email_2 (update, context):
    estado = EMAIL
    eid = update.message.text
    connStr = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\sharon.gabriela.levy\Desktop\KVN\Chatbot\Chatbot\Smart KVN\KVNEIDs.accdb;"
    )
    cnxn = pyodbc.connect(connStr)
    cursor = cnxn.cursor()
    cursor.execute('select * from EnterpriseIDs')
    counter = 0
    for row in cursor.fetchall():
        if eid in row:
            resp = row.Email
            counter = counter + 1
            context.bot.send_message(chat_id=update.message.chat_id, text= resp)
            markup = InlineKeyboardMarkup(btns.build_menu(btns.buttons_yeses_o_nos, n_cols=2))
            context.bot.send_message(chat_id=update.message.chat_id, text="Do you need something else? ", reply_markup = markup)
            estado = WHAT_ELSE

    if counter == 0:
        context.bot.send_message(chat_id=update.message.chat_id, text="That was not a valid ID, try again ")
        estado = EMAIL

    return estado

#---------------------------------------------------------------------------------------------------------------------------------

def number_eid (update, context):
    estado = NUMBER
    eid = update.message.text
    connStr = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\sharon.gabriela.levy\Desktop\KVN\Chatbot\Chatbot\Smart KVN\KVNEIDs.accdb;"
    )
    cnxn = pyodbc.connect(connStr)
    cursor = cnxn.cursor()
    cursor.execute('select * from EnterpriseIDs')
    counter = 0
    for row in cursor.fetchall():
        if eid in row:
            print(row.Email)
            resp = row.Telefono
            counter = counter + 1
            context.bot.send_message(chat_id=update.message.chat_id, text= resp)
            markup = InlineKeyboardMarkup(btns.build_menu(btns.buttons_yeses_o_nos, n_cols=2))
            context.bot.send_message(chat_id=update.message.chat_id, text="Do you need something else? ", reply_markup = markup)
            estado = WHAT_ELSE

    if counter == 0:
        context.bot.send_message(chat_id=update.message.chat_id, text="That was not a valid ID, try again ")
        estado = NUMBER

    return estado

#---------------------------------------------------------------------------------------------------------------------------------

def location_eid (update, context):
    estado = LOCATION_EID
    eid = update.message.text
    connStr = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\sharon.gabriela.levy\Desktop\KVN\Chatbot\Chatbot\Smart KVN\KVNEIDs.accdb;"
    )
    cnxn = pyodbc.connect(connStr)
    cursor = cnxn.cursor()
    cursor.execute('select * from EnterpriseIDs')
    counter = 0
    for row in cursor.fetchall():
        if eid in row:
            resp = row.ubicacion
            counter = counter + 1
            context.bot.send_message(chat_id=update.message.chat_id, text= resp)
            markup = InlineKeyboardMarkup(btns.build_menu(btns.buttons_yeses_o_nos, n_cols=2))
            context.bot.send_message(chat_id=update.message.chat_id, text="Do you need something else? ", reply_markup = markup)
            estado = WHAT_ELSE

    if counter == 0:
        context.bot.send_message(chat_id=update.message.chat_id, text="That was not a valid ID, try again ")
        estado = NUMBER

    return estado

#---------------------------------------------------------------------------------------------------------------------------------

def locations(update, context):
    msg =update.message.text
    estado = LOCATION
    respuesta = nrn.predictive_function(msg)
    
    if respuesta == "none":
        context.bot.send_message(chat_id=update.message.chat_id, text="Please, enter the location again ")
    else:
        if respuesta != "I didn't understand you, try again":
            dictreserva["location"] = respuesta
            context.bot.send_message(chat_id=update.message.chat_id, text="Well, how many people will attend the meeting?")
            estado = CANTIDAD

    return estado

#---------------------------------------------------------------------------------------------------------------------------------

def cantidad(update, context):
    msg =update.message.text
    estado = CANTIDAD
    respuesta = nrn.predictive_function(msg)
    
    if respuesta == "none":
        context.bot.send_message(chat_id=update.message.chat_id, text="Please, enter the location again ")
    else:
        if respuesta != "I didn't understand you, try again":
            dictreserva["people"] = respuesta
            context.bot.send_message(chat_id=update.message.chat_id, text="when will the meeting take place? (Use mm/dd/yyyy formatting) ")
            estado = FECHA
    
    return estado

#---------------------------------------------------------------------------------------------------------------------------------

def after_date_choice(update, context):
    msg =update.message.text
    estado = FECHA
    respuesta = nrn.funcion_fecha(msg)

    if respuesta == "wrong":
        context.bot.send_message(chat_id=update.message.chat_id, text=" That date has passed, try again")
        estado = FECHA

    elif respuesta == "Not a valid format":
        context.bot.send_message(chat_id=update.message.chat_id, text="Not a valid format. Try again using dd/mm/yyyy format. Good luck this time!")
        estado = FECHA

    elif respuesta != "I didn't understand you, try again":
        dictreserva["fecha"] = respuesta
        context.bot.send_message(chat_id=update.message.chat_id, text=" Please enter the starting time of the meeting. Use the HH:MM format ")
        estado = HORAINI

    return estado

#---------------------------------------------------------------------------------------------------------------------------------

def after_ini_choice(update, context):

    msg = update.message.text
    estado = HORAINI
    fecha = dictreserva['fecha']

    timest = nrn.funcion_time_ini(msg, fecha)
        
    if timest != "Can't make a reservation in the past. Try again." and timest != "Not valid. Try again.":
        
        dictreserva['timest'] = timest
        estado = HORAFIN        
        context.bot.send_message(chat_id=update.message.chat_id, text="Enter the ending time in a HH:MM (24 hours) format: ")

    else:

        context.bot.send_message(chat_id=update.message.chat_id, text=timest)

    return estado

#---------------------------------------------------------------------------------------------------------------------------------

def guardar_reserva(update, context):
    query = update.callback_query
    #conSQL.escribir_tabla(context.user_data, file_reservas)
    #context.bot.send_message(chat_id=query.message.chat_id, text="Information is being saved, please wait a few seconds.")
    #macro.run(file_macro,"addCosas")
    #print(context.user_data)

    context.bot.send_message(chat_id=update.message.chat_id, text="Give me a minute, I'm looking for a room..")
    result = reserva_selenium.seleccionar_sala(context.user_data)
    msg = ""
    try:
        msg = "All done!\nYour room: {} {} \nFloor: {} \nCapacity: {}".format(result['Room'], result['Neigh'], result['Floor'], result['Capacity'])
        #msg = "All done!\n{}".format(facts_to_str(result))
    except TypeError as e:
        msg = result
    
    context.bot.send_message(chat_id=query.message.chat_id, text=msg)
    
    context.user_data.clear()
    return ConversationHandler.END

#---------------------------------------------------------------------------------------------------------------------------------

def after_fin_choice(update, context):
    msg = update.message.text
    estado = HORAFIN
    start_t = dictreserva['timest']

    timeend = nrn.funcion_time_fin(msg, start_t)
        
    if timeend != "Can't end a meeting before it starts. Try again." and timeend != "Not a valid format. Try again.":
        
        dictreserva['timeend'] = timeend
        context.bot.send_message(chat_id=update.message.chat_id, text="Give me a few minutes, we'll reserve that room for you xoxo")
        estado = GUARDAR_RES

    else:

        context.bot.send_message(chat_id=update.message.chat_id, text=timeend)

    return estado

#---------------------------------------------------------------------------------------------------------------------------------

def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']
    update.message.reply_text("Bye")
    user_data.clear()
    return ConversationHandler.END

#---------------------------------------------------------------------------------------------------------------------------------

def error(update, context):

    logger.warning('Update "%s" caused error "%s"', update, error)

#---------------------------------------------------------------------------------------------------------------------------------

def main():

    updater = Updater("1299167087:AAGK9Z9JB-RWXZJMeDvy3VOW9l5yk0SyyiU", use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, start)],

        states={
            CHOOSING: [MessageHandler(Filters.text, ai_test),],

            CONFIRMAR: [CallbackQueryHandler(accept,pattern='^accept$'),
                        CallbackQueryHandler(cancel,pattern='^cancel$'),
                        ],

            LOCATION: [MessageHandler(Filters.text,locations),],

            CANTIDAD: [MessageHandler(Filters.text,cantidad),],

            FECHA: [MessageHandler(Filters.text, after_date_choice),],

            HORAINI: [MessageHandler(Filters.text, after_ini_choice),],

            HORAFIN: [MessageHandler(Filters.text, after_fin_choice),],

            EMAIL: [MessageHandler(Filters.text, email_2),],

            NUMBER: [MessageHandler(Filters.text, number_eid)],

            LOCATION_EID: [MessageHandler(Filters.text, location_eid)],

            GUARDAR_RES: [MessageHandler(Filters.text, guardar_reserva)],

            OPENING: [MessageHandler(Filters.text, opening)],

            REGISTER: [MessageHandler(Filters.text,register)],

            CHANGEDATA:[MessageHandler(Filters.text, changeData)],

            WHAT_ELSE: [CallbackQueryHandler(yes,pattern='^yes$'),
                        CallbackQueryHandler(no,pattern='^no$'),
                        ]
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done, pass_user_data=True)]

    )

    dp.add_handler(conv_handler)
    query_accept = CallbackQueryHandler(confirm)
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    dp.add_handler(query_accept)
    
    updater.idle()

#---------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
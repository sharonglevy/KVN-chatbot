# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 10:43:50 2019

@author: agustin.mediavilla
"""

from telegram import (InlineKeyboardButton)

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


buttons_cantidad = [
        InlineKeyboardButton("1-2", callback_data='2'),
        InlineKeyboardButton("3-4", callback_data='4'),
        InlineKeyboardButton("5-6", callback_data='6'),
        InlineKeyboardButton("7-8", callback_data='8'),
        InlineKeyboardButton("9-11", callback_data='11')
    ]


buttons_locations = [
        InlineKeyboardButton("Parque Patricios", callback_data='Buenos Aires- Parque Patricios'),
        InlineKeyboardButton("Defensa", callback_data='Buenos Aires - Defensa'),
        InlineKeyboardButton("Mar Del Plata", callback_data='Buenos Aires- Mar Del Plata'),
        InlineKeyboardButton("La Plata", callback_data='Buenos Aires - La Plata'),
        InlineKeyboardButton("Panamericana", callback_data='Buenos Aires - Panamericana')
    ]

buttons_confirmacion = [
        InlineKeyboardButton("Accept", callback_data='accept'),
        InlineKeyboardButton("Cancel", callback_data='cancel')
    ]


buttons_aceptacion = [
        InlineKeyboardButton("Accept", callback_data='accept'),
        InlineKeyboardButton("Deny", callback_data='deny')
    ]

buttons_yeses_o_nos = [
        InlineKeyboardButton("Yes", callback_data='yes'),
        InlineKeyboardButton("No", callback_data='no')
    ]

def build_reg_btns(chat_data):
    print(chat_data)
    response_ok = chat_data.replace('"R": "r', '"R": "Y')
    response_no = chat_data.replace('"R": "r', '"R": "N')
    print(response_no + '\n' + response_ok)
    buttons_aceptacion = [
        InlineKeyboardButton("Accept", callback_data=response_ok),
        InlineKeyboardButton("Deny", callback_data=response_no)
    ]
    return build_menu(buttons_aceptacion, n_cols=1)
    
    
date_keyboard = [['Today', 'Tomorrow']]

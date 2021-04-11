# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 09:38:03 2019

@author: agustin.mediavilla
"""

import config
import browser_things as bt

import time

def pantalla_carga():
    loading_img = bt.find_by_id('page-loading-overlay')
    bt.wait_invisible(loading_img)


def book_now():
    bt.load_site(config.urls['reservations'])
    #bt.wait_element_id("sidebar-wrapper")
    bt.wait_element_clickable('//*[@id="templates-grid"]/div/div[1]/div[2]/button[1]')
    bt.click_element(bt.find_by_xpath('//*[@id="templates-grid"]/div/div[1]/div[2]/button[1]'))
    
    
def goto_list():
    bt.click_element(bt.find_by_id("return-to-top"))
    time.sleep(1)
    bt.click_element(bt.find_by_xpath('//*[@id="result-tabs"]/li[1]/a'))
    
    pantalla_carga()
    bt.wait_invisible(bt.find_by_class('loading-animation'))


def completar_location(datos):
    bt.click_element(bt.find_by_xpath('//*[@id="location-filter-container"]/div[1]/div/a'))
    element = bt.wait_element_xpath('//div[starts-with(@id, "filter-main")]/div[1]/div[2]/div/input')
    time.sleep(3)
    bt.write_into(element, datos['Location'])
    time.sleep(1)
    bt.click_element(bt.find_by_xpath('//div[starts-with(@id, "filter-main")]/div[2]/div[1]/div/label/input'))
    bt.click_element(bt.find_by_xpath('//*[@id="filterModal"]/div/div/div[3]/button[1]'))
    pantalla_carga()
    
    
def completar_capacidad(datos):
    #loading_img = bt.find_by_id('page-loading-overlay')
    element = bt.wait_element_xpath('//*[@id="filter-container"]/div[1]/div[3]/div[2]/input')
    bt.write_into(element, datos['People'])   
    pantalla_carga()
    bt.click_element(bt.find_by_xpath('//*[@id="filter-container"]/div[2]/button'))
    pantalla_carga()
    
    
def completar_horario(datos):
    dateBox = bt.wait_element_id('booking-date-input')
    time.sleep(2)
    bt.write_into(dateBox, datos['Date'])
    bt.write_into(bt.find_by_xpath('//*[@id="booking-start"]/input'), datos['Starting Time'])
    bt.write_into(bt.find_by_xpath('//*[@id="booking-end"]/input'), datos['Ending Time'])
    

def buscar_sala(datos):
    book_now()
    completar_horario(datos)
    completar_location(datos)
    completar_capacidad(datos)
    goto_list()
    
    
def obtener_sala():
    sala = None
    tabla = bt.find_by_xpath('//*[@id="available-list"]/tbody')
    lista = bt.get_children_from("tr", tabla)
    timeout = 0
    
    while len(lista) <1 and timeout < 3:
        #time.sleep(1)
        timeout = timeout +1
        tabla = bt.find_by_xpath('//*[@id="available-list"]/tbody')
        lista = bt.get_children_from("tr", tabla)
        print(timeout)
    if len(lista) > 1:
        sala = lista[1]
    
    return sala


def agregar_sala(sala):
    btnAgregar = bt.find_by_class('add-to-cart', sala)
    bt.click_element(btnAgregar)
    bt.click_element(bt.find_by_xpath('//*[@id="setup--add-modal-save"]'))
    #bt.wait_element_id("toaster")
    esperar_agregada('selected-rooms-container','div')
    time.sleep(1)
    

def esperar_agregada(element_class, tag):
    #selected-rooms-container
    agregado = False
    tabla = bt.find_by_class(element_class)
    lista = bt.get_children_from(tag, tabla)
    timeout = 0
    
    while len(lista) <1 and timeout < 3:
        #time.sleep(1)
        timeout = timeout +1
        tabla = bt.find_by_class(element_class)
        lista = bt.get_children_from(tag, tabla)
        print(timeout)
    if len(lista) >= 1:
        agregado = True
    
    return agregado


def completar_confirmacion(datos):
    bt.click_element(bt.find_by_xpath('//*[@id="main-tabs"]/li[3]/a'))
    bt.write_into(bt.find_by_id("event-name"), datos['EID'])
    bt.select_in(bt.find_by_id("event-type"), "Workspace")
    bt.write_into(bt.find_by_xpath('//*[@id="reservation-details-billing"]/div/div[2]/div/div[1]/div/div/input'), "DS79400D") #"DS79400D")
    bt.click_element(bt.find_by_xpath('//*[@id="details"]/div[3]/div/span[2]/button'))
    #time.sleep(2)
    pantalla_carga()
    
    
def resultado_reserva():
    element = bt.wait_element_xpath('//*[@id="toaster"]/div/span[2]')
    #pantalla_carga()
    if element != None:
        resultado = element.text
    else:
        element = bt.wait_element_class('MsoNormal')
        if element != None and element.is_displayed():
            resultado = "OK"#element.text
            bt.click_element(bt.wait_element_id('help-text-close-btn'))
        else:
            resultado = "Ups! There was an error completing the reservation."
    
    return resultado


def parse_info_sala(sala, datos):
    parsed_info = 'OK'
    try:
        texto = sala.text
        texto = texto.replace(datos['Location'] + ' ', '')    
        arr = texto.split(' ')
        parsed_info = {
                'Room':arr[0],
                'Neigh':arr[1],
                'Floor':arr[2],
                'Capacity':arr[4],
                }
    except IndexError as e:
        print(e.with_traceback)
        print(sala.text)
        
    return parsed_info


#datos = config.client


def seleccionar_sala(datos=None):  
    resultado = ""
    if datos != None:
        buscar_sala(datos)
        sala = obtener_sala()
        if sala != None:
            info_sala = parse_info_sala(sala, datos)
            agregar_sala(sala)
            completar_confirmacion(datos)
            resultado = resultado_reserva()
            if resultado == "OK":
                resultado = info_sala
        else:
            resultado = "Sorry, there are no rooms that meet your needs."
    else:
        resultado = "I'm sorry, the information was lost so I can't make the reservation, please try again."
        
    return resultado

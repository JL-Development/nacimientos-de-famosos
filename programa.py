import wikipedia # libreria de python de wikipedia
from datetime import date # para saber el anio actual
import re #se usa para poder reemplazar los simbolos por espacios en un string
import requests
from flask import request
import json
from flask import Flask

app = Flask(__name__)


# CONSTANTES

wikipedia.set_lang("es") # setea el lenguaje en que se va a buscar en wikipedia

todays_date = date.today()

meses_nombres = {'enero': 1,'febrero': 2,'marzo': 3,'abril': 4,'mayo': 5,'junio': 6,'julio': 7,'agosto': 8,'septiembre': 9,'octubre': 10,'noviembre': 11,'diciembre': 12}
key_list = list(meses_nombres.keys())

signo = ("Capricornio", "Acuario", "Piscis", "Aries", "Tauro", "Géminis", "Cáncer", "Leo", "Virgo", "Libra", "Escorpio", "Sagitario")
fechas = (20, 19, 20, 20, 21, 21, 22, 22, 22, 22, 22, 21)

WIKI_REQUEST_IMAGEN = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='
WIKI_REQUEST_INFOBOX = 'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles='

lista_de_coincidencias = []


# funcion que devuelve el numero del mes que se ingresa y el nombre
def devolver_nombre_mes(num):
    return key_list[num-1] # busca el mes dentro del diccionario y se guarda el nombre


# devuelve el signo del zodiaco segun dia y mes
def calcular_signo(mes_numero,dia):
    mes_numero=mes_numero-1
    if dia>fechas[mes_numero]:
        mes_numero=mes_numero+1
    if mes_numero==12:
        mes_numero=0
    signo_persona = signo[mes_numero] # guarda en una variable el signo de la persona
    return signo_persona


#calcula la edad de la persona
def calcular_edad(anio):
    edad = todays_date.year - anio #resta anio actual menos anio de nacimiento
    return edad

# DEVUELVE TODAS LAS COINCIDENCIAS
@app.route('/famosos/coincidencias/')
def devolver_coincidencias():
    persona = request.args.get('nombre')
    coincidencias = []
    
    lista_de_coincidencias = wikipedia.search(persona)  #busca todas las coincidencias que exiten en wikipedia con el nombre

    for i in range(0,len(lista_de_coincidencias)): # imprime todas las coincidencias de wikipedia con el nombre ingresado
        coincidencias.append(lista_de_coincidencias[i])

    return json.dumps(coincidencias,ensure_ascii=False).encode('utf8')

def devolver_pagina_seleccionada(nombre):
    return wikipedia.WikipediaPage(nombre) # se queda con la pagina de wikipedia de la persona



def opcion_2_sin_api(pagina):
    
        # se queda con la pagina de la persona ingresada y se empieza a desarmar la fecha de nacimiento
        
        resumen = pagina.summary # obtiene el resumen
        resumen_primera_parte = resumen.split('(', 1) # se queda con lo que esta en el primer parentesis (lo de la derecha)
        resumen_segunda_parte = resumen_primera_parte[1].split('.',1) # se queda con lo que esta hasta el primer punto (lo del izquierda)
        fecha = resumen_segunda_parte[0]
        #print(fecha)
        
        # desarma la fecha y se queda con el numero del dia
        dia = int([int(i) for i in fecha.split() if i.isdigit()][0]) # se queda con el primer numero que esta en el string
        #print(dia)
        
        # se queda con el anio de nacimiento

        fecha = re.sub('[^a-zA-Z0-9\n\.]', ' ', fecha) # cambia todos los simbolos por espacios
        numeros_fechas = [int(i) for i in fecha.split() if i.isdigit()] # se queda con todos los numeros del string

        #print(numeros_fechas)

        for i in range (0,len(numeros_fechas)):
            if int(numeros_fechas[i]) > 1000: # cuando encuentra el primer numero mayor a mil, corta
                anio = int(numeros_fechas[i]) # se guarda el anio de nacimiento
                break
        #print(anio)
        
        # devuelve el numero del mes que se ingresa y el nombre

        meses_nombres = {'enero': 1,'febrero': 2,'marzo': 3,'abril': 4,'mayo': 5,'junio': 6,'julio': 7,'agosto': 8,'septiembre': 9,'octubre': 10,'noviembre': 11,'diciembre': 12}

        lista = fecha.split(" ") # guarda en una lista todos los elementos del string

        for i in lista:
          if i in meses_nombres: # se fija cual de esos está dentro del diccionario de meses
            mes = i # se guarda el nombre del mes y corta
            break

        #print(mes)

        mes_numero = int(meses_nombres[mes.lower()]) # busca el mes dentro del diccionario y se guarda el numero
        #print(mes_numero)
        
        # devuelve el signo del zodiaco segun dia y mes

        signo_persona = calcular_signo(mes_numero,dia)
        
        #print ("Signo: " + signo_persona)
        
        # calcula la edad de la persona

        edad = calcular_edad(anio)
        #print(edad)
        
        # dice toda la informacion de la persona
        
        print('---------- FICHA DE LA PERSONA ----------')

        print('Nombre:',pagina.title) #titulo de la pagina de wikipedia
        
        print('Fecha de Nacimiento:',dia,"de",mes,'de',anio)
        
        print('Edad:',edad)
        
        print('Signo del Zodíaco:',signo_persona)

        print('Información extraída de:',pagina.url)

        informacion = {'Nombre':pagina.title,'d_nac':dia,'m_nac':mes,'a_nac':anio,'edad':edad,'signo':signo_persona,'url':pagina.url}
        
        return json.dumps(informacion,ensure_ascii=False).encode('utf8')


def opcion_1_usa_api(pagina):
        ## EMPIEZA A CALCULAR LAS FECHAS

        response  = requests.get(WIKI_REQUEST_INFOBOX + pagina.title)
        json_data = json.loads(response.text)
        json_infobox = list(json_data['query']['pages'].values())[0]['revisions'][0]['*']
        info_box = json_infobox.split("Infobox")[1] # se queda con la info de la seccion "infobox" de wikipedia
        
        ## ---------- NACIMIENTO ----------- ##
        birth_date = json_infobox.split("birth_date")[1]
        birth_date = birth_date.split("}")[0] # se queda con la fecha de cumpleaños de la persona

        birth_date = re.sub('[^a-zA-Z0-9\n\.]', ' ', birth_date) # cambia todos los simbolos por espacios

        numeros_fechas_cumple = [int(i) for i in birth_date.split() if i.isdigit()] # se queda con todos los numeros del string

        anio_nacimiento = numeros_fechas_cumple[0]
        mes_nacimiento = numeros_fechas_cumple[1]
        dia_nacimiento = numeros_fechas_cumple[2]

        print(dia_nacimiento,mes_nacimiento,anio_nacimiento)
        
        ## ----------- MUERTE -------------- ##
        murio = False
        try: 
            birth_date = json_infobox.split("death_date")[1]
            birth_date = birth_date.split("}")[0]
            #print(birth_date)
            birth_date=re.sub('[^a-zA-Z0-9\n\.]', ' ', birth_date) # cambia todos los simbolos por espacios
            numeros_fechas_muerte = [int(i) for i in birth_date.split() if i.isdigit()] # se queda con todos los numeros del string

            anio_muerte = numeros_fechas_muerte[0]
            mes_muerte = numeros_fechas_muerte[1]
            dia_muerte = numeros_fechas_muerte[2]

            murio = True
            print(dia_muerte,mes_muerte,anio_muerte)

        except:
            print('La persona no murió.')
            #anio_muerte = 0
            pass
            
        ## ---------- IMAGEN --------------- ##
        
        response  = requests.get(WIKI_REQUEST_IMAGEN + pagina.title)
        json_data = json.loads(response.text)
        imagen_persona = list(json_data['query']['pages'].values())[0]['original']['source']

        print(imagen_persona)
        
        # dice toda la informacion de la persona

        mes_nacimiento_nombre = devolver_nombre_mes(mes_nacimiento)
        print(mes_nacimiento_nombre)
        edad = calcular_edad(anio_nacimiento)
        print(edad)
        signo = calcular_signo(mes_nacimiento,dia_nacimiento)
        print(signo)
        
        print(murio)
        if (murio):
            mes_muerte_nombre = devolver_nombre_mes(mes_muerte)

        print('---------- FICHA DE LA PERSONA ----------')

        print('Nombre:',pagina.title) #titulo de la pagina de wikipedia

        print('Fecha de Nacimiento:',dia_nacimiento,"de",mes_nacimiento_nombre,'de',anio_nacimiento)

        #print(murio)
        if (murio):
            print('Fecha de Muerte:',dia_muerte,"de",mes_muerte_nombre,'de',anio_muerte)
            print('La persona tendría:',edad,'años.')
        else:
            print('Edad:',edad)

        print('Signo del Zodíaco:',signo)

        print('Información extraída de:',pagina.url)

        print('Imagen de la persona:',imagen_persona)

        if(murio):
            informacion = {'murio':murio,'nombre':pagina.title,'d_nac':dia_nacimiento,'m_nac':mes_nacimiento_nombre,'a_nac':anio_nacimiento,'d_muerte':dia_muerte,'m_muerte':mes_muerte_nombre,'a_muerte':anio_muerte,'signo':signo,'pagina_url':pagina.url,'img': imagen_persona}
        else:
           informacion = {'murio':murio,'nombre':pagina.title,'d_nac':dia_nacimiento,'m_nac':mes_nacimiento_nombre,'a_nac':anio_nacimiento,'signo':signo,'pagina_url':pagina.url,'img': imagen_persona}

        
        return json.dumps(informacion,ensure_ascii=False).encode('utf8')

@app.route('/famosos/api/')
def programa():
    #coincidencias = devolver_coincidencias('Messi')
    #print(coincidencias)
    nombre = request.args.get('nombre')
    print(nombre)
    pagina = devolver_pagina_seleccionada(nombre)
    
    opcion_1 = True
    print(opcion_1)
    info = 404
    try:
        #print('entro 1')
        return opcion_1_usa_api(pagina)
    except:
        print('error en 1')
        opcion_1 = False
    print(opcion_1) 
       
    if(opcion_1 == False):
        try:
            #print('entro 2')
            return opcion_2_sin_api(pagina)
        except:
            return json.dumps(info)
            print('No es posible encontrar la persona')
    
    

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")


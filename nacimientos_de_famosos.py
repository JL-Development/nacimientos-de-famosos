#!/usr/bin/env python
# coding: utf-8

# In[1]:


import wikipedia # libreria de python de wikipedia
from datetime import date # para saber el anio actual
import re #se usa para poder reemplazar los simbolos por espacios en un string


# In[2]:


todays_date = date.today()


# In[3]:


wikipedia.set_lang("es") # setea el lenguaje en que se va a buscar en wikipedia


# In[4]:


persona = input('Ingrese persona: ')

lista_de_coincidencias = wikipedia.search(persona)  #busca todas las coincidencias que exiten en wikipedia con el nombre

for i in range(0,len(lista_de_coincidencias)): # imprime todas las coincidencias de wikipedia con el nombre ingresado
    print('Opcion',i,":",lista_de_coincidencias[i])


# In[5]:


# se queda con la pagina de la persona ingresada y se empieza a desarmar la fecha de nacimiento

opcion = int(input('Ingrese Opcion:'))
pagina = wikipedia.WikipediaPage(lista_de_coincidencias[opcion]) # se queda con la pagina de wikipedia de la persona

resumen = pagina.summary # obtiene el resumen

try:
    resumen_primera_parte = resumen.split('(', 1) # se queda con lo que esta en el primer parentesis (lo de la derecha)
    resumen_segunda_parte = resumen_primera_parte[1].split('.',1) #se queda con lo que esta hasta el primer punto (lo del izquierda)
    fecha = resumen_segunda_parte[0]
    print(fecha)
except:
  print("Por favor, ingrese otra persona.") 


# In[6]:


# desarma la fecha y se queda con el numero del dia

try:
    dia = int([int(i) for i in fecha.split() if i.isdigit()][0]) # se queda con el primer numero que esta en el string
    print(dia)
except:
    print("Por favor, ingrese otra persona.") 


# In[7]:


# se queda con el anio de nacimiento

fecha=re.sub('[^a-zA-Z0-9\n\.]', ' ', fecha) # cambia todos los simbolos por espacios
numeros_fechas = [int(i) for i in fecha.split() if i.isdigit()] # se queda con todos los numeros del string

print(numeros_fechas)

for i in range (0,len(numeros_fechas)):
    if int(numeros_fechas[i]) > 1000: #cuando encuentra el primer numero mayor a mil, corta
        anio = int(numeros_fechas[i]) # se guarda el anio de nacimiento
        break
print(anio)


# In[8]:


# devuelve el numero del mes que se ingresa y el nombre

meses_nombres = {'enero': 1,'febrero': 2,'marzo': 3,'abril': 4,'mayo': 5,'junio': 6,'julio': 7,'agosto': 8,'septiembre': 9,'octubre': 10,'noviembre': 11,'diciembre': 12}

lista = fecha.split(" ") # guarda en una lista todos los elementos del string

for i in lista:
  if i in meses_nombres: # se fija cual de esos está dentro del diccionario de meses
    mes = i # se guarda el nombre del mes y corta
    break
    
print(mes)

mes_numero = int(meses_nombres[mes.lower()]) # busca el mes dentro del diccionario y se guarda el numero
print(mes_numero)


# In[9]:


# devuelve el signo del zodiaco segun dia y mes

signo = ("Capricornio", "Acuario", "Piscis", "Aries", "Tauro", "Géminis", "Cáncer", "Leo", "Virgo", "Libra", "Escorpio", "Sagitario")
fechas = (20, 19, 20, 20, 21, 21, 22, 22, 22, 22, 22, 21)

mes_numero=mes_numero-1
if dia>fechas[mes_numero]:
    mes_numero=mes_numero+1
if mes_numero==12:
    mes_numero=0
    
signo_persona = signo[mes_numero] # guarda en una variable el signo de la persona
print ("Signo: " + signo_persona)


# In[10]:


#calcula la edad de la persona

edad = todays_date.year - anio #resta anio actual menos anio de nacimiento
print(edad)


# In[12]:


# dice toda la informacion de la persona

print('---------- FICHA DE LA PERSONA ----------')
print('Nombre:',pagina.title) #titulo de la pagina de wikipedia
print('Fecha de Nacimiento:',dia,"de",mes,'de',anio)
if(edad > 110):
    print('Edad:',edad,". Probablemente ya esté muerto.")
else:
    print('Edad:',edad)
print('Signo del Zodíaco:',signo_persona)


# In[ ]:





# Bitácora de Gestión de Conflictos 

Proyecto: Piedra, Papel o Tijera  
Equipo: Grupo nro 8  (los yorch)
Fase: 3 Inicio del Desarrollo (Semanas 11–12)

---

## Conflicto #1: Error de módulo al ejecutar el código

## Hechos
Al intentar ejecutar el juego, Python lanzó el error `ModuleNotFoundError: No module named 'game_logic'`. Esto ocurrió porque todo el código fue escrito en un único archivo `.py`, cuando la arquitectura del proyecto requiere que cada componente esté en su propio archivo separado (`game_logic.py`, `juego.py`, `server.py`, `client.py`).

## Sentimientos
La situación generó frustración en el equipo al no poder ver el programa funcionar, y cierta incertidumbre sobre si la arquitectura cliente-servidor era más compleja de lo esperado.

## Necesidades
El proyecto requiere que los archivos estén correctamente separados en módulos independientes, todos ubicados en la misma carpeta, para que Python pueda importar correctamente las funciones entre archivos.

## Petición
Se acordó como equipo revisar la estructura de carpetas antes de ejecutar cualquier archivo, asegurando que los 4 módulos (`game_logic.py`, `juego.py`, `server.py`, `client.py`) estén siempre en el mismo directorio. Además, se estableció probar el modo local primero antes de avanzar al modo multijugador.

---

## Conflicto #2: Problemas al ejecutar la interfaz en Tkinter

## Hechos
Con ayuda de la IA e investigaciones en la web, logramos realizar nuestra interfaz grafica (GUI) para nuestro ptoyecto, todo esto en la libreria de Tkinter, pero nos encontramos con que al momento de ejecutar todos los archivos el que no funcionaba o se mostraba era el de la interfaz realizada.

## Sentimientos
La situacion genero molestia y decepcion en los integrantes del equipo pero más en nuestro compañero Gabriel pues el era quien estaba acargo de realizar la interfaz en la libreria y al probarla y que no funcionase lo frustro demasiado.

## Necesidades
El proyecto necesita de manera OBLIGATORIA, que la interfaz este implementada de manera correcta pues mas alla de ser un atractivo visual es indispensable para que el programa funcionde y los usuarios puedan entender y disfrutar de nuestro juego/proyecto de la mejor manera.

## Petición
Como grupo acordamos que buscaremos la manera más eficiente de implementar la interfaz a nuestro proyecto para que asi quede totalmente limpio.

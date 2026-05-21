# 🎮 Proyectos Integradores — Primer Nivel
### Escuela de Ciencias de la Computación · Ingeniería en Sistemas de Información
**Periodo Académico: Marzo – Julio 2025**

---

> *"Un programa que funciona a las 2 AM es un programa que funciona."*
> — Todo estudiante de primer nivel, semana 12

---

## 🧠 ¿Qué estamos construyendo aquí?

Un **juego interactivo con modo multijugador cliente-servidor en red LAN**, desarrollado aplicando las fases clásicas del ciclo de vida del software: análisis, diseño, desarrollo, pruebas y presentación final.

¿Sencillo? Tal vez.
¿Épico cuando funciona en dos máquinas virtuales en tiempo real? **Absolutamente.**

Los equipos eligieron entre clásicos como:
- 🪤 Juego del Ahorcado
- ✂️ Piedra, Papel o Tijera
- 🏓 Atari Pong
- 🐍 Juego de la Serpiente
- 🔢 Adivina el Número
- 🔐 Generador Seguro de Contraseñas

Todos con **modo local + modo multijugador LAN** usando arquitectura cliente-servidor y sockets TCP. Sí, de verdad.

---

## 🏗️ Arquitectura del Sistema

```
[Jugador 1 - Servidor]  ←──── LAN / Sockets TCP ────→  [Jugador 2 - Cliente]
        │                                                        │
   game_logic.py                                           client.py
   server.py                                               Envía jugadas
   Procesa resultados                                      Muestra estado
   Determina ganador
```

### Estructura de carpetas esperada por equipo:

```
ProyectoJuego/
│
├── juego.py          # Modo local
├── server.py         # Lógica servidor (Jugador 1)
├── client.py         # Cliente de red (Jugador 2)
├── game_logic.py     # Módulo de lógica del juego
├── LICENSE           # Open Source (MIT, GPL, etc.)
└── README.md         # Esto que estás leyendo (pero de tu equipo)
```

---

## 🗓️ Fases del Proyecto

| Fase | Semanas | ¿Qué se hace? | Entregables |
|------|---------|---------------|-------------|
| **1 — Análisis** | 7–8 | Definir el problema, requisitos funcionales y no funcionales | Doc de requisitos + Contrato de Comunicación + Video |
| **2 — Diseño** | 9–10 | Diagramas funcionales y arquitectura cliente-servidor | Diagramas + Arquitectura de red + Video |
| **3 — Inicio Dev** | 11–12 | Repositorio en GitHub + código inicial modularizado | Link GitHub + Código base + Declaración de autoría |
| **4 — Desarrollo** | 13 | Condicionales, bucles, sockets funcionando | Código actualizado + Demo parcial + Video de avance |
| **5 — Pruebas** | 14 | Validación, manejo de errores, UX/UI, diseño cognitivo | Versión final + Infografía UX + Video demostrativo |
| **6 — Presentación** | 15 | Defensa oral del proyecto completo | Todo lo anterior + Reflexiones finales |

---

## ⚙️ Stack Técnico

- **Lenguaje:** Python 🐍
- **Comunicación:** Sockets TCP (`import socket`)
- **Entorno:** Máquinas virtuales en red LAN
- **Control de versiones:** Git + GitHub
- **Licencia:** Open Source (MIT / GPL — ¡el equipo decide!)
- **Tiempo de respuesta objetivo:** < 1 segundo (o el servidor te juzga)

---

## 📋 Requisitos No Funcionales (los que sí importan)

- ✅ Implementación en Python
- ✅ Comunicación TCP mediante sockets
- ✅ Sincronización entre jugadores en tiempo real
- ✅ Manejo de desconexión del cliente sin colapso del servidor
- ✅ Compatibilidad con máquinas virtuales
- ✅ Tiempo de respuesta < 1 segundo
- ✅ Licencia Open Source y respeto a la propiedad intelectual

---

## 👩‍🏫 Equipo Docente

| Docente | Asignatura |
|---------|------------|
| Fernanda Paulina Vizcaino Imacaña | Lógica de Programación |
| Bryan Steven Vinueza Bustamante | Arquitectura de Computadoras y SO |
| Marcelo Fernando Pérez Jurado | Introducción a Redes de Datos |
| Engel Arrieta Philip Andre | Effective Communication |
| Gabriela Estefania Chiliquinga Jimenez | Ingeniería y Pensamiento Humano |

---

## 📁 Repositorios de los Equipos

> Cada equipo añade su enlace aquí mediante Pull Request o directamente en esta tabla:

| Equipo | Juego | Repositorio | Estado |
|--------|-------|-------------|--------|
| Team 01 | 🎮 ... | [link]() | 🔧 En desarrollo |
| Team 02 | 🎮 ... | [link]() | 🔧 En desarrollo |
| Team 03 | 🎮 ... | [link]() | 🔧 En desarrollo |

*(Los equipos actualizan esta tabla con su nombre, juego y enlace)*

---

## ✅ ¿Cómo sé si mi entrega está bien?

Antes de hacer commit, pregúntate:

```python
checklist = {
    "README.md completo con licencia y créditos": False,
    "Código separado en módulos (no todo en un solo .py)": False,
    "Sockets TCP implementados en server.py y client.py": False,
    "Juego funciona en modo local": False,
    "Juego funciona en modo multijugador LAN": False,
    "Manejo de desconexión del cliente": False,
    "Video demostrativo grabado": False,
    "Bitácora de conflictos con Fórmula Asertiva": False,
}

if all(checklist.values()):
    print("¡Listo para presentar! 🎉")
else:
    pendientes = [k for k, v in checklist.items() if not v]
    print(f"Falta: {pendientes}")
```

---

## 📜 Ética y Licenciamiento

Este repositorio y todos los proyectos aquí alojados deben:

- Incluir una **licencia Open Source** en cada repo (`LICENSE`)
- **Citar correctamente** cualquier código de terceros, librería externa o asistencia de IA
- Garantizar que la **comunicación por sockets TCP** no exponga datos sensibles
- No contener código malicioso ni vulnerabilidades intencionales

> La ética no es un requisito de la rúbrica. Es un requisito de la profesión. 🤝

---

## 💬 Canales de Comunicación del Proyecto

*(Completar por cada equipo en su propio README, según el Contrato de Comunicación establecido en Fase 1)*

---

## 🏁 Criterios de Evaluación Final (Resumen)

| Criterio | Puntaje |
|----------|---------|
| Lógica y Funcionalidad del Sistema | /4 |
| Arquitectura y Redes (Cliente-Servidor) | /4 |
| Diseño Centrado en el Usuario | /4 |
| Ética y Responsabilidad Profesional | /4 |
| Comunicación, Defensa y Trabajo en Equipo | /4 |
| **TOTAL** | **/20** |

---

<div align="center">

**Escuela de Ciencias de la Computación — ESPE / UTE / [Universidad]**

*Periodo Marzo–Julio 2025 · Primer Nivel · Lógica de Programación*

Hecho con `while (café > 0): código()` ☕

</div>

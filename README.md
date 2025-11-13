# S U R V I V O R

Un juego 2D de disparos y supervivencia (top-down) desarrollado en Python con Pygame. ¡El objetivo es simple: sobrevive a las hordas de monstruos, acumula puntos y encuentra la salida!

![Screenshot del Menú Principal](./screenshots/gameplay_menu_principal.png)
![Screenshot de la Jugabilidad](./screenshots/gameplay_partida.png)
![Screenshot de Menú](./screenshots/gameplay_menu.png)
---

## 🎮 Jugabilidad

¡Tu misión es sobrevivir! Moverás a tu héroe a través de diferentes niveles infestados de enemigos. Deberás eliminarlos mientras buscas el cofre que te permitirá escapar al siguiente desafío.

### Controles
* **W, A, S, D:** Mover al personaje.
* **Click Izquierdo:** Disparar en la dirección del mouse.
* **E:** Interactuar con objetos (como puertas).

### Objetivo
* **Sobrevive:** No dejes que los enemigos te derroten.
* **Acumula Puntos:** Cada enemigo eliminado suma a tu puntaje.
* **Encuentra la Salida:** ¡Busca el cofre para escapar!
* **Gana:** Supera todos los niveles y registra tu puntaje en el ranking.

---

## ✨ Características Principales

* **Menú Completo:** Pantalla de inicio, menú de opciones, ranking y controles.
* **Selección de Personaje:** Elige entre varios héroes al comenzar.
* **Múltiples Niveles:** El juego carga niveles desde archivos `.csv`.
* **Ranking Persistente:** Los puntajes (Top 5) se guardan en un archivo `scores.csv`.
* **Opciones de Juego:** Ajusta la dificultad (Fácil, Normal, Difícil) y el volumen del juego.
* **Sistema de Items:** Recoge monedas (aumentan el score) y pociones (recuperan vida).

---

## 🚀 Instalación y Requisitos

Para poder ejecutar este juego, necesitas tener **Python 3** y la librería **Pygame** instaladas.

**1. Prerrequisitos:**
* [Python 3](https://www.python.org/downloads/) (El proyecto fue probado con 3.11).

**2. Clonar el Repositorio (Ejemplo):**
git clone https://github.com/sergiosmmr/Juego_pygame-survivor-.git cd juego_pygame_SURVIVOR


**3. Instalar Dependencias:**
Puedes instalar la única dependencia usando el archivo `requirements.txt`:
pip install -r requirements.txt


**4. Ejecutar el Juego:**
python main.py


---

## 🛠️ Tecnologías Utilizadas

Este proyecto fue construido utilizando:

* **Python 3:** Como lenguaje principal de programación.
* **Pygame:** La librería fundamental para el desarrollo del juego (manejo de gráficos, sonido, física y controles).
* **Módulo `csv`:** Utilizado para guardar y leer los puntajes del ranking.
* **Módulo `os`:** Para la gestión de archivos y rutas (carga de assets, verificación de `scores.csv`).

---

## 📂 Estructura del Proyecto

El código está organizado de forma modular para facilitar su mantenimiento:

/juego_pygame_SURVIVOR/
├── main.py                 # Bucle principal, gestión de eventos y diccionario de assets
├── pantalla.py             # Lógica de dibujado de todos los menús y pantallas
├── utils.py                # Funciones de ayuda (cargar imágenes, dibujar texto, etc.)
├── personaje.py            # Clase del Jugador (Player)
├── enemigo.py              # Clase de los Enemigos
├── weapon.py               # Clase del Arma y las Balas
├── mundo.py                # Clase del Mundo (carga y dibuja el mapa)
├── texto.py                # Clase para el texto de daño flotante
├── items.py                # Clase para los ítems (monedas, pociones)
├── constantes_varaibles.py   # Constantes (colores, velocidad, rutas, etc.)
├── /assets/                # Carpeta con todas las imágenes, fuentes y sonidos
├── /niveles/               # Archivos .csv con el diseño de los mapas
├── /screenshots/           # Capturas de pantalla del juego
├── scores.csv              # Archivo de guardado de puntajes (se crea al jugar)
├── README.md               # Documentación del proyecto
└── requirements.txt        # Dependencias de Python

---

## ✍️ Autor

* **Sergio Maximiliano Martinez Rivero**
* GitHub: [@sergiosmmr](https://github.com/sergiosmmr)
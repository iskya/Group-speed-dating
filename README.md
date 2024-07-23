# Group-speed-dating-bot
Bot de Discord que simula citas rápidas en grupo.

## Créditos
- Bot tomado y modificado de <a href="https://github.com/isabellaenriquez/speed-dating-bot">
Isabella Enriquez</a>
- Funcionalidad de cuenta regresiva acreditada a <a href="http://github.com/asns2001">Sanindie Silva</a>.


## Configuración
1. `git clone` este repositorio.
2. `cd` en la carpeta local.
3. `pip3 install -r requirements.txt` --> esto descargará todos los módulos requeridos; si estás usando Python 3 >= 3.4 descargado desde python.org, ya deberías tener pip.
4. Inicia sesión en el Portal de Desarrolladores de Discord y crea una aplicación.
5. Crea un bot en la pestaña Bot, añade la imagen del bot proporcionada (`logo.jpeg`) y copia el token. 
6. Crea un archivo ``.env`` en tu carpeta local; escribe `DISCORD_TOKEN='token'`, donde token es tu token personalizado del bot del paso 5, y `GUILD='guild'`, donde guild es el nombre del servidor en el que deseas ejecutar el bot.
7. Ve a la pestaña OAuth2 en el Portal y, en el Generador de URL, establece `bot` como scope.
8. En los permisos del bot, establece los permisos apropiados.
9. Copia el enlace bajo el generador de URL y pégalo en el navegador, luego sigue los pasos para agregar el bot a tu servidor deseado.
10. Modifica el decorador `@commands.has_role` antes de cada comando para que tenga el nombre del rol que puede usar el bot (o elimínalo por completo si deseas permitir que cualquiera lo use).
11. Si lo deseas, puedes modificar el estado del bot en la función `on_ready`.
12. Para ejecutar el bot, simplemente ejecuta `python3 bot.py` mientras estás en la carpeta.
# Comandos
- ``!add <USER ID>`` - agrega un miembro del servidor a la lista de participantes si hay un juego de citas rápidas en curso
- ``!begin <CHANNEL ID>`` - inicia un juego de citas rápidas, dado el ID del canal de voz donde están los participantes iniciales (nota: debe haber 4 o más usuarios para poder jugar); se te pedirá el número de rondas (si las hay), tamaño del grupo y la duración de cada ronda (si la hay)
- ``!end`` - fuerza el fin del juego
- ``!goodbye`` - cierra la sesión del bot
- ``!help`` - muestra una lista de los comandos
- ``!members <CHANNEL ID>`` - cuenta el número de usuarios en el canal de voz dado
- ``!participants`` - muestra los nombres de usuario de los participantes actualmente en el juego
- ``!remove <USER ID>`` - elimina un miembro del servidor de la lista de participantes si hay un juego de citas rápidas en curso
- ``!shuffle`` - mezcla forzadamente a los participantes

## Guía para los participantes
### ¡Bienvenidos al Group Speed Dating!

Vas a poder conocer gente nueva de una manera rápida y divertida 👋🏼 😉
Sigue estos pasos para participar :

- Únete al canal designado:
Busca al canal de voz designado al Group ⁠Speed Dating en el servidor.

- Espera tu turno:
Una vez en la sala, el bot te pondrá en una cola de espera.
Cuando sea tu turno, serás movido a un canal de voz distinto junto con otros participantes, el cual podrás ver en el listado de canales, asegúrate de estar en ese canal.

- Disfruta de la cita:
En la sala de voz, tendrás el tiempo designado para conversar con las demás personas.
Recuerda:
    - Activa tu micrófono para participar en la conversación.
    - Si lo deseas y el ancho de banda te lo permite, puedes activar tu cámara también.

#### ¡Conoce a los demás participantes, haz preguntas y diviértete!

#### Al finalizar la cita:
Al terminar el tiempo de la ronda, el bot te moverá automáticamente a otra sala con otro grupo de personas.
No cambies de sala manualmente, deja que el bot lo haga.

#### Consejos:
- Sé respetuoso con los demás participantes.
- Mantén una conversación fluida y haz preguntas interesantes.
- No te preocupes si no conectas con alguien, ¡hay muchas otras personas por conocer!

Si tienes inconvenientes con la actividad, lo puedes reportar en el canal ⁠⁠soporte-técnico y haremos lo posible en ayudarte.

### ¡Diviértete y disfruta de la experiencia!
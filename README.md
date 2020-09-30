# Segunda Tarea de la materia Introducción a Ciencia de Datos 2020 Equipo 7

**Profesor:** Liliana Millan

**Integrantes del equipo**

Num | Alumno                      | Clave única
--- | --------------------------- | -----------
1   | Angel Rafael Ortega Ramírez | 123972
2   | Eduardo Moreno              | 151280
3   | Yedam Fortiz                | 119523

## ¿Cómo reproducir los resultados de este repositorio?

Si usted desea reproducir los hallazgos encontrados en este trabajo, lo que tiene que hacer es lo siguiente:

1. clonar el repositorio en la dirección de su agrado dentro de su computadora con el comando: `git clone <url del repositorio> <nombre que desea poner al repositorio dentro de su sistema>`

2. descargar el csv de [esta url](https://datos.cdmx.gob.mx/explore/dataset/consumo-agua/download/?format=csv&timezone=America/Mexico_City&lang=es&use_labels_for_header=true&csv_separator=%2C) y colocarlo en la carpeta `data`.

3. **opcional, requiere pyenv:** Genera el ambiente virtual para este proyecto con el comando `pyenv virtualenv 3.7.4 nombre_de_tu_environment`

  Activa el ambiente virtual con el siguiente comando: `pyenv activate nombre_de_tu_environment`

  --> instalar ipykernel<br>
  `pip install ipykernel`

  --> hacer accesible el ambiente virtual al notebook de jupyter<br>
  `python -m ipykernel install --user --name nombre_de_tu_environment --display-name nombre_de_tu_environment`

4. Instalar el `requirements.txt` que se encuentra en el mismo directorio de este archivo `README.md` con el comando: `pip install -r requirements.txt`

5. Abre tu terminal y desde ella entra al directorio raíz de este archivo.

6. Corre el comando `jupyter notebook` (asegúrate de tener activo tu environment).

7. Abre el archivo `Laboratorio_limpio` y ya podrás operarlo sin problemas.

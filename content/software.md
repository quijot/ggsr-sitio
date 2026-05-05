---
title: "Software producido por el GGSR"
slug: "software"
date: 2014-05-24
toc: true
---

## [Servicio PPP _Experimental_ GGSR][ppp-ggsr]

Dado un archivo de observaciones RINEX de un sitio estático, se obtienen las coordenadas en el Marco de Referencia oficial de la Argentina, POSGAR07.

El **Servicio PPP** consta de los siguientes pasos:
1. Procesamiento el RINEX con el Servicio de NRCan [CSRS-PPP](https://webapp.geod.nrcan.gc.ca/geod/tools-outils/ppp.php) y obtención de coordenadas en el marco ITRF/IGS20 para la época de medición del RINEX.
2. [Transformación ITRF→POSGAR][ppp-ggsr] desarrollada por GGSR, para obtener coordenadas POSGAR07, época 2006.632.

### [Transformación ITRF→POSGAR][ppp-ggsr]

Permite transformar coordenadas ITRF/IGS (de **cualquier** época) al Marco de Referencia oficial de nuestro país, POSGAR07 (época 2006.632).

Esta aplicación es la sucesora de [Calculadora PPP](/software/ppp-pagani.pdf) y [Calculadora ITRF→POSGAR](/software/calc-pestarini.pdf) e incluye mejoras sustanciales en el cálculo, dado que [calcula una interpolación IDW con datos de las Estaciones Permanentes RAMSAC más cercanas al punto de interés][ppp-ggsr]omo-funciona), a partir de [sugerencias del Prof. Dr. Hermann Drewes](https://www.sirgas.org/fileadmin/docs/Boletines/Bol21/13_Drewes_2016_Differentials_vs_differences.pdf).

_Calculadora PPP_ y _Calculadora ITRF→POSGAR_, la semilla de este servicio, son respectivos trabajos finales de estudiantes de la carrera de Agrimensura de esta Facultad.

Para mayor información, puede consultar:
- Pagani, Gustavo Aníbal & Noguera, Gustavo. (diciembre, 2013). [Posicionamiento Puntual Preciso y su aplicaicón en Agrimensura](/software/ppp-pagani.pdf). FCEIyA, UNR.
- Pestarini, Santiago & Noguera, Gustavo. (noviembre, 2016) [Georreferenciación utilizando servicios de posicionamiento en línea](/publicaciones/calc-pestarini.pdf).

[ppp-ggsr]: https://ppp.up.railway.app/

## [Geocoo 1.0.1](/software/geocoo.zip)

Es un programa que ayuda a resolver problemas de cálculo que en la actualidad son habitualmente requeridos por diversas aplicaciones propias de la topografía y la geodesia.

Está diseñado para que su uso sea muy sencillo permitiendo generar salidas que a su vez puedan ser leídas por otros programas.

El programa básicamente realiza **conversiones entre distintos tipos de coordenadas** de uso habitual y **transformaciones entre distintos marcos de referencia**.

Una característica destacable es que el programa tiene un alto grado de parametrización lo que permite que el usuario pueda adaptar los cálculos a las características del problema a resolver.

[Descargar Geocoo](/software/geocoo.zip). Compatible con Windows XP Home, Windows XP Professional y con Windows Vista.

# Software recomendado por el GGSR

Software y documentación que el GGSR utiliza y/o recomienda.

## [teqc](https://www.unavco.org/software/data-processing/teqc/teqc.html#executables)

Una simple pero poderosa utilidad para resolver problemas de pre-procesamiento con GPS, GLONASS, Galileo, SBAS, Beidou, QZSS e IRNSS, especialmente con formatos RINEX o BINEX.

[Más información](http://www.unavco.org/software/data-processing/teqc/teqc.html).\
IMPORTANTE: _teqc ha llegado al final de su ciclo de vida (EOL) tras su lanzamiento final el 25 de febrero de 2019._ Aunque aún sigue funcionando con limitaciones.

## [RNXCMP](http://terras.gsi.go.jp/ja/crx2rnx.html)  

Yuki Hatanaka creó estos programas que permiten (des)comprimir un archivo de observaciones RINEX en otro más pequeño en formato ASCII.

[Data - Hatanaka Format Information](http://www.unavco.org/software/data-processing/preprocessing/preprocessing.html#hatanaka)\
[Formato RINEX en Wikipedia.org](https://es.wikipedia.org/wiki/Rinex)

## [GFZRNX](https://gnss.gfz.de/services/gfzrnx/)

Caja de herramientas diseñada y creada para las necesidades de la comunidad GNSS. Admite datos de observación, navegación y meteorológicos RINEX.

Permite verificación, reparación y manipulación (muestreo, selección de sistemas satelitales y tipos de observación) de archivos RINEX, operaciones de empalme/división, generación de estadísticas, extracción de metadatos y muchas más.

Gratuito para fines científicos y educativos.

## [GNSS Format Descriptions](http://www.gage.es/gFD)  

Explicación de los formatos estándar. Por ejemplo: [Observation RINEX 2.11 Format](https://server.gage.upc.edu/gLAB/HTML/Observation_Rinex_v2.11.html).


## [GPS Web Calendar](http://navigationservices.agi.com/GNSSWeb/)  

Fechas específicas para la comunidad GPS.

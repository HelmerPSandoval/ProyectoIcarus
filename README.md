# ProyectoIcarus.

Actualmente tiene todas las dependencias necesarias para desarrollar tanto en la parte de backend como en la parte de frontend.

## Instalación.
#### Instalar las dependencias necesarias para desarrollar en el backend:
se debe ejecutar `pip install -r requirements.txt` y se instalará todo lo necesario, ya sea en un virtual enviroment o de manera global.  
*ignorar este paso si ya se han instalado django y djangorestframework.*

#### Instalar las dependencias necesarias para desarrollar en el frontend:
1. se debe posicionar en el directorio ~/.../ProyectoIcarus/frontend  
2. se debe ejecutar `npm install` y las dependencias se instalarán en la carpeta node_modules.
  
## Estándares
Los commits que se hagan al repositorio tienen que tener el formato de [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/#specification)  

#### Resumen conventional commits
El formato a utilizar será orientado a commits de una sola linea, por lo que no se usará cuerpo ni pie de página, entonces el formato de un commit en este repositorio es el siguiente:

> tipo(ámbito): descripción 

donde **tipo** hace referencia al tipo de commit y corresponde a alguna de las siguientes opciones:  
- fix : se arregló un bug, se parchó una clase con código defectuoso, se solucionó un error.
- feat : de feature, commit relacionado a alguna feature en desarrollo, avance en el código de una funcionalidad.
- build : relacionado a la configuración del proyecto, de sus librerías, dependencias o herramientas.
- docs : cambio en la documentación.
- perf : mejoras en la performance/rendimiento (tiempos de ejecución).
- refactor : cambios de refactorización, no se añade nuevo codigo ni se arreglan errores.
- style : cambios de formato en el código, indentanciones, comas, orden de las funciones, etc.
- test : cambios relacionado a pruebas.
- revert : revertir los cambios efectuados en algún commit.
- chore : cambios que no afectan el código fuente (src) ni archivos de prueba.
  
 El **ámbito** es opcional, va entre parentesis y es un sustantivo, describe a que parte del proyecto afecta el commit, por ejemplo (modelo usuario, vista inicio, estilos css)
 
 Si el **commit puede perjudicar algún otro componente** se debe poner **!** luego del tipo/ámbito, por ejemplo: 
 - fix! : inicio de sesión 
 - fix(login)! : inicio de sesión

La descricpción es un breve resumen del commit.

Luego de los dos puntos (:) debe haber un espacio y luego viene la descripción.

## Versionado de software

los estándares de versionados a utilizar serán los de:  [Semantic Versioning](https://semver.org/lang/es/) 

#### Resumen Semantic Versioning

La versión de cada release debe mantener el siguiente formato:
  
> [vMAJOR.MINOR.PATCH] , ejemplo: v2.1.9, donde:

- MAJOR: Es el número correspondiente a cambios importantes en el código que podrían no ser compatibles con versiones anteriores.
- MINOR: Cambios menos, cada nueva feature completa puede incrementar este número.
- PATCH: Versión del parche (arreglos de bug, malfuncionamiento).

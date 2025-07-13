# Generador de Microservicios C#

> Herramienta CLI para generar la estructura de proyectos de microservicios en C#, con Clean Architecture, value objects, DTOs y más.

## 📋 Contenidos

- [Descripción](#-descripción)  
- [Características](#-características)  
- [Prerrequisitos](#-prerrequisitos)  
- [Instalación](#-instalación)  
- [TODO](#-todo)  
- [Contribuciones](#contribuciones)  
- [Licencia](#licencia)  

---

## 📖 Descripción

Este proyecto provee un generador automático para acelerar la creación de microservicios en C# con una arquitectura limpia (Clean Architecture). Incluye plantillas para:

- Entidades y value objects  
- Repositorios y unidades de trabajo  
- Interfaces y clases de DTOs  
- Constructores y métodos estáticos de “Update”  
- Configuración de proyecto (Docker, scaffolding, migraciones)

---

## ⚙️ Características #características

- Esqueleto de domain, application e infrastructure  
- Soporte para navegación y relaciones entre entidades  

---

## 🛠️ Prerrequisitos #prerrequisitos

- Python 3.8+  
- .NET 8 SDK  
- Jinja2 (`pip install jinja2`)  

---

## 🚀 Instalación #instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/pozeydon-code/generatorMicroservices.git
   cd generatorMicroservices
   ```
   
## 📝 TODO

- [ ] Verificar que se estén cargando correctamente las validaciones de las Entidades.
- [ ] Implementar Custom Errors.
- [ ] Crear validaciones y `try/catch` para evitar fuga de errores.
- [ ] Implementar DTOs (quizás deba ser una carpeta con cada DTO por si crece el proyecto) para manejar respuestas más limpias.
- [ ] Generar una versión que haga un scaffold y mapee los datos de la base, para no insertar las migraciones desde mi proyecto.
- [ ] Generar una versión que utilice plantillas con Jinja2.

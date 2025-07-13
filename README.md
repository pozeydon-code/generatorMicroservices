# Generador de Microservicios C#

> Herramienta CLI para generar la estructura de proyectos de microservicios en C#, con Clean Architecture, value objects, DTOs y más.

## 📋 Contenidos

- [Descripción](#descripción)  
- [Características](#características)  
- [Prerrequisitos](#prerrequisitos)  
- [Instalación](#instalación)  
- [Uso](#uso)  
- [Estructura de carpetas](#estructura-de-carpetas)  
- [TODO](#todo)  
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

## ⚙️ Características

- Generación de carpetas y archivos usando Jinja2  
- Mapeo de tipos de C# a partir de un JSON de propiedades  
- Esqueleto de domain, application e infrastructure  
- Soporte para navegación y relaciones entre entidades  

---

## 🛠️ Prerrequisitos

- Python 3.8+  
- .NET 8 SDK  
- Jinja2 (`pip install jinja2`)  

---

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/pozeydon-code/generatorMicroservices.git
   cd generatorMicroservices

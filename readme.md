# 🛒 Carrefull App

Aplicación web inteligente de gestión y optimización de compras familiares basada en recetas, desarrollada con **Python** y **Streamlit**.

## 🚀 Características
- **Arquitectura MVC:** Separación limpia de responsabilidades (Model, View, Controller).
- **Autenticación Segura:** Sistema de login y registro con hashing de contraseñas (`SHA-256`) utilizando técnicas de salting dinámico a través de variables de entorno.
- **Catálogo Independiente:** Base de datos relacional (`SQLite3`) que aísla las listas y recetas por identificador de usuario.
- **Ruta de Góndola Optimizada:** Indexación y ordenamiento automático de los productos según el pasillo o sector del supermercado para agilizar el proceso de compra física.
- **Exportación de Datos:** Procesamiento y cierre de lista con descarga inmediata en formato CSV compatible con sistemas externos.

## 🛠️ Tecnologías utilizadas
- Python 3.14+
- Streamlit (UI Engine)
- SQLite3 (Base de datos persistente embebida)
- Pandas (Procesamiento de datos en tablas)
- Hashlib & OS (Seguridad y Variables de Entorno)
# ☕ Backend de Café San Domingo

¡Bienvenido al repositorio del backend para la gestión de solicitudes de Café San Domingo!

Este proyecto es una API construida con **FastAPI** para manejar de forma eficiente las solicitudes de pedidos y la gestión de usuarios. Su objetivo principal es servir como el corazón de la aplicación, facilitando la creación de usuarios, la autenticación y, en una fase posterior, el registro de órdenes de café.

---

## 🚀 Tecnologías Utilizadas

- **FastAPI**: Un framework web moderno y de alto rendimiento para construir APIs con Python 3.7+ basado en tipado estándar de Python.
- **Base de datos**: Se ha implementado una base de datos relacional para la persistencia de los datos de usuarios y órdenes.

---

## 📝 Historial de Desarrollo

- **15 de agosto**: Se inició el proyecto y se completaron los siguientes hitos iniciales:
  - **Creación de la base de datos** y las tablas necesarias para `usuarios` y `órdenes`.
  - **Implementación del `endpoint` para la creación de usuarios**. Este `endpoint` permite registrar nuevos usuarios en la base de datos de manera segura y validada.

---

## 🛠️ Próximos Pasos

El siguiente paso crucial en el desarrollo del proyecto es la implementación del `endpoint` para la **creación de órdenes de café**. Esta funcionalidad requiere:

- **Validación de autenticación**: El `endpoint` debe verificar un token generado para el usuario.
- **Vinculación de la orden**: La orden debe estar directamente asociada al `ID` del usuario que realiza la solicitud. Este `ID` se extraerá del token de autenticación.

---

## ⚙️ Cómo Empezar

Para poner en marcha este backend en tu entorno local, sigue los siguientes pasos:

1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/sindresorhus/del](https://github.com/sindresorhus/del)
    ```
2.  Ve al directorio del proyecto:
    ```bash
    cd [nombre-del-proyecto]
    ```
3.  Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Ejecuta la aplicación con Uvicorn:
    ```bash
    uvicorn main:app --reload
    ```
    _(Nota: Asegúrate de que tu base de datos esté configurada y accesible.)_

---

## 🤝 Contribuciones

Si deseas contribuir, puedes hacerlo directamente en la rama de desarrollo para trabajar en la funcionalidad de órdenes. ¡Tus aportes son bienvenidos!

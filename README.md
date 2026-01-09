# Invoice Processing System with Azure Document Intelligence

Este proyecto es una **API backend** diseñada para la carga, almacenamiento y procesamiento automático de facturas utilizando servicios administrados de **Microsoft Azure**.

La solución permite recibir documentos en formato **Base64**, almacenarlos de forma segura en **Azure Blob Storage** y extraer información estructurada mediante **Azure Document Intelligence**, persistiendo los datos procesados en **Azure SQL Database**.

El objetivo principal del proyecto es servir como **referencia técnica replicable**, mostrando buenas prácticas de integración cloud, seguridad de secretos y procesamiento de documentos con IA, sin depender de recursos activos del autor.

---

## 🧱 Arquitectura general

La siguiente arquitectura describe el flujo completo del sistema y los servicios de Azure involucrados en el procesamiento de facturas.

![Architecture Diagram](samples/ArquitecturaCloud.png)

---

## 🔄 Flujo de la aplicación

1. El cliente (web o móvil) envía una factura codificada en **Base64**.
2. El backend desplegado en **Azure App Service**:
   - decodifica el archivo,
   - lo convierte a PDF o imagen,
   - lo almacena en **Azure Blob Storage**.
3. El backend genera un **SAS Token** temporal para acceso controlado al archivo.
4. **Azure Document Intelligence** analiza el documento almacenado.
5. La información estructurada extraída es procesada por la API.
6. Los datos finales y la metadata del documento se almacenan en **Azure SQL Database**.
7. Los secretos y credenciales se gestionan de forma segura mediante **Azure Key Vault**.

---

## ✨ Funcionalidades principales

- 📤 Carga segura de facturas en formato Base64.
- 🧠 Extracción automática de información usando IA.
- 🔐 Gestión segura de secretos con Azure Key Vault.
- 📦 Almacenamiento de documentos en Blob Storage.
- 🔍 Persistencia y consulta de datos procesados mediante API REST.
- ☁️ Arquitectura completamente basada en servicios administrados de Azure.

---

## 🛠 Tecnologías utilizadas

- **Azure App Service** – ejecución del backend.
- **Azure Blob Storage** – almacenamiento de documentos.
- **Azure Document Intelligence** – análisis inteligente de facturas.
- **Azure SQL Database** – persistencia de metadata y datos extraídos.
- **Azure Key Vault** – gestión de secretos y credenciales.
- **Python 3.11**
- **Flask**
- **python-dotenv**

---

## 📋 Requisitos previos

- Python **3.9+**
- **pip**
- Acceso a una **suscripción de Azure**
- Variables de entorno configuradas (ver documentación de configuración)

---

## 📚 Documentación adicional

- 📐 Arquitectura detallada: `docs/architecture.md`
- 🚀 Manual de despliegue en Azure: `docs/deployment.md`
- 🔐 Configuración de secretos y Key Vault: `docs/secrets.md`
- 📡 Manual de uso de la API: `docs/api-usage.md`

---

## 🧪 Estado del proyecto

Proyecto funcional y en evolución, enfocado en demostrar buenas prácticas de desarrollo backend y arquitectura cloud con Azure.

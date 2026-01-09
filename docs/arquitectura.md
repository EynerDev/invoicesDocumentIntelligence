## 🏗 Arquitectura del Sistema

Este proyecto implementa una arquitectura cloud orientada a servicios, utilizando componentes administrados de **Microsoft Azure** para el procesamiento automatizado de facturas.

El objetivo principal es recibir documentos desde un frontend, almacenarlos de forma segura, extraer información estructurada mediante inteligencia artificial y persistir los resultados para su posterior consulta.

---

### 📌 Diagrama de Arquitectura

![Arquitectura del Sistema](/samples/ArquitecturaCloud.png)

---

## 🔄 Flujo General de la Aplicación

1. Un **Frontend App** envía una factura en formato **Base64** al backend.
2. El **Backend**, desplegado en **Azure App Service**, recibe el archivo y:
   - Decodifica el Base64.
   - Convierte el archivo a PDF o imagen.
   - Sube el documento a **Azure Blob Storage**.
3. El backend genera una **URL segura (SAS Token)** para el archivo almacenado.
4. Usando esta URL, el backend invoca **Azure Document Intelligence**, que:
   - Analiza el documento.
   - Extrae información estructurada como proveedor, fecha, totales, impuestos, etc.
5. La información extraída y la metadata del documento se almacenan en **Azure SQL Database**.
6. Durante todo el proceso, los secretos y credenciales se obtienen de forma segura desde **Azure Key Vault**.

---

## 🧩 Componentes de la Arquitectura

### 🔹 Azure App Service
- Aloja la API backend desarrollada en **Python (Flask)**.
- Orquesta todo el flujo de la aplicación.
- Gestiona la carga de documentos, generación de SAS y llamadas a servicios externos.
- Consume secretos de manera segura mediante integración con Azure Key Vault.

---

### 🔹 Azure Blob Storage
- Almacena los archivos originales (PDF / imágenes).
- Permite acceso controlado mediante **SAS Tokens**.
- Actúa como fuente de datos para el procesamiento con Document Intelligence.

---

### 🔹 Azure Document Intelligence
- Servicio de inteligencia artificial especializado en documentos.
- Extrae información estructurada a partir de facturas.
- Elimina la necesidad de procesamiento manual o reglas personalizadas.

---

### 🔹 Azure SQL Database
- Almacena:
  - Metadata del documento (nombre, proveedor, ruta del archivo).
  - Datos extraídos de la factura.
- Permite consultas estructuradas y reportes posteriores.

---

### 🔹 Azure Key Vault
- Centraliza el almacenamiento de secretos sensibles como:
  - Cadenas de conexión.
  - Claves de servicios cognitivos.
  - Credenciales de almacenamiento.
- Evita el uso de secretos en el código o en el repositorio.

---

## 🔐 Seguridad y Buenas Prácticas

- ❌ No se almacenan secretos en el código fuente.
- ✅ Uso de **variables de entorno** en local y **Key Vault** en la nube.
- ✅ Acceso a blobs mediante **SAS Tokens** con expiración.
- ✅ Servicios administrados para reducir superficie de ataque y costos operativos.

---

## 📈 Escalabilidad y Extensibilidad

- El backend puede escalar automáticamente con App Service.
- Se pueden agregar nuevos tipos de documentos sin modificar la arquitectura base.
- El diseño permite integrar fácilmente otros servicios de Azure (Functions, Event Grid, etc.).

---

Esta arquitectura está pensada para ser **replicable**, **segura** y **lista para producción**, sirviendo como referencia para proyectos reales de procesamiento documental en la nube.

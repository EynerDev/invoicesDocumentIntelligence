# Invoice Processing System with Azure Document Intelligence

Este proyecto es una **API backend** diseñada para la carga, almacenamiento y procesamiento automático de facturas utilizando **servicios de Microsoft Azure**.

La solución permite recibir documentos en formato Base64, almacenarlos de forma segura en Azure Blob Storage y extraer información estructurada mediante **Azure Document Intelligence**, guardando la metadata resultante en una base de datos.

El proyecto está pensado para ser **replicable en cualquier suscripción de Azure**, incluyendo documentación paso a paso para crear los recursos necesarios y configurar el entorno, sin depender de recursos activos del autor.

---

## 🏗 Arquitectura General

La siguiente arquitectura describe el flujo completo del sistema y los servicios de Azure involucrados en el procesamiento de facturas.

![Arquitectura](samples/ArquitecturaCloud.png)

---

## 🔄 Flujo de la Aplicación

1. Los usuarios (clientes web/móvil) envían archivos en **Base64**.  
2. **App Service** recibe el archivo, lo convierte a PDF/imagen y lo guarda en **Blob Storage**.  
3. **App Service** registra la URL del blob en **Azure SQL Database**.  
4. Cuando el archivo ingresa a Blob Storage, se dispara la **Function App** (BlobTrigger).  
5. La Función genera un **SAS Token** y llama a **Document Intelligence**.  
6. **Document Intelligence** procesa el archivo y devuelve la información estructurada.  
7. Los resultados procesados ​​se guardan en **Cosmos DB** para consultas y análisis.  

---

## ✨ Funcionalidades principales

- 📤 Carga de facturas y almacenamiento seguro en la nube.  
- 🤖 Procesamiento automatizado con IA para extraer campos como fecha, total, impuestos, etc.  
- 🔍 Consulta de facturas procesadas mediante **API REST**.  
- 🔗 Integración completa con el ecosistema de **Azure**.  

---

## 🛠 Tecnologías utilizadas

- **Azure Blob Storage** (almacenamiento de archivos).
- **Azure Key Vault** (Almacenamiento de Secretos, Keys y Cadenas de conexion)
- **Azure Document Intelligence** (servicios cognitivos para procesar facturas).  
- **Azure SQL Database** (registro de metadatos).  
- **Azure App Service** (ejecución de la API en la nube).  
- **Python 3.11** + **Flask** (backend API).  
- **dotenv** (manejo de variables de entorno).  

---

## 📋 Requisitos previos

- Python **3.9+**  
- **pip**  
- Acceso a una **suscripción de Azure**  
- Un archivo `.env` con las configuraciones necesarias (basado en `.env.example`)  

---

## ⚙️ Instalación

1. Clona este repositorio:  
   ```bash
   git clone https://github.com/EynerDev/invoicesDocumentIntelligence.git
   cd invoicesDocumentIntelligence

2. 🚀 Despliegue en Azure (ejemplo con CLI)
   ```bash
   # Crear grupo de recursos
   az group create --name rg-facturas --location eastus
   
   # Crear cuenta de almacenamiento
   az storage account create \
     --name facturasstorage \
     --resource-group rg-facturas \
     --location eastus \
     --sku Standard_LRS
   
   # Crear base de datos SQL
   az sql server create \
     --name sqlfacturaserver \
     --resource-group rg-facturas \
     --location eastus \
     --admin-user adminuser \
     --admin-password YourP@ssword123
   
   # Crear CosmosDB
   az cosmosdb create \
     --name facturascosmos \
     --resource-group rg-facturas \
     --kind MongoDB


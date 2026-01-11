# 🚀 Manual de Despliegue en Azure

Este documento describe paso a paso cómo desplegar el **Invoice Processing System** en una suscripción de Azure, permitiendo que cualquier persona replique el proyecto sin depender de recursos del autor.

El despliegue está diseñado para ser **simple, seguro y reproducible**, usando servicios PaaS de Azure.

---

## 📌 Arquitectura del Despliegue

El sistema utiliza los siguientes servicios de Azure:

- Azure App Service (Backend API en Python)
- Azure Blob Storage (almacenamiento de documentos)
- Azure SQL Database (metadata de facturas)
- Azure Document Intelligence (procesamiento de documentos con modelo personalizado)
- Azure Key Vault (gestión de secretos)

---

## ✅ Requisitos Previos

Antes de iniciar, asegúrate de contar con:

- Una **suscripción activa de Azure**
- Acceso al **Portal de Azure**
- **Azure CLI** instalado (opcional, pero recomendado)
- Python **3.9 o superior** (solo para pruebas locales)

---

## 1️⃣ Crear Grupo de Recursos

Todos los recursos se agruparán en un mismo Resource Group.

```bash
az group create \
  --name rg-invoice-system \
  --location eastus
```
## 2️⃣ Crear Azure Storage Account

Este servicio almacenará las facturas procesadas.

```bash
az storage account create \
  --name invoicestorage123 \
  --resource-group rg-invoice-system \
  --location eastus \
  --sku Standard_LRS
```
Crear el contenedor para las facturas:

```bash
az storage container create \
  --name invoices \
  --account-name invoicestorage123
```
## 3️⃣ Crear Azure SQL Database
Crear servidor SQL

```bash
az sql server create \
  --name invoice-sql-server \
  --resource-group rg-invoice-system \
  --location eastus \
  --admin-user sqladmin \
  --admin-password YourStrongPassword123!
```
Crear Base de datos

```bash
az sql db create \
  --resource-group rg-invoice-system \
  --server invoice-sql-server \
  --name InvoiceDB \
  --service-objective Basic
```
⚠️ El esquema de la base de datos se inicializa en un paso posterior.

## 4️⃣ Crear Azure Document Intelligence

Este proyecto utiliza **Azure Document Intelligence con un modelo personalizado**, entrenado específicamente para el procesamiento de facturas.

### Crear el recurso

1. En el **Portal de Azure**:
   - Crear un recurso **Azure AI Services → Document Intelligence**
   - Seleccionar una región compatible
   - Crear el recurso

2. Una vez creado, ingresar al recurso y copiar:
   - **Endpoint**
   - **API Key**

Estos valores **no se almacenan en el código**, se guardan posteriormente en **Azure Key Vault**.

---

### 🧠 Crear y entrenar el modelo personalizado

El sistema **no utiliza modelos preconstruidos**, sino un **modelo entrenado por el usuario**, lo que permite mayor precisión según el tipo de factura.

#### Pasos para entrenar el modelo

1. Ingresar a **Document Intelligence Studio** desde el recurso creado.
2. Crear un **proyecto de modelo personalizado**.
3. Subir documentos de ejemplo (facturas reales o de prueba).
4. Etiquetar los campos relevantes, por ejemplo:
   - Número de factura
   - Fecha
   - Total
   - Impuestos
   - Proveedor
5. Entrenar el modelo.
6. Al finalizar, copiar el **Model ID** generado.

> ⚠️ El `Model ID` es obligatorio para que la API funcione correctamente.

Este identificador se utilizará en la aplicación para invocar el modelo entrenado y **debe almacenarse como secreto en Azure Key Vault**.

---

### 🔐 Secretos asociados a Document Intelligence

Los siguientes valores deben almacenarse en **Azure Key Vault**:

- `DOCUMENT_INTELLIGENCE_ENDPOINT`
- `DOCUMENT_INTELLIGENCE_API_KEY`
- `DOCUMENT_INTELLIGENCE_MODEL_ID`

La aplicación obtiene estos valores mediante configuración en **Azure App Service**, sin exponerlos en el repositorio.

## 5️⃣ Crear Azure Key Vault
```bash
az keyvault create \
  --name kv-invoice-system \
  --resource-group rg-invoice-system \
  --location eastus
```
En este Key Vault se almacenarán:

- Connection String de Azure SQL
- Connection String de Blob Storage
- Endpoint de Document Intelligence
- API Key de Document Intelligence
- Model ID del modelo entrenado

## 6️⃣ Crear App Service Plan
```bash
az appservice plan create \
  --name asp-invoice-system \
  --resource-group rg-invoice-system \
  --sku B1 \
  --is-linux
```
## 7️⃣ Crear Azure App Service
```bash
az webapp create \
  --name invoice-api-eyner \
  --resource-group rg-invoice-system \
  --plan asp-invoice-system \
  --runtime "PYTHON|3.11"
```
## 8️⃣ Desplegar el Código
Desde el repositorio local clonado:
```bash
az webapp up \
  --name invoice-api-eyner \
  --resource-group rg-invoice-system
```
## 9️⃣ Configurar Variables de Entorno

Las variables de entorno no se definen en el código ni en archivos .env en producción.

Se configuran en:

Azure App Service → Configuration → Application Settings

Cada variable debe referenciar un secreto almacenado en Azure Key Vault.

La integración con Key Vault se documenta en un archivo separado.

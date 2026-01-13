# 🔐 Configuración de Secretos con Azure Key Vault

Este documento describe cómo almacenar y consumir secretos de forma segura usando **Azure Key Vault**, integrándolo con **Azure App Service** sin exponer credenciales en el código.

---

## 🎯 Objetivo

- Eliminar el uso de archivos `.env` en producción.
- Centralizar secretos (cadenas de conexión, claves, endpoints).
- Permitir rotación de credenciales sin redeploy.
- Usar **Managed Identity** para acceso seguro.

---

## 🧱 Servicios involucrados

- Azure Key Vault  
- Azure App Service  
- Azure RBAC (Role-Based Access Control)

---

## 1️⃣ Crear Azure Key Vault
Si aun no lo haz creado

Desde el portal o CLI:

```bash
az keyvault create \
  --name kv-invoices-intelligence \
  --resource-group rg-invoices-centralus \
  --location centralus
```

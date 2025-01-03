-- Crear la base de datos
CREATE DATABASE invoices_documentIntelligence;
GO

-- Usar la base de datos recién creada
USE invoices_documentIntelligence;
GO

CREATE TABLE invoices_details (
id INT NOT NULL PRIMARY KEY IDENTITY(1,1),
id_invoice INT NOT NULL,
number_invoice BIGINT NOT NULL,
billed_month NVARCHAR(150) NOT NULL,
issue_date NVARCHAR (150) NOT NULL,
expiration_date NVARCHAR(150) NOT NULL,
last_payment NVARCHAR(150) NOT NULL,
suspension_date NVARCHAR(150) NOT NULL,
overdue_invoices NVARCHAR(150) NOT NULL,
total_overdue_debt BIGINT NOT NULL,
total_invoices_month BIGINT NOT NULL,
active INT NOT NULL DEFAULT(1),
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
update_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

GO

CREATE TABLE provider (
id INT NOT NULL PRIMARY KEY IDENTITY(1,1),
name NVARCHAR(150) NOT NULL,
nit BIGINT NOT NULL,
email NVARCHAR(150) NOT NULL,
address NVARCHAR(150) NOT NULL,
number BIGINT NOT NULL,
website NVARCHAR(150) NOT NULL,
active INT NOT NULL DEFAULT(1),
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
update_at DATETIME DEFAULT CURRENT_TIMESTAMP

)

GO

CREATE TABLE type_invoices (
id INT NOT NULL PRIMARY KEY IDENTITY(1,1),
name NVARCHAR(150) NOT NULL,
active INT NOT NULL DEFAULT(1),
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
update_at DATETIME DEFAULT CURRENT_TIMESTAMP


)

GO
CREATE TABLE invoices  (
id INT NOT NULL PRIMARY KEY IDENTITY(1,1),
type_id INT NOT NULL,
provider_id INT NOT NULL,
number_contract BIGINT NOT NULL,
path_storage NVARCHAR(500) NOT NULL,
active INT NOT NULL DEFAULT(1),
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
update_at DATETIME DEFAULT CURRENT_TIMESTAMP


)

GO 
ALTER TABLE invoices_details
ADD CONSTRAINT FK_invoices_invoices1
FOREIGN KEY (id_invoice) 
REFERENCES invoices(id);

GO 
ALTER TABLE invoices
ADD CONSTRAINT fk_invoices_provider
FOREIGN KEY (provider_id) 
REFERENCES provider(id);

GO 
ALTER TABLE invoices
ADD CONSTRAINT fk_invoices_type_invoices
FOREIGN KEY (type_id) 
REFERENCES type_invoices(id);


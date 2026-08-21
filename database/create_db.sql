-- Run this script on your SQL Server instance first
CREATE DATABASE LOGIN_DB_DEV;
GO

USE LOGIN_DB_DEV;
GO

-- Tables are auto-created by SQLAlchemy when the backend starts.
-- Verify after first run:
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE';

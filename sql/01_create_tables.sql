-- Curated Gold tables

IF OBJECT_ID('dbo.daily_user_metrics', 'U') IS NOT NULL DROP TABLE dbo.daily_user_metrics;
CREATE TABLE dbo.daily_user_metrics (
    event_date date NOT NULL,
    dau int NOT NULL
);

IF OBJECT_ID('dbo.daily_event_type_metrics', 'U') IS NOT NULL DROP TABLE dbo.daily_event_type_metrics;
CREATE TABLE dbo.daily_event_type_metrics (
    event_date date NOT NULL,
    event_type varchar(50) NOT NULL,
    event_count bigint NOT NULL
);

IF OBJECT_ID('dbo.daily_device_metrics', 'U') IS NOT NULL DROP TABLE dbo.daily_device_metrics;
CREATE TABLE dbo.daily_device_metrics (
    event_date date NOT NULL,
    device varchar(50) NOT NULL,
    event_count bigint NOT NULL
);

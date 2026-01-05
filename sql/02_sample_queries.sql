-- Sample analytics queries

-- DAU trend
SELECT event_date, dau
FROM dbo.daily_user_metrics
ORDER BY event_date;

-- Top event types by day
SELECT event_date, event_type, event_count
FROM dbo.daily_event_type_metrics
ORDER BY event_date, event_count DESC;

-- Device usage by day
SELECT event_date, device, event_count
FROM dbo.daily_device_metrics
ORDER BY event_date, event_count DESC;

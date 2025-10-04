-- Performance optimization settings for PostgreSQL
-- These settings are optimized for development/test environments
-- Production values should be adjusted based on available resources

-- Memory settings
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET work_mem = '4MB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';

-- Connection settings
ALTER SYSTEM SET max_connections = '100';

-- Logging settings for development
ALTER SYSTEM SET log_statement = 'mod';
ALTER SYSTEM SET log_duration = 'on';
ALTER SYSTEM SET log_min_duration_statement = '1000ms';

-- Checkpoint settings
ALTER SYSTEM SET checkpoint_completion_target = '0.9';
ALTER SYSTEM SET wal_buffers = '16MB';

-- Query planner settings
ALTER SYSTEM SET random_page_cost = '1.1';
ALTER SYSTEM SET effective_io_concurrency = '200';

-- Reload configuration
SELECT pg_reload_conf();

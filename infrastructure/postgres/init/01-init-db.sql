-- PostgreSQL initialization script for betting league championship
-- This script creates the necessary databases and users for all environments

-- Create development database
CREATE DATABASE betting_league_dev;

-- Create test database
CREATE DATABASE betting_league_test;

-- Create production database (will be overridden in prod environment)
CREATE DATABASE betting_league_prod;

-- Create application user with appropriate permissions
CREATE USER betting_app WITH PASSWORD 'app_password';

-- Grant privileges to application user
GRANT CONNECT, CREATE ON DATABASE betting_league_dev TO betting_app;
GRANT CONNECT, CREATE ON DATABASE betting_league_test TO betting_app;
GRANT CONNECT, CREATE ON DATABASE betting_league_prod TO betting_app;

-- Connect to each database and grant schema privileges
\c betting_league_dev;
GRANT ALL PRIVILEGES ON SCHEMA public TO betting_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO betting_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO betting_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO betting_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO betting_app;

\c betting_league_test;
GRANT ALL PRIVILEGES ON SCHEMA public TO betting_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO betting_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO betting_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO betting_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO betting_app;

\c betting_league_prod;
GRANT ALL PRIVILEGES ON SCHEMA public TO betting_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO betting_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO betting_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO betting_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO betting_app;

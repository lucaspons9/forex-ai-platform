-- init.sql
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_database WHERE datname = 'forex') THEN
      CREATE DATABASE forex;
   END IF;
END
$$;

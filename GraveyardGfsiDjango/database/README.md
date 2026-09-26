# MariaDB (Database)

This directory contains the active MariaDB setup.

## 1. Configure `.env`

Edit `database/.env` if needed, or keep it as-is.

Required variables:

- `MARIADB_ROOT_PASSWORD`
- `MARIADB_DATABASE`
- `MARIADB_USER`
- `MARIADB_PASSWORD`

If your password contains `$`, keep it quoted in `.env`, for example:

```env
MARIADB_PASSWORD='Dr0w$saP'
```

## 2. Start MariaDB

From the `database` directory:

```powershell
docker compose up -d
```

Or from repo root:

```powershell
docker compose -f database/docker-compose.yml up -d
```

## 3. Restore dump on first init

`cemetery.sql` is mounted to `/docker-entrypoint-initdb.d/`.
MariaDB imports it automatically only when the data volume is empty (first initialization).

## 4. Load a new dump

If you get a new dump:

1. Replace `database/cemetery.sql` with the new file.
2. Recreate container + volume so init runs again:

```powershell
docker compose down -v
docker compose up -d
```

From repo root, use:

```powershell
docker compose -f database/docker-compose.yml down -v
docker compose -f database/docker-compose.yml up -d
```

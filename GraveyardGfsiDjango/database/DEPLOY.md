# Deploying to Render + Aiven

The Django app runs on **Render** (free web service, Docker). The database is
**Aiven for MySQL** (free plan: 1 GB storage, no card, no time limit). Both are
free; the trade-off is that Render puts the app to sleep after 15 minutes
without visitors, so the first visit after that takes 30-60 seconds.

Files involved:

| File | Purpose |
|---|---|
| `render.yaml` (repo root) | Render Blueprint: service, Docker build, environment variables |
| `GraveyardGfsiDjango/st_anthony/Dockerfile` | Production image (gunicorn + whitenoise) |
| `GraveyardGfsiDjango/database/move_to_aiven.py` | Copies the local database to Aiven |

No secrets are stored in the repository. Render generates `SECRET_KEY`; the
database details are entered in Render's dashboard.

## 1. Create the Aiven database

1. Sign up at <https://aiven.io> (free, no credit card).
2. **Create service** → **MySQL** → plan **Free** → pick a region close to your
   Render region (e.g. a US East region for Render's Ohio/Virginia) → **Create**.
3. Wait until the service shows **Running** (a few minutes).
4. On the service's **Overview** page, note **Host**, **Port**, **User**
   (`avnadmin`), **Password** and **Database name** (`defaultdb`), and click
   **Download** next to **CA certificate**. Save it as
   `GraveyardGfsiDjango/database/ca.pem`.

## 2. Copy the data to Aiven

From `GraveyardGfsiDjango/database`, with the local Docker database running:

```bash
python move_to_aiven.py export
```

```bash
python move_to_aiven.py load --host YOUR-AIVEN-HOST --port YOUR-AIVEN-PORT --ca ca.pem
```

`load` asks for the Aiven password, checks the connection is encrypted, loads
all 24 tables and prints row counts (expect 4316 plots and 2558 people).
Then delete `cemeterydb_for_aiven.sql` — it contains every record and the admin
login hash. It is git-ignored, but shouldn't be left lying around.

## 3. Push the code

Render deploys from GitHub, so the deployment files must be committed and
pushed to the branch Render will watch (by default, the branch that holds
`render.yaml`).

## 4. Create the Render service

1. Sign up at <https://render.com> with GitHub. The repository belongs to the
   **CivicTechFredericton** organisation, so an org owner may need to approve
   Render's GitHub app for it.
2. **New** → **Blueprint** → choose `cemetary-gis` and the branch → Render
   reads `render.yaml`.
3. Fill in the prompted values:
   - `DB_HOST`, `DB_PORT`, `DB_PASSWORD`: from the Aiven Overview page
   - `DB_SSL_CA_PEM`: open `ca.pem` in a text editor and paste its **entire**
     contents, including the `BEGIN`/`END CERTIFICATE` lines
4. **Apply**. The first build takes a few minutes. The site appears at
   `https://st-anthony-cemetery.onrender.com` (or a similar name if taken).
5. Log in with the admin account (same username and password as locally).

Each push to the watched branch redeploys automatically. Database migrations
run at start-up; once the data is loaded they have nothing to do.

## Keeping it running

- **Render free**: sleeps after 15 minutes idle; 750 free hours per month.
- **Aiven free**: Aiven may power off free services that are unused for a long
  time. If the site shows a database error, open the Aiven console and power
  the service back on.
- **Re-importing the CSV into Aiven**: copy the importer's
  `config/database.conf`, set `DB_DSN` to the Aiven host/port/`defaultdb`,
  `DB_USER`/`DB_PASS` to the Aiven login and add `DB_SSL_CA=ca.pem`, then run
  `python import_cemetery.py --config that-file --dry-run` first.

## Troubleshooting

| Symptom | Check |
|---|---|
| Build fails installing `mysqlclient` | The Dockerfile's build stage installs its libraries; make sure Render uses the Docker runtime from `render.yaml`. |
| `Bad Request (400)` | Visiting a hostname other than the Render one? Add it to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`. |
| Can't connect to MySQL / SSL errors | `DB_SSL_CA_PEM` must be the full certificate text; host and port must match Aiven. |
| Logins or forms fail with CSRF errors | Using a custom domain? Add `https://your-domain` to `CSRF_TRUSTED_ORIGINS`. |

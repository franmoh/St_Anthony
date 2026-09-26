# St. Anthony Django App

## Prerequisites

- Python 3.13+
- MySQL server running
- `uv` installed (`pip install uv`)

## 1. Install Dependencies

From the project root (`st_anthony`):

```powershell
uv sync
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 2. Configure Environment Variables

Create `.env` from `.env.example` and update values for your local MySQL database.

Example:

```env
DB_NAME=st_anthony_db
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your_secret_key_here
```

## 3. Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

Note: Some models in `cemetery/models.py` use `managed = False`, so Django will not create/alter those tables.

## 4. Run the App

```powershell
python manage.py runserver
```

Default URL:

- `http://127.0.0.1:8000/`

## 5. `django-tailwind` Development

You can use Tailwind CSS classes in HTML. For development, use one of these options:

Option 1 (Recommended): Start both Django and Tailwind development servers simultaneously:

```powershell
python manage.py tailwind dev
```

Option 2: Start only the Tailwind watcher (run `python manage.py runserver` separately):

```powershell
python manage.py tailwind start
```

These commands run the Tailwind watcher, which monitors your HTML templates for class changes and recompiles `styles.css` automatically.

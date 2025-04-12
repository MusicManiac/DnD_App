# Task Manager API
A Django-based API and database solution for DnD 3.5. Properly sets up relations and defines the majority of game systems related to character creation and management. Includes but not limited to: Races, Classes, Skills, Feats, Spells, Items and so on.

Create, retrieve, update, and delete objects that are properly related to other objects:
- Sources
- Languages
- Races
- Classes and Prestige Classes
- Skills
- Alignments
- Feats
- Spells
- Schools of Magic
- Items
- Special Materials
- Race Types and Subtypes
- and other major game systems
- 
## Technologies, Packages and Applications used

- [Python 3.12.7](https://www.python.org/downloads/release/python-3127/)
- [Django](https://www.djangoproject.com/download/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [ruff](https://github.com/astral-sh/ruff) for linting
- [black](https://github.com/psf/black) for code formatting
- [pytest](https://docs.pytest.org/en/stable/) for testing
- [Pycharm](https://www.jetbrains.com/pycharm/) as IDE
- [pgAdmin](https://www.pgadmin.org/) for more convenient database management

## Installation
Ensure you have the following installed:
- [Python 3.12.7](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [pip](https://pip.pypa.io/en/stable/)
- [python3-virtualenv](https://virtualenv.pypa.io/en/latest/index.html) (only required if you're not using [PyCharm](https://www.jetbrains.com/pycharm/download/))
- (Optional) [pgAdmin](https://www.pgadmin.org/download/) for non-CLI database creation

### Steps

Setting up PSQL (CLI):
1. Open SQL shell (psql),
2. Log in as postgres user (default password is postgres),
   ```
   psql -U postgres
   ```
3. Setup initial database by running following commands in SQL shell (psql):
   ```
   CREATE USER dnd_app_admin WITH PASSWORD 'admin';
   CREATE DATABASE dnd_app;
   ALTER USER dnd_app_admin CREATEDB;
   GRANT ALL ON SCHEMA public TO dnd_app_admin;
   GRANT ALL PRIVILEGES ON DATABASE dnd_app TO dnd_app_admin;
   ALTER DATABASE dnd_app OWNER TO dnd_app_admin;
   ```
4. Later on you can delete traces of this repo by running following commands in psql:
   ```
   DROP DATABASE dnd_app;
   REVOKE ALL ON SCHEMA public FROM dnd_app_admin;
   DROP USER dnd_app_admin;
   ```
Setting up PSQL (pdAdmin):
1. Open pgAdmin and connect to your PostgreSQL server.
2. Right-click on the "Login/Group Roles" node in the tree view and select "Create" -> "Login/Group Role...".
3. In the "General" tab, enter `dnd_app_admin`.
4. In the "Privileges" tab, check the "Create Databases?", "Inherit rights from parent roles?" and "Can login?" options.
5. Right-click on the "Databases" node in the tree view and select "Create" -> "Database...".
6. Name the database `dnd_app` and owner to `dnd_app_admin` click "Save".

Setting up project:
1. Clone repo
2. Set up the database:
   - Option 1: Use provided backup file and CLI
     ```
     psql -U dnd_app_admin -h localhost -p 5432 -d dnd_app -f "dnd_app_backup.sql"
     ```
     to restore database from backup. 
   - Option 2: Use pgAdmin and provided backup file
     1. Open pgAdmin and connect to your PostgreSQL server.
     2. Right-click on the "Databases" node in the tree view and select "Create" -> "Database...".
     3. Name the database `dnd_app` and click "Save".
     4. Right-click on the newly created database and select "Restore...".
     5. Choose the provided backup file (`dnd_app_backup.sql`) and click "Restore".
   - Option 3: Ignore provided database backup and use custom command to create bare minimum database (command provided further in this README)
2. (If using PyCharm) Setup Python Interpreter and virtual environment
   1. Go to Settings -> Python Interpreter -> Add Interpreter -> Select Local Interpreter -> select installed python version 3.12.7
   2. Open new terminal in PyCharm, it will be using venv by default
3. (If not using Pycharm and setting up venv manually) Set up virtual environment
   1. In project directory run `virtualenv manual_venv --python=python3.12.7` which will create new virtual environment.
   2. Enter your venv with `source manual_venv/bin/activate`
4. In previously opened virtual environment terminal, install required packages:
   ```
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Make migrations and import provided initial data (only if chose option 3 in "Set up the database"):
   ```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py run_all_import_commands
   ```
6. Run the server with `python manage.py runserver`
7. Open http://127.0.0.1:8000/api/ or run CURL commands from terminal

## Tests
Testing is implemented using [pytest](https://docs.pytest.org/en/stable/) and can be done by running command `pytest` in your virtual environment.


## Usage
You can interact with API using cURLs and/or browser. There are more than 40 endpoints available, so I won't be listing then here.
GET, POST, PUT and DELETE methods are available for most of the endpoints (excluding module endpoints where only GET is available).


> [!NOTE]
> When using CLI (command line interface), remember that you have to replace `"` with `\"` inside double quotes when sending json over so it's parsed corectly, as example:<br />
> `curl -X POST http://localhost:8000/api/common/dice/ -H "Content-Type: application/json" -d "{"sides":"40"}"`<br />
> becomes<br />
> `curl -X POST http://localhost:8000/api/common/dice/ -H "Content-Type: application/json" -d "{\"sides\":\"40\"}"`


All of this is also accessible via browser by opening http://127.0.0.1:8000/api/ with the help of Django REST framework.


## License
[MIT](https://github.com/MusicManiac/DnD_App/blob/master/LICENSE)

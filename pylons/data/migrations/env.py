"""Alembic migrations.
"""
from elixr2.web.devop import run_alembic


# providing the app name first ensures that the alembic migration table
# is named after the project
run_alembic(packages="pylons, elixr2")

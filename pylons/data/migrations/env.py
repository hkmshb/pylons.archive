"""Alembic migrations.
"""
from elixr2.web.devop import run_alembic


run_alembic(packages="elixr2, pylons")

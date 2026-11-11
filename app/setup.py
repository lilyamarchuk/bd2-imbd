from setuptools import setup, find_packages

setup(
    name="imdb_backend",
    version="1.0.0",
    description="Back-end (Flask + MySQL) для бази даних imdb_lab",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "Flask", "Flask-SQLAlchemy", "SQLAlchemy", "PyMySQL", "cryptography", "PyYAML",
    ],
)

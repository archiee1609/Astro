from setuptools import setup, find_packages

setup(
    name="astro-vedic",
    version="2.0.0",
    description="High Precision Vedic Astrology and Sankhya Numerology System",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=[
        "skyfield",
        "timezonefinder",
        "geopy",
        "fastapi",
        "uvicorn",
        "rich",
        "requests",
        "pandas",
        "streamlit",
        "jinja2",
    ],
    python_requires=">=3.10",
)

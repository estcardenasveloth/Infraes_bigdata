from setuptools import setup, find_packages

setup(
    name="Infraes_bigdata",
    version="0.0.1",
    author="Julio César Cárdenas",
    author_email="julio.cardenas@est.iudigital.edu.co",  # Completa con tu correo
    description="Descripción breve del paquete",  # Añade una descripción
    py_modules=["actividad_1"],  # Si solo tienes un módulo
    install_requires=[
        "pandas",
        "openpyxl",
        "requests"
    ],
    # Si tienes más módulos o submódulos, puedes usar:
    # packages=find_packages()
)
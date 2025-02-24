from setuptools import setup, find_packages

setup(
    name="Infra_bigdata_actividad1",
    version="0.0.1",
    author="Julio César Cárdenas",
    author_email="tucorreo@dominio.com",  # Completa con tu correo
    description="Descripción breve del paquete",  # Añade una descripción
    py_modules=["actividad_1"],  # Si solo tienes un módulo
    install_requires=[
        "pandas",
        "openpyxl"
    ],
    # Si tienes más módulos o submódulos, puedes usar:
    # packages=find_packages()
)
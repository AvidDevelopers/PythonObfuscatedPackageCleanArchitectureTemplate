from setuptools import find_namespace_packages, setup

version = "0.2.0"


setup(
    name="animal",
    version=version,
    packages=find_namespace_packages(),
    include_package_data=True,  # Importants
    python_requires="~=3.8",
)

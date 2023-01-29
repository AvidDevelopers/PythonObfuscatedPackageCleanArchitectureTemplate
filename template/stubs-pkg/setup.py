# -*- coding: utf-8 -*-
from setuptools import find_namespace_packages, find_packages, setup

# Collect package from src_pkg Automatically
packages = find_namespace_packages(".")
packages_name = packages[0]
original_package_name, _, _ = packages_name.partition("-")


# Create <packages_name> for stubs of <original_package_name>

setup(
    name=packages_name,
    version="0.2.0",
    description=f"Type annotations for {original_package_name}",
    long_description=f"{packages_name} package",
    packages=[x for x in packages],
    include_package_data=True,  # Important
    python_requires=">=3.8,<3.11",
)

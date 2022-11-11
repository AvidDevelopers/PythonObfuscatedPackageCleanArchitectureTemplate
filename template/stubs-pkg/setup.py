# -*- coding: utf-8 -*-
from setuptools import setup, find_packages, find_namespace_packages


# Collect package from src_pkg Automatically
packages = find_namespace_packages(".")
packages_name = packages[0]
original_package_name, _, _ = packages_name.partition("-")


# Going to create <packages_name> for stubs of <original_package_name>


setup(
    name=packages_name,
    version="0.1.0",
    description=f"Type annotations for {original_package_name}",
    long_description=f"{packages_name} package",
    author="Sadegh Yazdani",
    author_email="m.s.yazdani85@gmail.com",
    license="GPLv3",
    packages=[x for x in packages],
    include_package_data=True,  # Important
    install_requires=[],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8,<3.11",
)

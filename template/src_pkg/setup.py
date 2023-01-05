from setuptools import find_namespace_packages, setup

version = "0.1.0"
DESCRIPTION = "A print package"
LONG_DESCRIPTION = """A simple class for print python objects with tails."""


setup(
    name="animal",
    version=version,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Sadegh Yazdani",
    author_email="m.s.yazdani85@gmail.com",
    license="GPLv3",
    packages=find_namespace_packages(),
    include_package_data=True,  # Importants
    install_requires=[],
    keywords="printing",
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires="~=3.8",
)

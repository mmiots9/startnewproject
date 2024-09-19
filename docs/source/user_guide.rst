|PyPI version fury.io| |PyPI license|

.. |PyPI version fury.io| image:: https://badge.fury.io/py/startnewproject.svg
   :target: https://pypi.org/project/startnewproject/

.. |PyPI license| image:: https://img.shields.io/pypi/l/startnewproject.svg
   :target: https://pypi.org/project/startnewproject/

CLI Documentation
=======================

This is the official documentation for the CLI version of startnewproject. All commands explained here have a corresponding function (see API), but I highly reccomend to run this package from the command line, as it was created for.

Installation
----------------

startnewproject can be installed via `pip` in an isolated environment (suggested):

.. code-block:: console

   (.venv) $ pip install startnewproject

To check the installation:

.. code-block:: console

   (.venv) $ startnewproject --version

.. warning::
    Whilst the python dependencies are automatically downloaded and installed, this package relies on git. Therefore, git should be installed and correctly set up on your machine.

Create a new project folder
------------------------------

To create a new project folder, with the structure specified in the config file, type:

.. code-block:: console

   (.venv) $ startnewproject -n "name of the project"

There are also other optional flags:

- *-c CONFIG, --config CONFIG*: Path to the configuration file. By default, it will use the template configuration file installed with this package.
- *-f, --force*: Overwrite existing project directory.
- *--readme-template README_TEMPLATE*: Type of readme to create. By default, it will create a README.txt. Possible values are: txt, md, html.

Configuration file
^^^^^^^^^^^^^^^^^^^^
The configuration file is the one in which folder structure is definted. The user can use the default one or provide a custom one. In the latter case, the file **must** be a .json file with this structure:

.. code-block:: console

    {
        "description": "This is the README of the entire project. Here you can find information about folder structure, files and project details.", 
        "subfolders": {
            "subfolder1": {
                "description": "This folder contains folders and files of the analyses.",
                "subfolders": {},
                "files": []
            },
            "subfolder2": {
                "description": "This folder contains folders and files of the analyses.",
                "subfolders": {
                    "subsubfolder1": {
                        "description": "This folder contains folders and files of the analyses.",
                        "subfolders": {},
                        "files": ["file1.txt"]
                    },
                },
                "files": ["myfile.html"]
            },
        ".gitignore": ["*.DS_Store", "__pycache__/", "*.pyc"],
        ".gitattributes": {
            "binary": ["*png", "*jpg", "*jpeg", "*gif", "*tiff", "*tif", "*bmp", "*ico", "*svg", "*pdf"]
        }
    }

In this way, every subfolder is created (with nested subfolders) as well as .gitignore and .gitattributes files in the root folder of the project.

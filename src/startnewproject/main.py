"""
This module is the main module where all the functions to run the cli of startnewproject are 
defined.
"""
import argparse
import os
from datetime import datetime
import subprocess
import json
import shutil
import sys
from .version import __version__

def create_gitignore(config: dict) -> None:
    """Create .gitignore file.

    This function creates a gitignore file in the current working directory. It takes the 
    ".gitgnore" list of the config and write its content on each line.
    If empty, no .gitignore file will be created.

    :param config: configuration dictionary
    :type config: dict
    """
    ext_to_ignore: list = config.get(".gitignore", [])
    if ext_to_ignore:
        with open(".gitignore", "w", encoding='utf-8') as gitignore_file:
            for ext in ext_to_ignore:
                gitignore_file.write(f"{ext}\n")


def create_gitattributes(config: dict) -> None:
    """Create gitattributes file.

    This function creates a gitattributes file in the current working directory. 
    It takes the ".gitattributes" dictionary of the config file in which arguments are defined. 
    It creates a line for each element in binary list.

    :param config: configuration dictionary
    :type config: dict
    """
    binary_list: list = config.get(".gitattributes", {}).get("binary", [])
    if binary_list:
        with open(".gitattributes", "w", encoding='utf-8') as gitattributes_file:
            for ext in binary_list:
                gitattributes_file.write(f"{ext} binary -text\n")


def create_folder(folder_dict: dict, name: str, readme_template: str) -> None:
    """Create folder.

    This function creates a folder in the current working directory. It takes a folder_dict with 
    "subfolders" and "files" as keys. For each subfolder, it runs this function recursively.
    For each file, it creates a file with the same name in the current working directory.
    It creates a line for each element in folder_dict.
    It also creates a REAMDE file based on the readme_template file.

    :param folder_dict: config dictionary with folder structure.
    :type folder_dict: dict
    :param name: name of the folder to create.
    :type name: str
    :param readme_template: type of README file. Either "txt", "md" or "html", default to "txt".
    :type readme_template: str
    """
    # Create files
    for file in folder_dict.get("files", []):
        with open(file, "w", encoding="utf-8") as file_file:
            file_file.write("")

    # Create README
    script_dir: str = os.path.dirname(os.path.abspath(__file__))
    if readme_template == "txt":
        readme_template_file: str = os.path.join(script_dir, 'templates', 'README.txt')
        create_txt_readme(folder_dict, name, readme_template_file)
    elif readme_template == "md":
        readme_template_file: str = os.path.join(script_dir, 'templates', 'README.md')
        create_md_readme(folder_dict, name, readme_template_file)
    elif readme_template == "html":
        readme_template_file: str = os.path.join(script_dir, 'templates', 'README.html')
        create_html_readme(folder_dict, name, readme_template_file)

    # Create subfolders
    for folder_name, dictionary in folder_dict.get("subfolders", {}).items():
        old_path = os.getcwd()
        os.makedirs(folder_name, exist_ok=True)
        os.chdir(folder_name)
        create_folder(dictionary, folder_name, readme_template)
        os.chdir(old_path)


def create_txt_readme(folder_dict: dict, name: str, readme_template: str) -> None:
    """Create txt README file.

    This function creates a README.txt file in the current working directory.


    :param folder_dict: config dictionary with folder structure.
    :type folder_dict: dict
    :param name: name of the actual folder, as header of the README.
    :type name: str
    :param readme_template: path to the README template.
    :type readme_template: str
    """

    # Read template file
    with open(readme_template, "r", encoding="utf-8") as template_file:
        template_content: str = template_file.read()

    # Replace name
    template_content: str = template_content.replace("<name>", name.upper())

    # Replace dates
    today: str = datetime.now().strftime('%Y-%m-%d')
    template_content: str = template_content.replace("<creation_date>", today)
    template_content: str = template_content.replace("<updated_date>", today)

    # Replace description
    template_content: str = template_content.replace("<description>",
                                                     folder_dict.get("description", ""))

    # Replace folders
    if folder_dict.get("subfolders", {}):
        folders_content: str = ""
        for subfolder_name, dictionary in folder_dict.get("subfolders", {}).items():
            folders_content += f'- {subfolder_name}: {dictionary.get("description", "")}\n'
        template_content: str = template_content.replace("<folders>", folders_content)
    else:
        template_content: str = template_content.replace("<folders>", "")

    # Replace files
    if folder_dict.get("files", []):
        files_content: str = ""
        for file in folder_dict.get("files", []):
            files_content += f'- {file}\n' # pylint: disable=consider-using-join
        template_content: str = template_content.replace("<files>", files_content)
    else:
        template_content: str = template_content.replace("<files>", "")

    # Write README file
    with open("README.txt", "w", encoding="utf-8") as readme_file:
        readme_file.write(template_content)


def create_md_readme(folder_dict: dict, name: str, readme_template: str) -> None:
    """Create md README file.

    This function creates a README.md file in the current working directory.


    :param folder_dict: config dictionary with folder structure.
    :type folder_dict: dict
    :param name: name of the actual folder, as header of the README.
    :type name: str
    :param readme_template: path to the README template.
    :type readme_template: str
    """

    # Read template file
    with open(readme_template, "r", encoding="utf-8") as template_file:
        template_content: str = template_file.read()

    # Replace name
    template_content: str = template_content.replace("<name>", name.upper())

    # Replace dates
    today: str = datetime.now().strftime('%Y-%m-%d')
    template_content: str = template_content.replace("<creation_date>", today)
    template_content: str = template_content.replace("<updated_date>", today)

    # Replace description
    template_content: str = template_content.replace("<description>",
                                                     folder_dict.get("description", ""))

    # Replace folders
    if folder_dict.get("subfolders", {}):
        folders_content: str = ""
        for subfolder_name, dictionary in folder_dict.get("subfolders", {}).items():
            folders_content += f'* {subfolder_name}: {dictionary.get("description", "")}\n'
        template_content = template_content.replace("<folders>", folders_content)
    else:
        template_content: str = template_content.replace("<folders>", "")

    # Replace files
    if folder_dict.get("files", []):
        files_content: str = ""
        for file in folder_dict.get("files", []):
            files_content += f'* {file}\n'
        template_content: str = template_content.replace("<files>", files_content)
    else:
        template_content: str = template_content.replace("<files>", "")

    # Write README file
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(template_content)

def create_html_readme(folder_dict: dict, name: str, readme_template: str) -> None:
    """Create html README file.

    This function creates a README.html file in the current working directory.


    :param folder_dict: config dictionary with folder structure.
    :type folder_dict: dict
    :param name: name of the actual folder, as header of the README.
    :type name: str
    :param readme_template: path to the README template.
    :type readme_template: str
    """

    # Read template file
    with open(readme_template, "r", encoding="utf-8") as template_file:
        template_content: str = template_file.read()

    # Replace name
    template_content: str = template_content.replace("<name>", name.upper())

    # Replace dates
    today: str = datetime.now().strftime('%Y-%m-%d')
    template_content: str = template_content.replace("<creation_date>", today)
    template_content: str = template_content.replace("<updated_date>", today)

    # Replace description
    template_content: str = template_content.replace("<description>",
                                                     folder_dict.get("description", ""))

    # Replace folders
    if folder_dict.get("subfolders", {}):
        folders_content: str = ""
        for subfolder_name, dictionary in folder_dict.get("subfolders", {}).items():
            folders_content += f'<li>{subfolder_name}: {dictionary.get("description", "")}</li>\n'
        template_content: str = template_content.replace("<folders>", folders_content)
    else:
        template_content: str = template_content.replace("<folders>", "")

    # Replace files
    if folder_dict.get("files", []):
        files_content: str = ""
        for file in folder_dict.get("files", []):
            files_content += f'<li>{file}</li>\n'
        template_content: str = template_content.replace("<files>", files_content)
    else:
        template_content: str = template_content.replace("<files>", "")

    # Write README file
    with open("README.html", "w", encoding="utf-8") as readme_file:
        readme_file.write(template_content)

def main() -> None:
    """Main cli function handler.

    This function is the main function of the module, which handles command line input values to run
    the different functions of createnewproject.
    """

    # Get default config file path
    script_dir: str = os.path.dirname(os.path.abspath(__file__))
    default_config_file: str = os.path.join(script_dir, 'templates', 'config.json')

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Create new project tool")
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__,
                        help="Show package version")
    parser.add_argument('-n', '--name', required=True,
                        help="Name of the new project. If you want it to be more than one word, please write it in quotes.") #pylint: disable=line-too-long
    parser.add_argument('-c', '--config', default=default_config_file,
                        help="Path to the configuration file. By default, it will use the template configuration file installed with this package.") #pylint: disable=line-too-long
    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help="Overwrite existing project directory.")
    parser.add_argument('--readme-template', default=('txt'),
                        help = "Type of readme to create. By default, it will create a README.txt.\nPossible values are: txt, md, html.") #pylint: disable=line-too-long

    args = parser.parse_args()
    if not args.name:
        parser.error("-n/--name is required. Please provide the name of the project.")

    if not args.readme_template in ["txt", "md", "html"]:
        parser.error("--readme_template must be one of the following: txt, md, html")

    # Check existance of project directory and check if force overwrite is allowed
    folder_name: str = args.name.replace(" ", "_").lower()
    if os.path.exists(folder_name) and not args.force:
        print(f"Error: {folder_name} already exists. Use -f/--force to overwrite it.")
        sys.exit(1)
    elif os.path.exists(folder_name) and args.force:
        shutil.rmtree(folder_name)
    os.makedirs(folder_name)
    os.chdir(folder_name)

    # Read config file
    with open(args.config, 'r', encoding="utf-8") as config_file:
        config = json.load(config_file)

    # Create .git folder
    _ = subprocess.run("git init", shell=True, check=False)

    # Create .gitignore file
    create_gitignore(config)

    # Create .gitatributes file
    create_gitattributes(config)

    # Loop through config dictionary and create folder
    create_folder(config, args.name, args.readme_template)

    # Commit changes
    _ = subprocess.run("git add .", shell=True, check=False)
    _ = subprocess.run("git commit -m 'Initial commit'", shell=True, check=False)

    # Create labnotebook
    _ = subprocess.run(f"labnotebook create -n '{args.name}'", shell=True, check=False)
    if args.readme_template == "html":
        with open(".labignore", "w", encoding="utf-8") as labignore_file:
            labignore_file.write("*README.html\n")
    _ = subprocess.run("labnotebook update", shell=True, check=False)
    _ = subprocess.run(f"labnotebook export -o {folder_name}_notebook.html", shell=True,
                       check=False)

if __name__ == "__main__":
    main()

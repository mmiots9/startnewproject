{{ name }} README

Created on: {{ creation_date }}
Updated on: {{ updated_date }}

{{ folder_dict.get("description") }}

FOLDERS
{% if folder_dict.get("subfolders", {}) -%}
{% for subfolder_name, dictionary in folder_dict.get("subfolders").items() -%}
- {{ subfolder_name }}: {{ dictionary.get("description", "") }}
{% endfor %}
{%- endif %}
FILES
{% if folder_dict.get("files", []) -%}
{% for file in folder_dict.get("files") -%}
- {{ file }}
{% endfor %}
{%- endif %}

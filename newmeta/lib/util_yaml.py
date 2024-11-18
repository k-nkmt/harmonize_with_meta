import os
import yaml
import json
import pandas as pd
from jinja2 import Template

def create_vmap_elements(data: pd.DataFrame) -> str: 
    '''create variable map elements from DataFrame for YAML output
    
    Args:
        data (pd.DataFrame): DataFrame with variable mapping information
    '''
    entries = sorted(set(col.split('_')[0] for col in data.columns if '_id' in col))

    template_str = """\
{% for index, row in data.iterrows() %}
  {{ row['var'] }}:
    label: {{ row['label'] }}
    type: {{ row['type'] }}
    {%- if row['type'] == 'dict' and row['dict'] %}
    dict: {{ row['dict'] }}
    {%- endif %}{% if row['type'] == 'assign' %}
    values: [{% for entry in entries %}'{{ row[entry + '_val']|int }}'{% if not loop.last %}, {% endif %}{% endfor %}]
  {% elif row['type'] != 'skip' and row['type'] is not none %}
    vars: [{% for entry in entries %}{% if pd.notna(row[entry + '_id']) %}{{ row[entry + '_id'] |int}}: {{ row[entry + '_val'] }}{% else %}null{% endif %}{% if not loop.last %}, {% endif %}{% endfor %}]
  {% endif %}
{%- endfor %}
"""

    template = Template(template_str, lstrip_blocks=True)
    map_str = template.render(data=data, entries=entries, pd=pd)
    return map_str

def generate_vmap_yaml(title:str, entries:list, notes:str='', map_str:str='' ) -> yaml: 
    """Generate YAML output for variable mapping

    Args:
        title (str): title of the variable mapping
        entries (list): list of entries
        notes (str): notes about the variable mapping
        map_str (str): string representation of the variable mapping
    """
    template = """\
title: {{ title }}
entries: {{ entries }}
notes: "{{ notes }}"
map: {{ map_str}}
"""
    tmpl = Template(template)
    yaml_output = tmpl.render(
        title=title,
        entries=entries,
        notes=notes,
        map_str=map_str
    ) 
    return yaml_output

def create_vmapdf(yaml_input: str) -> pd.DataFrame:
    """Create a DataFrame from a YAML file or string

    Args:
        yaml_input (str): Path to a YAML file or YAML string
    """
    if isinstance(yaml_input, str):
        try:
            with open(yaml_input, 'r', encoding='utf-8') as file:
                yaml_content = yaml.safe_load(file)
        except (FileNotFoundError, OSError):
            yaml_content = yaml.safe_load(yaml_input)
    else:
        yaml_content = yaml.safe_load(yaml_input)

    map_data = yaml_content.get('map', {})
    entries = yaml_content.get('entries', [])
    
    data_rows = []
    for var_name, var_info in map_data.items():
        row = {
            'var': var_name,
            'label': var_info.get('label'),
            'type': var_info.get('type'),
            'dict': var_info.get('dict')
        }
        
        # Initialize all entry columns
        for entry in entries:
            row[f'{entry}_id'] = None
            row[f'{entry}_val'] = None
        
        # Process vars if present
        if 'vars' in var_info:
            vars_list = var_info['vars']
            if isinstance(vars_list, list):
                for i, var_item in enumerate(vars_list):
                    if var_item is not None and isinstance(var_item, dict):
                        if i < len(entries):
                            entry = entries[i]
                            id_val = next(iter(var_item.items()))
                            row[f'{entry}_id'] = id_val[0]
                            row[f'{entry}_val'] = id_val[1]
        
        # Process values if present
        if 'values' in var_info:
            values = var_info['values']
            if isinstance(values, list):
                for i, value in enumerate(values):
                    if i < len(entries):
                        entry = entries[i]
                        row[f'{entry}_val'] = value
        
        data_rows.append(row)

    columns = ['var', 'label', 'type', 'dict']
    for entry in entries:
        columns.extend([f'{entry}_id', f'{entry}_val'])
    
    df = pd.DataFrame(data_rows, columns=columns)
    return df


def create_cmap_elements(df: pd.DataFrame) -> dict:
    """Create codebook mapping elements from DataFrame for YAML output

    Args:
        df (pd.DataFrame): DataFrame with codebook mapping information
    """
    entries = {}
    # Identify all prefixes that have '_code' columns (e.g., '2000', '2005')
    prefixes = sorted({col.split('_')[0] for col in df.columns if col.endswith('_code')})
    
    for prefix in prefixes:
        entry = {}
        for _, row in df.iterrows():
            inner_key = row.get(f"{prefix}_code")
            if pd.isna(inner_key) or not inner_key:
                continue
            value = row.get('code')
            if pd.isna(value):
                continue
            # Collect comment columns for this prefix
            comment_cols = [col for col in df.columns if col.startswith(f"{prefix}_com")]
            comments = [row[col] for col in comment_cols if pd.notna(row[col])]
            comment_str = ': '.join(comments) if comments else ''
            if comment_str:
                entry[inner_key] = f'"{value}" # {comment_str}'
            else:
                entry[inner_key] = f'"{value}"'
        entries[prefix] = entry
    return {'entries': entries}

def generate_cmap_yaml(name:str, from_:str, to:str, notes:str, entries:dict) -> yaml:
    """Generate YAML output for codebook mapping

    Args:
        name (str): name of the codebook
        from_ (str): source of the codebook
        to (str): target of the codebook
        notes (str): notes about the codebook
        entries (dict): codebook entries
    """
    template = """\
name: {{ name }}
from: {{ from_ }}
to: {{ to }}
notes: "{{ notes }}"
entries:
{%- for entry, data in entries.items() %}
  "{{ entry }}":
{%- for key, value_comment in data.items() %}
    "{{ key }}": {{ value_comment }}
{%- endfor %}
{%- endfor %}
"""
    tmpl = Template(template)
    yaml_output = tmpl.render(
        name=name,
        from_=from_,
        to=to,
        notes=notes,
        entries=entries['entries']
    )
    return yaml_output

def create_cmapdf(yaml_input: str) -> pd.DataFrame:
    """Create a DataFrame from a YAML file or string

    Args:
        yaml_input (str or Path): Path to a YAML file or YAML string
    """

    entries = {}
    current_entry = None
    
    if isinstance(yaml_input, (str, os.PathLike)):
        try:
            with open(yaml_input, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except (FileNotFoundError, OSError):
            lines = yaml_input.split('\n')
    else:
        lines = yaml_input.split('\n')

    # Extract entries and their contents
    for line in lines:
        if line.startswith('  ') and not line.startswith('    '):
            # Detect entry line (2-space indent)
            current_entry = line.strip().strip('":')
            entries[current_entry] = {}
        elif line.startswith('    ') and current_entry:
            # Process entry content (4-space indent)
            parts = line.strip().split('#')
            code_part = parts[0].strip()
            comment_part = parts[1].strip() if len(parts) > 1 else ''
            
            code, value = [x.strip().strip('"') for x in code_part.split(':')]
            
            # Split comments
            comment_parts = comment_part.split(':') if ':' in comment_part else [comment_part, '']
            
            entries[current_entry][code] = {
                f'{current_entry}_code': code,
                f'{current_entry}_com1': comment_parts[0].strip(),
                'code': value,
            }
            if len(comment_parts) > 1:
                entries[current_entry][code][f'{current_entry}_com2'] = comment_parts[1].strip()
    
    # Construct DataFrame
    df_rows = []
    first_entry = list(entries.keys())[0]
    for code in sorted(entries[first_entry].keys()):
        row = {'code': entries[first_entry][code]['code']}
        for entry in entries:
            if code in entries[entry]:
                row.update({k: v for k, v in entries[entry][code].items() 
                          if k != 'code'})
        df_rows.append(row)
    
    df = pd.DataFrame(df_rows)
    return df

def render_tpl(meta:dict, save_dir:str = None, df_code:str = 'df = pd.read_csv("{{entry}}.csv", dtype=str)', out_prefix:str= ''):
    """ Create a script for conversion based on metadata

    Args:
        meta (dict): Metadata dictionary read from YAML, etc.
        save_dir (str, optional): Directory to save the output. Defaults to None.
        df_code (str, optional): Code to read the DataFrame. Defaults to 'df = pd.read_csv("{{entry}}.csv", dtype=str)'.
        out_prefix (str, optional): Prefix for the output file. Defaults to None.
    """

    tpl = """
import pandas as pd
import json 

with open('codebook.json', 'r') as f:
    codebook = json.load(f)

# Read as DataFrame
"""  + df_code +"""
df.columns = ['var' + str(i+1) for i in range(len(df.columns))]

out = pd.DataFrame()
{% set i = meta.entries.index(entry) %}
{% for var, value in meta["map"].items() %}
  {%- if value["type"] == "copy" -%}
    {%- set item = value['vars'][i]-%}
    {%- if item  -%}
out["{{var}}"] = df["var{{item.keys() | join('')}}"] 
    {%- endif -%}
  {%- elif value["type"] == "dict" -%}
    {%- set item = value['vars'][i]-%}
    {%- if item and "dict" in value  -%}
out["{{var}}"] = df["var{{item.keys() | join('')}}"].map(codebook["{{value['dict']}}"]["{{entry}}"])
    {%- elif item -%}
out["{{var}}"] = df["var{{item.keys() | join('')}}"].map(codebook["{{var}}"]["{{entry}}"])
    {%- endif -%}
  {%- elif value["type"] == "assign" -%} 
out["{{var}}"] = "{{value['values'][i]}}"
  {%- elif value["type"] == none -%} 
out["{{var}}"] = ""
  {%- endif %}
{% endfor %}

# Extra Code


# Output
out.to_csv("{{out_prefix}}{{entry}}.csv", index=False)

"""

    entries = meta["entries"]
    template = Template(tpl)

    for entry in entries:
        rendered = template.render(meta=meta, entry = entry, df_code = df_code, out_prefix = out_prefix)
        if save_dir is None:
             save_dir = "."
        with open(f"{save_dir}/{entry}.py", "w") as f:
                f.write(rendered)

def create_codebook_file(directory: str, save_path:str = "codebook.json"):
    """Create a dictionary file for conversion from YAML files

    Args:
        directory (str): Directory containing YAML files
        save_path (str, optional): Path to save the output. Defaults to "codebook.json".
    """
    all_data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                all_data[data['name']] = data['entries']

    with open(save_path, "w") as f:
      json.dump(all_data, f)
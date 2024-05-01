import os
from ruamel.yaml import YAML
from jinja2 import Environment, BaseLoader, FileSystemLoader, select_autoescape


def load(config_file: str, config_vars: dict) -> dict:
    
    # load  the jinja2 templates
    if config_file == "-":
        # load from stdin
        env = Environment(loader=BaseLoader())
        template = env.from_string(sys.stdin.read())
    
    else:
        # load from a file
        config_file = os.path.abspath(os.path.expanduser(config_file))
        config_path = os.path.dirname(config_file)
        config_name = os.path.basename(config_file)
    
        env = Environment(
            loader=FileSystemLoader(config_path),
            autoescape=select_autoescape()
        )
        template = env.get_template(config_name)
    
    # render the template with the provided configuration variables
    config_data = template.render(**config_vars)
    
    # parse the expanded template as YAML
    yaml = YAML(typ='safe')
    config = yaml.load(config_data)
    
    return config


def save(config: dict, save_dir: str, name: str) -> None:
    
    if not name.endswith('.yaml'):
        name += ".yaml"
    cfg_file = os.path.join(save_dir, name)

    with open(cfg_file, 'w') as f:
        yaml=YAML()
        yaml.dump(config, f)


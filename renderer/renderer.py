from jinja2 import Template
import os
import subprocess
import sys
import tempfile
import json


def render_html_from_template(data):
    with open('./renderer/html_template.html', 'r') as file:
        template_str = file.read()

    # Compile the template
    template = Template(template_str)

    # Render the template with the data
    html = template.render(data=data)
    return html


def show_result_as_html(data):
    # Write result to temp file and open it
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(data)
        f.close()

    if os.name == 'nt':  # For Windows
        subprocess.Popen(["firefox.exe", f.name])
    elif os.name == 'posix':  # For Linux and macOS
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener, f.name])
    else:
        raise OSError('Unsupported operating system')


def show_result_as_text(data):
    data = json.dumps(data, indent=4, sort_keys=True)

    # Write result to temp file and open it
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(data)
        f.close()

    if os.name == 'nt':  # For Windows
        subprocess.Popen(["notepad.exe", f.name])
    elif os.name == 'posix':  # For Linux and macOS
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener, f.name])
    else:
        raise OSError('Unsupported operating system')

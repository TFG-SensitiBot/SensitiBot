import webbrowser
from jinja2 import Template
import os
import subprocess
import sys
import tempfile
import json


def show_result_as_text(data):
    """
    Shows the result as text.

    Args:
        data (dict): The data to show.

    Returns:
        None
    """
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


def show_result_as_html(data):
    """
    Shows the result as HTML.

    Args:
        data (dict): The data to show.

    Returns:
        None
    """
    html = render_html_from_template(data)

    # Write result to temp file and open it
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(html)
        f.close()

    webbrowser.open_new_tab("file://" + f.name)


def render_html_from_template(data):
    """
    Renders the HTML from the template.

    Args:
        data (dict): The data to show.

    Returns:
        str: The HTML.
    """
    with open('./renderer/html_template.html', 'r') as file:
        template_str = file.read()

    # Compile the template
    template = Template(template_str)

    # Render the template with the data
    html = template.render(data=data)
    return html

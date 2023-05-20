import datetime
import webbrowser
from jinja2 import Template
import os
import subprocess
import sys
import tempfile
import json


def show_result_as_text(data, name, deep_search=False):
    """
    Shows the result as text.

    Args:
        data (dict): The data to show.

    Returns:
        None
    """
    generate_report = ask_generate_report()
    if not generate_report:
        return
    data = json.dumps(data, indent=4, sort_keys=True)

    # Write result to temp file and open it
    prefix = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{name}_{"deep-search_" if deep_search else ""}'
    suffix = '.json'
    with tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, mode='w', delete=False) as f:
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


def ask_generate_report():
    """
    Asks the user if he wants to generate a report.

    Args:
        None.

    Returns:
        bool: True if the user wants to generate a report, False otherwise.
    """
    ask_generate = input("\nDo you want to generate a report? (yes/no): ")
    while ask_generate.lower() not in ("yes", "no"):
        ask_generate = input("Please enter either 'yes' or 'no': ")
    if ask_generate.lower() == "yes":
        return True

    return False

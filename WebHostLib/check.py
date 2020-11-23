import zipfile
from typing import *

from flask import request, flash, redirect, url_for, session, render_template

from WebHostLib import app

banned_zip_contents = (".sfc",)


def allowed_file(filename):
    return filename.endswith(('.txt', ".yaml", ".zip"))


from Mystery import roll_settings
from Utils import parse_yaml


@app.route('/mysterycheck', methods=['GET', 'POST'])
def mysterycheck():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
        else:
            file = request.files['file']
            options = get_yaml_data(file)
            if type(options) == str:
                flash(options)
            else:
                results, _ = roll_options(options)
                return render_template("checkresult.html", results=results)

    return render_template("check.html")


def get_yaml_data(file) -> Union[Dict[str, str], str]:
    options = {}
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return 'No selected file'
    elif file and allowed_file(file.filename):
        if file.filename.endswith(".zip"):

            with zipfile.ZipFile(file, 'r') as zfile:
                infolist = zfile.infolist()

                for file in infolist:
                    if file.filename.endswith(banned_zip_contents):
                        return "Uploaded data contained a rom file, which is likely to contain copyrighted material. Your file was deleted."
                    elif file.filename.endswith(".yaml"):
                        options[file.filename] = zfile.open(file, "r").read()
                    elif file.filename.endswith(".txt"):
                        options[file.filename] = zfile.open(file, "r").read()
        else:
            options = {file.filename: file.read()}
    if not options:
        return "Did not find a .yaml file to process."
    return options


def roll_options(options: Dict[str, Union[dict, str]]) -> Tuple[Dict[str, Union[str, bool]], Dict[str, dict]]:
    results = {}
    rolled_results = {}
    for filename, text in options.items():
        try:
            if type(text) is dict:
                yaml_data = text
            else:
                yaml_data = parse_yaml(text)
        except Exception as e:
            results[filename] = f"Failed to parse YAML data in {filename}: {e}"
        else:
            try:
                rolled_results[filename] = roll_settings(yaml_data)
            except Exception as e:
                results[filename] = f"Failed to generate mystery in {filename}: {e}"
            else:
                results[filename] = True
    return results, rolled_results

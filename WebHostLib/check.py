import zipfile
import base64
from typing import Union, Dict, Set, Tuple

from flask import request, flash, redirect, url_for, render_template
from markupsafe import Markup

from WebHostLib import app

banned_zip_contents = (".sfc",)


def allowed_file(filename):
    return filename.endswith(('.txt', ".yaml", ".zip"))


from Generate import roll_settings, PlandoOptions
from Utils import parse_yamls


@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
        else:
            files = request.files.getlist('file')
            options = get_yaml_data(files)
            if isinstance(options, str):
                flash(options)
            else:
                results, _ = roll_options(options)
                if len(options) > 1:
                    # offer combined file back
                    combined_yaml = "---\n".join(f"# original filename: {file_name}\n{file_content.decode('utf-8-sig')}"
                                                 for file_name, file_content in options.items())
                    combined_yaml = base64.b64encode(combined_yaml.encode("utf-8-sig")).decode()
                else:
                    combined_yaml = ""
                return render_template("checkResult.html",
                                       results=results, combined_yaml=combined_yaml)
    return render_template("check.html")


@app.route('/mysterycheck')
def mysterycheck():
    return redirect(url_for("check"), 301)


def get_yaml_data(files) -> Union[Dict[str, str], str, Markup]:
    options = {}
    for uploaded_file in files:
        # if user does not select file, browser also
        # submit an empty part without filename
        if uploaded_file.filename == '':
            return 'No selected file'
        elif uploaded_file.filename in options:
            return f'Conflicting files named {uploaded_file.filename} submitted'
        elif uploaded_file and allowed_file(uploaded_file.filename):
            if uploaded_file.filename.endswith(".zip"):

                with zipfile.ZipFile(uploaded_file, 'r') as zfile:
                    infolist = zfile.infolist()

                    if any(file.filename.endswith(".archipelago") for file in infolist):
                        return Markup("Error: Your .zip file contains an .archipelago file. "
                                      'Did you mean to <a href="/uploads">host a game</a>?')

                    for file in infolist:
                        if file.filename.endswith(banned_zip_contents):
                            return ("Uploaded data contained a rom file, "
                                    "which is likely to contain copyrighted material. "
                                    "Your file was deleted.")
                        elif file.filename.endswith((".yaml", ".json", ".yml", ".txt")):
                            options[file.filename] = zfile.open(file, "r").read()
            else:
                options[uploaded_file.filename] = uploaded_file.read()
    if not options:
        return "Did not find a .yaml file to process."
    return options


def roll_options(options: Dict[str, Union[dict, str]],
                 plando_options: Set[str] = frozenset({"bosses", "items", "connections", "texts"})) -> \
        Tuple[Dict[str, Union[str, bool]], Dict[str, dict]]:
    plando_options = PlandoOptions.from_set(set(plando_options))
    results = {}
    rolled_results = {}
    for filename, text in options.items():
        try:
            if type(text) is dict:
                yaml_datas = (text, )
            else:
                yaml_datas = tuple(parse_yamls(text))
        except Exception as e:
            results[filename] = f"Failed to parse YAML data in {filename}: {e}"
        else:
            try:
                if len(yaml_datas) == 1:
                    rolled_results[filename] = roll_settings(yaml_datas[0],
                                                             plando_options=plando_options)
                else:
                    for i, yaml_data in enumerate(yaml_datas):
                        rolled_results[f"{filename}/{i + 1}"] = roll_settings(yaml_data,
                                                                              plando_options=plando_options)
            except Exception as e:
                results[filename] = f"Failed to generate options in {filename}: {e}"
            else:
                results[filename] = True
    return results, rolled_results

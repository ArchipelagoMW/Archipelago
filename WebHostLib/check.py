import os
import zipfile
import base64
from collections.abc import Set

from flask import request, flash, redirect, url_for, render_template
from markupsafe import Markup

from WebHostLib import app
from WebHostLib.upload import allowed_options, allowed_options_extensions, banned_file

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
                    combined_yaml = "\n---\n".join(f"# original filename: {file_name}\n{file_content.decode('utf-8-sig')}"
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


def get_yaml_data(files) -> dict[str, str] | str | Markup:
    options = {}
    for uploaded_file in files:
        if banned_file(uploaded_file.filename):
            return ("Uploaded data contained a rom file, which is likely to contain copyrighted material. "
                    "Your file was deleted.")
        # If the user does not select file, the browser will still submit an empty string without a file name.
        elif uploaded_file.filename == "":
            return "No selected file."
        elif uploaded_file.filename in options:
            return f"Conflicting files named {uploaded_file.filename} submitted."
        elif uploaded_file and allowed_options(uploaded_file.filename):
            if uploaded_file.filename.endswith(".zip"):
                if not zipfile.is_zipfile(uploaded_file):
                    return f"Uploaded file {uploaded_file.filename} is not a valid .zip file and cannot be opened."

                uploaded_file.seek(0)  # offset from is_zipfile check
                with zipfile.ZipFile(uploaded_file, "r") as zfile:
                    for file in zfile.infolist():
                        # Remove folder pathing from str (e.g. "__MACOSX/" folder paths from archives created by macOS).
                        base_filename = os.path.basename(file.filename)

                        if base_filename.endswith(".archipelago"):
                            return Markup("Error: Your .zip file contains an .archipelago file. "
                                          'Did you mean to <a href="/uploads">host a game</a>?')
                        elif base_filename.endswith(".zip"):
                            return "Nested .zip files inside a .zip are not supported."
                        elif banned_file(base_filename):
                            return ("Uploaded data contained a rom file, which is likely to contain copyrighted "
                                    "material. Your file was deleted.")
                        # Ignore dot-files.
                        elif not base_filename.startswith(".") and allowed_options(base_filename):
                            options[file.filename] = zfile.open(file, "r").read()
            else:
                options[uploaded_file.filename] = uploaded_file.read()

    if not options:
        return f"Did not find any valid files to process. Accepted formats: {allowed_options_extensions}"
    return options


def roll_options(options: dict[str, dict | str],
                 plando_options: Set[str] = frozenset({"bosses", "items", "connections", "texts"})) -> \
        tuple[dict[str, str | bool], dict[str, dict]]:
    plando_options = PlandoOptions.from_set(set(plando_options))
    results: dict[str, str | bool] = {}
    rolled_results: dict[str, dict] = {}
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
                        if yaml_data is not None:
                            rolled_results[f"{filename}/{i + 1}"] = roll_settings(yaml_data,
                                                                                  plando_options=plando_options)
            except Exception as e:
                if e.__cause__:
                    results[filename] = f"Failed to generate options in {filename}: {e} - {e.__cause__}"
                else:
                    results[filename] = f"Failed to generate options in {filename}: {e}"
            else:
                results[filename] = True
    return results, rolled_results

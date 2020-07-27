import zipfile


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
            options = {}
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
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
                    flash("Did not find a .yaml file to process.")
                else:
                    results = {}
                    for filename, text in options.items():
                        try:
                            yaml_data = parse_yaml(text)
                        except Exception as e:
                            results[filename] = f"Failed to parse YAML data in {filename}: {e}"
                        else:
                            try:
                                roll_settings(yaml_data)
                            except Exception as e:
                                results[filename] = f"Failed to generate mystery in {filename}: {e}"
                            else:
                                results[filename] = "Looks fine"
                    return render_template("checkresult.html", results=results)

            else:
                flash("Not recognized file format. Awaiting a .yaml file.")

    return render_template("check.html")

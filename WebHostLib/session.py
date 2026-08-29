from uuid import uuid4, UUID

from flask import session, render_template

from WebHostLib import app


@app.before_request
def register_session():
    session.permanent = True  # technically 31 days after the last visit
    if not session.get("_id", None):
        session["_id"] = uuid4()  # uniquely identify each session without needing a login


@app.route('/session')
def show_session():
    return render_template(
        "session.html",
    )


@app.route('/session/<string:_id>')
def set_session(_id: str):
    new_id: UUID = UUID(_id, version=4)
    old_id: UUID = session["_id"]
    if old_id != new_id:
        session["_id"] = new_id
    return render_template(
        "session.html",
        old_id=old_id,
    )

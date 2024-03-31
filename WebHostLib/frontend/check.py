from browser import document, window
Any = object  # runtime import of typing is not implemented yet


def on_load(_: Any) -> None:
    document["check-button"].bind("click", lambda _: document["file-input"].click())
    document["file-input"].bind("change", lambda _: document["check-form"].submit())


window.bind("load", on_load)

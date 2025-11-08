import re
from collections import Counter

import mistune
from werkzeug.utils import secure_filename


__all__ = [
    "ImgUrlRewriteInlineParser",
    'render_markdown',
]


class ImgUrlRewriteInlineParser(mistune.InlineParser):
    relative_url_base: str

    def __init__(self, relative_url_base: str, hard_wrap: bool = False) -> None:
        super().__init__(hard_wrap)
        self.relative_url_base = relative_url_base

    @staticmethod
    def _find_game_name_by_folder_name(name: str) -> str | None:
        from worlds.AutoWorld import AutoWorldRegister

        for world_name, world_type in AutoWorldRegister.world_types.items():
            if world_type.__module__ == f"worlds.{name}":
                return world_name
        return None

    def parse_link(self, m: re.Match[str], state: mistune.InlineState) -> int | None:
        res = super().parse_link(m, state)
        if res is not None and state.tokens and state.tokens[-1]["type"] == "image":
            image_token = state.tokens[-1]
            url: str = image_token["attrs"]["url"]
            if not url.startswith("/") and not "://" in url:
                # replace relative URL to another world's doc folder with the webhost folder layout
                if url.startswith("../../") and "/docs/" in self.relative_url_base:
                    parts = url.split("/", 4)
                    if parts[2] != ".." and parts[3] == "docs":
                        game_name = self._find_game_name_by_folder_name(parts[2])
                        if game_name is not None:
                            url = "/".join(parts[1:2] + [secure_filename(game_name)] + parts[4:])
                # change relative URL to point to deployment folder
                url = f"{self.relative_url_base}/{url}"
                image_token['attrs']['url'] = url
        return res


def render_markdown(path: str, img_url_base: str | None = None) -> str:
    markdown = mistune.create_markdown(
        escape=False,
        plugins=[
            "strikethrough",
            "footnotes",
            "table",
            "speedup",
        ],
    )

    heading_id_count: Counter[str] = Counter()

    def heading_id(text: str) -> str:
        nonlocal heading_id_count

        # there is no good way to do this without regex
        s = re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-").strip("-")
        n = heading_id_count[s]
        heading_id_count[s] += 1
        if n > 0:
            s += f"-{n}"
        return s

    def id_hook(_: mistune.Markdown, state: mistune.BlockState) -> None:
        for tok in state.tokens:
            if tok["type"] == "heading" and tok["attrs"]["level"] < 4:
                text = tok["text"]
                assert isinstance(text, str)
                unique_id = heading_id(text)
                tok["attrs"]["id"] = unique_id
                tok["text"] = f"<a href=\"#{unique_id}\">{text}</a>"  # make header link to itself

    markdown.before_render_hooks.append(id_hook)
    if img_url_base:
        markdown.inline = ImgUrlRewriteInlineParser(img_url_base)

    with open(path, encoding="utf-8-sig") as f:
        document = f.read()
    html = markdown(document)
    assert isinstance(html, str), "Unexpected mistune renderer in render_markdown"
    return html

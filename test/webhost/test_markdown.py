import os
import unittest
from tempfile import NamedTemporaryFile

from mistune import HTMLRenderer, Markdown

from WebHostLib.markdown import ImgUrlRewriteInlineParser, render_markdown


class ImgUrlRewriteTest(unittest.TestCase):
    markdown: Markdown
    base_url = "/static/generated/docs/some_game"

    def setUp(self) -> None:
        self.markdown = Markdown(
            renderer=HTMLRenderer(escape=False),
            inline=ImgUrlRewriteInlineParser(self.base_url),
        )

    def test_relative_img_rewrite(self) -> None:
        html = self.markdown("![Image](image.png)")
        self.assertIn(f'src="{self.base_url}/image.png"', html)

    def test_absolute_img_no_rewrite(self) -> None:
        html = self.markdown("![Image](/image.png)")
        self.assertIn(f'src="/image.png"', html)
        self.assertNotIn(self.base_url, html)

    def test_remote_img_no_rewrite(self) -> None:
        html = self.markdown("![Image](https://example.com/image.png)")
        self.assertIn(f'src="https://example.com/image.png"', html)
        self.assertNotIn(self.base_url, html)

    def test_relative_link_no_rewrite(self) -> None:
        # The parser is only supposed to update images, not links.
        html = self.markdown("[Link](image.png)")
        self.assertIn(f'href="image.png"', html)
        self.assertNotIn(self.base_url, html)

    def test_absolute_link_no_rewrite(self) -> None:
        html = self.markdown("[Link](/image.png)")
        self.assertIn(f'href="/image.png"', html)
        self.assertNotIn(self.base_url, html)

    def test_auto_link_no_rewrite(self) -> None:
        html = self.markdown("<https://example.com/image.png>")
        self.assertIn(f'href="https://example.com/image.png"', html)
        self.assertNotIn(self.base_url, html)

    def test_relative_img_to_other_game(self) -> None:
        html = self.markdown("![Image](../../generic/docs/image.png)")
        self.assertIn(f'src="{self.base_url}/../Archipelago/image.png"', html)


class RenderMarkdownTest(unittest.TestCase):
    """Tests that render_markdown does the right thing."""
    base_url = "/static/generated/docs/some_game"

    def test_relative_img_rewrite(self) -> None:
        f = NamedTemporaryFile(delete=False)
        try:
            f.write("![Image](image.png)".encode("utf-8"))
            f.close()
            html = render_markdown(f.name, self.base_url)
            self.assertIn(f'src="{self.base_url}/image.png"', html)
        finally:
            os.unlink(f.name)

    def test_no_img_rewrite(self) -> None:
        f = NamedTemporaryFile(delete=False)
        try:
            f.write("![Image](image.png)".encode("utf-8"))
            f.close()
            html = render_markdown(f.name)
            self.assertIn(f'src="image.png"', html)
            self.assertNotIn(self.base_url, html)
        finally:
            os.unlink(f.name)

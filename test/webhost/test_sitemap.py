import urllib.parse
import html
import re
from flask import url_for

import WebHost
from . import TestBase


class TestSitemap(TestBase):

    # Codes for OK and some redirects that we use
    valid_status_codes = [200, 302, 308]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        WebHost.copy_tutorials_files_to_static()

    def test_sitemap_route(self) -> None:
        """Verify that the sitemap route works correctly and renders the template without errors."""
        with self.app.test_request_context():
            # Test the /sitemap route
            with self.client.open("/sitemap") as response:
                self.assertEqual(response.status_code, 200)
                self.assertIn(b"Site Map", response.data)

            # Test the /index route which should also serve the sitemap
            with self.client.open("/index") as response:
                self.assertEqual(response.status_code, 200)
                self.assertIn(b"Site Map", response.data)

            # Test using url_for with the function name
            with self.client.open(url_for('get_sitemap')) as response:
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Site Map', response.data)

    def test_sitemap_links(self) -> None:
        """
        Verify that all links in the sitemap are valid by making a request to each one.
        """
        with self.app.test_request_context():
            with self.client.open(url_for("get_sitemap")) as response:
                self.assertEqual(response.status_code, 200)
                html_content = response.data.decode()

            # Extract all href links using regex
            href_pattern = re.compile(r'href=["\'](.*?)["\']')
            links = href_pattern.findall(html_content)

            self.assertTrue(len(links) > 0, "No links found in sitemap")

            # Test each link
            for link in links:
                # Skip external links
                if link.startswith(("http://", "https://")):
                    continue

                link = urllib.parse.unquote(html.unescape(link))

                with self.client.open(link) as response, self.subTest(link=link):
                    self.assertIn(response.status_code, self.valid_status_codes,
                                 f"Link {link} returned invalid status code {response.status_code}")

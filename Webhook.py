import logging
from typing import Any, Dict, List, Optional, Tuple, Union
import requests

logger = logging.getLogger(__name__)


class Webhook:

    content: Optional[Union[str, bytes]]
    url: str

    def __init__(self, url: str, **kwargs) -> None:
        """
        Init Webhook.
        ---------
        :param str url: your webhook url
        """

        self.content = kwargs.get("content")
        self.url = url

    def set_content(self, content: str) -> None:
        """
        Set the content of the webhook.
        :param str content: content of the webhook
        """
        self.content = content

    def api_post_request(self) -> "requests.Response":
        """
        Post the JSON webhook data to the specified url.
        :return: Response of the sent webhook
        """
        return requests.post(self.url, json=self.content)

    def execute(self) -> "requests.Response":
        """
        Execute the sending of the webhook with the given data.
        :param bool remove_embeds: clear the stored embeds after webhook is executed
        :return: Response of the sent webhook
        """
        response = self.api_post_request()
        if response.status_code in [200, 204]:
            logger.debug("Webhook executed")
        else:
            logger.debug(
                "Webhook status code {status_code}: {content}".format(
                    status_code=response.status_code,
                    content=response.content.decode("utf-8"),
                )
            )

        return response

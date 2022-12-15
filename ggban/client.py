import asyncio
import json
from typing import List, Optional, Union

import aiohttp

from ggban.exceptions import (
    Error,
    Forbidden,
    NotFoundError,
    TooManyRequests,
    UnauthorizedError,
)
from ggban.types import BanQuery, ReportQuery


class Client:
    def __init__(
        self,
        id: int,
        token: str,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        self._api: str = "https://api-elsa.yuuu.es/v1"
        self._id: int = id
        self._token: str = token
        self._loop = loop
        self._session = session

    def __del__(self):
        try:
            if self._loop is None:
                self._loop = asyncio.get_event_loop()
            self._loop.create_task(self._close())
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            self._loop.run_until_complete(self._close())

    async def _close(self):
        if self._session is not None and not self._session.closed:
            await self._session.close()

    async def _create(self):
        self._session = aiohttp.ClientSession()

    async def _request(
        self, path: str, method: str = "POST", data: dict = {}, **kwargs
    ) -> Optional[Union[dict, str]]:
        """
        Make a request and handle errors
        Args:
            path: Path on the API without a leading slash
            method: The request method. Defaults to GET
            **kwargs: Keyword arguments passed to the request method.
        Returns: The json response
        """

        json_data = dict(id=self._id, api=self._token, **data)
        if self._session is None:
            await self._create()

        request = await self._session.request(
            method=method, url=f"{self._api}/{path}", json=json_data, **kwargs
        )

        if request.status in [200, 201]:
            try:
                resp: dict = await request.json()
            except json.JSONDecodeError:
                resp: str = await request.text()

            if not resp["ok"] and resp["data"] == []:
                raise Error(name="No defined.", message="No data.", code=0)

            return resp["data"]

        if request.status == 204:
            return {}
        if request.status > 400:
            if request.status == 401:
                raise UnauthorizedError("Make sure your token is correct.")
            elif request.status == 403:
                raise Forbidden(token=self._token)
            elif request.status == 404:
                raise NotFoundError()
            elif request.status == 429:
                raise TooManyRequests(method=path, message=request.url)
            else:
                raise Error(name="No defined.", message="No data.", code=0)

    async def get_user(self, user_id: int) -> BanQuery:
        data = await self._request(
            path="user/query", method="POST", data={"telegram_id": user_id}
        )
        return BanQuery(**data)

    async def get_report(self, report_id: int) -> ReportQuery:
        data = await self._request(
            path="report/query", method="POST", data={"report_id": report_id}
        )
        return ReportQuery(**data)

    async def new_report(
        self,
        user_id: int,
        reported_id: int,
        reason: str,
        proofs: Optional[Union[bytearray, List[bytearray]]] = None,
    ):
        data = await self._request(
            path="report/new",
            method="POST",
            data=dict(
                telegram_id=reported_id, reason=reason, author_id=user_id, proofs=proofs
            ),
        )
        if data != []:
            return int(data["report_id"])
        raise Exception("Report not created.")

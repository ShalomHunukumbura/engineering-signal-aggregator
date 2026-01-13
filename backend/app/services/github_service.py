from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings


class GithubService:
    def __init__(self) -> None:
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "engineering-signal-aggregator",
        }
        if settings.github_token:
            self.headers["Authorization"] = f"Bearer {settings.github_token}"

    async def _get(
        self, path: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        # GitHub pagination: we keep it simple (page through until empty)
        out: list[dict[str, Any]] = []
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.headers, timeout=30
        ) as client:
            page = 1
            while True:
                r = await client.get(
                    path, params={**(params or {}), "per_page": 100, "page": page}
                )
                r.raise_for_status()
                data = r.json()
                if not isinstance(data, list) or len(data) == 0:
                    break
                out.extend(data)
                page += 1
        return out

    async def list_pull_requests(self, owner: str, repo: str) -> list[dict[str, Any]]:
        # state=all so we can show merged/closed too
        return await self._get(
            f"/repos/{owner}/{repo}/pulls", params={"state": "all", "sort": "updated"}
        )

    async def list_issues(self, owner: str, repo: str) -> list[dict[str, Any]]:
        # issues endpoint includes PRs too; filter them out later
        return await self._get(
            f"/repos/{owner}/{repo}/issues", params={"state": "all", "sort": "updated"}
        )

    async def list_commits(self, owner: str, repo: str) -> list[dict[str, Any]]:
        return await self._get(f"/repos/{owner}/{repo}/commits")

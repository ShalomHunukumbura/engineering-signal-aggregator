from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.models.github import GithubPullRequest, GithubIssue, GithubCommit


def _dt(s: str | None) -> datetime | None:
    if not s:
        return None
    # GitHub timestamps are ISO8601 like "2026-01-13T12:34:56Z"
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def upsert_pull_requests(
    db: Session, owner: str, repo: str, prs: list[dict[str, Any]]
) -> int:
    rows = []
    for pr in prs:
        rows.append(
            {
                "repo_owner": owner,
                "repo_name": repo,
                "gh_id": pr["id"],
                "number": pr["number"],
                "title": pr.get("title") or "",
                "state": pr.get("state") or "open",
                "url": pr.get("html_url") or "",
                "created_at_gh": _dt(pr.get("created_at")),
                "updated_at_gh": _dt(pr.get("updated_at")),
                "merged_at_gh": _dt(pr.get("merged_at")),
                "author_login": (pr.get("user") or {}).get("login"),
            }
        )

    if not rows:
        return 0

    stmt = insert(GithubPullRequest).values(rows)
    stmt = stmt.on_conflict_do_update(
        constraint="uq_pr_repo_ghid",
        set_={
            "number": stmt.excluded.number,
            "title": stmt.excluded.title,
            "state": stmt.excluded.state,
            "url": stmt.excluded.url,
            "created_at_gh": stmt.excluded.created_at_gh,
            "updated_at_gh": stmt.excluded.updated_at_gh,
            "merged_at_gh": stmt.excluded.merged_at_gh,
            "author_login": stmt.excluded.author_login,
            "fetched_at": datetime.now(timezone.utc),
        },
    )
    db.execute(stmt)
    return len(rows)


def upsert_issues(
    db: Session, owner: str, repo: str, issues: list[dict[str, Any]]
) -> int:
    rows = []
    for it in issues:
        # Filter out PRs (issues endpoint includes them)
        if it.get("pull_request"):
            continue

        rows.append(
            {
                "repo_owner": owner,
                "repo_name": repo,
                "gh_id": it["id"],
                "number": it["number"],
                "title": it.get("title") or "",
                "state": it.get("state") or "open",
                "url": it.get("html_url") or "",
                "created_at_gh": _dt(it.get("created_at")),
                "updated_at_gh": _dt(it.get("updated_at")),
                "closed_at_gh": _dt(it.get("closed_at")),
                "author_login": (it.get("user") or {}).get("login"),
            }
        )

    if not rows:
        return 0

    stmt = insert(GithubIssue).values(rows)
    stmt = stmt.on_conflict_do_update(
        constraint="uq_issue_repo_ghid",
        set_={
            "number": stmt.excluded.number,
            "title": stmt.excluded.title,
            "state": stmt.excluded.state,
            "url": stmt.excluded.url,
            "created_at_gh": stmt.excluded.created_at_gh,
            "updated_at_gh": stmt.excluded.updated_at_gh,
            "closed_at_gh": stmt.excluded.closed_at_gh,
            "author_login": stmt.excluded.author_login,
            "fetched_at": datetime.now(timezone.utc),
        },
    )
    db.execute(stmt)
    return len(rows)


def upsert_commits(
    db: Session, owner: str, repo: str, commits: list[dict[str, Any]]
) -> int:
    rows = []
    for c in commits:
        commit = c.get("commit") or {}
        author = c.get("author") or {}
        rows.append(
            {
                "repo_owner": owner,
                "repo_name": repo,
                "sha": c.get("sha") or "",
                "url": c.get("html_url") or "",
                "message": (commit.get("message") or "").strip(),
                "author_login": author.get("login"),
                "committed_at_gh": _dt(((commit.get("author") or {}).get("date"))),
            }
        )

    if not rows:
        return 0

    stmt = insert(GithubCommit).values(rows)
    stmt = stmt.on_conflict_do_update(
        constraint="uq_commit_repo_sha",
        set_={
            "url": stmt.excluded.url,
            "message": stmt.excluded.message,
            "author_login": stmt.excluded.author_login,
            "committed_at_gh": stmt.excluded.committed_at_gh,
            "fetched_at": datetime.now(timezone.utc),
        },
    )
    db.execute(stmt)
    return len(rows)

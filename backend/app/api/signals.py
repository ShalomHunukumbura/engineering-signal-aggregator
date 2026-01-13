from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.services.github_service import GithubService
from app.services.github_store import (
    upsert_pull_requests,
    upsert_issues,
    upsert_commits,
)

router = APIRouter()


@router.post("/sync/github")
async def sync_github(db: Session = Depends(get_db)):
    owner = settings.github_default_owner
    repo = settings.github_default_repo

    gh = GithubService()

    prs = await gh.list_pull_requests(owner, repo)
    issues = await gh.list_issues(owner, repo)
    commits = await gh.list_commits(owner, repo)

    pr_count = upsert_pull_requests(db, owner, repo, prs)
    issue_count = upsert_issues(db, owner, repo, issues)
    commit_count = upsert_commits(db, owner, repo, commits)

    db.commit()

    return {
        "repo": f"{owner}/{repo}",
        "stored": {
            "pull_requests": pr_count,
            "issues": issue_count,
            "commits": commit_count,
        },
    }


@router.get("/signals/summary")
def signals_summary(db: Session = Depends(get_db)):
    owner = settings.github_default_owner
    repo = settings.github_default_repo

    from app.models.github import GithubPullRequest, GithubIssue, GithubCommit

    pr_total = (
        db.query(GithubPullRequest).filter_by(repo_owner=owner, repo_name=repo).count()
    )
    issue_total = (
        db.query(GithubIssue).filter_by(repo_owner=owner, repo_name=repo).count()
    )
    commit_total = (
        db.query(GithubCommit).filter_by(repo_owner=owner, repo_name=repo).count()
    )

    return {
        "repo": f"{owner}/{repo}",
        "totals": {
            "pull_requests": pr_total,
            "issues": issue_total,
            "commits": commit_total,
        },
    }

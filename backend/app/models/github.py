from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    DateTime,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class GithubRepo(Base):
    __tablename__ = "github_repos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped["DateTime"] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("owner", "name", name="uq_github_repo_owner_name"),
    )


class GithubPullRequest(Base):
    __tablename__ = "github_pull_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    repo_owner: Mapped[str] = mapped_column(String(200), nullable=False)
    repo_name: Mapped[str] = mapped_column(String(200), nullable=False)

    gh_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)

    created_at_gh: Mapped["DateTime"] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at_gh: Mapped["DateTime"] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    merged_at_gh: Mapped["DateTime | None"] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    author_login: Mapped[str] = mapped_column(String(200), nullable=False)

    fetched_at: Mapped["DateTime"] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("repo_owner", "repo_name", "gh_id", name="uq_pr_repo_ghid"),
    )


class GithubIssue(Base):
    __tablename__ = "github_issues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    repo_owner: Mapped[str] = mapped_column(String(200), nullable=False)
    repo_name: Mapped[str] = mapped_column(String(200), nullable=False)

    gh_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)

    title: Mapped[str] = mapped_column(Text, nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)

    created_at_gh: Mapped["DateTime"] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at_gh: Mapped["DateTime"] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    closed_at_gh: Mapped["DateTime | None"] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    author_login: Mapped[str | None] = mapped_column(String(200), nullable=True)

    fetched_at: Mapped["DateTime"] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("repo_owner", "repo_name", "gh_id", name="uq_issue_repo_ghid"),
    )


class GithubCommit(Base):
    __tablename__ = "github_commits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    repo_owner: Mapped[str] = mapped_column(String(200), nullable=False)
    repo_name: Mapped[str] = mapped_column(String(200), nullable=False)

    sha: Mapped[str] = mapped_column(String(60), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)

    message: Mapped[str] = mapped_column(Text, nullable=False)
    author_login: Mapped[str | None] = mapped_column(String(200), nullable=True)

    committed_at_gh: Mapped["DateTime"] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    fetched_at: Mapped["DateTime"] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("repo_owner", "repo_name", "sha", name="uq_commit_repo_sha"),
    )

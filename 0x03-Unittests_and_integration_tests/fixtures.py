#!/usr/bin/env python3
"""Fixtures for testing GithubOrgClient."""

org_payload = {
    "login": "google",
    "repos_url": "https://api.github.com/orgs/google/repos"
}

repos_payload = [
    {"name": "repo1", "license": {"key": "mit"}},
    {"name": "repo2", "license": {"key": "apache-2.0"}},
]

expected_repos = ["repo1", "repo2"]
apache2_repos = ["repo2"]

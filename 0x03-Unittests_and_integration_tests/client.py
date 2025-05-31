#!/usr/bin/env python3
"""Client for GitHub organization data."""

import requests


def get_json(url):
    """Fetch JSON data from a URL."""
    return requests.get(url).json()


class GithubOrgClient:
    """Client for GitHub Organization info."""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        """Initialize with organization name."""
        self.org_name = org_name

    @property
    def org(self):
        """Return organization metadata."""
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self):
        """Extract repos_url from organization metadata."""
        return self.org.get("repos_url")

    def public_repos(self, license=None):
        """Return list of public repo names, optionally filtered by license."""
        repos = get_json(self._public_repos_url)
        repo_names = [
            repo["name"] for repo in repos
            if license is None or self.has_license(repo, license)
        ]
        return repo_names

    @staticmethod
    def has_license(repo, license_key):
        """Check if repo has a specific license."""
        return repo.get("license", {}).get("key") == license_key

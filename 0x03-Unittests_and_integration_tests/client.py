#!/usr/bin/env python3
"""Client module to interface with GitHub API."""
import requests


def get_json(url):
    """GET JSON from a given URL."""
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    """GitHub Organization client."""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Get organization information."""
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self):
        """Get public repositories URL from organization payload."""
        return self.org.get("repos_url")

    def public_repos(self):
        """Return names of public repositories."""
        return [repo["name"] for repo in get_json(self._public_repos_url)]

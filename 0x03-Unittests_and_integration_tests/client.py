#!/usr/bin/env python3
"""Client module to interface with GitHub API."""
import requests


def get_json(url):
    """GET JSON from a given URL."""
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self):
        return self.org["repos_url"]

    def public_repos(self, license=None):
        """Return list of public repos. If license is specified, filter by license."""
        repos = get_json(self._public_repos_url)
        repo_names = [repo["name"] for repo in repos]

        if license is None:
            return repo_names

        # Filter by license
        return [
            repo["name"]
            for repo in repos
            if repo.get("license", {}).get("key") == license
        ]

    @staticmethod
    def has_license(repo, license_key):
        return repo.get("license", {}).get("key") == license_key

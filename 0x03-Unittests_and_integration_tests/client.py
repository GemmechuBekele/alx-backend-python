#!/usr/bin/env python3
"""Client for GitHub organization data."""

import requests
from typing import List, Optional, Dict, Any


def get_json(url: str) -> Dict[str, Any]:
    """Fetch JSON data from a URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


class GithubOrgClient:
    """Client for GitHub Organization info."""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str) -> None:
        """Initialize with organization name."""
        self.org_name = org_name

    @property
    def org(self) -> Dict[str, Any]:
        """Return organization metadata."""
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self) -> str:
        """Extract repos_url from organization metadata."""
        return self.org["repos_url"]

    def public_repos(self, license: Optional[str] = None) -> List[str]:
        """Return list of public repo names, optionally filtered by license."""
        repos = get_json(self._public_repos_url)
        if license is not None:
            repos = [repo for repo in repos 
                    if self.has_license(repo, license)]
        return [repo["name"] for repo in repos]

    @staticmethod
    def has_license(repo: Dict[str, Any], license_key: str) -> bool:
        """Check if repo has a specific license."""
        return repo.get("license", {}).get("key") == license_key
import re
from typing import Iterator

from github import Github

from omnicite.sources.software.base_software import BaseSoftware
from omnicite.special_fields.name_field import NameField
from omnicite.special_fields.version_field import VersionField


class GitHubRepository(BaseSoftware):
    def __init__(
        self,
        identifier: str,
    ):
        super().__init__(identifier, None)

    def retrieve_information(self):
        repo_name = self.identifier
        if self.identifier.startswith("https://"):
            match = re.match(r"^https://github\.com/(.*)$", self.identifier)
            repo_name = match.group(1)
        g = Github()
        repo = g.get_repo(repo_name)
        last_release = repo.get_releases()[0]
        self.fields = {
            "title": repo.name,
            "author": NameField(repo.owner.name),
            "url": repo.svn_url,
            "version": VersionField(last_release.title),
            "date": last_release.published_at.date(),
            "year": last_release.published_at.date().year,
        }

    def _unique_id_generator(self) -> Iterator[str]:
        essential_fields = (
            self.fields["author"].field_contents[0].final_name,
            self.fields["date"].year,
            self.fields["version"],
        )
        yield self._format_unique_identifier(*essential_fields)
        i = 1
        while True:
            yield self._format_unique_identifier(*essential_fields, i)
            i += 1

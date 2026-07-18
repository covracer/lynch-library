"""Download episodes from the AliveandKickn Libsyn archive."""

from argparse import ArgumentParser
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import urlopen

from django.core.management.base import BaseCommand, CommandError


class EpisodeLinksParser(HTMLParser):
    """Extract episode links from a Libsyn archive page."""

    def __init__(self) -> None:
        super().__init__()
        self.episode_links: list[str] = []
        self.in_episode_title = False

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        """Collect links nested in Libsyn episode headings."""
        attributes = dict(attributes)
        if tag == 'h2':
            self.in_episode_title = 'section-heading' in attributes.get('class', '').split()
            return
        if tag == 'a' and self.in_episode_title:
            self.episode_links.append(attributes['href'])

    def handle_endtag(self, tag: str) -> None:
        """Leave the current episode heading."""
        if tag == 'h2':
            self.in_episode_title = False


class AudioParser(HTMLParser):
    """Extract audio URLs from a Libsyn episode page."""

    def __init__(self) -> None:
        super().__init__()
        self.audio_urls: list[str] = []

    def handle_starttag(self, _tag: str, attributes: list[tuple[str, str | None]]) -> None:
        """Collect MP3 and M4A attributes."""
        attributes = dict(attributes)
        urls = [attributes.get(name, '') for name in ('content', 'href', 'src')]
        self.audio_urls.extend(
            url for url in urls if urlparse(url).path.lower().endswith(('.m4a', '.mp3'))
        )


def read_url(url: str) -> bytes:
    """Read an HTTPS resource."""
    if urlparse(url).scheme != 'https':
        raise CommandError(f'Only HTTPS URLs are supported: {url}')
    with urlopen(url) as response:  # noqa: S310 -- scheme checked above
        return response.read()


def parse_episode_links(document: bytes) -> list[str]:
    """Return episode links in archive display order."""
    parser = EpisodeLinksParser()
    parser.feed(document.decode())
    return parser.episode_links


def parse_audio_url(document: bytes) -> str:
    """Return the first audio URL from an episode page."""
    parser = AudioParser()
    parser.feed(document.decode())
    if not parser.audio_urls:
        raise CommandError('Episode page has no audio URL')
    return parser.audio_urls[0]


class Command(BaseCommand):
    """Download an episode into the local source mirror."""

    help = 'Download an AliveandKickn episode by its chronological number'

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Accept a chronological episode number and storage options."""
        parser.add_argument('episode_number', type=int)
        parser.add_argument('--archive-url', default='https://aliveandkickn.libsyn.com/2019/12')
        parser.add_argument('--output', type=Path, default=Path('library/podcasts'))

    def handle(self, episode_number: int, archive_url: str, output: Path, **_options: Any) -> None:
        """Discover and download the selected episode."""
        episode_links = list(reversed(parse_episode_links(read_url(archive_url))))
        if episode_number < 1 or episode_number > len(episode_links):
            raise CommandError(
                f'Episode number must be between 1 and {len(episode_links)} for {archive_url}'
            )
        episode_url = episode_links[episode_number - 1]
        audio_url = parse_audio_url(read_url(episode_url))
        episode_path = urlparse(episode_url).path.strip('/')
        archive_path = urlparse(archive_url).path.strip('/')
        destination = (
            output
            / urlparse(episode_url).hostname
            / archive_path
            / episode_path
            / Path(urlparse(audio_url).path).name
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(read_url(audio_url))
        self.stdout.write(str(destination))

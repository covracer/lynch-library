"""Tests for fetching an episode from a Libsyn archive."""

from io import BytesIO, StringIO
from pathlib import Path

from pytest import MonkeyPatch

from library.management.commands.fetch_podcast_episode import (
    Command,
    parse_audio_url,
    parse_episode_links,
)


def test_parse_episode_links():
    document = b"""<h2 class="section-heading"><a href="https://example.com/new">New</a></h2>
<h2 class="section-heading"><a href="https://example.com/old">Old</a></h2>"""
    assert parse_episode_links(document) == ['https://example.com/new', 'https://example.com/old']


def test_parse_audio_url():
    document = b'<meta property="og:audio" content="https://media.example.com/episode.m4a">'
    assert parse_audio_url(document) == 'https://media.example.com/episode.m4a'


def test_fetch_second_episode(monkeypatch: MonkeyPatch, tmp_path: Path):
    responses = {
        'https://example.com/2019/12': b"""<h2 class="section-heading"><a href="https://example.com/second">Second</a></h2>
<h2 class="section-heading"><a href="https://example.com/first">First</a></h2>""",
        'https://example.com/second': b'<audio src="https://media.example.com/second.mp3"></audio>',
        'https://media.example.com/second.mp3': b'audio',
    }
    monkeypatch.setattr(
        'library.management.commands.fetch_podcast_episode.urlopen',
        lambda url: BytesIO(responses[url]),
    )
    stdout = StringIO()
    Command(stdout=stdout).handle(
        episode_number=2, archive_url='https://example.com/2019/12', output=tmp_path
    )
    assert (tmp_path / 'example.com/2019/12/second/second.mp3').read_bytes() == b'audio'

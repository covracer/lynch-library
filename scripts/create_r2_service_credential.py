"""Create bucket-scoped R2 credentials without storing them in Terraform state."""

from asyncio import run
from hashlib import sha256
from os import environ
from urllib.parse import urlunsplit

from aiohttp import ClientSession

from config import settings

API_URL = 'https://api.cloudflare.com/client/v4'
BUCKET_NAME = 'library'

async def main() -> None:
    """Create one account-owned token and print its S3 credentials."""
    account_id = environ['CLOUDFLARE_ACCOUNT_ID']
    tokens_path = f'/accounts/{account_id}/tokens'
    async with ClientSession(
        headers={'Authorization': f'Bearer {environ["CLOUDFLARE_API_TOKEN"]}'}
    ) as client:
        async with client.get(f'{API_URL}{tokens_path}') as response:
            response.raise_for_status()
            tokens = (await response.json())['result']
        if settings.CONA in (token['name'] for token in tokens):
            raise RuntimeError(
                f'{settings.CONA!r} already exists; rotate or delete it in Cloudflare'
            )
        async with client.get(f'{API_URL}{tokens_path}/permission_groups') as response:
            response.raise_for_status()
            permission_groups = (await response.json())['result']
        permission_group_id = next(
            group['id']
            for group in permission_groups
            if group['name'] == 'Workers R2 Storage Bucket Item Write'
        )
        async with client.post(
            f'{API_URL}{tokens_path}',
            json={
                'name': settings.CONA,
                'policies': [
                    {
                        'effect': 'allow',
                        'permission_groups': [{'id': permission_group_id}],
                        'resources': {
                            f'com.cloudflare.edge.r2.bucket.{account_id}_default_{BUCKET_NAME}': '*'
                        },
                    },
                ],
            },
        ) as response:
            response.raise_for_status()
            token = (await response.json())['result']
    credentials = f'{token["id"]}:{sha256(token["value"].encode()).hexdigest()}'
    print(
        'export R2_URL='
        + urlunsplit(
            ('https', f'{credentials}@{account_id}.r2.cloudflarestorage.com', BUCKET_NAME, '', '')
        )
    )


if __name__ == '__main__':
    run(main())

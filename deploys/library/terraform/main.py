"""Configure the R2 podcast archive."""

from os import environ

from helicopyter import resource, terraform

terraform.required_providers(
    cloudflare={'source': 'cloudflare/cloudflare', 'version': '~> 5.21'},
)
resource.cloudflare_r2_bucket.library(
    account_id=environ['CLOUDFLARE_ACCOUNT_ID'],
    location='enam',
    name='library',
    storage_class='Standard',
)

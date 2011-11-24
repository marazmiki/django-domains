from django.conf import settings
from domains.utils import SiteIDHook

settings.SITE_ID = SiteIDHook()
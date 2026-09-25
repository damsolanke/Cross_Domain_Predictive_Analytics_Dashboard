"""
Central configuration for the external API keys the dashboard reads.

Every connector obtains its key through :func:`get_api_key`, so this module is
the one place that knows the environment variable names. Each service has a
canonical variable and a legacy alias (the generic name the code used
originally); the canonical name wins when both are set.

    OPENWEATHER_API_KEY   (alias: WEATHER_API_KEY)         OpenWeatherMap
    ALPHAVANTAGE_API_KEY  (alias: ECONOMIC_API_KEY)        Alpha Vantage
    NEWSAPI_KEY           (alias: SOCIAL_MEDIA_API_KEY)    News API
    TOMTOM_API_KEY        (alias: TRANSPORTATION_API_KEY)  TomTom Traffic

A missing key is not an error: ``get_api_key`` returns ``None``, logs a single
warning for that service, and the connectors fall back to simulated data.
"""
import logging
import os
from typing import Dict, Optional, Tuple

from dotenv import load_dotenv

# Load .env from the project root (same behaviour as app/__init__.py). Values
# already present in the environment are never overridden.
load_dotenv()

logger = logging.getLogger(__name__)

# domain -> (canonical variable name, legacy aliases in order of precedence)
API_KEY_VARS: Dict[str, Tuple[str, Tuple[str, ...]]] = {
    'weather': ('OPENWEATHER_API_KEY', ('WEATHER_API_KEY',)),
    'economic': ('ALPHAVANTAGE_API_KEY', ('ECONOMIC_API_KEY',)),
    'social_media': ('NEWSAPI_KEY', ('SOCIAL_MEDIA_API_KEY',)),
    'transportation': ('TOMTOM_API_KEY', ('TRANSPORTATION_API_KEY',)),
}

# Human-readable service names used in the missing-key warning
API_SERVICE_NAMES: Dict[str, str] = {
    'weather': 'OpenWeatherMap',
    'economic': 'Alpha Vantage',
    'social_media': 'News API',
    'transportation': 'TomTom Traffic',
}

_warned_domains = set()


def env_var_names(domain: str) -> Tuple[str, ...]:
    """Return the canonical variable name followed by its aliases for *domain*."""
    canonical, aliases = API_KEY_VARS[domain]
    return (canonical, *aliases)


def get_api_key(domain: str) -> Optional[str]:
    """
    Return the API key configured for *domain*, or None if none is set.

    The canonical variable takes precedence over its aliases and blank values
    count as unset. The first time a domain is found to have no key a warning
    is logged; later calls stay silent so the fallback does not spam the logs.
    """
    if domain not in API_KEY_VARS:
        raise ValueError(
            f"Unknown API key domain {domain!r}; expected one of {sorted(API_KEY_VARS)}"
        )

    for name in env_var_names(domain):
        value = os.environ.get(name, '').strip()
        if value:
            return value

    if domain not in _warned_domains:
        _warned_domains.add(domain)
        canonical, aliases = API_KEY_VARS[domain]
        logger.warning(
            "%s is not set (alias: %s); the %s connector will use simulated data.",
            canonical, ', '.join(aliases), API_SERVICE_NAMES[domain],
        )
    return None


def get_all_api_keys() -> Dict[str, Optional[str]]:
    """Return ``{domain: key-or-None}`` for every configured service."""
    return {domain: get_api_key(domain) for domain in API_KEY_VARS}


def reset_missing_key_warnings() -> None:
    """Forget which domains have already been warned about (used by tests)."""
    _warned_domains.clear()

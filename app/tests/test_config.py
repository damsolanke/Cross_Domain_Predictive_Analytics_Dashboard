"""
Tests for app.config: canonical/alias API key resolution and the no-key fallback.
"""
import os
import unittest
from unittest import mock

from app.config import API_KEY_VARS, get_api_key, reset_missing_key_warnings

# Every environment variable name the config module reads
ALL_KEY_NAMES = [
    name for canonical, aliases in API_KEY_VARS.values() for name in (canonical, *aliases)
]


def _env_without_api_keys(**overrides):
    """Copy of os.environ with every API key variable removed, plus overrides."""
    env = {k: v for k, v in os.environ.items() if k not in ALL_KEY_NAMES}
    env.update(overrides)
    return env


class TestApiKeyConfig(unittest.TestCase):
    """get_api_key() resolves canonical names, legacy aliases and missing keys."""

    def setUp(self):
        reset_missing_key_warnings()

    def test_canonical_name_takes_precedence_over_alias(self):
        env = _env_without_api_keys(TOMTOM_API_KEY='canonical-key', TRANSPORTATION_API_KEY='alias-key')
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(get_api_key('transportation'), 'canonical-key')

    def test_legacy_alias_still_works(self):
        env = _env_without_api_keys(WEATHER_API_KEY='alias-key')
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(get_api_key('weather'), 'alias-key')

    def test_blank_value_counts_as_unset(self):
        env = _env_without_api_keys(NEWSAPI_KEY='   ', SOCIAL_MEDIA_API_KEY='')
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertLogs('app.config', level='WARNING'):
                self.assertIsNone(get_api_key('social_media'))

    def test_missing_key_warns_once(self):
        with mock.patch.dict(os.environ, _env_without_api_keys(), clear=True):
            with self.assertLogs('app.config', level='WARNING') as captured:
                self.assertIsNone(get_api_key('economic'))
                self.assertIsNone(get_api_key('economic'))
        self.assertEqual(len(captured.output), 1)
        self.assertIn('ALPHAVANTAGE_API_KEY', captured.output[0])

    def test_unknown_domain_is_rejected(self):
        with self.assertRaises(ValueError):
            get_api_key('nonexistent')


class TestConnectorsWithoutKeys(unittest.TestCase):
    """Connectors serve simulated data, not an error payload, when no key is configured."""

    def test_transportation_traffic_falls_back_to_simulated_data(self):
        with mock.patch.dict(os.environ, _env_without_api_keys(), clear=True):
            from app.api.connectors.transportation_connector import TransportationConnector
            connector = TransportationConnector()
            data = connector.fetch_data({'city': 'Chicago', 'data_type': 'traffic', 'timeframe': 'day'})
        self.assertIsNone(connector.api_key)
        self.assertEqual(connector.status, 'using fallback data')
        self.assertNotIn('error', data)
        self.assertTrue(data['hotspots'])
        self.assertEqual(len(data['traffic_data']), 24)

    def test_social_media_news_falls_back_to_simulated_data(self):
        with mock.patch.dict(os.environ, _env_without_api_keys(), clear=True):
            from app.api.connectors.social_media_connector import SocialMediaConnector
            connector = SocialMediaConnector()
            data = connector.fetch_data({'platform': 'news', 'data_type': 'trends', 'timeframe': 'day'})
        self.assertIsNone(connector.api_key)
        self.assertEqual(connector.status, 'using fallback data')
        self.assertNotIn('error', data)
        self.assertIn('trending_topics', data)


if __name__ == '__main__':
    unittest.main()

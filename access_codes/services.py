import os
import requests
import logging

logger = logging.getLogger(__name__)

class ShopifyService:
    @staticmethod
    def verify_access_code(code: str) -> dict:
        """
        Verifies if an access code is valid via Shopify API.
        Returns a dict: {'is_valid': bool, 'meta': dict}
        """
        # User requested to bypass real API validation and accept any 8-character string "for now"
        if len(code) == 8:
            return {
                'is_valid': True,
                'meta': {'mocked': True, 'code': code, 'note': 'Bypassed Shopify API check'}
            }
        
        return {
            'is_valid': False,
            'meta': {'error': 'Must be exactly 8 characters'}
        }


import uuid
from datetime import datetime, timedelta
from urllib.parse import urlencode

import aiohttp
import json

from .datatypes import DiscordToken, Metadata, MetadataField


class DLRLightAPI:
    def __init__(self, client_id: int | str, redirect_uri: str, client_secret: str, discord_token: str):
        self.client_id = int(client_id)
        self.redirect_uri = redirect_uri
        self.client_secret = client_secret
        self.discord_token = discord_token

    async def _request(self, method: str, url: str, headers: dict, data: dict = None) -> dict:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.request(method, url, data=data) as response:
                if response.status == 200:
                    return await response.json()
                response.raise_for_status()

    @property
    def oauth_url(self) -> (str, str):
        state = str(uuid.uuid4())
        ROOT = 'https://discord.com/api/oauth2/authorize'
        query = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'state': state,
            'scope': 'role_connections.write identify',  # list of scopes?
            'prompt': 'consent',
        }
        url = ROOT + '?' + urlencode(query)

        return url, state

    async def get_oauth_token(self, code: str) -> DiscordToken:
        URL = 'https://discord.com/api/v10/oauth2/token'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
        }

        try:
            token_data = await self._request('POST', URL, headers, data)

            return DiscordToken(
                access_token=token_data['access_token'],
                refresh_token=token_data['refresh_token'],
                expires_in=token_data['expires_in'],
                expires_at=datetime.now() + timedelta(seconds=token_data['expires_in']),
            )
        except Exception as e:
            raise Exception(f"Error fetching OAuth tokens: {e}")

    async def refresh_token(self, token: DiscordToken) -> DiscordToken:
        URL = 'https://discord.com/api/v10/oauth2/token'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': token.refresh_token,
        }

        token_data = await self._request('POST', URL, headers, data)
        return DiscordToken(
            access_token=token_data['access_token'],
            refresh_token=token_data['refresh_token'],
            expires_in=timedelta(seconds=token_data['expires_in']),
            expires_at=datetime.now() + timedelta(seconds=token_data['expires_in']),
        )

    async def get_user_data(self, token: DiscordToken) -> dict:
        URL = 'https://discord.com/api/v10/oauth2/@me'
        headers = {
            'Authorization': f'Bearer {token.access_token}',
        }

        return await self._request('GET', URL, headers)

    async def push_metadata(self, token: DiscordToken, metadata: Metadata) -> None:
        URL = f'https://discord.com/api/v10/users/@me/applications/{self.client_id}/role-connection'

        headers = {
            'Authorization': f'Bearer {token.access_token}',
            'Content-Type': 'application/json',
        }

        await self._request('PUT', URL, headers, data=metadata.to_dict())

    async def get_metadata(self, token: DiscordToken) -> dict:
        URL = f'https://discord.com/api/v10/users/@me/applications/{self.client_id}/role-connection'

        headers = {
            'Authorization': f'Bearer {token.access_token}',
        }

        return await self._request('GET', URL, headers)

    async def register_metadata_schema(self, metadata: Metadata) -> dict:
        URL = f'https://discord.com/api/v10/applications/{self.client_id}/role-connections/metadata'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bot {self.discord_token}',
        }

        return await self._request('PUT', URL, headers, data=json.dumps(metadata.to_schema()))  # noqa


Client = DLRLightAPI

import os

from dlr_light_api import Client
from dlr_light_api.datatypes import Metadata, DiscordToken
from flask import Flask, redirect, request, Response, make_response
from flask.sessions import SecureCookieSessionInterface

from examples.creating_metadata import ShikimoriMetadata

app = Flask(__name__)
app.secret_key = os.environ.get('COOKIE_SECRET')
session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)

REDIRECT_URL = 'https://discord.com/app'


linked_role_client = Client(
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET'),
    redirect_uri=os.environ.get('REDIRECT_URI'),
    discord_token=os.environ.get('DISCORD_TOKEN')
)


@app.route('/linked-role')
def linked_role():
    url, state = linked_role_client.oauth_url

    response = make_response(redirect(url))
    response.set_cookie(key='clientState', value=state, max_age=60 * 5)

    return response


@app.route('/discord-oauth-callback')
async def discord_oauth_callback():
    discord_state = request.args.get('state')
    client_state = request.cookies.get('clientState')
    if client_state != discord_state:
        return Response("State verification failed.", status=403)

    try:
        code = request.args['code']
        token = await linked_role_client.get_oauth_token(code)

        print("Authorised, token acquired!")
        print(token)

        # Here you can save token and update metadata
        # ...

        return redirect(REDIRECT_URL)
    except Exception as e:
        return Response(str(e), status=500)


@app.route('/update-metadata', methods=['POST'])
async def update_metadata():
    try:
        user_id = int(request.form['userId'])
        await _update_metadata(user_id)

        return Response(status=204)
    except Exception as e:
        return Response(str(e), status=500)


async def _update_metadata(user_id: int):
    # you need to get token for particular user, implement it by yourself
    token: DiscordToken = ...

    # then you need to obtain metadata, lets use meta from previous example
    metadata: ShikimoriMetadata = ShikimoriMetadata(
        anime_watched=9999,
        total_hours=9999,
        platform_username='imPDA'
    )

    # refresh token if needed
    if token.is_expired:
        token = await linked_role_client.refresh_token(token)
        # ... save new token ...

    await linked_role_client.push_metadata(token, metadata.to_payload())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    # Now if you run this code and navigate to https://yoursite/linked-role you will be redirected to Discord
    # authorisation page. After confirmation, you will receive token and then redirected to `REDIRECT_URL`.

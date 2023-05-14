import os

from dlr_light_api import Client

# Let's use metadata from first example and register it.
from creating_metadata import ShikimoriMetadata


if __name__ == '__main__':
    # 1) Create a client. To register metadata schema `client id` and `discord token` is needed.
    # https://discord.com/developers/docs/tutorials/configuring-app-metadata-for-linked-roles#registering-your-metadata-schema
    client = Client(
        client_id=os.environ.get('CLIENT_ID'),
        redirect_uri=os.environ.get('REDIRECT_URI'),  # can be None, isn't required for registering the schema
        client_secret=os.environ.get('CLIENT_SECRET'),  # can be None, isn't required for registering the schema
        discord_token=os.environ.get('DISCORD_TOKEN')
    )

    # 2) Register the schema.
    print("Registering the schema:", ShikimoriMetadata.to_schema())
    client.register_metadata_schema(ShikimoriMetadata)
    print("Done!")

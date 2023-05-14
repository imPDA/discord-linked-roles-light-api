# from dlr_light_api.datatypes import MetadataField, MetadataType, Metadata
from src.dlr_light_api.datatypes import MetadataField, MetadataType, Metadata


# 1) Create a new field, set the type, the name and the description of field.
class TitlesWatched(MetadataField):
    type: MetadataType = MetadataType.INTEGER_GREATER_THAN_OR_EQUAL
    name: str = 'titles_watched'
    description: str = 'titles watched'


# 1.1) Create another field (optional, maximum up to 5 fields).
class TotalWatchTime(MetadataField):
    type: MetadataType = MetadataType.INTEGER_GREATER_THAN_OR_EQUAL
    name: str = 'hours_watching'
    description: str = 'hours watching anime'


# 2) Create metadata, set the platform name and add all fields created above. `None` means optional field.
class ShikimoriMetadata(Metadata):
    anime_watched: TitlesWatched
    total_hours: TotalWatchTime = None
    platform_name: str = 'shikimori.me'


if __name__ == '__main__':
    metadata = ShikimoriMetadata(
        anime_watched=9999,  # or anime_watched=TitlesWatched(key=9999),
        platform_username='imPDA'
        # total_hours is optional, is can be added later
    )

    print(metadata.to_payload())
    # {
    #     "platform_name": "shikimori.me",
    #     "platform_username": "imPDA",
    #     "anime_watched": "9999"
    # }

    metadata.anime_watched = 8888  # you can change and add properties like this
    metadata.total_hours = TotalWatchTime(key=7777)  # or like this
    metadata.platform_username = '~imPDA~'
    metadata.platform_name = 'shikimori.one'
    # this will cause `KeyError: No such a field (unknown_field)`
    # metadata.unknown_field = 'wtf'

    print(metadata.to_payload())
    # {
    #     "platform_name": "shikimori.one",
    #     "platform_username": "~imPDA~",
    #     "anime_watched": "8888",
    #     "total_hours": "7777"
    # }

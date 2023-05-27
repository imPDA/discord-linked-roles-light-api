from dlr_light_api.datatypes import Metadata, MetadataField, MetadataType


class ShikiMetadata(Metadata):
    platform_name = 'shikimori.me'
    total_titles = MetadataField(MetadataType.INT_GTE, 'Titles Watched', 'total titles watched')
    total_hours = MetadataField(MetadataType.INT_GTE, 'Total Hours', 'hours spend watching anime')


if __name__ == '__main__':
    print('Schema:', ShikiMetadata.to_schema())

    # ✔️ metadata can be provided as a dict
    a = ShikiMetadata({'total_titles': 1, 'total_hours': 11, 'platform_username': 'qwerty'})
    assert a.total_titles.value == 1
    assert a.total_hours.value == 11
    assert a.platform_username == 'qwerty'
    print(a.to_dict())

    # ✔️ metadata can be provided as a k/w arguments
    b = ShikiMetadata(total_titles=2)
    assert b.total_titles.value == 2
    assert b.total_hours.value is None
    assert b.platform_username is None

    # ✔️ metadata can be set directly, and it will be automatically converted into MetadataField
    c = ShikiMetadata()
    c.total_titles = 3
    assert type(c.total_titles) == MetadataField
    assert c.total_titles.value == 3

    # ❌ you can`t provide both args and kwargs
    # d = ShMetadata({'total_titles': 4}, total_hours=44)
    # >>> ValueError: Only args OR kwargs can be provided at the same time

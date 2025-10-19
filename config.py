DEBUG: bool = True

if DEBUG:
    # тестовый
    TOKEN: str = "7742068663:AAH-xi3TdKyC3467HNJy6bFLVOEHOT45jWk"
    CHANNEL: int = -1002542074756
    GROUP: int = -1002653430202
    ADMIN: int = 777198928
    # Коротко: это “короткий” ID канала для ссылок вида https://t.me/c/<id>/<msg_id>. Он берётся из chat_id канала,
    # просто без префикса -100.
    LINK_ID: int = 2542074756
else:
    # прод
    TOKEN: str = "8478992235:AAFsKKpCpfNqqsQrxbUj_J3JguSMgNmG77I"
    CHANNEL: int = -1001918020494
    GROUP: int = -1001926536763
    ADMIN: int = 107953601
    LINK_ID: int = 1918020494


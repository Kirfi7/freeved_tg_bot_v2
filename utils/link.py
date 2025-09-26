import config


def get_link(msg_id: int) -> str:
    link = F'https://t.me/c/{config.LINK_ID}/{msg_id}'
    return link

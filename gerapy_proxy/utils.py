def strip_response(data):
    """
    strip response data
    :param data:
    :return:
    """
    if not data:
        return
    if isinstance(data, str):
        return data.strip()

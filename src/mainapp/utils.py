def get_title_cased_str(string: str) -> str:
    """
    Convert snakecased string to a titlecased string
    """
    return string.replace('_', ' ').title()

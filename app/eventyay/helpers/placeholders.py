import re


def rename_placeholder(text, old, new):
    """Rename ``{old}`` to ``{new}`` in a stored email text, including the editor's ``data-variable`` chips."""
    if not text:
        return text
    text = text.replace(f'{{{old}}}', f'{{{new}}}')
    return re.sub(rf'(data-variable=\\?["\']){re.escape(old)}(\\?["\'])', rf'\g<1>{new}\g<2>', text)

def generate_table(concept, source=None, attribute='sites', media=False):
    """Generate a table."""
    ret = '\n<div style="display: flex; flex-wrap: wrap;">\n'
    count = 0
    for obj in [concept, source]:
        if obj is not None:
            for link in getattr(obj, attribute):
                if media:
                    if link.type.startswith("image/"):
                        ret += f'<div style="flex: 1 0 33%;"><img src="{link.url}" style="max-width: 100%;"/></div>\n'
                    elif link.type.startswith("video/"):
                        ret += f'<div style="flex: 1 0 33%;"><video src="{link.url}" style="max-width: 100%;" controls></video></div>\n'
                else:
                    ret += f'<div style="flex: 1 0 33%;"><a href="{link.url}">{link.title}</a></div>\n'
                count += 1
    ret += '</div>\n'
    return ret

def generate_link_table(concept, source=None):
    """Generate a table of links."""
    return generate_table(concept, source)

def generate_media_table(concept, source=None):
    """Generate a table of media."""
    return generate_table(concept, source, attribute='media', media=True)
from bottle import run as run_web, route
from bot.bot import concepts, source_ids
from markdown import markdown

complete = []

@route('/')
def index():
    display = []
    for c in concepts.values():
        if c.id not in source_ids:
            display.append(f"<a href=\"{c.id}\">\
                {c.category} :: {c.name}\
            </a>")
    return '<br>'.join(display)


@route('/<id:int>')
def channel(id):
    if id in concepts:
        concept = concepts[id]
        if concept.source in concepts:
            source = concepts[concept.source]
            return f"""
            <div style="display: flex; height: 100vh;">
                <div style="width: 50%; overflow: auto;">
                    ------parent------<br><br>{markdown(str(concept))}
                </div>
                <div style="width: 50%; overflow: auto;">
                    ------source------<br><br>{markdown(str(source))}
                </div>
            </div>
            """
        else:
            return f"""
            <div style="height: 100vh; overflow: auto;">
                ------parent------<br><br>{markdown(str(concept))}
            </div>
            """


def run_webui():
    run_web(host='localhost', port=8080, quiet=True)
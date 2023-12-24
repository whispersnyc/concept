from bottle import run as run_web, route
from bot.bot import concepts, sources
from markdown import markdown

@route('/')
def index():
    display = []
    for c in concepts.values():
        if c.id not in sources:
            display.append(f"<a href=\"{c.id}\">\
                {c.category} :: {c.name}\
            </a>")
    return '<br>'.join(display)


@route('/<id:int>')
def channel(id):
    if id in concepts:
        concept = concepts[id]
        ret = {"parent": str(concept)}

        if concept.post:
            ret["post"] = markdown(concept.post)
        if concept.source in concepts:
            source = concepts[concept.source]
            ret["source"] = str(source)
        
        return [f"------{k}------<br><br>{v}<br><br>" \
                for (k,v) in ret.items()]


def run_webui():
    run_web(host='localhost', port=8080, quiet=True)
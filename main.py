import threading
from bottle import run as run_web, route
from bot.bot import run_bot, concepts, sources
from markdown import markdown

@route('/')
def index():
    display = []
    for c in concepts.values():
        if c.id not in sources:
            txt = c.category + ' :: ' + c.name
            display.append(f"<a href=\"id/{c.id}\">{txt}</a>")
    return '<br>'.join(display)


@route('/id/<id:int>')
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

# Run web UI on a separate thread
webui_thread = threading.Thread(target=run_webui)
webui_thread.start()

# Run bot in the main thread
run_bot()
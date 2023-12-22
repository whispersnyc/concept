import threading
from bottle import run as run_web, route
from bot.bot import run_bot, concepts, sources

@route('/')
def index():
    display = []
    for c in concepts.values():
        if c.id not in sources:
            txt = c.category + ' :: ' + c.name
            display.append(f"<a href=\"id/{c.id}\">{txt}</a>")
    return '<br>'.join(display)


@route('/id/<id>')
def channel(id):
    if (id := int(id)) in concepts:
        concept = concepts[id]
        ret = str(concept)

        if concept.post:
            ret += f"<br><br>----post----<br><br>{
                concept.post.replace('<','').replace('>','').replace('\n','<br>')}"
        if concept.source in concepts:
            source = concepts[concept.source]
            ret += '<br><br>----src-----<br><br>'+str(source)
        return ret


def run_webui():
    run_web(host='localhost', port=8080, quiet=True)

# Run web UI on a separate thread
webui_thread = threading.Thread(target=run_webui)
webui_thread.start()

# Run bot in the main thread
run_bot()
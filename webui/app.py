from bottle import run as run_web, route, request, redirect
from bot.bot import concepts, source_ids
from markdown import markdown
from time import sleep

complete = []
queue = None

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
            <form action="/refresh_concept" method="post">
                <input type="hidden" name="concept_id" value="{id}">
                <input type="hidden" name="source_id" value="{source.id}">
                <input type="submit" value="(Re)load links/media">
            </form>
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
            <form action="/refresh_concept" method="post">
                <input type="hidden" name="concept_id" value="{id}">
                <input type="submit" value="Refresh Concept">
            </form>
            <div style="height: 100vh; overflow: auto;">
                ------parent------<br><br>{markdown(str(concept))}
            </div>
            """

@route('/refresh_concept', method='POST')
def refresh_concept():
    concept_id = request.forms.get('concept_id')
    queue.put(('refresh_concept', concept_id))
    if source_id := request.forms.get('source_id'):
        queue.put(('refresh_concept', source_id))
    
    return redirect(f'/{concept_id}')


def run_webui(message_queue):
    global queue
    queue = message_queue
    run_web(host='localhost', port=8080, quiet=True)
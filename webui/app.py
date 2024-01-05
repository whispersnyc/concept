from bottle import run as run_web, route, request, redirect
from bot.bot import concepts, source_ids
from markdown import markdown
from time import sleep

complete = []
queue = None


@route('/')
def index():
    display = [
        """<form action="/new_idea" method="post">
            <input type="text" name="idea" placeholder="Enter your new idea here">
            <input type="submit" value="Submit Idea">
        </form>
        <form action="/refresh_concept" method="post">
            <input type="hidden" name="concept_id" value="-1">
            <input type="submit" value="(Re)load links/media">
        </form>"""
    ]
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
                <input type="submit" value="(Re)load links/media">
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
    
    if concept_id == '-1': return redirect('/')
    return redirect(f'/{concept_id}')


@route('/new_idea', method='POST')
def new_idea():
    idea = request.forms.get('idea')
    queue.put(('new_idea', idea))
    return redirect('/')



def run_webui(message_queue):
    global queue
    queue = message_queue
    run_web(host='0.0.0.0', port=8080, quiet=True)
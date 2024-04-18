from bottle import run as run_web, route, request, redirect
from bot.bot import concepts, source_ids
from .tables import generate_link_table, generate_media_table
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
        concept, source = concepts[id], None
        source_html = '<input type="hidden" name="source_id" value="%s">'

        if concept.source in concepts:
            source = concepts[concept.source]
            source_html = source_html.replace('%s', str(source.id))

        link_table = generate_link_table(concept, source)
        media_table = generate_media_table(concept, source)

        return f"""
        <div style="display: flex; height: 100vh;">
            <div style="width: 50%; overflow: auto; display: flex; flex-wrap: wrap;">
                <form action="/refresh_concept" method="post" style="width: 100%;">
                    <input type="hidden" name="concept_id" value="{id}">
                    {source_html}
                    <input type="submit" value="(Re)load links/media">
                </form>
                {markdown(str(concept))}
                <div style="width: 100%;">------links------<br><br>{link_table}</div>
            </div>
            <div style="width: 50%; overflow: auto; display: flex; flex-wrap: wrap;">
                <div style="width: 100%;">------media------<br><br>{media_table}</div>
            </div>
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
import queue
import threading
from bot.bot import run_bot
from webui.app import run_webui

message_queue = queue.Queue()

# Run web UI on a separate thread
webui_thread = threading.Thread(
    target=run_webui, args=(message_queue,))
webui_thread.start()

# Run bot in the main thread
run_bot(message_queue)
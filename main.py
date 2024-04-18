import queue
import threading
from bot.bot import run_bot
from webui.app import run_webui
from concept import CACHE_DIR
import os, shutil

message_queue = queue.Queue()

# Run web UI on a separate thread
webui_thread = threading.Thread(
    target=run_webui, args=(message_queue,))
webui_thread.start()

print(CACHE_DIR)
def clear_cache():
    print("Clearing cache")
    for filename in os.listdir(CACHE_DIR):
        file_path = os.path.join(CACHE_DIR, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
#clear_cache()

# Run bot in the main thread
run_bot(message_queue)
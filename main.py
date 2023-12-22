import threading
from bot.bot import run_bot
from webui.app import run_webui

# Run web UI on a separate thread
webui_thread = threading.Thread(target=run_webui)
webui_thread.start()

# Run bot in the main thread
run_bot()
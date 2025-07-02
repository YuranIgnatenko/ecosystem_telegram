from web import thread_app_flask_run
from tcp import thread_run_tcp_client
from desktop import thread_desktop_start

from ..storage.tcp_channel_data import *

# if __name__ == '__main__':
thread_run_tcp_client()
thread_app_flask_run()
thread_desktop_start()
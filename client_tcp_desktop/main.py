from web import thread_app_flask_run
from tcp import thread_run_tcp_client
from desktop import thread_desktop_start

# import sys
# sys.path.append(r"C:\Users\EliteBook\Desktop\Code\ecosystem_telegram")
# from storage.tcp_channel_data import TcpChannelData
# from config import ADDR

# if __name__ == '__main__':
thread_run_tcp_client()
thread_app_flask_run()
thread_desktop_start()
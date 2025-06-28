from web import thread_app_flask_run
from web import thread_run_tcp_client

if __name__ == '__main__':
	thread_run_tcp_client()
	thread_app_flask_run()
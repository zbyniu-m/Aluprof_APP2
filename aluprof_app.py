from aluprof_app import create_app, logger
from waitress import serve

app = create_app()

if __name__ == "__main__":
   host = '0.0.0.0'
   port = 8000
   threads = 10
   logger.info(
        f'Serwer uruchomiony ip: {host}, port: {port}, threads: {threads}')
   print('sever waitress is running')
   serve(app, host=host, port=port, threads=threads)


import socket
import sys
import subprocess
import csv

def run_script():
    subprocess.run('conda activate lp')
    subprocess.run('bash run.sh -i samples/test -o tmp/output -c tmp/output/results.csv')

def get_csv():
    with open('results.csv', 'r') as f:
        csv_reader = csv.reader(f)
        final = ''
        for item in csv_reader:
            final+= str(line)
        return str.encode(final) + b'\r\n'

def conn_handler(connection):
    try:
        with conn:
            conn.settimeout(50)
            conn.send(b'Ready To Recieve\r\n')
            data = b''
            while True:
                incoming = conn.recv(2048)
                print(len(incoming))
                if len(incoming) < 2040:
                    return data
                data += incoming
    except (socket.timeout, TimeoutError):
        sys.stderr.write("ERROR: Timeout\n")
    except:
        sys.stderr.write("unknown error\n")

def save_img(bts, name):
    with open('samples/test'+name, 'wb') as f:
        f.write(str.encode(str(bts)))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", 53523))
            print('listening on port 53523')
            s.listen(10)
            while True:
                conn, addr = None, None
                conn, addr = s.accept()
                data = b''
                if conn:
                    print('connected to: something')
                    data = conn_handler(conn)
                    print('saving data')
                    save_img(data,'1.png')
                    print('data2')
                    data = conn_handler(conn)
                    data = conn_handler(conn)
                    save_img(data,'3.png')
                    run_script()
                    with conn:
                        conn.send(get_csv)
from flask import Flask, request, jsonify
import json
import threading
from datetime import datetime
from time import sleep
import requests


app = Flask(__name__)

running = False
stop_event = threading.Event()


def process_json(filename):
    global running
    global stop_event
    global url 

    with open(filename, 'r', encoding='utf-8-sig') as file:
        parsed_data = json.load(file)

    sorted_move_log = dict(
        sorted(
            parsed_data.get("MoveLog", {}).items(), 
            key=lambda x: x[1]['TimeStamp']
        )
    )

    request_time = next(iter(sorted_move_log.values()))['TimeStamp']
    request_time = datetime.strptime(request_time, '%Y/%m/%d %H:%M:%S.%f')

    for _, record in sorted_move_log.items():
        if running:
            current_request_time = datetime.strptime(record['TimeStamp'], '%Y/%m/%d %H:%M:%S.%f')
            interval = current_request_time - request_time

            # for testing purposes, shows the pause before next request in CLI
            print(f'Interval before the next request: {interval}')

            simulated_request_time = datetime.now()
            record['TimeStamp'] = simulated_request_time.strftime('%Y/%m/%d %H:%M:%S.%f')

            sleep(interval.total_seconds())

            if url:
                response = requests.get(
                    url=url, 
                    data=json.dumps(record), 
                    headers={'Content-Type': 'application/json'}
                )
            else:
                # for testing purposes, shows the request in CLI
                print(json.dumps(record, indent=4)) 

            request_time = current_request_time
        else:
            break

    running = False
    stop_event.set()


@app.route('/', methods=['GET'])
def process():
    global running
    global stop_event
    global url

    command = request.args.get('command', '').lower()
    url = request.args.get('url', '').lower()

    if command == 'start' and not running:
        filename = request.args.get('filename')
        if not filename:
            filename = 'STS_Moves_z0_Up.json'

        try:
            running = True
            stop_event.clear()
            threading.Thread(target=process_json(filename)).start()
            return jsonify({'message': 'Process started'})

        except FileNotFoundError:
            return jsonify({'message': 'File not found'}), 404
    elif command == 'stop' and running:
        running = False
        stop_event.set()
        return jsonify({'message': 'Processing stopped'})
    else:
        return jsonify({'message': 'Invalid command or operation already in progress'}), 400


if __name__ == "__main__":
    app.run(debug=True)
import subprocess
import json
from flask import Flask, jsonify, request, Response
from collections import OrderedDict
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import logger


app = Flask(__name__)
BASE_TEST_DIR = 'test_suite'


@app.route('/automation_ui', methods=['POST'])
def automation_ui():
    try:
        req_data = request.get_json(silent=True) or {}

        test_path = req_data.get('path', '')
        full_path = os.path.join(BASE_TEST_DIR, test_path)
        logger.info(f'flask path={full_path}')

        env_value = req_data.get('env', 'test')
        logger.info(f'flask env={env_value}')
        env = os.environ.copy()
        env['ENV'] = env_value

        input = subprocess.run(
            ['pytest', full_path, '-v', '--tb=short', f'--env={env_value}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=1800,

        )
        result = OrderedDict([
            ("status", "success" if input.returncode == 0 else "failed"),
            ("result", "check log for details."),
            ("path", full_path),
            ("env", env_value)
        ])
        return Response(json.dumps(result), mimetype='application/json')
    except subprocess.TimeoutExpired as e:
        logger.error(f'flask eeror: {e}')
        result = OrderedDict([
            ("status", "error"),
            ("result", f"{e}")
        ])
        return Response(json.dumps(result), mimetype='application/json')
    except Exception as e:
        logger.error(f'flask error: {e}')
        result = OrderedDict([
            ("status", "error"),
            ("result", f"{e}")
        ])
        return Response(json.dumps(result), mimetype='application/json')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 9801)))

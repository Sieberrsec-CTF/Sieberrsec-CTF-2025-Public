import subprocess
import os

def run_code(file_path, input_path, lang):
    if lang == 'cpp':
        exe = file_path.replace('.cpp', '')
        compile_cmd = ['g++', file_path, '-o', exe]
        if subprocess.run(compile_cmd).returncode != 0:
            return 'CE', ''
        try:
            with open(input_path, 'r') as f:
                result = subprocess.run(
                    [exe],
                    stdin=f,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=2
                )
                return 'OK', result.stdout.decode().strip()
        except subprocess.TimeoutExpired:
            return 'TLE', ''
        except Exception:
            return 'RE', ''

    elif lang == 'py':
        try:
            with open(input_path, 'r') as f:
                result = subprocess.run(
                    ['python3', file_path],
                    stdin=f,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=2
                )
                if result.returncode != 0:
                    return 'RE', result.stderr.decode()
                return 'OK', result.stdout.decode().strip()
        except subprocess.TimeoutExpired:
            return 'TLE', ''
        except Exception as e:
            return 'RE', str(e)

    return 'UNSUPPORTED', ''

def judge_submission(file_path, lang):
    input_dir = 'inputs'
    output_dir = 'outputs'
    inputs = sorted(os.listdir(input_dir))

    for inp in inputs:
        input_path = os.path.join(input_dir, inp)
        output_path = os.path.join(output_dir, inp.replace('.in', '.out'))

        verdict, user_out = run_code(file_path, input_path, lang)
        if verdict != 'OK':
            return verdict, f'Failed on {inp}'

        with open(output_path) as f:
            expected = f.read().strip()

        if user_out != expected:
            return 'WA', f'Wrong answer on {inp}'

    return 'AC', 'All testcases passed'

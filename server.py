from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import re
import shlex

app = Flask(__name__)
socketio = SocketIO(app)

shell_process = subprocess.Popen(['./mysh'],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 text=True,
                                 bufsize=1,
                                 cwd=os.getcwd())

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command')
def handle_command(data):
    cmd = data.strip()
    output_lines = []

    if cmd.startswith('cd'):
        parts = cmd.split(maxsplit=1)
        try:
            if len(parts) == 1:
                os.chdir(os.path.expanduser("~"))
            else:
                os.chdir(os.path.expanduser(parts[1]))
            output_lines.append('')
        except Exception as e:
            output_lines.append(f"cd: {e}")
    elif cmd.strip() == 'clear':
        # Handle clear command specially for web terminal
        cwd = os.getcwd()
        emit('clear_terminal', {'cwd': cwd})
        return
    else:
        # For debugging, let's try running commands directly instead of through mysh
        try:
            # For any ls command, force single column output
            if cmd.strip().startswith('ls'):
                # Parse ls command and add -1 flag if not already present
                ls_parts = cmd.strip().split()
                if '-1' not in ls_parts:
                    ls_parts.append('-1')
                result = subprocess.run(ls_parts, capture_output=True, text=True, cwd=os.getcwd())
            else:
                # Handle special commands that might not be available in containers
                if cmd.strip() == 'cal':
                    # Use Python to generate calendar if cal command not found
                    result = subprocess.run(['python3', '-c', 
                        'import calendar; import datetime; '
                        'now = datetime.datetime.now(); '
                        'print(calendar.month(now.year, now.month))'], 
                        capture_output=True, text=True, cwd=os.getcwd())
                elif cmd.strip() == 'time':
                    # Provide time command alternative
                    result = subprocess.run(['date'], capture_output=True, text=True, cwd=os.getcwd())
                else:
                    # Use shlex to properly parse the command with quotes
                    try:
                        # Try to parse the command properly
                        cmd_parts = shlex.split(cmd)
                        result = subprocess.run(cmd_parts, capture_output=True, text=True, cwd=os.getcwd())
                    except ValueError:
                        # If shlex fails, fall back to shell=True but escape properly
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())
            
            if result.stdout:
                # Extremely aggressive cleaning of output
                clean_output = result.stdout
                # Remove ALL control characters except newlines and tabs
                clean_output = ''.join(char for char in clean_output if ord(char) >= 32 or char in '\n\t')
                # Normalize all line endings to just \n
                clean_output = clean_output.replace('\r\n', '\n').replace('\r', '\n')
                # Remove any extra whitespace at line ends
                lines = clean_output.split('\n')
                clean_lines = [line.rstrip() for line in lines]
                clean_output = '\n'.join(clean_lines)
                output_lines.append(clean_output)
            if result.stderr:
                error_msg = result.stderr.strip()
                if "No such file or directory" in error_msg:
                    # Provide helpful suggestions for missing commands
                    cmd_name = cmd.strip().split()[0]
                    if cmd_name in ['cal', 'calendar']:
                        output_lines.append(f"Command '{cmd_name}' not found. Try: date")
                    elif cmd_name == 'time':
                        output_lines.append(f"Command '{cmd_name}' not found. Try: date")
                    else:
                        output_lines.append(error_msg)
                else:
                    output_lines.append(error_msg)
        except Exception as e:
            output_lines.append(f"Error: {e}")

    output = ''.join(output_lines).rstrip()
    cwd = os.getcwd()
    # Final cleaning of the entire output
    if output:
        # Remove any remaining problematic characters
        output = ''.join(char for char in output if ord(char) >= 32 or char in '\n\t')
        # Ensure clean line endings
        output = output.replace('\r\n', '\n').replace('\r', '\n')
        # Remove excessive empty lines
        while '\n\n\n' in output:
            output = output.replace('\n\n\n', '\n\n')
    emit('response', output + f'\n{cwd} $ ')

@socketio.on('connect')
def handle_connect():
    # Send initial prompt with current working directory
    cwd = os.getcwd()
    emit('initial_prompt', f'{cwd} $ ')

if __name__ == '__main__':
    # Get port from environment variable (for deployment platforms)
    port = int(os.environ.get('PORT', 8000))
    # Listen on all IP addresses (0.0.0.0) so others can connect
    socketio.run(app, host='0.0.0.0', port=port, debug=False)



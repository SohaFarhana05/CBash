# Unix Terminal Web App

A web-based Unix terminal built with Flask and Socket.IO, featuring:

- **Interactive Terminal**: Full terminal experience in your browser
- **Real-time Communication**: WebSocket-based command execution
- **Custom Shell**: Built with C for authentic Unix experience
- **Modern UI**: Clean terminal interface with xterm.js
- **Command History**: Navigate through previous commands with arrow keys

## Features

- ✅ Execute Unix commands (`ls`, `cat`, `grep`, `date`, etc.)
- ✅ Directory navigation with `cd`
- ✅ Command history with up/down arrows
- ✅ Terminal clearing with `clear`
- ✅ Real-time output display
- ✅ Proper text alignment and formatting

## Deployment

### Railway
1. Fork this repository
2. Connect your Railway account to GitHub
3. Deploy directly from Railway dashboard

### Heroku
1. Create a new Heroku app
2. Connect to your GitHub repository
3. Enable automatic deploys from main branch

### Local Development
```bash
pip install -r requirements.txt
gcc -o mysh main.c
python server.py
```

Visit `http://localhost:8000` to use the terminal.

## Technologies

- **Backend**: Python, Flask, Socket.IO
- **Frontend**: HTML5, JavaScript, xterm.js
- **Shell**: Custom C implementation
- **Deployment**: GitHub Actions, Gunicorn

---
Build with ❤️ by Soha

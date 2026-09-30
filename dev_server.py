"""
Local development server with live-reload.

Run this instead of app.py while you're working on the site:

    python dev_server.py

It serves the same Flask app, but watches the templates and app.py for
changes and automatically refreshes your browser tab when it sees one —
no need to stop and restart the server, and no need to hit refresh
yourself. Leave this running in a terminal and just save your files.

For production (e.g. on Render), the app is still served with gunicorn
as before — this file is dev-only and is not used there.
"""

from livereload import Server

from app import app

if __name__ == "__main__":
    server = Server(app.wsgi_app)

    # Refresh the browser whenever a template or the app code changes.
    server.watch("templates/*.html")
    server.watch("app.py")

    print("Live-reload dev server running at http://127.0.0.1:5000")
    print("Edit a template and save — your browser tab will refresh itself.")
    server.serve(port=5000, host="127.0.0.1", debug=True)

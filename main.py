import sys
import waitress
from src import app, init_db
from src.configman import config

def main():
    """Load config and run the production server."""
    # Load configuration from configman into Flask's app.config
    app.config['DB_PATH'] = config.get('path')
    app.config['MASTER_TOKEN'] = config.get('master_token')

    # Initialize the database with the loaded config
    init_db()

    host = config.get('host', '127.0.0.1')
    port = config.get('port', 5000)

    print(f"CrispyDB is now running on {host}:{port}")
    try:
        waitress.serve(app, host=host, port=port)
    except (KeyboardInterrupt, EOFError):
        print("\nShutting down server.")
        sys.exit(0)

if __name__ == "__main__":
    main()

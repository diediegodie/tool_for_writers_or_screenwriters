"""
Main application entry point.
Runs the Flask development server.
"""

import os
from app import create_app

# Get environment from environment variable
config_name = os.environ.get("FLASK_ENV", "development")

# Create Flask app instance
app = create_app(config_name)

if __name__ == "__main__":
    # Run development server
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=app.config["DEBUG"],
    )

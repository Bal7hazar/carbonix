# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
"""App main module."""

import os

from carbonix.controllers.dashboard_controller import DashboardController

if __name__ == "__main__":
    controller = DashboardController()
    controller.run(debug=os.environ.get("CARBONIX_DEBUG", True))
    server = controller.view.server

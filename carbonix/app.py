# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
"""App main module."""

from carbonix.controllers.dashboard_controller import DashboardController

if __name__ == "__main__":
    controller = DashboardController()
    server = controller.view.server
    controller.run()

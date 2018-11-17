from flask import render_template, Blueprint

error_pages = Blueprint("error_pages", __name__)

#404 Page: Show default view for 404 (not found) error
@error_pages.app_errorhandler(404)
def error_404(error):
    return render_template("error_pages/404.html"), 404

#403 Page: Show default view for 403 (forbidden) error
@error_pages.app_errorhandler(403)
def error_403(error):
    return render_template("error_pages/403.html"), 403

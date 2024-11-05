# don/views/admin.py
from flask import Blueprint, render_template, request, redirect, url_for
from .results import update_interval, scheduler, fetch_data

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/admin', methods=["GET", "POST"])
def admin():
    global update_interval

    if request.method == "POST":
        selected_interval = int(request.form.get("update_interval"))
        update_interval = selected_interval  # Update the interval globally

        # Update the scheduler job with the new interval
        job = scheduler.get_jobs()[0]
        job.reschedule(trigger="interval", seconds=update_interval)

        # Force an immediate fetch after changing the interval
        fetch_data()

        return redirect(url_for('admin.admin'))

    return render_template("admin.html", current_interval=update_interval)
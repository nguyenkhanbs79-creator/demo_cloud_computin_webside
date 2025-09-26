import os
from datetime import datetime
from typing import Optional

from flask import Flask, redirect, render_template, request, url_for, flash
from google.cloud import datastore


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "change-me")

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise RuntimeError("Missing GOOGLE_CLOUD_PROJECT environment variable")

    client = datastore.Client(project=project_id)

    KIND = "Task"

    def entity_to_dict(entity: datastore.Entity) -> dict:
        return {
            "id": entity.key.id,
            "title": entity.get("title", ""),
            "description": entity.get("description", ""),
            "status": entity.get("status", "pending"),
            "created_at": entity.get("created_at"),
        }

    @app.route("/")
    def index():
        query = client.query(kind=KIND)
        query.order = ["-created_at"]
        tasks = [entity_to_dict(entity) for entity in query.fetch()]
        return render_template("index.html", tasks=tasks)

    @app.route("/tasks", methods=["POST"])
    def create_task():
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "pending")

        if not title:
            flash("Title is required.", "error")
            return redirect(url_for("index"))

        key = client.key(KIND)
        entity = datastore.Entity(key=key)
        entity.update(
            {
                "title": title,
                "description": description,
                "status": status,
                "created_at": datetime.utcnow(),
            }
        )
        client.put(entity)
        flash("Task created successfully!", "success")
        return redirect(url_for("index"))

    def get_task_or_404(task_id: int) -> Optional[datastore.Entity]:
        key = client.key(KIND, task_id)
        entity = client.get(key)
        if entity is None:
            flash("Task not found.", "error")
        return entity

    @app.route("/tasks/<int:task_id>/edit")
    def edit_task(task_id: int):
        entity = get_task_or_404(task_id)
        if entity is None:
            return redirect(url_for("index"))
        task = entity_to_dict(entity)
        return render_template("edit.html", task=task)

    @app.route("/tasks/<int:task_id>", methods=["POST"])
    def update_task(task_id: int):
        entity = get_task_or_404(task_id)
        if entity is None:
            return redirect(url_for("index"))

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "pending")

        if not title:
            flash("Title is required.", "error")
            return redirect(url_for("edit_task", task_id=task_id))

        entity.update(
            {
                "title": title,
                "description": description,
                "status": status,
            }
        )
        client.put(entity)
        flash("Task updated successfully!", "success")
        return redirect(url_for("index"))

    @app.route("/tasks/<int:task_id>/delete", methods=["POST"])
    def delete_task(task_id: int):
        key = client.key(KIND, task_id)
        client.delete(key)
        flash("Task deleted.", "info")
        return redirect(url_for("index"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)

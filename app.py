import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import Session, WBSElement, ProjectDetails

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def index():
    session = Session()
    try:
        wbs_elements = session.query(WBSElement).all()
        project_details = session.query(ProjectDetails).all()
    except Exception as e:
        flash(f"Error fetching data: {str(e)}", "error")
        wbs_elements, project_details = [], []
    finally:
        session.close()
    return render_template("index.html", wbs_elements=wbs_elements, project_details=project_details)

@app.route("/add", methods=["POST"])
def add_wbs_element():
    name = request.form.get("name")
    project_id = request.form.get("project_id")
    parent_id = request.form.get("parent_id")
    budget = request.form.get("budget", 0.0)

    if not name or not project_id:
        flash("Name and Project ID are required.", "error")
        return redirect(url_for("index"))

    session = Session()
    try:
        new_element = WBSElement(
            name=name,
            project_id=int(project_id),
            parent_id=int(parent_id) if parent_id else None,
            budget=float(budget)
        )
        session.add(new_element)
        session.commit()
        flash("WBS Element added successfully!", "success")
    except Exception as e:
        session.rollback()
        flash(f"Error adding WBS element: {str(e)}", "error")
    finally:
        session.close()
    return redirect(url_for("index"))

@app.route("/addprojects", methods=["POST"])
def addproject():
    project_name = request.form.get("project_name")
    project_number = request.form.get("project_number")
    if not project_name or not project_number:
        flash("Project Name and Project Number are required.", "error")
        return redirect(url_for("index"))
    session = Session()
    try:
        new_project = ProjectDetails(project_number=project_number, project_name=project_name)
        session.add(new_project)
        session.commit()
        flash(f"Project '{project_name}' added successfully!", "success")
    except Exception as e:
        session.rollback()
        flash(f"Error adding project: {str(e)}", "error")
    finally:
        session.close()
    return redirect(url_for("index"))

@app.route("/deleteproject/<int:project_id>")
def delete_project(project_id):
    session = Session()
    try:
        element = session.query(ProjectDetails).get(project_id)
        if not element:
            flash("Project not found.", "error")
        else:
            children = session.query(WBSElement).filter_by(project_id=element.id).all()
            if children:
                flash(f"Cannot delete {element.project_name} because it has children.", "error")
            else:
                session.delete(element)
                session.commit()
                flash("Project deleted successfully.", "success")
    except Exception as e:
        session.rollback()
        flash(f"Error deleting project: {str(e)}", "error")
    finally:
        session.close()
    return redirect(url_for("index"))

@app.route("/deletewbs/<int:element_id>")
def delete_wbs_element(element_id):
    session = Session()
    try:
        element = session.query(WBSElement).get(element_id)
        if not element:
            flash("WBS Element not found.", "error")
        else:
            children = session.query(WBSElement).filter_by(parent_id=element.id).all()
            if children:
                flash(f"Cannot delete {element.name} because it has children.", "error")
            else:
                session.delete(element)
                session.commit()
                flash("WBS Element deleted successfully.", "success")
    except Exception as e:
        session.rollback()
        flash(f"Error deleting WBS element: {str(e)}", "error")
    finally:
        session.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
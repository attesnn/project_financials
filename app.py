# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
from models import Session, WBSElement, ProjectDetails  # Import database session and WBS model

# Initialize the Flask app
app = Flask(__name__)

# Route for the home page
@app.route("/")
def index():
    """
    Display all WBS elements in a table.
    """
    # Create a database session
    session = Session()
    
    # Query all WBS elements from the database
    wbs_elements = session.query(WBSElement).all()
    project_details = session.query(ProjectDetails).all()  
    
    # Close the session to free up resources
    session.close()
    
    # Render the 'index.html' template and pass the WBS elements to it
    return render_template("index.html", wbs_elements=wbs_elements, project_details=project_details)

# Route to handle adding a new WBS element
@app.route("/add", methods=["POST"])

def add_wbs_element():
    """
    Add a new WBS element to the database.
    """
    # Get form data from the request
    name = request.form.get("name")  # Required field: Name of the WBS element
    parent_id = request.form.get("parent_id")  # Optional field: Parent ID
    budget = request.form.get("budget", 0.0)  # Optional field: Budget (default to 0.0)
    
    # Create a database session
    session = Session()
    
    # Create a new WBS element object
    new_element = WBSElement(
        name=name,
        parent_id=int(parent_id) if parent_id else None,  # Convert parent_id to int if provided
        budget=float(budget)  # Convert budget to float
    )
    
    # Add the new element to the session and commit it to the database
    session.add(new_element)
    session.commit()
    
    # Close the session
    session.close()
    
    # Redirect the user back to the home page after adding the element
    return redirect(url_for("index"))

@app.route("/addproject", methods=["POST"])
def add_project():
    """
    Add a new project to the database.
    """
    # Get form data from the request
    project_name = request.form.get("project_name")
    project_number = request.form.get("project_number")

    # Create a database session
    session = Session()

    # Create a new project object
    new_project = ProjectDetails(
        project_name=project_name,
        project_number=project_number
    )

    # Add the new project to the session and commit it to the database
    session.addproject(new_project)
    session.commit()

    # Close the session
    session.close()

    # Redirect the user back to the home page after adding the project
    return redirect(url_for("index"))


# Route to handle deleting a WBS element
@app.route("/delete/<int:element_id>")
def delete_wbs_element(element_id):
    """
    Delete a WBS element from the database.
    """
    # Create a database session
    session = Session()
    
    # Query the WBS element by its ID
    element = session.query(WBSElement).get(element_id)
    
    if element:
        # Check if the element has any children
        children = session.query(WBSElement).filter_by(parent_id=element.id).all()
        
        if children:
            # If the element has children, print a message (for debugging)
            print(f"Cannot delete {element.name} (ID: {element.id}) because it has children.")
        else:
            # If no children, delete the element and commit the change
            session.delete(element)
            session.commit()
    
    # Close the session
    session.close()
    
    # Redirect the user back to the home page after deletion
    return redirect(url_for("index"))

# Run the Flask app
if __name__ == "__main__":
    """
    Start the Flask development server.
    """
    # Run the app in debug mode (auto-reloads on code changes)
    app.run(debug=True)
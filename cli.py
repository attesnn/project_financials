from models import Session, WBSElement, ProjectDetails

def add_wbs_element(name, project_id, budget=0.0):
    session = Session()
    new_element = WBSElement(name=name, project_id=project_id, budget=budget)
    session.add(new_element)
    session.commit()
    print(f"Added WBS element: {name} (Parent: {parent_id}) (Project: {project_id}) ")

def add_project(project_name, project_number):
    session = Session()
    new_project = ProjectDetails(project_name=project_name, project_number=project_number)
    session.add(new_project)
    session.commit()
    print(f"Added Project: {project_name} (project_number: {project_number}) (ID: {new_project.id})")

def display_wbs():
    session = Session()
    elements = session.query(WBSElement).all()
    
    # Simple print (we'll improve this later)
    for element in elements:
        print(f"ID: {element.id}, Name: {element.name}, Parent: {element.parent_id}, Budget: {element.budget}, Project: {element.project_id}")

def display_proj():
    session = Session()
    projects = session.query(ProjectDetails).all()

    for project in projects:
        print(f"ID: {project.id}, Project Name: {project.project_name}, Project Number: {project.project_number}")

def delete_wbs_element(element_id):
    session = Session()
    element = session.query(WBSElement).get(element_id)
    
    if element:
        # Check if the element has children
        children = session.query(WBSElement).filter_by(parent_id=element.id).all()
        if children:
            print(f"Cannot delete {element.name} (ID: {element.id}) because it has children.")
        else:
            # Ask for confirmation
            confirm = input(f"Are you sure you want to delete {element.name} (ID: {element.id})? (y/n): ").strip().lower()
            if confirm == "y":
                session.delete(element)
                session.commit()
                print(f"Deleted WBS element: {element.name} (ID: {element.id})")
            else:
                print("Deletion canceled.")
    else:
        print(f"WBS element with ID {element_id} not found!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "projadd":
            project_name = sys.argv[2]
            project_number = str(sys.argv[3]) if len(sys.argv) > 3 else None
            add_project(project_name, project_number)      

        elif command == "projdisplay":
            display_proj()
    
        elif command == "wbsadd":
            if len(sys.argv) < 4:
                print("Usage: python cli.py wbsadd <name> <project_id> [budget] [parent_id]")
            else:
                name = sys.argv[2]
                project_id = int(sys.argv[3]) if len(sys.argv) > 3 else None
                budget = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
                parent_id = int(sys.argv[5]) if len(sys.argv) > 5 else None
                add_wbs_element(name, parent_id, budget)
        
        elif command == "wbsdelete":
            element_id = int(sys.argv[2])
            delete_wbs_element(element_id)
        
        elif command == "wbsdisplay":
            display_wbs()
        
        else:
            print("Invalid command. Use 'wbsadd', 'wbsdelete', or 'wbsdisplay'.")
    else:
        print("Usage: python cli.py [command] [args]")
    
    
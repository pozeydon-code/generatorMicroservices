import os
from utilities.services.projects import create_project, clean_project_files
from utilities.services.solution import create_solution_file, add_projects_to_solution, add_project_references
from utilities.services.entities import create_entities_folder, generate_entity_code, save_entity_file

def create_solution_structure(base_path, solution_name, service_name, dotnet_version):
    layers = ["Domain", "Application", "Infrastructure", "API"]

    for layer in layers:
        project_path = create_project(layer, service_name, dotnet_version, base_path)
        clean_project_files(project_path, layer, service_name)

    create_solution_file(solution_name, base_path)
    add_projects_to_solution(service_name, layers, base_path)
    add_project_references(service_name, base_path)

def generate_domain_entities(base_path, service_name, entities):
    entities_path = create_entities_folder(base_path, service_name)

    for entity_name, props in entities.items():
        code = generate_entity_code(service_name, entity_name, props)
        save_entity_file(entities_path, entity_name, code)

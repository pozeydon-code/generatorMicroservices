import os
from utilities.domain.generate_primitives import generate_primitives
from utilities.filesystem.generate_global_usings import generate_global_usings_domain
from utilities.services.apply_migrations import add_and_apply_migrations
from utilities.services.generate_entity_configurations import generate_entity_configurations
from utilities.services.api_layer import generate_api_layer
from utilities.services.application_layer import generate_application_layer
from utilities.services.create_connection_strings import add_connection_string_to_appsettings
from utilities.services.infrastructure_layer import generate_infrastructure_layer
from utilities.services.loader import load_service_definitions
from utilities.filesystem.create_directory import create_directory
from utilities.services.generator import create_solution_structure, generate_domain_entities
from utilities.services.package_instalation import install_efcore_nugets
from utilities.services.value_objects import generate_value_objects

def main():
    solution_name = "CleanArchSolution"
    base_path = os.path.join(os.getcwd(), solution_name)
    json_path = os.path.join(os.getcwd(), "data", "services_definition.json")
    dotnet_version = "net8.0"

    definitions = load_service_definitions(json_path)
    create_directory(base_path)
    print(f"Estructura base creada en: {base_path}")

    for service, content in definitions.items():
        create_solution_structure(base_path, solution_name, service, dotnet_version)
        install_efcore_nugets(base_path, service)

        generate_domain_entities(base_path, service, content.get("Entities", {}))
        generate_value_objects(base_path, service, content.get("Entities", {}))
        generate_primitives(base_path, service)
        generate_global_usings_domain(base_path, service)

        generate_application_layer(base_path, service, content.get("Entities", {}))

        generate_infrastructure_layer(base_path, service, content.get("Entities", {}))
        generate_entity_configurations(base_path, service, content.get("Entities", {}))
        if "ConectionStrings" in content:
            add_connection_string_to_appsettings(base_path, service, content["ConectionStrings"])

        # TODO: Create Dependency Injection
        generate_api_layer(base_path, service, content.get("Entities", {}))
        add_and_apply_migrations(base_path, service)

if __name__ == "__main__":
    main()

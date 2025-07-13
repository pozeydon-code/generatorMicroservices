
import os
from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file
from utilities.filesystem.generate_global_usings import generate_global_usings_infrastructure
from utilities.infrastructure.generate_db_context import generate_dbcontext
from utilities.infrastructure.generate_dependency_injection import generate_di_infrastructure
from utilities.infrastructure.generate_repository_implementation import generate_repository_impl


def generate_infrastructure_layer(base_path, service_name, entities):
    infra_base = os.path.join(base_path, "Services", service_name, f"{service_name}.Infrastructure")
    repo_path = os.path.join(infra_base, "Repositories")
    persistence_path = os.path.join(infra_base, "Persistence")
    create_directory(repo_path)
    create_directory(persistence_path)

    # Repositorios
    for entity_name in entities:
        generate_repository_impl(service_name, repo_path, entity_name)

    # DbContext
    generate_dbcontext(service_name, persistence_path, entities)

    # DI Extension
    generate_di_infrastructure(service_name, infra_base, entities)

    generate_global_usings_infrastructure(base_path, service_name)

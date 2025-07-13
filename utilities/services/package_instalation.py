import os
from utilities.system.run_command import run_command


def install_efcore_nugets(base_path, service_name):
    base_service_path = os.path.join(base_path, "Services", service_name)

    infra_path = os.path.join(base_service_path, f"{service_name}.Infrastructure")
    application_path = os.path.join(base_service_path, f"{service_name}.Application")
    api_path = os.path.join(base_service_path, f"{service_name}.API")
    domain_path = os.path.join(base_service_path, f"{service_name}.Domain")

    ef_packages_api = [
        "ErrorOr",
        "Microsoft.EntityFrameworkCore.Design",
    ]

    ef_packages_application = [
        "ErrorOr",
        "FluentValidation",
        "FluentValidation.AspNetCore",
        "Microsoft.EntityFrameworkCore",
        "MediatR"
    ]

    ef_packages_infrastructure = [
        "Microsoft.EntityFrameworkCore.SqlServer",
    ]

    ef_packages_domain = [
        "ErrorOr",
        "MediatR"
    ]

    for pkg in ef_packages_api:
        run_command(f"dotnet add package {pkg}", cwd=api_path)

    for pkg in ef_packages_application:
        run_command(f"dotnet add package {pkg}", cwd=application_path)

    for pkg in ef_packages_infrastructure:
        run_command(f"dotnet add package {pkg}", cwd=infra_path)

    for pkg in ef_packages_domain:
        run_command(f"dotnet add package {pkg}", cwd=domain_path)

    print(f"Paquetes EF Core instalados para {service_name} en las capas API, Application, Infrastructure y Domain.")

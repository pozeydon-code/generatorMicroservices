import os
from utilities.system.run_command import run_command


def install_efcore_nugets(base_path, service_name):
    base_service_path = os.path.join(base_path, "Services", service_name)

    infra_path = os.path.join(base_service_path, f"{service_name}.Infrastructure")
    api_path = os.path.join(base_service_path, f"{service_name}.API")

    ef_packages = [
        "Microsoft.EntityFrameworkCore",
        "Microsoft.EntityFrameworkCore.SqlServer",
        "Microsoft.EntityFrameworkCore.Abstractions",
        "Microsoft.Extensions.Configuration.Json"
    ]

    for pkg in ef_packages:
        run_command(f"dotnet add package {pkg}", cwd=infra_path)
        run_command(f"dotnet add package {pkg}", cwd=api_path)

    run_command(f"dotnet add package Microsoft.EntityFrameworkCore.Design", cwd=api_path)

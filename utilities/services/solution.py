import os
from utilities.system.run_command import run_command

def create_solution_file(solution_name, base_path):
    if not os.path.exists(os.path.join(base_path, f"{solution_name}.sln")):
        run_command(f"dotnet new sln -n {solution_name}", cwd=base_path)

def add_projects_to_solution(service_name, layers, base_path):
    for layer in layers:
        proj = os.path.join("Services", service_name, f"{service_name}.{layer}", f"{service_name}.{layer}.csproj")
        run_command(f"dotnet sln add {proj}", cwd=base_path)

def add_project_references(service_name, base_path):
    run_command(f"dotnet add {service_name}.Application.csproj reference ../{service_name}.Domain/{service_name}.Domain.csproj",
                cwd=os.path.join(base_path, f"Services/{service_name}/{service_name}.Application"))
    run_command(f"dotnet add {service_name}.Infrastructure.csproj reference ../{service_name}.Application/{service_name}.Application.csproj",
                cwd=os.path.join(base_path, f"Services/{service_name}/{service_name}.Infrastructure"))
    run_command(f"dotnet add {service_name}.Infrastructure.csproj reference ../{service_name}.Domain/{service_name}.Domain.csproj",
                cwd=os.path.join(base_path, f"Services/{service_name}/{service_name}.Infrastructure"))
    run_command(f"dotnet add {service_name}.API.csproj reference ../{service_name}.Application/{service_name}.Application.csproj ../{service_name}.Infrastructure/{service_name}.Infrastructure.csproj ",
                cwd=os.path.join(base_path, f"Services/{service_name}/{service_name}.API"))

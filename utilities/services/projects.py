import os
from utilities.filesystem.create_directory import create_directory
from utilities.system.run_command import run_command

def create_project(layer, service_name, dotnet_version, base_path):
    project_name = f"{service_name}.{layer}"
    project_path = os.path.join(base_path, "Services", service_name, project_name)
    create_directory(os.path.dirname(project_path))

    template = "classlib" if layer != "API" else "webapi -controllers"
    run_command(f"dotnet new {template} -n {project_name} -f {dotnet_version}", cwd=os.path.dirname(project_path))

    return project_path

def clean_project_files(project_path, layer, service_name):
    if layer == "API":
        remove_files_api = [
            "Controllers/WeatherForecastController.cs",
            f"{service_name}.API.http",
            "WeatherForecast.cs"
        ]
        for file in remove_files_api:
            _remove_file(os.path.join(project_path, file))

    remove_files_common = ["Class1.cs"]
    for file in remove_files_common:
        _remove_file(os.path.join(project_path, file))

def _remove_file(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"[-] Archivo eliminado: {path}")

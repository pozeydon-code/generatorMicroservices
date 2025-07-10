import os
from utilities.filesystem.create_file import create_file


def generate_global_usings(base_path, service_name):
    api_path = os.path.join(base_path, "Services", service_name, f"{service_name}.API")
    content = """// Auto-generated global usings
global using MediatR;
global using Microsoft.AspNetCore.Mvc;
global using System.Threading.Tasks;
"""
    create_file(os.path.join(api_path, "GlobalUsings.cs"), content)


def generate_global_usings_application(base_path, service_name):
    api_path = os.path.join(base_path, "Services", service_name, f"{service_name}.Application")
    content = f"""// Auto-generated global usings
global using MediatR;
global using {service_name}.Domain.Entities;
global using {service_name}.Domain.ValueObjects;
"""
    create_file(os.path.join(api_path, "GlobalUsings.cs"), content)

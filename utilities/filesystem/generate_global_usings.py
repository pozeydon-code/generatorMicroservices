import os
from utilities.filesystem.create_file import create_file


def generate_global_usings_application(base_path, service_name):
    api_path = os.path.join(base_path, "Services", service_name, f"{service_name}.Application")
    content = f"""// Auto-generated global usings
global using MediatR;
global using {service_name}.Domain.Entities;
global using {service_name}.Domain.ValueObjects;
global using FluentValidation;
global using ErrorOr;
global using Microsoft.EntityFrameworkCore;
"""
    create_file(os.path.join(api_path, "GlobalUsings.cs"), content)


def generate_global_usings_infrastructure(base_path, service_name):
    api_path = os.path.join(base_path, "Services", service_name, f"{service_name}.Infrastructure")
    content = f"""// Auto-generated global usings
global using MediatR;
global using Microsoft.EntityFrameworkCore;
"""
    create_file(os.path.join(api_path, "GlobalUsings.cs"), content)


def generate_global_usings_api(api_path):
    content = f"""// Auto-generated global usings
global using ErrorOr;
global using Microsoft.AspNetCore.Mvc;
global using MediatR;
"""
    create_file(os.path.join(api_path, "GlobalUsings.cs"), content)

def generate_global_usings_domain(base_path, service_name):
    domain_path = os.path.join(base_path, "Services", service_name, f"{service_name}.Domain")
    content = f"""// Auto-generated global usings
global using System.Text.RegularExpressions;
global using {service_name}.Domain.ValueObjects;
global using MediatR;
"""
    create_file(os.path.join(domain_path, "GlobalUsings.cs"), content)

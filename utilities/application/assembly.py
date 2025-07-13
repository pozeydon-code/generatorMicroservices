import os
from utilities.filesystem.create_file import create_file


def generate_assembly_application(base_path, service_name):
    lines = [
        "using System.Reflection;",
        "",
        f"namespace {service_name}.Application;",
        f"public class ApplicationAssemblyReference",
        "{",
        f"  internal static readonly Assembly Assembly = typeof(ApplicationAssemblyReference).Assembly;",
        "}",
    ]
    create_file(os.path.join(base_path, f"ApplicationAssemblyReference.cs"), "\n".join(lines))

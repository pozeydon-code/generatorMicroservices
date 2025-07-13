import os
from utilities.filesystem.create_file import create_file


def generate_assembly_api(base_path, service_name):
    lines = [
        "using System.Reflection;",
        "",
        f"namespace {service_name}.API;",
        f"public class PresentationAssemblyReference",
        "{",
        f"  internal static readonly Assembly Assembly = typeof(PresentationAssemblyReference).Assembly;",
        "}",
    ]
    create_file(os.path.join(base_path, f"PresentationAssemblyReference.cs"), "\n".join(lines))

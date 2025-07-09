import os
from mappings.value_mappings import value_object_mappings
from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file
from utilities.services.parser import parse_csharp_type

def create_entities_folder(base_path, service_name):
    domain_path = os.path.join(base_path, "Services", service_name, f"{service_name}.Domain")
    entities_path = os.path.join(domain_path, "Entities")
    create_directory(entities_path)
    return entities_path

def generate_entity_code(service_name, entity_name, props):
    lines = [
        "using System;",
        "using ProductService.Domain.Entities;",
        "using ProductService.Domain.ValueObjects;",
        "",
        f"namespace {service_name}.Domain.Entities",
        "{",
        f"    public class {entity_name}",
        "    {"
    ]
    for prop_name, prop_def in props.items():
        if isinstance(prop_def, dict) and prop_def.get("navigation"):
            csharp_type = parse_csharp_type(prop_def["type"])
            prop_csharp_name = f"{prop_name}Navigation"
        else:
            csharp_type = parse_csharp_type(prop_def)
            prop_csharp_name = prop_name

        lines.append(f"        public {csharp_type} {prop_csharp_name} {{ get; set; }}")
    lines.append("    }")
    lines.append("}")
    return "\n".join(lines)

def save_entity_file(entities_path, entity_name, content):
    file_path = os.path.join(entities_path, f"{entity_name}.cs")
    create_file(file_path, content)

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
        f"namespace {service_name}.Domain.Entities;",
        f"public class {entity_name}",
        "{"
    ]

    ctor_params = []       # lista de "Tipo nombreParam"
    assignments = []       # lista de "this.Prop = nombreParam;"

    for prop_name, prop_def in props.items():
        if isinstance(prop_def, dict) and prop_def.get("navigation"):
            csharp_type = parse_csharp_type(prop_def["type"])
            prop_csharp_name = f"{prop_name}Navigation"
        else:
            csharp_type = parse_csharp_type(prop_def)
            prop_csharp_name = prop_name

        lines.append(f"    public {csharp_type} {prop_csharp_name} {{ get; private set; }}")
        lines.append(f"")

        # Generar un constructor para crear y un constructor para updatear
        # ignorar navegaciones
        if isinstance(prop_def, dict) and prop_def.get("navigation"):
            continue
        param_name = prop_csharp_name[0].lower() + prop_csharp_name[1:]
        ctor_params.append(f"{csharp_type} {param_name}")
        assignments.append(f"        {prop_csharp_name} = {param_name};")

    lines.append(f"    public {entity_name} () {{ }}")

    # 3) Constructor público con todos los parámetros
    params_sig = ", ".join(ctor_params)
    lines.append(f"    public {entity_name}({params_sig})")
    lines.append("    {")
    lines.extend(assignments)
    lines.append("    }")
     # 4) Método estático Update<Entity>
    lines.append(f"    public static {entity_name} Update{entity_name}({params_sig})")
    lines.append("    {")
    # argumentos en mismo orden
    args_list = ", ".join(p.split(" ")[1] for p in ctor_params)
    lines.append(f"        return new {entity_name}({args_list});")
    lines.append("    }")

    lines.append("")
    lines.append("}")
    return "\n".join(lines)

def save_entity_file(entities_path, entity_name, content):
    file_path = os.path.join(entities_path, f"{entity_name}.cs")
    create_file(file_path, content)

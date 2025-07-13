import os
from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file
from utilities.services.parser import parse_csharp_type


def generate_create_command(commands_root, service_name, entity_name, props):
    # ——————————————————————————————
    cmd_path = os.path.join(commands_root, f"{entity_name}Command", "Create")
    create_directory(cmd_path)
    command_lines = [
        "using System;",
        "using MediatR;",
        f"namespace {service_name}.Application.Commands.{entity_name}Command.Create",
        "{",
        f"    public class Create{entity_name}Command : IRequest<ErrorOr<Guid>>",
        "    {"
    ]
    for prop_name, prop_def in props.items():
        if prop_name == "Id": continue
        if isinstance(prop_def, dict) and prop_def.get("navigation"):
            continue
        if isinstance(prop_def, dict) and "valueObject" in prop_def:
            base_type = prop_def["type"]
        else:
            base_type = prop_def
        cs_type = parse_csharp_type(base_type)
        command_lines.append(f"        public {cs_type} {prop_name} {{ get; set; }}")
    command_lines += [
        "    }",
        "}"
    ]
    command_content = "\n".join(command_lines)
    create_file(os.path.join(cmd_path, f"Create{entity_name}Command.cs"), command_content)

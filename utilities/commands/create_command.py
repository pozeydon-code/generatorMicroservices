import os
from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file


def generate_create_command_handler(commands_root, service_name, entity_name, props):
    # Directorio handler
    cmd_path = os.path.join(commands_root, entity_name, "Create")
    create_directory(cmd_path)

    # Líneas iniciales
    lines = [
        "using System;",
        "using MediatR;",
        f"using {service_name}.Application.Interfaces;",
        f"using {service_name}.Domain.Entities;",
    ]

    lines += [
        "",
        f"namespace {service_name}.Application.Commands.{entity_name}Command.Create",
        "{",
        f"    public class Create{entity_name}CommandHandler : IRequestHandler<Create{entity_name}Command, Guid>",
        "    {",
        f"        private readonly I{entity_name}Repository _repo;",
        f"        public Create{entity_name}CommandHandler(I{entity_name}Repository repo) => _repo = repo;",
        "",
        f"        public async Task<Guid> Handle(Create{entity_name}Command request, CancellationToken ct)",
        "        {",
    ]

    # 1) Validaciones VO
    for prop_name, prop_def in props.items():
        if prop_name == "Id": continue
        if isinstance(prop_def, dict) and "valueObject" in prop_def:
            vo = prop_def["valueObject"]
            var = prop_name.lower()  # e.g. name, description, email
            lines += [
                f"            if ({vo}.Create(request.{prop_name}) is not {vo} {var})",
                f"                throw new Exception(\"Error de creación de la propiedad {vo}\");",
                ""
            ]

    # 2) Construcción del entity initializer
    init_lines = [f"            var entity = new {entity_name}", "            {", "                Id = Guid.NewGuid(),"]
    assigns = []
    for prop_name, prop_def in props.items():
        if prop_name == "Id": continue
        # ignorar navegaciones
        if isinstance(prop_def, dict) and prop_def.get("navigation"):
            continue
        if isinstance(prop_def, dict) and "valueObject" in prop_def:
            var = prop_name.lower()
            assigns.append(f"                {prop_name} = {var}")
        else:
            assigns.append(f"                {prop_name} = request.{prop_name}")
    init_lines += [",\n".join(assigns)]
    init_lines.append("            };")
    lines += init_lines

    # 3) Guardar y return
    lines += [
        "            await _repo.AddAsync(entity);",
        "            return entity.Id;",
        "        }",
        "    }",
        "}"
    ]

    # Escribir en el archivo
    content = "\n".join(lines)
    create_file(
        os.path.join(cmd_path, f"Create{entity_name}CommandHandler.cs"),
        content
    )

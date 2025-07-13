import os
from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file


def generate_create_command_handler(commands_root, service_name, entity_name, props):
    # Directorio handler
    cmd_path = os.path.join(commands_root, f"{entity_name}Command", "Create")
    create_directory(cmd_path)

    # Líneas iniciales
    lines = [
        "using System;",
        "using MediatR;",
        f"using {service_name}.Application.Interfaces;",
        f"using {service_name}.Domain.Entities;",
        f"using {service_name}.Domain.Primitives;",
    ]

    lines += [
        "",
        f"namespace {service_name}.Application.Commands.{entity_name}Command.Create",
        "{",
        f"    public class Create{entity_name}CommandHandler : IRequestHandler<Create{entity_name}Command, ErrorOr<Guid>>",
        "    {",
        f"        private readonly I{entity_name}Repository _repo;",
        f"        private readonly IUnitOfWork _unitOfWork;",
        f"        public Create{entity_name}CommandHandler(I{entity_name}Repository repo, IUnitOfWork unitOfWork)",
        "        {",
        "            _repo = repo ?? throw new ArgumentNullException(nameof(repo));",
        "            _unitOfWork = unitOfWork ?? throw new ArgumentNullException(nameof(unitOfWork));",
        "        }",
        "",
        f"        public async Task<ErrorOr<Guid>> Handle(Create{entity_name}Command request, CancellationToken ct)",
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
    init_lines = [f"            var entity = new {entity_name}("]
    assigns = []
    for prop_name, prop_def in props.items():
        if prop_name == "Id":
            assigns.append(f"                Guid.NewGuid()")
            continue
        # ignorar navegaciones
        if isinstance(prop_def, dict) and prop_def.get("navigation"):
            continue
        if isinstance(prop_def, dict) and "valueObject" in prop_def:
            var = prop_name.lower()
            assigns.append(f"                {var}")
        else:
            assigns.append(f"                request.{prop_name}")
    init_lines += [",\n".join(assigns)]
    init_lines.append("            );")
    lines += init_lines

    # 3) Guardar y return
    lines += [
        "            await _repo.AddAsync(entity);",
        "            await _unitOfWork.SaveChangesAsync(ct);",
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

import os
from utilities.filesystem.create_file import create_file


def generate_update_command_handler(commands_root, service_name, entity_name, props):
    upd_path = os.path.join(commands_root, f"{entity_name}Command", "Update")

    command_lines = [
        f"using {service_name}.Application.Interfaces;",
        f"using {service_name}.Domain.Entities;",
        f"using {service_name}.Domain.Primitives;",
        f"namespace {service_name}.Application.Commands.{entity_name}Command.Update;",
        "",
        f"public class Update{entity_name}CommandHandler : IRequestHandler<Update{entity_name}Command, ErrorOr<Guid>>",
        "{",
        f"    private readonly I{entity_name}Repository _repo;",
        f"    private readonly IUnitOfWork _unitOfWork;",
        f"    public Update{entity_name}CommandHandler(I{entity_name}Repository repo, IUnitOfWork unitOfWork)",
        "    {",
        "        _repo = repo ?? throw new ArgumentNullException(nameof(repo));",
        "        _unitOfWork = unitOfWork ?? throw new ArgumentNullException(nameof(unitOfWork));",
        "    }",
        "",
        f"    public async Task<ErrorOr<Guid>> Handle(Update{entity_name}Command request, CancellationToken ct)",
        "    {",
        "        if (!await _repo.ExistsAsync(request.Id))",
        "            throw new Exception(\"Not Found\");",
        "",
    ]
        # 1) Validaciones VO
    for prop_name, prop_def in props.items():
        if prop_name == "Id": continue
        if isinstance(prop_def, dict) and "valueObject" in prop_def:
            vo = prop_def["valueObject"]
            var = prop_name.lower()  # e.g. name, description, email
            command_lines += [
                f"            if ({vo}.Create(request.{prop_name}) is not {vo} {var})",
                f"                throw new Exception(\"Error de creación de la propiedad {vo}\");",
                ""
            ]
    # 2) Construcción del entity initializer
    init_lines = [f"            {entity_name} entity = {entity_name}.Update{entity_name}("]
    assigns = []
    for prop_name, prop_def in props.items():
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
    command_lines += init_lines

    command_lines += [
        f"        _repo.UpdateAsync(entity);",
        f"        await _unitOfWork.SaveChangesAsync(ct);",
        f"        return entity.Id;",
        "    }",
        "}"
    ]
    create_file(os.path.join(upd_path, f"Update{entity_name}CommandHandler.cs"), "\n".join(command_lines))

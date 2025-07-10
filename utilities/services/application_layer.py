import os

from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file
from utilities.filesystem.generate_global_usings import generate_global_usings_application
from utilities.services.parser import parse_csharp_type
from utilities.commands.create_command import generate_create_command_handler


def generate_application_layer(base_path, service_name, entities):
    app_base = os.path.join(base_path, "Services", service_name, f"{service_name}.Application")

    dto_path = os.path.join(app_base, "Dtos")
    interfaces_path = os.path.join(app_base, "Interfaces")
    services_path = os.path.join(app_base, "Services")
    commands_root = os.path.join(app_base, "Commands")
    queries_root  = os.path.join(app_base, "Queries")
    create_directory(dto_path)
    create_directory(interfaces_path)
    create_directory(services_path)
    create_directory(commands_root)
    create_directory(queries_root)

    generate_global_usings_application(base_path, service_name)

    for entity_name, props in entities.items():
        generate_dto(service_name, dto_path, entity_name, props)
        generate_interface(service_name, interfaces_path, entity_name)
        generate_service_stub(service_name, services_path, entity_name)
        # ——————————————————————————————
        # 1) CreateCommand & Handler
        cmd_path = os.path.join(commands_root, f"{entity_name}Command", "Create")
        create_directory(cmd_path)
        # 1) Genera primero las líneas de la clase
        command_lines = [
            "using System;",
            "using MediatR;",
            f"namespace {service_name}.Application.Commands.{entity_name}Command.Create",
            "{",
            f"    public class Create{entity_name}Command : IRequest<Guid>",
            "    {"
        ]
        # añade cada propiedad
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

        # 2) Haz el join fuera de la f-string
        command_content = "\n".join(command_lines)

        # 3) Crea el archivo
        create_file(os.path.join(cmd_path, f"Create{entity_name}Command.cs"), command_content)

        generate_create_command_handler(commands_root, service_name, entity_name, props)

        # 2) UpdateCommand & Handler
        upd_path = os.path.join(commands_root, f"{entity_name}Command", "Update")
        create_directory(upd_path)
        # Genera primero las líneas de la clase
        command_lines = [
            "using System;",
            "using MediatR;",
            f"namespace {service_name}.Application.Commands.{entity_name}Command.Update",
            "{",
            f"    public class Update{entity_name}Command : IRequest<Guid>",
            "    {"
        ]

        # añade cada propiedad
        for prop_name, prop_def in props.items():
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

        create_file(os.path.join(upd_path, f"Update{entity_name}Command.cs"), command_content)
        create_file(os.path.join(upd_path, f"Update{entity_name}CommandHandler.cs"), f"""
 using MediatR;
 using {service_name}.Application.Interfaces;
 using {service_name}.Domain.Entities;
 namespace {service_name}.Application.Commands.{entity_name}Command.Update
 {{
     public class Update{entity_name}CommandHandler : IRequestHandler<Update{entity_name}Command, Guid>
     {{
         private readonly I{entity_name}Repository _repo;
         public Update{entity_name}CommandHandler(I{entity_name}Repository repo) => _repo = repo;

         public async Task<Guid> Handle(Update{entity_name}Command request, CancellationToken ct)
         {{
             var entity = await _repo.GetByIdAsync(request.Id);
             // TODO: mapear propiedades de request a entity
             _repo.UpdateAsync(entity);
             return entity.Id;
         }}
     }}
 }}
 """.strip())

        qry_all = os.path.join(queries_root, f"{entity_name}Query", "GetAll")
        create_directory(qry_all)
        create_file(os.path.join(qry_all, f"GetAll{entity_name}Query.cs"), f"""
 using MediatR;
 using System.Collections.Generic;
 using {service_name}.Domain.Entities;
 namespace {service_name}.Application.Queries.{entity_name}Query.GetAll
 {{
     public class GetAll{entity_name}Query : IRequest<IEnumerable<{entity_name}>> {{ }}
 }}
 """.strip())

        create_file(os.path.join(qry_all, f"GetAll{entity_name}QueryHandler.cs"), f"""
 using MediatR;
 using {service_name}.Application.Interfaces;
 namespace {service_name}.Application.Queries.{entity_name}Query.GetAll
 {{
     public class GetAll{entity_name}QueryHandler : IRequestHandler<GetAll{entity_name}Query, IEnumerable<{entity_name}>>
     {{
         private readonly I{entity_name}Repository _repository;
         public GetAll{entity_name}QueryHandler(I{entity_name}Repository repository) => _repository = repository;

         public async Task<IEnumerable<{entity_name}>> Handle(GetAll{entity_name}Query request, CancellationToken ct) =>
             await _repository.GetAllAsync();
     }}
 }}
 """.strip())

        # 4) GetById Query & Handler
        qry_id = os.path.join(queries_root, f"{entity_name}Query", "GetById")
        create_directory(qry_id)
        create_file(os.path.join(qry_id, f"Get{entity_name}ByIdQuery.cs"), f"""
 using MediatR;
 using {service_name}.Domain.Entities;
 namespace {service_name}.Application.Queries.{entity_name}Query.GetById
 {{
     public class Get{entity_name}ByIdQuery : IRequest<{entity_name}?>
     {{
         public Guid Id {{ get; set; }}
     }}
 }}
 """.strip())

        create_file(os.path.join(qry_id, f"Get{entity_name}ByIdQueryHandler.cs"), f"""
 using MediatR;
 using {service_name}.Application.Interfaces;
 namespace {service_name}.Application.Queries.{entity_name}Query.GetById
 {{
     public class Get{entity_name}ByIdQueryHandler : IRequestHandler<Get{entity_name}ByIdQuery, {entity_name}?>
     {{
         private readonly I{entity_name}Repository _repository;
         public Get{entity_name}ByIdQueryHandler(I{entity_name}Repository repository) => _repository = repository;

         public async Task<{entity_name}?> Handle(Get{entity_name}ByIdQuery request, CancellationToken ct){{
             if(await _repository.GetByIdAsync(request.Id) is not {entity_name} {entity_name.lower()})
                return null;
            return {entity_name.lower()};
         }}
     }}
 }}
 """.strip())
def generate_dto(service_name, dto_path, entity_name, props):
    lines = ["using System;",
             f"using {service_name}.Domain.Entities;",
             f"using {service_name}.Domain.ValueObjects;",
             "",
             f"namespace {service_name}.Application.Dtos", "{"]
    lines.append(f"    public class {entity_name}Dto")
    lines.append("    {")
    for prop_name, prop_type in props.items():
        lines.append(f"        public {parse_csharp_type(prop_type)} {prop_name} {{ get; set; }}")
    lines.append("    }")
    lines.append("}")

    create_file(os.path.join(dto_path, f"{entity_name}Dto.cs"), "\n".join(lines))

def generate_interface(service_name, interfaces_path, entity_name):
    lines = [
        "using System;",
        "using System.Collections.Generic;",
        "using System.Threading.Tasks;",
        f"using {service_name}.Domain.Entities;",
        "",
        f"namespace {service_name}.Application.Interfaces;",
        f"public interface I{entity_name}Repository",
        "   {",
        f"      Task<IEnumerable<{entity_name}>> GetAllAsync();",
        f"      Task<{entity_name}?> GetByIdAsync(Guid id);",
        f"      Task AddAsync({entity_name} entity);",
        f"      void UpdateAsync({entity_name} entity);",
        f"      Task DeleteAsync(Guid id);",
        "   }",
    ]
    create_file(os.path.join(interfaces_path, f"I{entity_name}Repository.cs"), "\n".join(lines))

def generate_service_stub(service_name, services_path, entity_name):
    lines = [
        "using System;",
        "using System.Threading.Tasks;",
        f"using {service_name}.Application.Interfaces;",
        f"using {service_name}.Domain.Entities;",
        "",
        f"namespace {service_name}.Application.Services;",
        f"public class {entity_name}Service",
        "{",
        f"  private readonly I{entity_name}Repository _repository;",
        "",
        f"  public {entity_name}Service(I{entity_name}Repository repository)",
        "   {",
        "       _repository = repository;",
        "   }",
        "",
        f"  public async Task CreateAsync({entity_name} entity)",
        "   {",
        "       // Agregar validaciones aquí si se requiere",
        "       await _repository.AddAsync(entity);",
        "   }",
        "}",
    ]
    create_file(os.path.join(services_path, f"{entity_name}Service.cs"), "\n".join(lines))

import os

from utilities.application.dependency_injection import generate_di_application
from utilities.services.parser import parse_csharp_type
from utilities.filesystem.create_file import create_file
from utilities.filesystem.create_directory import create_directory

from utilities.application.idb_context import generate_idb_context
from utilities.application.assembly import generate_assembly_application
from utilities.application.behaviors import generate_behavior_infrastructure
from utilities.filesystem.generate_global_usings import generate_global_usings_application
from utilities.application.commands.create.create_command import generate_create_command
from utilities.application.commands.update.update_command import generate_update_command
from utilities.application.commands.create.create_command_handler import generate_create_command_handler
from utilities.application.commands.update.update_command_handler import generate_update_command_handler


def generate_application_layer(base_path, service_name, entities):
    app_base = os.path.join(base_path, "Services", service_name, f"{service_name}.Application")

    dto_path = os.path.join(app_base, "Dtos")
    interfaces_path = os.path.join(app_base, "Interfaces")
    common_path = os.path.join(app_base, "Common")
    behaviors_path = os.path.join(common_path, "Behaviors")
    services_path = os.path.join(app_base, "Services")
    commands_root = os.path.join(app_base, "Commands")
    queries_root  = os.path.join(app_base, "Queries")
    create_directory(dto_path)
    create_directory(interfaces_path)
    create_directory(services_path)
    create_directory(commands_root)
    create_directory(common_path)
    create_directory(behaviors_path)

    generate_global_usings_application(base_path, service_name)
    generate_behavior_infrastructure(behaviors_path, service_name)
    generate_idb_context(interfaces_path, service_name, entities)
    generate_assembly_application(app_base, service_name)
    generate_di_application(app_base, service_name, entities)
    for entity_name, props in entities.items():
        generate_dto(service_name, dto_path, entity_name, props)
        generate_interface(service_name, interfaces_path, entity_name)
        generate_service_stub(service_name, services_path, entity_name)

        generate_create_command(commands_root, service_name, entity_name, props)
        generate_create_command_handler(commands_root, service_name, entity_name, props)

        generate_update_command(commands_root, service_name, entity_name, props)
        generate_update_command_handler(commands_root, service_name, entity_name, props)

        qry_all = os.path.join(queries_root, f"{entity_name}Query", "GetAll")
        create_directory(qry_all)
        create_file(os.path.join(qry_all, f"GetAll{entity_name}Query.cs"), f"""
 using MediatR;
 using System.Collections.Generic;
 using {service_name}.Domain.Entities;
 namespace {service_name}.Application.Queries.{entity_name}Query.GetAll
 {{
     public class GetAll{entity_name}Query : IRequest<ErrorOr<IReadOnlyList<{entity_name}>>> {{ }}
 }}
 """.strip())

        create_file(os.path.join(qry_all, f"GetAll{entity_name}QueryHandler.cs"), f"""
 using MediatR;
 using {service_name}.Application.Interfaces;
 namespace {service_name}.Application.Queries.{entity_name}Query.GetAll
 {{
     public class GetAll{entity_name}QueryHandler : IRequestHandler<GetAll{entity_name}Query, ErrorOr<IReadOnlyList<{entity_name}>>>
     {{
         private readonly I{entity_name}Repository _repository;
         public GetAll{entity_name}QueryHandler(I{entity_name}Repository repository) => _repository = repository;

         public async Task<ErrorOr<IReadOnlyList<{entity_name}>>> Handle(GetAll{entity_name}Query request, CancellationToken ct) =>
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
     public class Get{entity_name}ByIdQuery : IRequest<ErrorOr<{entity_name}?>>
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
     public class Get{entity_name}ByIdQueryHandler : IRequestHandler<Get{entity_name}ByIdQuery, ErrorOr<{entity_name}?>>
     {{
         private readonly I{entity_name}Repository _repository;
         public Get{entity_name}ByIdQueryHandler(I{entity_name}Repository repository) => _repository = repository;

         public async Task<ErrorOr<{entity_name}?>> Handle(Get{entity_name}ByIdQuery request, CancellationToken ct){{
             if(await _repository.GetByIdAsync(request.Id) is not {entity_name} {entity_name.lower()})
                throw new Exception($"{entity_name} with ID {{request.Id}} not found.");
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
        f"      Task<List<{entity_name}>> GetAllAsync();",
        f"      Task<{entity_name}?> GetByIdAsync(Guid id);",
        f"      Task<bool> ExistsAsync(Guid id);",
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

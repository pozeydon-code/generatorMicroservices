import os

from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file
from utilities.services.parser import parse_csharp_type


def generate_application_layer(base_path, service_name, entities):
    app_base = os.path.join(base_path, "Services", service_name, f"{service_name}.Application")

    dto_path = os.path.join(app_base, "Dtos")
    interfaces_path = os.path.join(app_base, "Interfaces")
    services_path = os.path.join(app_base, "Services")
    create_directory(dto_path)
    create_directory(interfaces_path)
    create_directory(services_path)

    for entity_name, props in entities.items():
        generate_dto(service_name, dto_path, entity_name, props)
        generate_interface(service_name, interfaces_path, entity_name)
        generate_service_stub(service_name, services_path, entity_name)

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

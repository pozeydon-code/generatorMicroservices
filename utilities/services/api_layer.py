# === PASO 5: GENERAR API CONTROLLERS Y CONFIG ===

import os
from utilities.filesystem.generate_global_usings import generate_global_usings
from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file


def generate_api_layer(base_path, service_name, entities):
    api_base = os.path.join(base_path, "Services", service_name, f"{service_name}.API")
    controllers_path = os.path.join(api_base, "Controllers")
    create_directory(controllers_path)
    generate_global_usings(base_path, service_name)
    for entity in entities:
        generate_controller(service_name, entity, controllers_path, entities)

    generate_program_cs(service_name, api_base)

def generate_controller(service_name, entity_name, controllers_path, entities):
    props = entities[entity_name]

    dto_ns = f"{service_name}.API.Controllers"
    cmd_ns = f"{service_name}.Application.Commands.{entity_name}"
    qry_ns = f"{service_name}.Application.Queries.{entity_name}"

    # Detectar relaciones de navegación
    includes = []
    for prop_name, prop_def in props.items():
        if isinstance(prop_def, dict) and prop_def.get("navigation"):
            includes.append(prop_name)

    lines = [
        f"using {service_name}.Application.Commands.{entity_name}Command.Create;",
        f"using {service_name}.Application.Commands.{entity_name}Command.Update;",
        f"using {service_name}.Application.Queries.{entity_name}Query.GetAll;",
        f"using {service_name}.Application.Queries.{entity_name}Query.GetById;",
        "namespace " + dto_ns,
        "{",
        "    [ApiController]",
        f"    [Route(\"api/[controller]\")]",
        f"    public class {entity_name}Controller : ControllerBase",
        "    {",
        "        private readonly IMediator _mediator;",
        "",
        f"        public {entity_name}Controller(IMediator mediator)",
        "        {",
        "            _mediator = mediator;",
        "        }",
        ""
    ]

    # Create
    lines += [
        "        [HttpPost]",
        f"        public async Task<IActionResult> Create([FromBody] Create{entity_name}Command command)",
        "        {",
        "            var id = await _mediator.Send(command);",
        "            return CreatedAtAction(nameof(GetById), new { id }, null);",
        "        }",
        ""
    ]

    # Update
    lines += [
        "        [HttpPut]",
        f"        public async Task<IActionResult> Update([FromBody] Update{entity_name}Command command)",
        "        {",
        "            await _mediator.Send(command);",
        "            return NoContent();",
        "        }",
        ""
    ]

    # GetAll
    lines += [
        "        [HttpGet]",
        f"        public async Task<IActionResult> GetAll()",
        "        {",
        f"            var items = await _mediator.Send(new GetAll{entity_name}Query());",
        "            return Ok(items);",
        "        }",
        ""
    ]

    # GetById
    lines += [
        "        [HttpGet(\"{id}\")]",
        f"        public async Task<IActionResult> GetById(Guid id)",
        "        {",
        f"            var item = await _mediator.Send(new Get{entity_name}ByIdQuery {{ Id = id }});",
        "            if (item == null) return NotFound();",
        "            return Ok(item);",
        "        }"
    ]

    lines += [
        "    }",
        "}"
    ]

    create_file(os.path.join(controllers_path, f"{entity_name}Controller.cs"), "\n".join(lines))


def generate_program_cs(service_name, api_base):
    lines = [
        "using Microsoft.EntityFrameworkCore;",
        "using Microsoft.OpenApi.Models;",
        f"using {service_name}.Infrastructure.DependencyInjection;",
        f"using {service_name}.Infrastructure.Persistence;",
        "",
        "var builder = WebApplication.CreateBuilder(args);",
        "",
        'var connectionString = builder.Configuration.GetConnectionString("SqlServer") ?? "Server=(localdb)\\\\mssqllocaldb;Database=AppDb;Trusted_Connection=True;";',
        f'builder.Services.AddInfrastructure(connectionString);',
        "builder.Services.AddControllers();",
        "builder.Services.AddEndpointsApiExplorer();",
        "// Registrar MediatR",
        "builder.Services.AddMediatR(typeof(Program).Assembly);",
        "builder.Services.AddSwaggerGen(c =>",
        "{",
        f'    c.SwaggerDoc("v1", new OpenApiInfo {{ Title = "{service_name} API", Version = "v1" }});',
        "});",
        "",
        "var app = builder.Build();",
        "",
        "// Ejecutar migraciones y seeder",
        "using (var scope = app.Services.CreateScope())",
        "{",
        "    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();",
        "    await db.Database.MigrateAsync();"
        "}",
        "",
        "app.UseSwagger();",
        "app.UseSwaggerUI();",
        "",
        "app.UseHttpsRedirection();",
        "app.UseAuthorization();",
        "app.MapControllers();",
        "",
        "app.Run();"
    ]

    create_file(os.path.join(api_base, "Program.cs"), "\n".join(lines))

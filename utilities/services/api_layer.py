# === PASO 5: GENERAR API CONTROLLERS Y CONFIG ===

import os
from utilities.api.assembly import generate_assembly_api
from utilities.api.generate_api_controllers import generate_api_base_controller, generate_api_errors_controller
from utilities.api.generate_common import generate_errors, generate_http
from utilities.api.generate_dependency_injection import generate_di_api
from utilities.api.generate_extensions import generate_extensions
from utilities.api.generate_middlewares import generate_middleware_exception_handling
from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file
from utilities.filesystem.generate_global_usings import generate_global_usings_api


def generate_api_layer(base_path, service_name, entities):
    api_base = os.path.join(base_path, "Services", service_name, f"{service_name}.API")
    controllers_path = os.path.join(api_base, "Controllers")
    middleware_path = os.path.join(api_base, "Middlewares")
    extensions_path = os.path.join(api_base, "Extensions")
    common_path = os.path.join(api_base, "Common")
    create_directory(common_path)
    http_path = os.path.join(common_path, "Http")
    error_path = os.path.join(common_path, "Errors")
    generate_middleware_exception_handling(middleware_path, service_name)
    generate_api_base_controller(controllers_path, service_name)
    generate_api_errors_controller(controllers_path, service_name)
    generate_extensions(extensions_path, service_name)
    generate_http(http_path, service_name)
    generate_errors(error_path, service_name)
    generate_di_api(api_base, service_name)
    generate_global_usings_api(api_base)
    generate_assembly_api(api_base, service_name)
    for entity in entities:
        generate_controller(service_name, entity, controllers_path, entities)

    generate_program_cs(service_name, api_base)

def generate_controller(service_name, entity_name, controllers_path, entities):
    props = entities[entity_name]

    controller_ns = f"{service_name}.API.Controllers"
    cmd_ns = f"{service_name}.Application.Commands.{entity_name}"
    qry_ns = f"{service_name}.Application.Queries.{entity_name}"

    # Detectar relaciones de navegación
    includes = []
    for prop_name, prop_def in props.items():
        if isinstance(prop_def, dict) and prop_def.get("navigation"):
            includes.append(prop_name)

    lines = [
        f"using {cmd_ns}Command.Create;",
        f"using {cmd_ns}Command.Update;",
        f"using {qry_ns}Query.GetAll;",
        f"using {qry_ns}Query.GetById;",
        "namespace " + controller_ns,
        "{",
        "    [ApiController]",
        f"    [Route(\"api/[controller]\")]",
        f"    public class {entity_name}Controller : ApiController",
        "    {",
        "        private readonly ISender _mediator;",
        "",
        f"        public {entity_name}Controller(ISender mediator)",
        "        {",
        "            _mediator = mediator ?? throw new ArgumentNullException(nameof(mediator));",
        "        }",
        ""
    ]

    # Create
    lines += [
        "        [HttpPost]",
        f"        public async Task<IActionResult> Create([FromBody] Create{entity_name}Command command)",
        "        {",
        "            var createdResult = await _mediator.Send(command);",
        "            return createdResult.Match(",
        "                created => Ok(created),",
        "                error => Problem(error)",
        "            );",
        "        }",
        ""
    ]

    # Update
    lines += [
        "        [HttpPut]",
        f"        public async Task<IActionResult> Update(Guid id, [FromBody] Update{entity_name}Command command)",
        "        {",
        "            if (command.Id != id)",
        "            {",
        "                List<Error> errors = new()",
        "                {",
        f"                    Error.Validation(\"{entity_name}.UpdateInvalid\", \"The request Id does not match with the url Id.\")",
        "                };",
        "                return Problem(errors);",
        "            }",
        "            var updatedResult = await _mediator.Send(command);",
        "            return updatedResult.Match(",
        "                updated => Ok(updated),",
        "                errors => Problem(errors)",
        "            );",
        "        }",
        ""
    ]

    # Delete
    # lines += [
    #     "        [HttpDelete(\"{id}\")]",
    #     f"        public async Task<IActionResult> Delete(Guid id)",
    #     "        {",
    #     "            var deletedResult = await _mediator.Send(id);",
    #     "            return deletedResult.Match(",
    #     "                deleted => NoContent(),",
    #     "                errors => Problem(errors)",
    #     "            );",
    #     "        }",
    # ]

    # GetAll
    lines += [
        "        [HttpGet]",
        f"        public async Task<IActionResult> GetAll()",
        "        {",
        f"            var itemsResult = await _mediator.Send(new GetAll{entity_name}Query());",
        "",
        "            return itemsResult.Match(",
        "                items => Ok(items),",
        "                errors => Problem(errors)",
        "            );",
        "        }",
        ""
    ]

    # GetById
    lines += [
        "        [HttpGet(\"{id}\")]",
        f"       public async Task<IActionResult> GetById(Guid id)",
        "        {",
        f"            var itemResult = await _mediator.Send(new Get{entity_name}ByIdQuery {{ Id = id }});",
        "",
        "            return itemResult.Match(",
        "                item => Ok(item),",
        "                errors => Problem(errors)",
        "            );",
        "        }"
    ]

    lines += [
        "    }",
        "}"
    ]

    create_file(os.path.join(controllers_path, f"{entity_name}Controller.cs"), "\n".join(lines))


def generate_program_cs(service_name, api_base):
    lines = [
        f"using {service_name}.Application;",
        f"using {service_name}.Infrastructure;",
        f"using {service_name}.API;",
        f"using {service_name}.API.Extensions;",
        f"using {service_name}.API.Middlewares;",
        "using Microsoft.OpenApi.Models;",
        "",
        "var builder = WebApplication.CreateBuilder(args);",
        "",
        f'builder.Services.AddPresentation()',
        "                 .AddInfrastructure(builder.Configuration)",
        "                 .AddApplication();",
        "",
        "builder.Services.AddSwaggerGen(c =>",
        "{",
        f'    c.SwaggerDoc("v1", new OpenApiInfo {{ Title = "{service_name} API", Version = "v1" }});',
        "});",
        "",
        "var app = builder.Build();",
        "// Configure the HTTP request pipeline.",
        "if (app.Environment.IsDevelopment())",
        "{",
        "    app.UseSwagger();",
        "    app.UseSwaggerUI();",
        "    app.ApplyMigrations();",
        "}",
        "",
        "app.UseExceptionHandler(\"/error\");",
        "",
        "app.UseHttpsRedirection();",
        "",
        "app.UseAuthorization();",
        "",
        "app.UseMiddleware<GlobalExceptionHandlingMiddleware>();",
        "",
        "app.MapControllers();",
        "",
        "app.Run();"
    ]

    create_file(os.path.join(api_base, "Program.cs"), "\n".join(lines))

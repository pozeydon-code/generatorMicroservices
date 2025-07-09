# === PASO 5: GENERAR API CONTROLLERS Y CONFIG ===

import os
from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file


def generate_api_layer(base_path, service_name, entities):
    api_base = os.path.join(base_path, "Services", service_name, f"{service_name}.API")
    controllers_path = os.path.join(api_base, "Controllers")
    create_directory(controllers_path)

    for entity in entities:
        generate_controller(service_name, entity, controllers_path, entities)

    generate_program_cs(service_name, api_base)

def generate_controller(service_name, entity_name, controllers_path, entities):
    props = entities[entity_name]

    # Detectar relaciones de navegación
    includes = []
    for prop_name, prop_def in props.items():
        if isinstance(prop_def, dict) and prop_def.get("navigation"):
            includes.append(prop_name)

    lines = [
        "using Microsoft.AspNetCore.Mvc;",
        "using Microsoft.EntityFrameworkCore;",
        f"using {service_name}.Domain.Entities;",
        f"using {service_name}.Application.Interfaces;",
        f"using {service_name}.Infrastructure.Persistence;",
        "",
        f"namespace {service_name}.API.Controllers",
        "{",
        "    [ApiController]",
        f"    [Route(\"api/[controller]\")]",
        f"    public class {entity_name}Controller : ControllerBase",
        "    {",
        f"        private readonly AppDbContext _context;",
        "",
        f"        public {entity_name}Controller(AppDbContext context)",
        "        {",
        "            _context = context;",
        "        }",
        ""
    ]

    # GET ALL
    lines.append("        [HttpGet]")
    getall_line = f"        public async Task<IActionResult> GetAll() => Ok(await _context.{entity_name}s"

    for inc in includes:
        getall_line += f".Include(x => x.{inc}Navigation)"

    getall_line += ".ToListAsync());"
    lines.append(getall_line)
    lines.append("")

    # GET BY ID
    lines.append("        [HttpGet(\"{id}\")]")
    getbyid_line = f"        public async Task<IActionResult> GetById(Guid id) => Ok(await _context.{entity_name}s"

    for inc in includes:
        getbyid_line += f".Include(x => x.{inc}Navigation)"

    getbyid_line += ".FirstOrDefaultAsync(x => x.Id == id));"
    lines.append(getbyid_line)
    lines.append("")

    # POST
    lines.append("        [HttpPost]")
    lines.append(f"        public async Task<IActionResult> Create([FromBody] {entity_name} entity)")
    lines.append("        {")
    lines.append("            await _context.AddAsync(entity);")
    lines.append("            await _context.SaveChangesAsync();")
    lines.append("            return CreatedAtAction(nameof(GetById), new { id = entity.Id }, entity);")
    lines.append("        }")
    lines.append("")

    # PUT
    lines.append("        [HttpPut]")
    lines.append(f"        public async Task<IActionResult> Update([FromBody] {entity_name} entity)")
    lines.append("        {")
    lines.append("            _context.Update(entity);")
    lines.append("            await _context.SaveChangesAsync();")
    lines.append("            return NoContent();")
    lines.append("        }")
    lines.append("")

    # DELETE
    lines.append("        [HttpDelete(\"{id}\")]")
    lines.append(f"        public async Task<IActionResult> Delete(Guid id)")
    lines.append("        {")
    lines.append(f"            var entity = await _context.{entity_name}s.FindAsync(id);")
    lines.append("            if (entity == null) return NotFound();")
    lines.append("            _context.Remove(entity);")
    lines.append("            await _context.SaveChangesAsync();")
    lines.append("            return NoContent();")
    lines.append("        }")

    lines.append("    }")
    lines.append("}")

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


import os
from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file


def generate_infrastructure_layer(base_path, service_name, entities):
    infra_base = os.path.join(base_path, "Services", service_name, f"{service_name}.Infrastructure")
    repo_path = os.path.join(infra_base, "Repositories")
    persistence_path = os.path.join(infra_base, "Persistence")
    di_path = os.path.join(infra_base, "DependencyInjection")
    create_directory(repo_path)
    create_directory(persistence_path)
    create_directory(di_path)

    # Repositorios
    for entity_name in entities:
        generate_repository_impl(service_name, repo_path, entity_name)

    # DbContext
    generate_dbcontext(service_name, persistence_path, entities)

    # DI Extension
    generate_di_extension(service_name, di_path, entities)

def generate_repository_impl(service_name, repo_path, entity_name):
    lines = [
        "using System;",
        "using System.Collections.Generic;",
        "using System.Threading.Tasks;",
        "using Microsoft.EntityFrameworkCore;",
        f"using {service_name}.Domain.Entities;",
        f"using {service_name}.Application.Interfaces;",
        f"using {service_name}.Infrastructure.Persistence;",
        "",
        f"namespace {service_name}.Infrastructure.Repositories;",
        f"public class {entity_name}Repository : I{entity_name}Repository",
        "{",
        f"  private readonly AppDbContext _context;",
        "",
        f"  public {entity_name}Repository(AppDbContext context)",
        "   {",
        "       _context = context;",
        "   }",
        "",
        f"  public async Task<IEnumerable<{entity_name}>> GetAllAsync() => await _context.Set<{entity_name}>().ToListAsync();",
        f"  public async Task<{entity_name}?> GetByIdAsync(Guid id) => await _context.Set<{entity_name}>().FindAsync(id);",
        f"  public async Task AddAsync({entity_name} entity) => await _context.Set<{entity_name}>().AddAsync(entity);",
        f"  public void UpdateAsync({entity_name} entity) => _context.Set<{entity_name}>().Update(entity);",
        f"  public async Task DeleteAsync(Guid id)",
        "   {",
        f"      var entity = await GetByIdAsync(id);",
        "       if (entity != null)",
        "           _context.Set<{0}>().Remove(entity);".format(entity_name),
        "   }",
        "}",
    ]
    create_file(os.path.join(repo_path, f"{entity_name}Repository.cs"), "\n".join(lines))

def generate_dbcontext(service_name, persistence_path, entities):
    lines = [
        "using Microsoft.EntityFrameworkCore;",
        f"using {service_name}.Domain.Entities;",
        "",
        f"namespace {service_name}.Infrastructure.Persistence",
        "{",
        "    public class AppDbContext : DbContext",
        "    {",
        "        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }",
        ""
    ]

    for entity in entities:
        lines.append(f"        public DbSet<{entity}> {entity}s {{ get; set; }}")
    lines.append("")
    lines.append("        protected override void OnModelCreating(ModelBuilder modelBuilder)")
    lines.append("        {")
    lines.append("            base.OnModelCreating(modelBuilder);")
    lines.append("            modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);")
    lines.append("        }")

    lines.append("    }")
    lines.append("}")

    create_file(os.path.join(persistence_path, "AppDbContext.cs"), "\n".join(lines))


def generate_di_extension(service_name, di_path, entities):
    lines = [
        "using Microsoft.Extensions.DependencyInjection;",
        "using Microsoft.EntityFrameworkCore;",
        f"using {service_name}.Application.Interfaces;",
        f"using {service_name}.Infrastructure.Repositories;",
        f"using {service_name}.Infrastructure.Persistence;",
        "",
        f"namespace {service_name}.Infrastructure.DependencyInjection",
        "{",
        "    public static class DependencyInjection",
        "    {",
        "        public static IServiceCollection AddInfrastructure(this IServiceCollection services, string connectionString)",
        "        {",
        '            services.AddDbContext<AppDbContext>(options => options.UseSqlServer(connectionString));'
    ]
    for entity in entities:
        lines.append(f"            services.AddScoped<I{entity}Repository, {entity}Repository>();")
    lines.append("            return services;")
    lines.append("        }")
    lines.append("    }")
    lines.append("}")

    create_file(os.path.join(di_path, "DependencyInjection.cs"), "\n".join(lines))

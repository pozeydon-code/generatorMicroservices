import os
from utilities.filesystem.create_file import create_file


def generate_di_infrastructure(service_name, di_path, entities):
    lines = [
        "using Microsoft.Extensions.DependencyInjection;",
        "using Microsoft.EntityFrameworkCore;",
        "using Microsoft.Extensions.Configuration;",
        f"using {service_name}.Application.Interfaces;",
        f"using {service_name}.Infrastructure.Repositories;",
        f"using {service_name}.Infrastructure.Persistence;",
        f"using {service_name}.Domain.Primitives;",
        "",
        f"namespace {service_name}.Infrastructure;",
        "public static class DependencyInjection",
        "{",
        "    public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)",
        "    {",
        '        services.AddPersistence(configuration);',
        '        return services;',
        '    }',
        '',
        '    public static IServiceCollection AddPersistence(this IServiceCollection services, IConfiguration configuration)',
        "    {",
        "        services.AddDbContext<AppDbContext>(options =>",
        "            options.UseSqlServer(configuration.GetConnectionString(\"SqlServer\")));",
        "",
        "        // Registrar repositorios",
        "        services.AddScoped<IAppDbContext>(sp => sp.GetRequiredService<AppDbContext>());",
        "",
        "        services.AddScoped<IUnitOfWork>(sp => sp.GetRequiredService<AppDbContext>());",
    ]
    for entity in entities:
        lines.append(f"        services.AddScoped<I{entity}Repository, {entity}Repository>();")
    lines.append("        return services;")
    lines.append("    }")
    lines.append("}")

    create_file(os.path.join(di_path, "DependencyInjection.cs"), "\n".join(lines))

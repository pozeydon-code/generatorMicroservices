import os

from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file


def generate_extensions(extensions_path, service_name):
    create_directory(extensions_path)
    lines = [
        f"using {service_name}.Infrastructure.Persistence;",
        "using Microsoft.EntityFrameworkCore;",
        "",
        f"namespace {service_name}.API.Extensions;",
        "public static class MigrationExtensions",
        "{",
        "    public static void ApplyMigrations(this WebApplication app)",
        "    {",
        "        using var scope = app.Services.CreateScope();",
        "        var dbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();",
        "        dbContext.Database.Migrate();",
        "    }",
        "}",
    ]
    create_file(os.path.join(extensions_path, "MigrationExtensions.cs"), "\n".join(lines))

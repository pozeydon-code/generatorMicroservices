import os

from utilities.filesystem.create_file import create_file


def generate_idb_context(interfaces_path, service_name, entities):
    lines = [
        f"namespace {service_name}.Application.Interfaces;",
        "public interface IAppDbContext",
        "{",
        '',
    ]

    for entity in entities:
        lines.append(f"    public DbSet<{entity}> {entity}s {{ get; set; }}")

    lines.append(f"    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);")
    lines.append("}")

    create_file(os.path.join(interfaces_path, "IAppDbContext.cs"), "\n".join(lines))

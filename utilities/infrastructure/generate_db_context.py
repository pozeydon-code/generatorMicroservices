import os
from utilities.filesystem.create_file import create_file


def generate_dbcontext(service_name, persistence_path, entities):
    lines = [
        "using Microsoft.EntityFrameworkCore;",
        f"using {service_name}.Domain.Entities;",
        f"using {service_name}.Domain.Primitives;",
        f"using {service_name}.Application.Interfaces;",
        "",
        f"namespace {service_name}.Infrastructure.Persistence;",
        "public class AppDbContext : DbContext, IAppDbContext, IUnitOfWork",
        "{",
        "    private readonly IPublisher _publisher;",
        "    public AppDbContext(DbContextOptions options, IPublisher publisher) : base(options)",
        "    {",
        "        _publisher = publisher ?? throw new ArgumentNullException(nameof(publisher));",
        "    }"
    ]

    for entity in entities:
        lines.append(f"    public DbSet<{entity}> {entity}s {{ get; set; }}")
    lines.append("")
    lines.append("    protected override void OnModelCreating(ModelBuilder modelBuilder)")
    lines.append("    {")
    lines.append("        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);")
    lines.append("    }")
    lines.append("")
    lines.append("    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = new CancellationToken())")
    lines.append("    {")
    lines.append("        var domainEvents = ChangeTracker.Entries<AggregateRoot>()")
    lines.append("                                        .Select(e => e.Entity)")
    lines.append("                                        .Where(e => e.GetDomainEvents().Any())")
    lines.append("                                        .SelectMany(e => e.GetDomainEvents());")
    lines.append("")
    lines.append("        var result = await base.SaveChangesAsync(cancellationToken);")
    lines.append("")
    lines.append("        foreach (var domainEvent in domainEvents)")
    lines.append("        {")
    lines.append("            await _publisher.Publish(domainEvent, cancellationToken);")
    lines.append("        }")
    lines.append("")
    lines.append("        return result;")
    lines.append("    }")
    lines.append("}")

    create_file(os.path.join(persistence_path, "AppDbContext.cs"), "\n".join(lines))

import os
from utilities.filesystem.create_file import create_file


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
        f"  public async Task<List<{entity_name}>> GetAllAsync() => await _context.Set<{entity_name}>().ToListAsync();",
        f"  public async Task<{entity_name}?> GetByIdAsync(Guid id) => await _context.Set<{entity_name}>().SingleOrDefaultAsync(e => e.Id == id);",
        f"  public async Task<bool> ExistsAsync(Guid id) => await _context.Set<{entity_name}>().AnyAsync(e => e.Id == id);",
        f"  public async Task AddAsync({entity_name} entity) => await _context.Set<{entity_name}>().AddAsync(entity);",
        f"  public void UpdateAsync({entity_name} entity) => _context.Set<{entity_name}>().Update(entity);",
        f"  public async Task DeleteAsync(Guid id)",
        "   {",
        f"      var entity = await GetByIdAsync(id);",
        "       if (entity != null)",
        f"           _context.Set<{entity_name}>().Remove(entity);",
        "   }",
        "}",
    ]
    create_file(os.path.join(repo_path, f"{entity_name}Repository.cs"), "\n".join(lines))

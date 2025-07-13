import os

from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file


def generate_primitives(base_path, service_name):
    primitives_path = os.path.join(base_path, "Services", service_name, f"{service_name}.Domain", "Primitives")
    create_directory(primitives_path)
    generate_aggregate_root(primitives_path, service_name)
    generate_domain_event(primitives_path, service_name)
    generate_uow(primitives_path, service_name)

def generate_aggregate_root(primitives_path, service_name):
    lines = [
        f"namespace {service_name}.Domain.Primitives;",
        "",
        f"public abstract class AggregateRoot",
        "{",
        "   private readonly List<DomainEvent> _domainEvents = new();",
        "",
        "   public ICollection<DomainEvent> GetDomainEvents() => _domainEvents;",
        "",
        "   protected void Raise(DomainEvent domainEvent)",
        "   {",
        "       _domainEvents.Add(domainEvent);",
        "   }",
        "}",
    ]

    create_file(os.path.join(primitives_path, "AggregateRoot.cs"), "\n".join(lines))

def generate_domain_event(primitives_path, service_name):
    lines = [
        f"namespace {service_name}.Domain.Primitives;",
        "",
        f"public record DomainEvent(Guid Id) : INotification;",
    ]

    create_file(os.path.join(primitives_path, "DomainEvent.cs"), "\n".join(lines))

def generate_uow(primitives_path, service_name):
    lines = [
        f"namespace {service_name}.Domain.Primitives;",
        "",
        f"public interface IUnitOfWork",
        "{",
        "   Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);",
        "}",
    ]

    create_file(os.path.join(primitives_path, "UnitOfWork.cs"), "\n".join(lines))

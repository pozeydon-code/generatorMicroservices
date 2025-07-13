import os
from utilities.filesystem.create_file import create_file


def generate_behavior_infrastructure(behaviors_path, service_name):
    lines = [
        f"namespace {service_name}.Application.Common.Behaviors;",
        "public class ValidationBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>",
        "where TRequest : IRequest<TResponse>",
        "where TResponse : IErrorOr",
        "{",
        "    private readonly IValidator<TRequest>? _validator;",
        "    public ValidationBehavior(IValidator<TRequest>? validator = null)",
        "    {",
        "        _validator = validator;",
        "    }",
        '',
        "    public async Task<TResponse> Handle(",
        "        TRequest request,",
        "        RequestHandlerDelegate<TResponse> next,",
        "        CancellationToken cancellationToken)",
        "    {",
        "        if (_validator is null)",
        "            return await next();",
        "",
        "        var validatorResult = await _validator.ValidateAsync(request, cancellationToken);",
        "",
        "        if (validatorResult.IsValid)",
        "            return await next();",
        "",
        "        var errors = validatorResult.Errors",
        "            .ConvertAll(validationFailure => Error.Validation(",
        "                validationFailure.PropertyName,",
        "                validationFailure.ErrorMessage",
        "            ));",

        "        return (dynamic)errors;",
        "    }"
        "}"
    ]


    create_file(os.path.join(behaviors_path, "ValidationBehavior.cs"), "\n".join(lines))

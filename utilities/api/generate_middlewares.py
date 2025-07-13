import os

from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file


def generate_middleware_exception_handling(middleware_path, service_name):
    create_directory(middleware_path)
    lines = [
        "using System.Net;",
        "using System.Text.Json;",
        "",
        f"namespace {service_name}.API.Middlewares;",
        "public class GlobalExceptionHandlingMiddleware : IMiddleware",
        "{",
        "    ILogger<GlobalExceptionHandlingMiddleware> _logger;",
        "",
        "    public GlobalExceptionHandlingMiddleware(ILogger<GlobalExceptionHandlingMiddleware> logger) => _logger = logger;",
        "",
        "    public async Task InvokeAsync(HttpContext context, RequestDelegate next)",
        "    {",
        "        try",
        "        {",
        "            await next(context);",
        "        }",
        "        catch (Exception ex)",
        "        {",
        "             _logger.LogError(ex, ex.Message);",
        "",
        "            context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;",
        "",
        "            ProblemDetails problem = new()",
        "            {",
        "                Status = (int)HttpStatusCode.InternalServerError,",
        "                Type = \"Server Error\",",
        "                Title = \"Server Error\",",
        "                Detail = \"An internal server has occurred.\"",
        "            };",
        "",
        "            string json = JsonSerializer.Serialize(problem);",
        "            context.Response.ContentType = \"application/json\";",
        "            await context.Response.WriteAsync(json);",
        "        }",
        "    }",
        "}",
    ]
    create_file(os.path.join(middleware_path, "GlobalExceptionHandlingMiddleware.cs"), "\n".join(lines))

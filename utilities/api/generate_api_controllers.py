import os
from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file


def generate_api_base_controller(controller_path, service_name):

    lines = [
        "using Microsoft.AspNetCore.Mvc.ModelBinding;",
        f"using {service_name}.API.Common.Errors;",
        "",
        f"namespace {service_name}.API.Controllers;",
        "[ApiController]",
        f"[Route(\"api/v1\")]",
        "public class ApiController : ControllerBase",
        "{",
        "    protected IActionResult Problem(List<Error> errors)"
        "    {",
        "        if(errors.Count is 0)",
        "        {",
        "            return Problem();",
        "        }",
        "",
        "        if(errors.All(error => error.Type == ErrorType.Validation))",
        "        {",
        "            return ValidationProblem(errors);",
        "        }",
        "",
        "        HttpContext.Items[HttpContextItemKeys.Errors] = errors;",
        "        return Problem(errors[0]);",
        "    }",
        "",
        "    protected IActionResult Problem(Error error)"
        "    {",
        "       var statusCode = error.Type switch",
        "       {",
        "           ErrorType.Conflict => StatusCodes.Status409Conflict,",
        "           ErrorType.Validation => StatusCodes.Status400BadRequest,",
        "           ErrorType.NotFound => StatusCodes.Status404NotFound,",
        "           _ => StatusCodes.Status500InternalServerError,",
        "       };",
        "",
        "       return Problem(statusCode: statusCode, title: error.Description);",
        "    }",
        "",
        "    protected IActionResult ValidationProblem(List<Error> errors)"
        "    {",
        "        var modelStateDictionary = new ModelStateDictionary();",
        "",
        "        foreach (var error in errors)",
        "        {",
        "            modelStateDictionary.AddModelError(error.Code, error.Description);",
        "        }",
        "",
        "        return ValidationProblem(modelStateDictionary);",
        "    }",
        "}",
    ]
    create_file(os.path.join(controller_path, "ApiController.cs"), "\n".join(lines))

def generate_api_errors_controller(controller_path, service_name):
    create_directory(controller_path)
    lines = [
        "using Microsoft.AspNetCore.Diagnostics;",
        f"using Microsoft.AspNetCore.Mvc;",
        "",
        f"namespace {service_name}.API.Controllers;",
        f"[Route(\"api/v1/[controller]\")]",
        "public class ErrorController : ControllerBase",
        "{",
        "    [ApiExplorerSettings(IgnoreApi = true)]",
        "    [Route(\"/error\")]",
        "    public IActionResult Error()",
        "    {",
        "        Exception? exception = HttpContext.Features.Get<IExceptionHandlerFeature>()?.Error;",
        "        return Problem();",
        "    }",
        "}",
    ]
    create_file(os.path.join(controller_path, "ErrorsController.cs"), "\n".join(lines))

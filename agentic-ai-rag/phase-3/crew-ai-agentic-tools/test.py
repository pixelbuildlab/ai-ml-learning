# from tools import BaseTool
# from jsonschema import validate, ValidationError
# from pydantic import BaseModel


# class SchemaValidatorInput(BaseModel):
#     data: dict
#     schema: dict


# class SchemaValidatorTool(BaseTool):
#     name: str = "validate_json_schema"
#     description: str = (
#         "Validates JSON data against a JSON Schema. "
#         "Returns whether the data is valid."
#     )
#     args_schema = SchemaValidatorInput

#     def _run(self, data: dict, schema: dict) -> str:
#         try:
#             validate(instance=data, schema=schema)
#             return "VALID"
#         except ValidationError as e:
#             return f"INVALID: {e.message}"

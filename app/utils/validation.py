from app.exceptions import ValidationError


def validate_required_fields(payload: dict, required: list):
    missing = [field for field in required if payload.get(field) in (None, "")]
    if missing:
        raise ValidationError(
            f"Campos obrigatorios ausentes: {', '.join(missing)}",
            fields={f: "required" for f in missing},
        )
    return payload


def validate_schema(payload: dict, schema_callable):
    """
    schema_callable deve receber dict e retornar dict validado
    ou lançar ValidationError.
    """
    try:
        return schema_callable(payload)
    except ValidationError:
        raise
    except Exception as exc:  # fallback generico
        raise ValidationError(str(exc))

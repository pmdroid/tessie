from arcade_tdk.errors import ToolExecutionError


def validate_vin(vin: str) -> bool:
    if not vin:
        raise ToolExecutionError(
            message="VIN cannot be empty",
            developer_message="VIN parameter is required"
        )
    
    vin = vin.strip().upper()
    if len(vin) != 17:
        raise ToolExecutionError(
            message=f"VIN must be exactly 17 characters, got {len(vin)}",
            developer_message=f"Invalid VIN length: '{vin}'"
        )
    
    return True
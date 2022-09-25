from src.sockets.hardware_namespace import hardware_devices


def find_socket_id_by_device_id(device_id: str) -> str | None:
    """
    Find socket id by device id.

    Args:
        device_id (str): Device id.

    Returns:
        str | None: Socket id.
    """
    return hardware_devices.get(device_id)

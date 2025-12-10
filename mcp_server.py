from multiprocessing.resource_sharer import DupFd

from mcp.server.fastmcp import FastMCP
import subprocess
from dataclasses import dataclass


mcp = FastMCP("Tools Server")
DEFAULT_IP = "192.168.1.201"

@dataclass
class LightState:
    """ Tracks the state of an LED. Defaults are the default on state"""
    on_or_off: str = "on"
    cct: bool = True
    brightness: int = 100
    color: tuple[int, int, int] = (0, 0, 0)

@mcp.tool()
def get_light_state() -> LightState:
    """
    Get the state of the (LED) lights

    Returns:

    """
    # Found the cmd line operation worked better than the library calls...
    cmd = f'flux_led --info {DEFAULT_IP}'
    result = str(subprocess.check_output(cmd, shell=True))
    # Extract required data
    on_or_off = "on" if " ON " in result else "off"
    cct = True if "[CCT:" in result else False
    brightness = 100
    if "Brightness:" in result:
        brightness = int(result.split("Brightness: ")[1][:3].replace("%", "").strip())
    color = (0, 0, 0)
    if "[Color:" in result:
        color = tuple([int(x) for x in result.split("[Color: (")[1].split(")")[0].split(",")])
    return LightState(on_or_off, cct, brightness, color)


if __name__ == "__main__":
    mcp.run()

from collections.abc import Iterable
from typing import Any

from app.models import Datacenter
from remnawave import RemnawaveSDK

from app.services import WGDashboardClient


def create_datacenters_clients(
    datacenters: Iterable[Datacenter],
) -> dict[int, dict[str, Any]]:
    datacenter_clients: dict[int, dict[str, Any]] = {}

    for datacenter in datacenters:
        clients: dict[str, Any] = {}

        if datacenter.remnawave_supported:
            clients["remnawave_client"] = RemnawaveSDK(
                base_url=datacenter.remnawave_url,
                token=datacenter.remnawave_token,
            )
            clients["remnawave_internal_squad"] = datacenter.remnawave_internal_squad

        if datacenter.amnezia_supported:
            clients["amnezia_supported"] = True
            clients["amnezia_interface"] = datacenter.amnezia_interface

        if datacenter.wireguard_supported:
            clients["wireguard_supported"] = True
            clients["wireguard_interface"] = datacenter.wireguard_interface

        if datacenter.wireguard_supported or datacenter.amnezia_supported:
            clients["wgdashboard_client"] = WGDashboardClient(
                base_url=datacenter.wgdashboard_url,
                api_key=datacenter.wgdashboard_token,
            )

        datacenter_clients[datacenter.id] = clients

    return datacenter_clients
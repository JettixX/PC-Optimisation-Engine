from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class CPU:
    id: str
    manufacturer: str
    model: str
    socket: str
    cores: int
    threads: int
    base_clock_ghz: float
    boost_clock_ghz: float
    tdp_w: int
    integrated_graphics: bool
    price: Optional[float] = None

    @classmethod
    def from_opendb(cls, data: dict) -> "CPU":
        cores = data.get("cores", {})
        clocks = data.get("clocks", {})
        performance_clocks = clocks.get("performance", {})
        specifications = data.get("specifications", {})
        integrated_graphics = specifications.get("integratedGraphics")

        return cls(
            id=str(data.get("opendb_id", "")),
            manufacturer=data.get("metadata", {}).get(
                "manufacturer", "Unknown"
            ),
            model=data.get("metadata", {}).get(
                "name", "Unknown"
            ),
            socket=data.get("socket", "Unknown"),
            cores=int(cores.get("total", 0)),
            threads=int(cores.get("threads", 0)),
            base_clock_ghz=float(
                performance_clocks.get("base", 0.0)
            ),
            boost_clock_ghz=float(
                performance_clocks.get("boost", 0.0)
            ),
            tdp_w=int(specifications.get("tdp", 0)),
            integrated_graphics=integrated_graphics is not None,
        )


@dataclass
class Motherboard:
    id: str
    manufacturer: str
    model: str
    socket: str
    form_factor: str
    memory_type: str
    memory_slots: int
    max_memory_gb: int
    power_connectors: dict[str, str | list[str]] ## dictionary with values being strings or lists
    m2_slots: List[dict]
    storage_devices: List[str]
    pcie_slots: List[dict]
    wifi: bool
    price: Optional[float] = None

    @classmethod
    def from_opendb(cls, data: dict) -> "Motherboard":
        memory = data.get("memory", {})

        # OpenDB represents M.2 slots as a list of slot definitions.
        m2_slots = data.get("m2_slots", [])

        return cls(
            id=str(data.get("opendb_id", "")),
            manufacturer=data.get("metadata", {}).get(
                "manufacturer", "Unknown"
            ),
            model=data.get("metadata", {}).get(
                "name", "Unknown"
            ),
            socket=data.get("socket", "Unknown"),
            form_factor=data.get("form_factor", "Unknown"),
            memory_type=memory.get("ram_type", "Unknown"),
            memory_slots=int(memory.get("slots", 0)),
            max_memory_gb=int(memory.get("max", 0)),
            power_connectors=data.get("power_connectors", ),
            m2_slots=m2_slots,
            storage_devices=data.get("storage_devices", "Unknown"),
            pcie_slots=data.get("pcie_slots", []),
            wifi=_has_wifi(data),
        )


@dataclass
class GPU:
    id: str
    manufacturer: str
    model: str
    vram_gb: int
    length_mm: float
    tdp_w: int
    total_slot_width: int
    power_connectors: dict[str, int]
    performance_score: Optional[float] = None
    price: Optional[float] = None

    @classmethod
    def from_opendb(cls, data: dict) -> "GPU":
        return cls(
            id=str(data.get("opendb_id", "")),
            manufacturer=data.get("metadata", {}).get(
                "manufacturer", "Unknown"
            ),
            model=data.get("metadata", {}).get(
                "name", "Unknown"
            ),
            vram_gb=int(data.get("memory", 0)),
            length_mm=float(data.get("length", 0)),
            tdp_w=int(data.get("tdp", 0)),
            total_slot_width=int(data.get("total_slot_width", 0)),
            power_connectors=data.get("power_connectors", {}),
            performance_score=None,
        )


@dataclass
class RAM:
    id: str
    manufacturer: str
    model: str
    memory_type: str
    speed_mt_s: int
    capacity_gb: int
    modules: int
    module_capacity_gb: int
    cas_latency: int
    rgb: bool
    price: Optional[float] = None

    @classmethod
    def from_opendb(cls, data: dict) -> "RAM":
        modules = data.get("modules", {})

        return cls(
            id=str(data.get("opendb_id", "")),
            manufacturer=data.get("metadata", {}).get(
                "manufacturer", "Unknown"
            ),
            model=data.get("metadata", {}).get(
                "name", "Unknown"
            ),
            memory_type=data.get("ram_type", "Unknown"),
            speed_mt_s=int(data.get("speed", 0)),
            capacity_gb=int(data.get("capacity", 0)),
            modules=int(modules.get("quantity", 0)),
            module_capacity_gb=int(
                modules.get("capacity_gb", 0)
            ),
            cas_latency=int(data.get("cas_latency", 0)),
            rgb=bool(data.get("rgb", False)),
        )


@dataclass
class STORAGE:
    id: str
    manufacturer: str
    model: str
    capacity_gb: int
    storage_type: str
    form_factor: str
    interface: str
    nvme: bool
    price: Optional[float] = None

    @classmethod
    def from_opendb(cls, data: dict) -> "STORAGE":
        return cls(
            id=str(data.get("opendb_id", "")),
            manufacturer=data.get("metadata", {}).get(
                "manufacturer", "Unknown"
            ),
            model=data.get("metadata", {}).get(
                "name", "Unknown"
            ),
            capacity_gb=int(data.get("capacity", 0)),
            storage_type=data.get(
                "storage_type",
                data.get("type", "Unknown")
            ),
            form_factor=data.get("form_factor", "Unknown"),
            interface=data.get("interface", "Unknown"),
            nvme=bool(data.get("nvme", False)),
        )


@dataclass
class PSU:
    id: str
    manufacturer: str
    model: str
    wattage_w: int
    form_factor: str
    efficiency_rating: str
    modular: str
    length_mm: str
    connectors: dict[str, int]
    price: Optional[float] = None

    @classmethod
    def from_opendb(cls, data: dict) -> "PSU":
        return cls(
            id=str(data.get("opendb_id", "")),
            manufacturer=data.get("metadata", {}).get(
                "manufacturer", "Unknown"
            ),
            model=data.get("metadata", {}).get(
                "name", "Unknown"
            ),
            wattage_w=int(data.get("wattage", 0)),
            form_factor=data.get("form_factor", "Unknown"),
            efficiency_rating=data.get(
                "efficiency_rating", "Unknown"
            ),
            modular=data.get("modular", "Unknown"),
            length_mm=data.get("length", "Unknown"),
            connectors=data.get("connectors", {}),
        )


@dataclass
class CASE:
    id: str
    manufacturer: str
    model: str
    form_factor: str
    expansion_slots: int
    supported_motherboard_form_factors: List[str]
    supported_power_supply_form_factors: List[str]
    supports_rear_connecting_motherboard: bool
    max_gpu_length_mm: Optional[float]
    max_cpu_cooler_height_mm: Optional[float]
    max_psu_length_mm: Optional[float]
    price: Optional[float] = None

    @classmethod
    def from_opendb(cls, data: dict) -> "CASE":
        return cls(
            id=str(data.get("opendb_id", "")),
            manufacturer=data.get("metadata", {}).get(
                "manufacturer", "Unknown"
            ),
            model=data.get("metadata", {}).get(
                "name", "Unknown"
            ),
            form_factor=data.get("form_factor", "Unknown"),
            expansion_slots=int(data.get("expansion_slots", 0)),
            supported_motherboard_form_factors=data.get(
                "supported_motherboard_form_factors", []
            ),
            supported_power_supply_form_factors=data.get("supported_power_supply_form_factors", []),
            supports_rear_connecting_motherboard=data.get("supports_rear_connecting_motherboard", "Unknown"),
            max_gpu_length_mm=_optional_float(
                data.get("max_video_card_length")
            ),
            max_cpu_cooler_height_mm=_optional_float(
                data.get("max_cpu_cooler_height")
            ),
            max_psu_length_mm=_optional_float(
                data.get("max_psu_length")
            ),
        )


@dataclass
class COOLER:
    id: str
    manufacturer: str
    model: str
    cpu_sockets: List[str]
    water_cooled: bool
    radiator_size_mm: Optional[int]
    fan_size_mm: Optional[int]
    fan_quantity: Optional[int]
    height_mm: Optional[float]
    price: Optional[float] = None

    @classmethod
    def from_opendb(cls, data: dict) -> "COOLER":
        return cls(
            id=str(data.get("opendb_id", "")),
            manufacturer=data.get("metadata", {}).get(
                "manufacturer", "Unknown"
            ),
            model=data.get("metadata", {}).get(
                "name", "Unknown"
            ),
            cpu_sockets=data.get("cpu_sockets", []),
            water_cooled=bool(data.get("water_cooled", False)),
            radiator_size_mm=_optional_int(
                data.get("radiator_size")
            ),
            fan_size_mm=_optional_int(
                data.get("fan_size")
            ),
            fan_quantity=_optional_int(
                data.get("fan_quantity")
            ),
            height_mm=_optional_float(
                data.get("height")
            ),
        )


def _optional_int(value) -> Optional[int]:
    if value is None:
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _optional_float(value) -> Optional[float]:
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _has_wifi(data: dict) -> bool:
    """
    OpenDB fields can vary between records/versions.
    We therefore check common wireless-related fields
    rather than assuming one exact representation.
    """
    candidates = [
        data.get("wifi"),
        data.get("wireless"),
        data.get("onboard_wifi"),
        data.get("onboard_wireless"),
    ]

    for value in candidates:
        if value is True:
            return True

    return False
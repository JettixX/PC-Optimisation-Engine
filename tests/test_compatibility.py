from src.models.components import CPU, Motherboard
from src.compatibility.rules import cpuMoboCompatibility


def testCpuMoboCompatibility():
    cpu = CPU(
        id = "testCpu",
        manufacturer = "AMD",
        socket = "AM5",
        cores = 8,
        threads = 16,
        tdp = 120,
        price = 300,
    )

    mobo = Motherboard(
        id = "testMobo",
        manufacturer = "ASRock",
        model = "Test Board 3000",
        socket = "AM5",
        formFactor = "ATX",
        memoryType = "DDR5",
        m2Slots = "2",
        wifi = True,
        price = 150,
    )

    assert testCpuMoboCompatibility(cpu, mobo)


def testBadCpuMoboCompatibility():
    cpu = CPU(
        id = "testCpu",
        manufacturer = "AMD",
        socket = "AM4",
        cores = 8,
        threads = 16,
        tdp = 120,
        price = 300,
    )

    mobo = Motherboard(
        id = "testMobo",
        manufacturer = "ASRock",
        model = "Test Board 3000",
        socket = "AM5",
        formFactor = "ATX",
        memoryType = "DDR5",
        m2Slots = "2",
        wifi = True,
        price = 150,
    )

    assert not testCpuMoboCompatibility(cpu, mobo)
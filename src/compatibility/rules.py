from PCOptimisationEngine.src.models.components import CPU, MOTHERBOARD, RAM, CASE, COOLER, STORAGE, PSU, GPU

## CPU <-> MOBO
def cpu_mobo_compatibility(
        cpu: CPU,
        mobo: MOTHERBOARD
) -> bool:
    return cpu.socket == mobo.socket

## MOBO <-> RAM

def mobo_ram_compatibility(
        mobo: MOTHERBOARD,
        ram: RAM
) -> bool: ## RAM speed PCIe lane discrepancies will be shown to user in the optimisation stage.
    return (mobo.memory_type == ram.memory_type) and (mobo.memory_slots >= ram.modules) and (mobo.max_memory_gb >= ram.capacity_gb)

## MOBO <-> CASE

def mobo_case_compatibility(
        mobo: MOTHERBOARD,
        case: CASE
) -> bool:
    return mobo.form_factor in case.supported_motherboard_form_factors
# rear facing motherboards will be added later

## GPU <-> CASE

def case_gpu_compatibility(
        case: CASE,
        gpu: GPU
) -> bool:
    return (case.maxGpuLengthMm >= gpu.lengthMm) and (case.expansion_slots >= gpu.total_slot_width)

## CASE <-> COOLER

def cooler_case_compatibility( ## combine aio, air, water into one function
        cooler: COOLER,
        case: CASE
) -> bool:
    return cooler.height_mm <= case.max_cpu_cooler_height_mm

#def aio_case_compatibility( ## will be implemented after supported_radiator_sizes is found in db
#        aio: COOLER,
#        case: CASE
#) -> bool:
#    return aio.radiator_size_mm == case.supported_radiator_sizes

## COOLER <-> CPU
def cooler_cpu_compatibility(
        cooler: COOLER,
        cpu: CPU
) -> bool:
    return cpu.socket in cooler.cpu_sockets #cpu_sockets is a list of supported sockets

## GPU <-> MOBO ## Will be completed after data normalisation - PCIe lane width is not normalised (PCIe 5.0 x16/PCIe x16 are the same)
#def gpu_mobo_compatibility(
#        gpu: GPU,
#        mobo: MOTHERBOARD
#) -> bool:
#    mobo.

## GPU <-> PSU needs fixing
def gpu_psu_compatibility(
        gpu: GPU,
        psu: PSU
) -> bool:
    for i in range (0, len(gpu.power_connectors)):
        for j in range (0, len(psu.connectors)):
                if (gpu.power_connectors[i].upper() == psu.connectors[j].upper() and gpu.power_connectors[i].get() <= psu.connectors[j].get()):
                     return True
    return False ## Doesn't have the right connector, right amount of connector, or both

## MOBO <-> PSU

#def mobo_psu_compatibility( ## requires complex data normalisation
#          mobo: MOTHERBOARD,
#          psu: PSU
#) -> bool:
#     for i in range (0, len(mobo.power_connectors)):
#          if(mobo.power_connectors[i].lower() == "main_power"):
#               if (hasattr(mobo.power_connectors[i], "pop")):  ## check if main power is a list of cables or just 1 cable
#                    num_cables = len(mobo.power_connectors[i])
#                    for j in range (0, len(psu.connectors)):
#                         if (psu.connectors[i].lower() == power_connector)
                    
## PSU <-> CASE

def psu_case_compatibility(
        psu: PSU,
        case: CASE
) -> bool:
    return (psu.form_factor in case.supported_power_supply_form_factors) and (psu.length_mm <= case.max_psu_length_mm)

## STORAGE <-> MOBO

def storage_mobo_compatibility( ## regex or other pattern matching will later be used to normalise data
                                ## e.g. "M.2 PCIe 3.0 x4" and "PCIe 3.0 x4" are the same here
        storage: STORAGE,
        mobo: MOTHERBOARD
) -> bool:
    if (storage.storage_type == "SSD" and storage.nvme == True):
        for i in range(0, len(mobo.m2_slots)): ## checks if any slot's interface matches the SSD's interface
                if (len(mobo.m2_slots) >= 1 and storage.interface == mobo.m2_slots[i]["interface"]):
                        return True
        return False ## SSD did not pass constraints
    if("SATA" in storage.interface.upper()): ## SATA constraints (must have SATA connector)
        for i in range(0, len(mobo.storage_devices)):
                       if ("SATA" in mobo.storage_devices[i].upper()):  ## SATA drives are backwards compatible, so 6bps drive will work with 3gbs mobo.
                                                                        ## A warning will be given to users in the optimisation stage about this.
                            return True ## Mobo has SATA cable
                       return False ## No SATA connection - incompatible
        return False ## Some other drive not supported
        ## Not a SATA or SSD drive

## PSU <-> ALL

def psu_all_components_compatibility( ## heuristic ensuring safe PSU headroom (30%)
        psu: PSU,
        gpu: GPU,
        cpu: CPU
) -> bool:
     return psu.wattage_w >= 1.3 * (gpu.tdp_w + cpu.tdp_w + 100) ## allocate ~100W for motherboard, RAM, storage etc
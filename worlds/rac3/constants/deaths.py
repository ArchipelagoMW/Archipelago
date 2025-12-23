class RAC3DEATH:
    EATEN = "was Eaten"
    DIED = "Died"
    DROWNED = "Drowned"
    FELL = "Fell"
    FROZEN = "became an Ice cube"


DEATH_FROM_ACTION: dict[int, str] = {
    0x31: RAC3DEATH.EATEN,
    0x39: RAC3DEATH.DIED,
    0x6C: RAC3DEATH.DROWNED,
    0x79: RAC3DEATH.FELL,
    0x7D: RAC3DEATH.DROWNED,  # Lava/Mud Instant
    0x7E: RAC3DEATH.DROWNED,  # Lava Bounce
    0x81: RAC3DEATH.FROZEN,
}

CLANK_DEATH_FROM_ACTION: dict[int, str] = {
    0x50: RAC3DEATH.FROZEN,
    0x74: RAC3DEATH.FELL,
}

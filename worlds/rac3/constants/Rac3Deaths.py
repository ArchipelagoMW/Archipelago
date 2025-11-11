class RAC3DEATH:
    EATEN = "was Eaten"
    DROWNED = "Drowned"
    FELL = "Fell"
    LAVA = "Drowned"
    FROZEN = "became an Ice cube"


DEATH_FROM_ACTION: dict[int, str] = {
    0x31: RAC3DEATH.EATEN,
    0x6C: RAC3DEATH.DROWNED,
    0x79: RAC3DEATH.FELL,
    0x7E: RAC3DEATH.LAVA,
    0x81: RAC3DEATH.FROZEN
}

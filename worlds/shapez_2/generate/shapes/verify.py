
def is_valid_shape(shape: str, parts: int | None, layers: int | None) -> bool:

    shape_layers = shape.split(":")

    if len(shape_layers) == 0 or (layers is not None and len(shape_layers) > layers):
        return False

    for lay in shape_layers:
        if parts is not None and len(lay) != parts * 2:
            return False
        for x in range(0, len(lay), 2):
            if lay[x:x+2] in "P--":
                continue
            if lay[x+1] not in "urbgymcw":
                return False
            if len(lay) == 12 and lay[x] not in "HFGc":
                return False
            if len(lay) == 8 and lay[x] not in "CRSWc":
                return False

    return True

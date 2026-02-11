
shapes: dict[str, list[str]] = {
    "regular": [
        "CuRuCuCu", "CuRuCuCu:CuCuCuCu", "CuRuCuCu:CbCbCbCb",
        "CuRuCuCu:P-P-P-P-:CbCbCbCb", "CwRwCwCw:P-P-P-P-:CcCcCcCc",
    ],
    "hard": [
        "CuRuCuCu", "CuRuCuCu:CuCuCuWu", "CuRuCuCu:CbCbCbWb",
        "CwRwCwCw:CcCcCcWc", "CwRwCwCw:CcCcCcWc:P-P-P-P-:CwRwCwWw",
    ],
    "insane": [
        "CuRuCuCu", "Su--Su--:WuRuWuCu", "Su--Su--:WuRuWuCu:WbRbWbCb",
        "Sc--Sc--:WwRwWwCw:WcRcWcCc", "Sc--Sc--:WwRwWwCw:WcRcWcCc:P-P-P-P-:CwRwCw--",
    ],
    "hexagonal": [
        "HuGbGbGbGbHu", "HuGbGbGbGbHu:Hb--------Hb:HuHuHuHuHuHu",
        "HwGbGbGbGbHw:Hb--------Hb:HwHwHwHwHwHw", "HwGbGbGbGbHw:HbP-P-P-P-Hb:P---------P-:HwHwHwHwHwHw"
    ],
}

points: dict[str, list[int]] = {
    "tetragonal": [1, 2, 5, 10, 20],
    "hexagonal": [2, 4, 8, 10, 12],
}

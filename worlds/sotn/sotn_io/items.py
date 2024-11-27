import constants

items_list = [
    {
        "name": "Heart",
        "type": constants.TYPE["HEART"],
        "id": 0,
        "tiles": [
            {"zones": constants.ZONE["ST0"], "entities": [0x26e0, 0x28de], "candle": 0x30, },
            {"zones": constants.ZONE["ST0"], "entities": [0x26fe, 0x28e8], "candle": 0x30, },
            {"zones": constants.ZONE["ST0"], "entities": [0x2708, 0x28f2], "candle": 0x20, },
            {"zones": constants.ZONE["ST0"], "entities": [0x2712, 0x28fc], "candle": 0x30, },
            {"zones": constants.ZONE["ST0"], "entities": [0x2726, 0x2906], "candle": 0x30, },
            {"zones": constants.ZONE["ARE"], "entities": [0x2f1e, 0x35ce], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x2f5a, 0x35ec], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x2f82, 0x3600], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x350e, 0x3b8c], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3518, 0x3b96], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3072, 0x3704], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3086, 0x36fa], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x30a4, 0x36e6], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x30b8, 0x36dc], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x33ce, 0x3a60], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x33e2, 0x39ca], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3400, 0x3aba], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3450, 0x3ad8], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3266, 0x3966], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3284, 0x38e4], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x32c0, 0x3952], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x32de, 0x38d0], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x31a8, 0x383a], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x31bc, 0x3830], "candle": 0x10, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2dce, 0x36ae], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2dd8, 0x36b8], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2d7e, 0x365e], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2d92, 0x3654], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2e82, 0x3744], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2cfc, 0x35d2], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3044, 0x3938], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x306c, 0x3924], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2c84, 0x3564], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2c8e, 0x358c], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x30a8, 0x3a00], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x30bc, 0x3a0a], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x30ee, 0x39c4], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x30f8, 0x3a32], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3134, 0x3a1e], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x313e, 0x3988], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x315c, 0x39b0], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3166, 0x3a28], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x32e2, 0x3bf4], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x32ec, 0x3bfe], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x331e, 0x3c12], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3328, 0x3c08], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3382, 0x3c6c], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3396, 0x3c62], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x33aa, 0x3c9e], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x33be, 0x3c8a], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x33e6, 0x3c76], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3440, 0x3d16], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x344a, 0x3d0c], "candle": 0x20, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1b2e, 0x1ebc], "candle": 0x00, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1b4c, 0x1eda], "candle": 0x10, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1b88, 0x1f0c], "candle": 0x00, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1bb0, 0x1f20], "candle": 0x00, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2ad6, 0x3468], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2aea, 0x3472], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2b4e, 0x3490], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2c02, 0x3580], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2c3e, 0x3594], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2cac, 0x363e], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x295a, 0x327e], "candle": 0x00, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2d56, 0x379c], "candle": 0x00, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2d60, 0x37e2], "candle": 0x00, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2d6a, 0x380a], "candle": 0x00, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2eb4, 0x3814], "candle": 0x00, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2ebe, 0x3850], "candle": 0x00, },
            {"zones": constants.ZONE["DAI"], "entities": [0x306c, 0x39ea], "candle": 0x10, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3722, 0x3ee8], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3768, 0x3e0c], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x37a4, 0x3dc6], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x37ea, 0x3e16], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x37f4, 0x3e3e], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3812, 0x3e20], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3830, 0x3dbc], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x386c, 0x3db2], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3628, 0x3cd6], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3650, 0x3ce0], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x33e4, 0x3aba], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x33f8, 0x3b5a], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3466, 0x3a4c], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3484, 0x3ae2], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3498, 0x3b78], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x34d4, 0x3ad8], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x34e8, 0x3b82], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x36c8, 0x3d4e], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2e32, 0x3e38], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2e6e, 0x3e24], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2e78, 0x3e1a], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2eaa, 0x3e06], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2eb4, 0x3cda], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2ebe, 0x3dfc], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2ed2, 0x3cd0], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2efa, 0x3df2], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2f04, 0x3cc6], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2f18, 0x3de8], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2f40, 0x3dd4], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2f4a, 0x3cb2], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2f5e, 0x3dca], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2f7c, 0x3db6], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2fa4, 0x3c94], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2fc2, 0x3c8a], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2ff4, 0x3e88], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2ffe, 0x3e9c], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3012, 0x3e6a], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3026, 0x3e92], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3030, 0x3ea6], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3062, 0x3f8c], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x306c, 0x3faa], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x308a, 0x3ece], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x30a8, 0x3ed8], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x30bc, 0x3f28], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x30c6, 0x3f32], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x30d0, 0x3f6e], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x30da, 0x3fbe], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x30e4, 0x3ee2], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x30f8, 0x3f50], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3102, 0x3eec], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x310c, 0x3f5a], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3120, 0x3f78], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x312a, 0x3fc8], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x315c, 0x3f00], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3184, 0x3f46], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3198, 0x3fdc], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3274, 0x40f4], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3292, 0x4108], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x329c, 0x4112], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x32ba, 0x413a], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x32ce, 0x414e], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x32d8, 0x4158], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x32ec, 0x4162], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x32f6, 0x416c], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x35ee, 0x446e], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x362a, 0x4482], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3332, 0x41b2], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3378, 0x41c6], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3418, 0x42c0], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3436, 0x42d4], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x344a, 0x42e8], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x345e, 0x42f2], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3468, 0x42fc], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x349a, 0x4306], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x34a4, 0x4310], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x34c2, 0x4324], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x34cc, 0x432e], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x34e0, 0x4338], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x293a, 0x37ba], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x294e, 0x37c4], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x33a0, 0x423e], "candle": 0x20, },
            {"zones": constants.ZONE["NO0"], "entities": [0x33b4, 0x4220], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x31b6, 0x4068], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x31ca, 0x404a], "candle": 0x20, },
            {"zones": constants.ZONE["NO0"], "entities": [0x31de, 0x40b8], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3210, 0x40a4], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x322e, 0x4040], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3238, 0x4090], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x36f2, 0x4568], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x36fc, 0x4586], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x353a, 0x43b0], "candle": 0x20, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3544, 0x43d8], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3558, 0x43a6], "candle": 0x20, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3562, 0x4400], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x358a, 0x440a], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x359e, 0x43ba], "candle": 0x20, },
            {"zones": constants.ZONE["NO1"], "entities": [0x39b8, 0x4176], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3864, 0x407c], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3878, 0x3fc8], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3882, 0x4086], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x38e6, 0x400e], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x35ee, 0x3dde], "candle": 0x60, },
            {"zones": constants.ZONE["NO1"], "entities": [0x360c, 0x3dca], "candle": 0x60, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3b5c, 0x440a], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3b66, 0x43b0], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3b70, 0x4342], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3c56, 0x42b6], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3c6a, 0x4298], "candle": 0x50, },
            {"zones": constants.ZONE["NO2"], "entities": [0x39b6, 0x416a], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3a24, 0x40e8], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3a38, 0x414c], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3a60, 0x4156], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x363c, 0x3d6e], "candle": 0x30, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3650, 0x3d78], "candle": 0x30, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3678, 0x3d96], "candle": 0x30, },
            {"zones": constants.ZONE["NO2"], "entities": [0x34fc, 0x3c56], "candle": 0x40, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3524, 0x3c42], "candle": 0x40, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3538, 0x3c38], "candle": 0x40, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3830, 0x3f9e], "candle": 0x10, },
            {"zones": constants.ZONE["NO2"], "entities": [0x384e, 0x3fa8], "candle": 0x10, },
            {"zones": constants.ZONE["NO2"], "entities": [0x38b2, 0x3fb2], "candle": 0x10, },
            {"zones": constants.ZONE["NO2"], "entities": [0x38bc, 0x3f12], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x38ee, 0x402a], "candle": 0x10, },
            {"zones": constants.ZONE["NO2"], "entities": [0x38f8, 0x3f08], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x359c, 0x3cce], "candle": 0x60, },
            {"zones": constants.ZONE["NO2"], "entities": [0x35b0, 0x3cd8], "candle": 0x60, },
            {"zones": constants.ZONE["NO2"], "entities": [0x35ec, 0x3d28], "candle": 0x20, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3600, 0x3d32], "candle": 0x20, },
            {"zones": constants.ZONE["NO2"], "entities": [0x36dc, 0x3e40], "candle": 0x60, },
            {"zones": constants.ZONE["NO2"], "entities": [0x36fa, 0x3e0e], "candle": 0x40, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3704, 0x3e04], "candle": 0x40, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3740, 0x3e68], "candle": 0x60, },
            {"zones": constants.ZONE["NO2"], "entities": [0x374a, 0x3e5e], "candle": 0x60, },
            {"zones": constants.ZONE["NO2"], "entities": [0x377c, 0x3e4a], "candle": 0x60, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x43c2, 0x4b44, 0x419e, 0x48d0],
             "candle": 0x00, },
            {"zones": constants.ZONE["NO3"], "entities": [0x43d6, 0x4b4e], "candle": 0x00, },
            {"zones": constants.ZONE["NO3"], "entities": [0x43e0, 0x4b58], "candle": 0x00, },
            {"zones": constants.ZONE["NO3"], "entities": [0x43fe, 0x4b62], "candle": 0x00, },
            {"zones": constants.ZONE["NO3"], "entities": [0x4412, 0x4b6c], "candle": 0x00, },
            {"zones": constants.ZONE["NO3"], "entities": [0x4430, 0x4b76], "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3e18, 0x4590, 0x3bb8, 0x42e0],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3e22, 0x45ae, 0x3bc2, 0x42fe],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3e2c, 0x45a4, 0x3bcc, 0x42f4],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3eea, 0x468a, 0x3c94, 0x43da],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3efe, 0x4676, 0x3ca8, 0x43c6],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3f08, 0x466c, 0x3cbc, 0x43bc],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3e4a, 0x45d6, 0x3bea, 0x4326],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x42a0, 0x4a90, 0x407c, 0x4826],
             "candle": 0x00, },
            {"zones": constants.ZONE["NO3"], "entities": [0x42c8, 0x4a36], "candle": 0x00, },
            {"zones": constants.ZONE["NO3"], "entities": [0x4354, 0x4a40], "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x4368, 0x4a86, 0x4144, 0x481c],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3f4e, 0x46e4, 0x3d0c, 0x4448],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3f62, 0x46ee, 0x3d20, 0x4452],
             "candle": 0x00, },
            {"zones": constants.ZONE["NO3"], "entities": [0x3f76, 0x46f8], "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3f80, 0x4720, 0x3d34, 0x4484],
             "candle": 0x00, },
            {"zones": constants.ZONE["NO3"], "entities": [0x3f94, 0x472a], "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3f9e, 0x4702, 0x3d48, 0x4466],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3fb2, 0x470c, 0x3d52, 0x4470],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3fc6, 0x4716, 0x3d66, 0x447a],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x40fc, 0x487e, 0x3eba, 0x45e2],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x4124, 0x48e2, 0x3eec, 0x465a],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x414c, 0x48d8, 0x3f14, 0x4650],
             "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3294, 0x4326], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x32b2, 0x4344], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3e10, 0x4e98], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x35dc, 0x4646], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x35e6, 0x4664], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x350a, 0x4600], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x351e, 0x456a], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3532, 0x457e], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3546, 0x45e2], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3578, 0x452e], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3582, 0x4542], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x342e, 0x44ac], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3442, 0x44b6], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x33fc, 0x448e], "candle": 0x60, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3460, 0x44fc], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3488, 0x44e8], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3370, 0x43f8], "candle": 0x60, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3384, 0x4416], "candle": 0x60, },
            {"zones": constants.ZONE["NO4"], "entities": [0x33a2, 0x4402], "candle": 0x60, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3e1a, 0x4ea2], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3e74, 0x4ec0], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3ece, 0x4f56], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x4086, 0x50c8], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x4108, 0x50dc], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x411c, 0x50e6], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3fd2, 0x5064], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x369a, 0x4722], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3a78, 0x4b1e], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3b54, 0x4b00], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3b5e, 0x4b32], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3be0, 0x4c36], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3c08, 0x4c2c], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3d20, 0x4d30], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3de8, 0x4d4e], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3df2, 0x4d58], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x38a2, 0x48c6], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x38ac, 0x48bc], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3938, 0x49de], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x37e4, 0x475e], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x37ee, 0x4754], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2a78, 0x33c6], "candle": 0x10, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2f8c, 0x38a8], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2f96, 0x38bc], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2fbe, 0x392a], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2fdc, 0x38f8], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2ffa, 0x3934], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x3022, 0x3902], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2ee2, 0x3826], "candle": 0x10, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2f00, 0x381c], "candle": 0x10, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x304a, 0x398e], "candle": 0x10, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x3068, 0x3984], "candle": 0x10, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2e10, 0x374a], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2e42, 0x3772], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x28de, 0x3204], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x28f2, 0x3236], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x29e2, 0x32fe], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2938, 0x3272], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x297e, 0x32a4], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x29d8, 0x32f4], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x29ec, 0x3312], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2a1e, 0x3380], "candle": 0x10, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2a46, 0x336c], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2ce4, 0x363c], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2d48, 0x3628], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2d52, 0x3632], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2abe, 0x3434], "candle": 0x10, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2b22, 0x3470], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2b36, 0x345c], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2b9a, 0x34e8], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2c08, 0x3524], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x30ae, 0x39fc], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x30b8, 0x39f2], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x30c2, 0x3a06], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x30d6, 0x3a1a], "candle": 0x20, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2d40, 0x3792], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2d5e, 0x3756], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2d72, 0x374c], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2d7c, 0x377e], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2d0e, 0x371a], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2d22, 0x3724], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2bba, 0x3648], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2be2, 0x36d4], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2c0a, 0x362a], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2c1e, 0x36c0], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2c50, 0x36b6], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2c82, 0x3698], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2cbe, 0x367a], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2ce6, 0x3620], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x24bc, 0x2f4a], "candle": 0x40, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x24c6, 0x2fa4], "candle": 0x40, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2660, 0x30a8], "candle": 0x40, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x26ec, 0x315c], "candle": 0x40, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x26f6, 0x3148], "candle": 0x40, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x28d6, 0x3454], "candle": 0x50, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2980, 0x354e], "candle": 0x60, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x299e, 0x338c], "candle": 0x00, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x29b2, 0x33b4], "candle": 0x00, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2a16, 0x33aa], "candle": 0x00, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2a3e, 0x3378], "candle": 0x00, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2a48, 0x3418], "candle": 0x50, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2a70, 0x353a], "candle": 0x60, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2a8e, 0x336e], "candle": 0x00, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2aa2, 0x3396], "candle": 0x00, },
            {"zones": constants.ZONE["TOP"], "entities": [0x2106, 0x28a6], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x214c, 0x28b0], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x217e, 0x28c4], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x2188, 0x28ce], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x21a6, 0x275c], "candle": 0x30, },
            {"zones": constants.ZONE["TOP"], "entities": [0x21e2, 0x2766], "candle": 0x30, },
            {"zones": constants.ZONE["TOP"], "entities": [0x21ec, 0x28e2], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x2200, 0x2770], "candle": 0x20, },
            {"zones": constants.ZONE["TOP"], "entities": [0x2214, 0x28ec], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x2228, 0x277a], "candle": 0x30, },
            {"zones": constants.ZONE["TOP"], "entities": [0x223c, 0x2900], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x225a, 0x290a], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x2264, 0x27ca], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x226e, 0x2784], "candle": 0x30, },
            {"zones": constants.ZONE["TOP"], "entities": [0x22be, 0x291e], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x22f0, 0x2860], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x2390, 0x284c], "candle": 0x60, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2464, 0x2a36], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x248c, 0x2a22], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x24be, 0x2a04], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x209a, 0x264e], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x20a4, 0x2644], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x1fa0, 0x2536], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x1faa, 0x2540], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x1ff0, 0x2554], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x1ffa, 0x255e], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x223e, 0x289c], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2248, 0x27f2], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2324, 0x28e2], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x237e, 0x28c4], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2194, 0x2784], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x21bc, 0x270c], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x21e4, 0x2798], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x21f8, 0x2720], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2108, 0x269e], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x211c, 0x26a8], "candle": 0x10, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x27ee, 0x331c], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x27f8, 0x3312], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x27c6, 0x32ea], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x27d0, 0x32f4], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2b4a, 0x3696], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2762, 0x3286], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2ab4, 0x35f6], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2adc, 0x35e2], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2726, 0x31dc], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2730, 0x325e], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x28b6, 0x3402], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x28c0, 0x3434], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x28ca, 0x3470], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x28d4, 0x33f8], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2906, 0x33c6], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x291a, 0x3448], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2924, 0x33e4], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2938, 0x33da], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2d5c, 0x388a], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2d7a, 0x3894], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2db6, 0x3880], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2dc0, 0x3876], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2df2, 0x390c], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2e56, 0x3920], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2ee2, 0x3934], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2f3c, 0x393e], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2fa0, 0x3948], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x3018, 0x3b3c], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x3022, 0x3b46], "candle": 0x20, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x1974, 0x1dca], "candle": 0x10, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x19ba, 0x1df2], "candle": 0x00, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x19e2, 0x1e42], "candle": 0x00, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x1a1e, 0x1e56], "candle": 0x00, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x206c, 0x2a0a], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x20bc, 0x29ec], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x20da, 0x29e2], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x213e, 0x2abe], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x2166, 0x2aaa], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x21de, 0x2b36], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x1ee6, 0x292e], "candle": 0x00, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x226a, 0x2c3a], "candle": 0x00, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x2274, 0x2be0], "candle": 0x00, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x23e6, 0x2cda], "candle": 0x00, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x23f0, 0x2c8a], "candle": 0x00, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x23fa, 0x2c30], "candle": 0x00, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x2512, 0x2e60], "candle": 0x10, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1b50, 0x2212], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1b96, 0x221c], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1baa, 0x21b8], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1bc8, 0x21a4], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1bd2, 0x2172], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1bf0, 0x21f4], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1c18, 0x21ae], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1c86, 0x20f0], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1ed4, 0x249c], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1ef2, 0x2492], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1f56, 0x2500], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1d1c, 0x2316], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1d4e, 0x2366], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1d76, 0x230c], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1d80, 0x2370], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1d94, 0x23d4], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1e02, 0x22ee], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1e3e, 0x23c0], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1e70, 0x2424], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x371c, 0x4948], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3744, 0x4952], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3758, 0x477c], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x37bc, 0x48e4], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x37c6, 0x4790], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x37e4, 0x479a], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x383e, 0x47ae], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x385c, 0x47b8], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3884, 0x4902], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x38a2, 0x48f8], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x38d4, 0x490c], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x38de, 0x47c2], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x391a, 0x47cc], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x396a, 0x47e0], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x397e, 0x47ea], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3668, 0x4722], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3672, 0x4704], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x367c, 0x46f0], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3686, 0x46dc], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x36ae, 0x46fa], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x36b8, 0x46e6], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x39ce, 0x4aba], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x39e2, 0x4a38], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x39ec, 0x4b14], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3a28, 0x4a7e], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3a32, 0x4a4c], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3a3c, 0x4a9c], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3a46, 0x4b00], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3a50, 0x4aa6], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3a5a, 0x4af6], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3a78, 0x4ac4], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3a82, 0x4a74], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3a8c, 0x4a42], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3aa0, 0x4ace], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3aaa, 0x4aec], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3ac8, 0x4ae2], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3adc, 0x4a6a], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3ae6, 0x4a56], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x362c, 0x4696], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3636, 0x468c], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3b22, 0x4ba0], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3b40, 0x4b96], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3b72, 0x4b8c], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3b86, 0x4b82], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3b9a, 0x4b6e], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4428, 0x54ce], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x445a, 0x54ba], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x40e0, 0x5154], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4158, 0x5140], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x42a2, 0x52f8], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x42ca, 0x530c], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x42f2, 0x5320], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4306, 0x532a], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x431a, 0x5334], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4360, 0x533e], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x436a, 0x5348], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x43a6, 0x535c], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x43c4, 0x5366], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x43d8, 0x5370], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x36e0, 0x4754], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x36f4, 0x474a], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4072, 0x50e6], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4086, 0x50f0], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x40a4, 0x50dc], "candle": 0x20, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4194, 0x528a], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x419e, 0x521c], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x41c6, 0x51f4], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4216, 0x523a], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4220, 0x51ea], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x422a, 0x5276], "candle": 0x20, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4248, 0x5262], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4518, 0x5596], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4522, 0x558c], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x452c, 0x55a0], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4536, 0x5582], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3fa0, 0x5014], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3fb4, 0x5050], "candle": 0x20, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3fc8, 0x500a], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3ffa, 0x5000], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4004, 0x505a], "candle": 0x20, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x402c, 0x503c], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4036, 0x5046], "candle": 0x20, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x404a, 0x501e], "candle": 0x10, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x2012, 0x2780], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x203a, 0x27da], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x2044, 0x26f4], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x20bc, 0x26ea], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x2260, 0x2942], "candle": 0x60, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x2288, 0x2956], "candle": 0x60, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x23dc, 0x2c58], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x23e6, 0x2c1c], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x245e, 0x2ad2], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x2468, 0x2b36], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x2472, 0x2b90], "candle": 0x50, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2484, 0x2c7c], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2498, 0x2c72], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x24ca, 0x2cc2], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x24de, 0x2cb8], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x24f2, 0x2d1c], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2538, 0x2cd6], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2574, 0x2d6c], "candle": 0x30, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x25a6, 0x2d4e], "candle": 0x30, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x25c4, 0x2d44], "candle": 0x30, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2614, 0x2de4], "candle": 0x40, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2628, 0x2dee], "candle": 0x40, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2650, 0x2e02], "candle": 0x40, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2718, 0x3096], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2786, 0x30a0], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2a60, 0x323a], "candle": 0x60, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2a6a, 0x3230], "candle": 0x60, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2a9c, 0x3280], "candle": 0x20, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2ab0, 0x3276], "candle": 0x20, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2aec, 0x32c6], "candle": 0x60, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2b3c, 0x32da], "candle": 0x60, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2b46, 0x32e4], "candle": 0x60, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2baa, 0x332a], "candle": 0x40, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2bbe, 0x3334], "candle": 0x40, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2bd2, 0x3302], "candle": 0x60, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x3106, 0x3818], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x3156, 0x3804], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x31ba, 0x37f0], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x31ce, 0x37e6], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2c7e, 0x334a], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2c88, 0x335e], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2c92, 0x3372], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x320a, 0x38cc], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x321e, 0x38d6], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x3250, 0x38ea], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2cc4, 0x3390], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2efe, 0x35e8], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2f08, 0x362e], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2f3a, 0x3624], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2f44, 0x35d4], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x3034, 0x3746], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x3052, 0x373c], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x3084, 0x3732], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x30b6, 0x371e], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x30ca, 0x3714], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2c4c, 0x3318], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2c56, 0x3322], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2c60, 0x332c], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2e2c, 0x34f8], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2e4a, 0x3502], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2e86, 0x3552], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3b50, 0x4aa0], "candle": 0x50, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3b64, 0x4ab4], "candle": 0x50, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3010, 0x3f88], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x301a, 0x3f60], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3024, 0x3f7e], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2f34, 0x3f24], "candle": 0x50, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2f48, 0x3eb6], "candle": 0x50, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2f8e, 0x3f10], "candle": 0x50, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2fac, 0x3efc], "candle": 0x50, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2fd4, 0x3ea2], "candle": 0x50, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2e9e, 0x3e16], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2ebc, 0x3e0c], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2e26, 0x3d6c], "candle": 0x60, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2ee4, 0x3e34], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2f16, 0x3e48], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2d90, 0x3d26], "candle": 0x60, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2dcc, 0x3cea], "candle": 0x60, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2dea, 0x3d1c], "candle": 0x60, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3696, 0x462c], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x36f0, 0x4640], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x36fa, 0x4636], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x38f8, 0x48ca], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x390c, 0x48c0], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3966, 0x48ac], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x384e, 0x4794], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3c0e, 0x4b54], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x322c, 0x417c], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3240, 0x4172], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3286, 0x4226], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x32a4, 0x4244], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3358, 0x4212], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x338a, 0x4398], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x339e, 0x438e], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3588, 0x4460], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x361e, 0x45aa], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3632, 0x45b4], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x30ba, 0x4104], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x30c4, 0x40fa], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2372, 0x2c5c], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2728, 0x3026], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2732, 0x303a], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2778, 0x30b2], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x27a0, 0x306c], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x27b4, 0x30a8], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x27d2, 0x3062], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x26a6, 0x2fa4], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x26c4, 0x2f9a], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2890, 0x3184], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x28ae, 0x318e], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x27fa, 0x30f8], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2818, 0x30ee], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x25fc, 0x2ed2], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2624, 0x2ee6], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2192, 0x2a7c], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x21a6, 0x2a4a], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x21f6, 0x2acc], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2200, 0x2ac2], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2232, 0x2b12], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2296, 0x2ba8], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x22a0, 0x2b94], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x22aa, 0x2b6c], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x22fa, 0x2bf8], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2318, 0x2c02], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2520, 0x2e3c], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2534, 0x2e32], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x25a2, 0x2e46], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x239a, 0x2c84], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x23ae, 0x2c98], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2408, 0x2cca], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x244e, 0x2d56], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x24b2, 0x2d88], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2836, 0x312a], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2854, 0x313e], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x285e, 0x3148], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2868, 0x3134], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2d42, 0x35aa], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2d4c, 0x35dc], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2d60, 0x35e6], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2d7e, 0x35be], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2cfc, 0x356e], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2d10, 0x3564], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2b8a, 0x34b0], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2b9e, 0x342e], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2c20, 0x344c], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2c66, 0x346a], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2c7a, 0x3474], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2cac, 0x34ba], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2cb6, 0x3488], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2cd4, 0x349c], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x26ee, 0x2e66], "candle": 0x40, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2716, 0x2ec0], "candle": 0x40, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x281a, 0x2ff6], "candle": 0x40, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2932, 0x3140], "candle": 0x40, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x293c, 0x3154], "candle": 0x40, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2a9a, 0x338e], "candle": 0x60, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2acc, 0x3334], "candle": 0x50, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2b08, 0x337a], "candle": 0x60, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2b58, 0x330c], "candle": 0x50, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1ad2, 0x1fbe], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1ae6, 0x1fb4], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1af0, 0x1faa], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1b04, 0x1fa0], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1b22, 0x1f96], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1b4a, 0x1f8c], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1b86, 0x2090], "candle": 0x30, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1b90, 0x1f82], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1ba4, 0x1f78], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1bb8, 0x2086], "candle": 0x30, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1bc2, 0x1f6e], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1bcc, 0x1f64], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1be0, 0x207c], "candle": 0x20, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1bea, 0x1f5a], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1bfe, 0x2072], "candle": 0x30, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1c08, 0x1f50], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1c1c, 0x2068], "candle": 0x30, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1c30, 0x1f46], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1c3a, 0x1f3c], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1c44, 0x1f32], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1c62, 0x1f28], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1c9e, 0x1f1e], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1ca8, 0x1f14], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1cb2, 0x1f0a], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1cd0, 0x1f00], "candle": 0x60, },
            {"addresses": [0x043c3612, 0x044917e2, 0x0455cc62, 0x045e99ba, 0x0467755a, 0x048fb156, 0x049d3a26,
                           0x04aa1a42, 0x04b68aea, 0x04c328ee, 0x04cfbd2e, 0x04da5736, 0x04e327d2, 0x04ee32fe,
                           0x04f86072, 0x05050946, 0x050f8e72, 0x051ade86, 0x0526c722, 0x053f6466, 0x054b290e,
                           0x05573db2, 0x0560fbe2, 0x056be926, 0x0575197a, 0x057e077a, 0x05883f4a, 0x0590361a,
                           0x059bca06, 0x05a6ee9a, 0x05af32a6, 0x0606f0da, 0x060fdd0e, 0x061a7792, 0x0624789a,
                           0x0630618a, 0x063aafe2, 0x06471a0a, 0x065094be, 0x065918ba, 0x06621d0a, 0x066b4092,
                           0x06742eaa, 0x067d0d06, 0x06862056, 0x0692c45e, 0x069d21f2, 0x06a611d6, 0x047a3e76],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c362e, 0x044917fe, 0x0455cc7e, 0x045e99d6, 0x04677576, 0x048fb172, 0x049d3a42,
                           0x04aa1a5e, 0x04b68b06, 0x04c3290a, 0x04cfbd4a, 0x04da5752, 0x04e327ee, 0x04ee331a,
                           0x04f8608e, 0x05050962, 0x050f8e8e, 0x051adea2, 0x0526c73e, 0x053f6482, 0x054b292a,
                           0x05573dce, 0x0560fbfe, 0x056be942, 0x05751996, 0x057e0796, 0x05883f66, 0x05903636,
                           0x059bca22, 0x05a6eeb6, 0x05af32c2, 0x0606f0f6, 0x060fdd2a, 0x061a77ae, 0x062478b6,
                           0x063061a6, 0x063aaffe, 0x06471a26, 0x065094da, 0x065918d6, 0x06621d26, 0x066b40ae,
                           0x06742ec6, 0x067d0d22, 0x06862072, 0x0692c47a, 0x069d220e, 0x06a611f2, 0x047a3fc2],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3630, 0x04491800, 0x0455cc80, 0x045e99d8, 0x04677578, 0x048fb174, 0x049d3a44,
                           0x04aa1a60, 0x04b68b08, 0x04c3290c, 0x04cfbd4c, 0x04da5754, 0x04e327f0, 0x04ee331c,
                           0x04f86090, 0x05050964, 0x050f8e90, 0x051adea4, 0x0526c740, 0x053f6484, 0x054b292c,
                           0x05573dd0, 0x0560fc00, 0x056be944, 0x05751998, 0x057e0798, 0x05883f68, 0x05903638,
                           0x059bca24, 0x05a6eeb8, 0x05af32c4, 0x0606f0f8, 0x060fdd2c, 0x061a77b0, 0x062478b8,
                           0x063061a8, 0x063ab000, 0x06471a28, 0x065094dc, 0x065918d8, 0x06621d28, 0x066b40b0,
                           0x06742ec8, 0x067d0d24, 0x06862074, 0x0692c47c, 0x069d2210, 0x06a611f4, 0x047a3fc4],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3632, 0x04491802, 0x0455cc82, 0x045e99da, 0x0467757a, 0x048fb176, 0x049d3a46,
                           0x04aa1a62, 0x04b68b0a, 0x04c3290e, 0x04cfbd4e, 0x04da5756, 0x04e327f2, 0x04ee331e,
                           0x04f86092, 0x05050966, 0x050f8e92, 0x051adea6, 0x0526c742, 0x053f6486, 0x054b292e,
                           0x05573dd2, 0x0560fc02, 0x056be946, 0x0575199a, 0x057e079a, 0x05883f6a, 0x0590363a,
                           0x059bca26, 0x05a6eeba, 0x05af32c6, 0x0606f0fa, 0x060fdd2e, 0x061a77b2, 0x062478ba,
                           0x063061aa, 0x063ab002, 0x06471a2a, 0x065094de, 0x065918da, 0x06621d2a, 0x066b40b2,
                           0x06742eca, 0x067d0d26, 0x06862076, 0x0692c47e, 0x069d2212, 0x06a611f6, 0x047a3fc6],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3634, 0x04491804, 0x0455cc84, 0x045e99dc, 0x0467757c, 0x048fb178, 0x049d3a48,
                           0x04aa1a64, 0x04b68b0c, 0x04c32910, 0x04cfbd50, 0x04da5758, 0x04e327f4, 0x04ee3320,
                           0x04f86094, 0x05050968, 0x050f8e94, 0x051adea8, 0x0526c744, 0x053f6488, 0x054b2930,
                           0x05573dd4, 0x0560fc04, 0x056be948, 0x0575199c, 0x057e079c, 0x05883f6c, 0x0590363c,
                           0x059bca28, 0x05a6eebc, 0x05af32c8, 0x0606f0fc, 0x060fdd30, 0x061a77b4, 0x062478bc,
                           0x063061ac, 0x063ab004, 0x06471a2c, 0x065094e0, 0x065918dc, 0x06621d2c, 0x066b40b4,
                           0x06742ecc, 0x067d0d28, 0x06862078, 0x0692c480, 0x069d2214, 0x06a611f8, 0x047a3fc8],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3636, 0x04491806, 0x0455cc86, 0x045e99de, 0x0467757e, 0x048fb17a, 0x049d3a4a,
                           0x04aa1a66, 0x04b68b0e, 0x04c32912, 0x04cfbd52, 0x04da575a, 0x04e327f6, 0x04ee3322,
                           0x04f86096, 0x0505096a, 0x050f8e96, 0x051adeaa, 0x0526c746, 0x053f648a, 0x054b2932,
                           0x05573dd6, 0x0560fc06, 0x056be94a, 0x0575199e, 0x057e079e, 0x05883f6e, 0x0590363e,
                           0x059bca2a, 0x05a6eebe, 0x05af32ca, 0x0606f0fe, 0x060fdd32, 0x061a77b6, 0x062478be,
                           0x063061ae, 0x063ab006, 0x06471a2e, 0x065094e2, 0x065918de, 0x06621d2e, 0x066b40b6,
                           0x06742ece, 0x067d0d2a, 0x0686207a, 0x0692c482, 0x069d2216, 0x06a611fa, 0x047a3fca],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3638, 0x04491808, 0x0455cc88, 0x045e99e0, 0x04677580, 0x048fb17c, 0x049d3a4c,
                           0x04aa1a68, 0x04b68b10, 0x04c32914, 0x04cfbd54, 0x04da575c, 0x04e327f8, 0x04ee3324,
                           0x04f86098, 0x0505096c, 0x050f8e98, 0x051adeac, 0x0526c748, 0x053f648c, 0x054b2934,
                           0x05573dd8, 0x0560fc08, 0x056be94c, 0x057519a0, 0x057e07a0, 0x05883f70, 0x05903640,
                           0x059bca2c, 0x05a6eec0, 0x05af32cc, 0x0606f100, 0x060fdd34, 0x061a77b8, 0x062478c0,
                           0x063061b0, 0x063ab008, 0x06471a30, 0x065094e4, 0x065918e0, 0x06621d30, 0x066b40b8,
                           0x06742ed0, 0x067d0d2c, 0x0686207c, 0x0692c484, 0x069d2218, 0x06a611fc, 0x047a3fcc],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c363a, 0x0449180a, 0x0455cc8a, 0x045e99e2, 0x04677582, 0x048fb17e, 0x049d3a4e,
                           0x04aa1a6a, 0x04b68b12, 0x04c32916, 0x04cfbd56, 0x04da575e, 0x04e327fa, 0x04ee3326,
                           0x04f8609a, 0x0505096e, 0x050f8e9a, 0x051adeae, 0x0526c74a, 0x053f648e, 0x054b2936,
                           0x05573dda, 0x0560fc0a, 0x056be94e, 0x057519a2, 0x057e07a2, 0x05883f72, 0x05903642,
                           0x059bca2e, 0x05a6eec2, 0x05af32ce, 0x0606f102, 0x060fdd36, 0x061a77ba, 0x062478c2,
                           0x063061b2, 0x063ab00a, 0x06471a32, 0x065094e6, 0x065918e2, 0x06621d32, 0x066b40ba,
                           0x06742ed2, 0x067d0d2e, 0x0686207e, 0x0692c486, 0x069d221a, 0x06a611fe, 0x047a3fce],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c363c, 0x0449180c, 0x0455cc8c, 0x045e99e4, 0x04677584, 0x048fb180, 0x049d3a50,
                           0x04aa1a6c, 0x04b68b14, 0x04c32918, 0x04cfbd58, 0x04da5760, 0x04e327fc, 0x04ee3328,
                           0x04f8609c, 0x05050970, 0x050f8e9c, 0x051adeb0, 0x0526c74c, 0x053f6490, 0x054b2938,
                           0x05573ddc, 0x0560fc0c, 0x056be950, 0x057519a4, 0x057e07a4, 0x05883f74, 0x05903644,
                           0x059bca30, 0x05a6eec4, 0x05af32d0, 0x0606f104, 0x060fdd38, 0x061a77bc, 0x062478c4,
                           0x063061b4, 0x063ab00c, 0x06471a34, 0x065094e8, 0x065918e4, 0x06621d34, 0x066b40bc,
                           0x06742ed4, 0x067d0d30, 0x06862080, 0x0692c488, 0x069d221c, 0x06a61200, 0x047a3fd0],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c363e, 0x0449180e, 0x0455cc8e, 0x045e99e6, 0x04677586, 0x048fb182, 0x049d3a52,
                           0x04aa1a6e, 0x04b68b16, 0x04c3291a, 0x04cfbd5a, 0x04da5762, 0x04e327fe, 0x04ee332a,
                           0x04f8609e, 0x05050972, 0x050f8e9e, 0x051adeb2, 0x0526c74e, 0x053f6492, 0x054b293a,
                           0x05573dde, 0x0560fc0e, 0x056be952, 0x057519a6, 0x057e07a6, 0x05883f76, 0x05903646,
                           0x059bca32, 0x05a6eec6, 0x05af32d2, 0x0606f106, 0x060fdd3a, 0x061a77be, 0x062478c6,
                           0x063061b6, 0x063ab00e, 0x06471a36, 0x065094ea, 0x065918e6, 0x06621d36, 0x066b40be,
                           0x06742ed6, 0x067d0d32, 0x06862082, 0x0692c48a, 0x069d221e, 0x06a61202, 0x047a3fd2],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3640, 0x04491810, 0x0455cc90, 0x045e99e8, 0x04677588, 0x048fb184, 0x049d3a54,
                           0x04aa1a70, 0x04b68b18, 0x04c3291c, 0x04cfbd5c, 0x04da5764, 0x04e32800, 0x04ee332c,
                           0x04f860a0, 0x05050974, 0x050f8ea0, 0x051adeb4, 0x0526c750, 0x053f6494, 0x054b293c,
                           0x05573de0, 0x0560fc10, 0x056be954, 0x057519a8, 0x057e07a8, 0x05883f78, 0x05903648,
                           0x059bca34, 0x05a6eec8, 0x05af32d4, 0x0606f108, 0x060fdd3c, 0x061a77c0, 0x062478c8,
                           0x063061b8, 0x063ab010, 0x06471a38, 0x065094ec, 0x065918e8, 0x06621d38, 0x066b40c0,
                           0x06742ed8, 0x067d0d34, 0x06862084, 0x0692c48c, 0x069d2220, 0x06a61204, 0x047a3fd4],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3642, 0x04491812, 0x0455cc92, 0x045e99ea, 0x0467758a, 0x048fb186, 0x049d3a56,
                           0x04aa1a72, 0x04b68b1a, 0x04c3291e, 0x04cfbd5e, 0x04da5766, 0x04e32802, 0x04ee332e,
                           0x04f860a2, 0x05050976, 0x050f8ea2, 0x051adeb6, 0x0526c752, 0x053f6496, 0x054b293e,
                           0x05573de2, 0x0560fc12, 0x056be956, 0x057519aa, 0x057e07aa, 0x05883f7a, 0x0590364a,
                           0x059bca36, 0x05a6eeca, 0x05af32d6, 0x0606f10a, 0x060fdd3e, 0x061a77c2, 0x062478ca,
                           0x063061ba, 0x063ab012, 0x06471a3a, 0x065094ee, 0x065918ea, 0x06621d3a, 0x066b40c2,
                           0x06742eda, 0x067d0d36, 0x06862086, 0x0692c48e, 0x069d2222, 0x06a61206, 0x047a3fd6],
             "enemy": constants.GLOBAL_DROP, }
        ],
    },
    {
        "name": "Big heart",
        "type": constants.TYPE["HEART"],
        "id": 1,
        "tiles": [
            {"zones": constants.ZONE["ST0"], "entities": [0x27da, 0x296a], "candle": 0x30, },
            {"zones": constants.ZONE["ST0"], "entities": [0x2834, 0x2974], "candle": 0x30, },
            {"zones": constants.ZONE["ST0"], "entities": [0x27bc, 0x294c], "candle": 0x30, },
            {"zones": constants.ZONE["ARE"], "entities": [0x2f32, 0x35d8], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3068, 0x370e], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3360, 0x3a4c], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x337e, 0x39c0], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x325c, 0x38ee], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x31da, 0x3826], "candle": 0x10, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2d2e, 0x35fa], "candle": 0x10, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2d56, 0x360e], "candle": 0x00, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2db0, 0x367c], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2e8c, 0x374e], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x349a, 0x3d8e], "candle": 0x00, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3076, 0x392e], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2ca2, 0x35a0], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3116, 0x3a3c], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x312a, 0x39ba], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x330a, 0x3bcc], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x33b4, 0x3c94], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3436, 0x3d20], "candle": 0x20, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1b24, 0x1eb2], "candle": 0x00, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1b92, 0x1ef8], "candle": 0x10, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1ba6, 0x1f02], "candle": 0x10, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1bce, 0x1f70], "candle": 0x00, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2c2a, 0x358a], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2c84, 0x3634], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x29c8, 0x3350], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x287e, 0x3210], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2888, 0x321a], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2892, 0x3224], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x27a2, 0x312a], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x27ac, 0x3134], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x28c4, 0x330a], "candle": 0x00, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2e28, 0x3832], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2e3c, 0x37d8], "candle": 0x10, },
            {"zones": constants.ZONE["LIB"], "entities": [0x374a, 0x3dd0], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3772, 0x3e48], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3420, 0x3b64], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3452, 0x3aec], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2e8c, 0x3e10], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2f36, 0x3cbc], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2f68, 0x3dc0], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2fae, 0x3d8e], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2fea, 0x3e74], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3008, 0x3eb0], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x30ee, 0x3f3c], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3148, 0x3ef6], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x318e, 0x3f64], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x32c4, 0x4144], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x330a, 0x4176], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3620, 0x4478], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3382, 0x41d0], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3440, 0x42de], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x34b8, 0x431a], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2dc4, 0x3c58], "candle": 0x80, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2de2, 0x3c62], "candle": 0x80, },
            {"zones": constants.ZONE["NO0"], "entities": [0x33c8, 0x422a], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3206, 0x4036], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3224, 0x407c], "candle": 0x20, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3706, 0x4572], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3530, 0x43e2], "candle": 0x10, },
            {"zones": constants.ZONE["NO1"], "entities": [0x394a, 0x4112], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x385a, 0x3fbe], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3576, 0x3d52], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x35b2, 0x3d70], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3b48, 0x42ca], "candle": 0x50, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3a9c, 0x41b0], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x39e8, 0x40de], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3664, 0x3d8c], "candle": 0x30, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3560, 0x3c2e], "candle": 0x40, },
            {"zones": constants.ZONE["NO2"], "entities": [0x37ea, 0x3ecc], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x381c, 0x400c], "candle": 0x10, },
            {"zones": constants.ZONE["NO2"], "entities": [0x388a, 0x3ef4], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3916, 0x4034], "candle": 0x10, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3722, 0x3e72], "candle": 0x60, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3eb8, 0x4644, 0x3c58, 0x4394],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3e0e, 0x459a, 0x3bae, 0x42ea],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3ef4, 0x4680, 0x3c9e, 0x43d0],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x42e6, 0x4a7c, 0x40b8, 0x4812],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x412e, 0x48b0, 0x3ef6, 0x4614],
             "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x32da, 0x4358], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x35c8, 0x465a], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x34ce, 0x454c], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x34d8, 0x45a6], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3438, 0x44c0], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x33c0, 0x4466], "candle": 0x60, },
            {"zones": constants.ZONE["NO4"], "entities": [0x33f2, 0x4484], "candle": 0x60, },
            {"zones": constants.ZONE["NO4"], "entities": [0x338e, 0x4420], "candle": 0x60, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3e24, 0x4eac], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x36a4, 0x472c], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3afa, 0x4b28], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3bb8, 0x4aec], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2f64, 0x38da], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x3004, 0x393e], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2924, 0x325e], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2a3c, 0x3362], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2d7a, 0x3650], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2b4a, 0x340c], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2bfe, 0x3510], "candle": 0x20, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2bec, 0x3634], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2c64, 0x36ac], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2ca0, 0x3684], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2cf0, 0x35d0], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2782, 0x3152], "candle": 0x40, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x282c, 0x321a], "candle": 0x40, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2976, 0x3508], "candle": 0x50, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x29ee, 0x3544], "candle": 0x60, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2a5c, 0x33a0], "candle": 0x00, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2aac, 0x3404], "candle": 0x50, },
            {"zones": constants.ZONE["TOP"], "entities": [0x23f4, 0x29aa], "candle": 0x30, },
            {"zones": constants.ZONE["TOP"], "entities": [0x216a, 0x28ba], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x22aa, 0x2914], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x2318, 0x2856], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x2322, 0x2694], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x2598, 0x2b58], "candle": 0x30, },
            {"zones": constants.ZONE["RARE"], "entities": [0x24aa, 0x2a0e], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2004, 0x2568], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2298, 0x2892], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x22b6, 0x27de], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x21ee, 0x27a2], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x20f4, 0x2694], "candle": 0x10, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x278a, 0x32b8], "candle": 0x00, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2794, 0x32c2], "candle": 0x10, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x27bc, 0x32e0], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2b40, 0x36a0], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2ca8, 0x37c2], "candle": 0x00, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2aaa, 0x3600], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x26cc, 0x31be], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x28de, 0x343e], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x28f2, 0x33d0], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2d84, 0x38c6], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2ea6, 0x392a], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x302c, 0x3b50], "candle": 0x20, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x19b0, 0x1e06], "candle": 0x00, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x19f6, 0x1e60], "candle": 0x10, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x1a14, 0x1e6a], "candle": 0x10, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x1ac8, 0x1f46], "candle": 0x00, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x2152, 0x2ab4], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x21f2, 0x2b2c], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x25d0, 0x2f28], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x1e1e, 0x278a], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x1e28, 0x276c], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x1e32, 0x2762], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x1d2e, 0x2690], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x1d38, 0x2686], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x1fcc, 0x27c6], "candle": 0x00, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x233c, 0x2bea], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x2350, 0x2c94], "candle": 0x10, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1c22, 0x217c], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1c4a, 0x21fe], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1dbc, 0x237a], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1dd0, 0x22f8], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3726, 0x488a], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3780, 0x4786], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x37da, 0x48ee], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3942, 0x47d6], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x36a4, 0x470e], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x36c2, 0x46d2], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x39d8, 0x4a88], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3a14, 0x4b0a], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3a64, 0x4ab0], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3b2c, 0x4baa], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3b90, 0x4b78], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4432, 0x54c4], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x40d6, 0x515e], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x42de, 0x5316], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4388, 0x5352], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x35e6, 0x465a], "candle": 0x80, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3604, 0x4664], "candle": 0x80, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x41b2, 0x5226], "candle": 0x20, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x41bc, 0x5280], "candle": 0x10, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x212a, 0x2820], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x20b2, 0x27d0], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x22ce, 0x29c4], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x2300, 0x29e2], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x24e0, 0x2bea], "candle": 0x50, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x248e, 0x2c86], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x251a, 0x2d12], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2588, 0x2d62], "candle": 0x30, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2600, 0x2dda], "candle": 0x40, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x26c8, 0x2f06], "candle": 0x10, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x272c, 0x2efc], "candle": 0x10, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x275e, 0x2f56], "candle": 0x10, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2772, 0x2f4c], "candle": 0x10, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x279a, 0x2ef2], "candle": 0x10, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x27e0, 0x30d2], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2826, 0x2f42], "candle": 0x10, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2844, 0x2f38], "candle": 0x10, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2876, 0x2ede], "candle": 0x10, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x28da, 0x2ed4], "candle": 0x10, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x28ee, 0x30dc], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2b64, 0x32ee], "candle": 0x60, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2fee, 0x36a6], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2ff8, 0x369c], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x312e, 0x380e], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2d1e, 0x33f4], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2ca6, 0x3368], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x3232, 0x38e0], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2f30, 0x35de], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2e40, 0x353e], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3b3c, 0x4a96], "candle": 0x50, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x302e, 0x3f6a], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2fde, 0x3f2e], "candle": 0x50, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2fe8, 0x3ed4], "candle": 0x50, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2ea8, 0x3e02], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2e1c, 0x3d76], "candle": 0x60, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2e76, 0x3d9e], "candle": 0x60, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2db8, 0x3cf4], "candle": 0x60, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x36e6, 0x464a], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3c04, 0x4b5e], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3254, 0x4262], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x32fe, 0x421c], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x275a, 0x301c], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x278c, 0x3076], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x21ec, 0x2ad6], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x230e, 0x2c0c], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x250c, 0x2e28], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x23c2, 0x2ce8], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2444, 0x2d74], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2b76, 0x350a], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2bda, 0x3438], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2c48, 0x3460], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2cc0, 0x34c4], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x28a6, 0x314a], "candle": 0x40, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x295a, 0x31d6], "candle": 0x40, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2aa4, 0x3320], "candle": 0x50, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2ac2, 0x3384], "candle": 0x60, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2b30, 0x32e4], "candle": 0x50, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1d70, 0x21b2], "candle": 0x30, },
            {"addresses": [0x043c3644, 0x04491814, 0x0455cc94, 0x045e99ec, 0x0467758c, 0x048fb188, 0x049d3a58,
                           0x04aa1a74, 0x04b68b1c, 0x04c32920, 0x04cfbd60, 0x04da5768, 0x04e32804, 0x04ee3330,
                           0x04f860a4, 0x05050978, 0x050f8ea4, 0x051adeb8, 0x0526c754, 0x053f6498, 0x054b2940,
                           0x05573de4, 0x0560fc14, 0x056be958, 0x057519ac, 0x057e07ac, 0x05883f7c, 0x0590364c,
                           0x059bca38, 0x05a6eecc, 0x05af32d8, 0x0606f10c, 0x060fdd40, 0x061a77c4, 0x062478cc,
                           0x063061bc, 0x063ab014, 0x06471a3c, 0x065094f0, 0x065918ec, 0x06621d3c, 0x066b40c4,
                           0x06742edc, 0x067d0d38, 0x06862088, 0x0692c490, 0x069d2224, 0x06a61208, 0x047a3fd8],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3646, 0x04491816, 0x0455cc96, 0x045e99ee, 0x0467758e, 0x048fb18a, 0x049d3a5a,
                           0x04aa1a76, 0x04b68b1e, 0x04c32922, 0x04cfbd62, 0x04da576a, 0x04e32806, 0x04ee3332,
                           0x04f860a6, 0x0505097a, 0x050f8ea6, 0x051adeba, 0x0526c756, 0x053f649a, 0x054b2942,
                           0x05573de6, 0x0560fc16, 0x056be95a, 0x057519ae, 0x057e07ae, 0x05883f7e, 0x0590364e,
                           0x059bca3a, 0x05a6eece, 0x05af32da, 0x0606f10e, 0x060fdd42, 0x061a77c6, 0x062478ce,
                           0x063061be, 0x063ab016, 0x06471a3e, 0x065094f2, 0x065918ee, 0x06621d3e, 0x066b40c6,
                           0x06742ede, 0x067d0d3a, 0x0686208a, 0x0692c492, 0x069d2226, 0x06a6120a, 0x047a3fda],
             "enemy": constants.GLOBAL_DROP, }
        ]
    },
    {
        "name": "$1",
        "type": constants.TYPE["GOLD"],
        "id": 2,
        "tiles": [
            {"zones": constants.ZONE["CAT"], "entities": [0x2e0a, 0x36ea], "candle": 0x10, },
            {"zones": constants.ZONE["CAT"], "entities": [0x30b2, 0x397e], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x33f0, 0x3c58], "candle": 0x20, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1b9c, 0x1f16], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x35f6, 0x3c90], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2e82, 0x3d16], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2ea0, 0x3d20], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2ec8, 0x3d2a], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2edc, 0x3d34], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2f2c, 0x3d48], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2f54, 0x3d52], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2f72, 0x3d5c], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3a2e, 0x40f2], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x37fe, 0x4002], "candle": 0x10, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3e04, 0x45b8, 0x3ba4, 0x4308],
             "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x40f2, 0x48ec, 0x3eb0, 0x4664],
             "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x33ca, 0x4470], "candle": 0x60, },
            {"zones": constants.ZONE["NO4"], "entities": [0x33d4, 0x447a], "candle": 0x60, },
            {"zones": constants.ZONE["NO4"], "entities": [0x33de, 0x445c], "candle": 0x60, },
            {"zones": constants.ZONE["NO4"], "entities": [0x33e8, 0x4452], "candle": 0x60, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3fe6, 0x505a], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2d02, 0x368c], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2bf4, 0x34fc], "candle": 0x20, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2d90, 0x3774], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x29f8, 0x3382], "candle": 0x00, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x283e, 0x3362], "candle": 0x10, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2942, 0x3466], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2de8, 0x3952], "candle": 0x20, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x1a00, 0x1e4c], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1f2e, 0x250a], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x376c, 0x48da], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x37b2, 0x48d0], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x37f8, 0x48c6], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x387a, 0x48b2], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x38ac, 0x48a8], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3906, 0x489e], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3956, 0x4894], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x24e8, 0x2d26], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2c9c, 0x3354], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2e90, 0x34ee], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2e30, 0x3db2], "candle": 0x60, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2e4e, 0x3dbc], "candle": 0x60, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2e62, 0x3d94], "candle": 0x60, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2e80, 0x3d8a], "candle": 0x60, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x383a, 0x479e], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2584, 0x2df6], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x243a, 0x2d7e], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2d2e, 0x35a0], "candle": 0x10, },
            {"addresses": [0x043c3614, 0x044917e4, 0x0455cc64, 0x045e99bc, 0x0467755c, 0x048fb158, 0x049d3a28,
                           0x04aa1a44, 0x04b68aec, 0x04c328f0, 0x04cfbd30, 0x04da5738, 0x04e327d4, 0x04ee3300,
                           0x04f86074, 0x05050948, 0x050f8e74, 0x051ade88, 0x0526c724, 0x053f6468, 0x054b2910,
                           0x05573db4, 0x0560fbe4, 0x056be928, 0x0575197c, 0x057e077c, 0x05883f4c, 0x0590361c,
                           0x059bca08, 0x05a6ee9c, 0x05af32a8, 0x0606f0dc, 0x060fdd10, 0x061a7794, 0x0624789c,
                           0x0630618c, 0x063aafe4, 0x06471a0c, 0x065094c0, 0x065918bc, 0x06621d0c, 0x066b4094,
                           0x06742eac, 0x067d0d08, 0x06862058, 0x0692c460, 0x069d21f4, 0x06a611d8, 0x047a3fa8],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3648, 0x04491818, 0x0455cc98, 0x045e99f0, 0x04677590, 0x048fb18c, 0x049d3a5c,
                           0x04aa1a78, 0x04b68b20, 0x04c32924, 0x04cfbd64, 0x04da576c, 0x04e32808, 0x04ee3334,
                           0x04f860a8, 0x0505097c, 0x050f8ea8, 0x051adebc, 0x0526c758, 0x053f649c, 0x054b2944,
                           0x05573de8, 0x0560fc18, 0x056be95c, 0x057519b0, 0x057e07b0, 0x05883f80, 0x05903650,
                           0x059bca3c, 0x05a6eed0, 0x05af32dc, 0x0606f110, 0x060fdd44, 0x061a77c8, 0x062478d0,
                           0x063061c0, 0x063ab018, 0x06471a40, 0x065094f4, 0x065918f0, 0x06621d40, 0x066b40c8,
                           0x06742ee0, 0x067d0d3c, 0x0686208c, 0x0692c494, 0x069d2228, 0x06a6120c, 0x047a3fdc],
             "enemy": constants.GLOBAL_DROP, }
        ]
    }, {
        "name": "$25",
        "type": constants.TYPE["GOLD"],
        "id": 3,
        "tiles": [
            {"zones": constants.ZONE["ARE"], "entities": [0x2f78, 0x35f6], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3356, 0x39b6], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3414, 0x3ac4], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3432, 0x3ace], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x32ac, 0x38da], "candle": 0x10, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2cf2, 0x35dc], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2cca, 0x3596], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x30c6, 0x39ce], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x30e4, 0x3a14], "candle": 0x20, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1b42, 0x1ed0], "candle": 0x10, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1d04, 0x206a], "candle": 0x00, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2b08, 0x347c], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2cd4, 0x3648], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2914, 0x32ce], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x354c, 0x3c04], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3416, 0x3ab0], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3696, 0x3d62], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2e96, 0x3ce4], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2f22, 0x3dde], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3314, 0x4180], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3422, 0x42ca], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3710, 0x457c], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x354e, 0x43f6], "candle": 0x10, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3602, 0x3dd4], "candle": 0x60, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3a44, 0x43ec], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3c42, 0x4324], "candle": 0x50, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3880, 0x3f1c], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x35ba, 0x3ce2], "candle": 0x60, },
            {"zones": constants.ZONE["NO2"], "entities": [0x36d2, 0x3e36], "candle": 0x60, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3768, 0x3e54], "candle": 0x60, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3ee0, 0x4694, 0x3c80, 0x43e4],
             "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x35d2, 0x4650], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3e6a, 0x4eb6], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x409a, 0x50d2], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2a96, 0x33bc], "candle": 0x10, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2fd2, 0x390c], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2e06, 0x3786], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2988, 0x32ae], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2d0c, 0x3646], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2d16, 0x3696], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2ae6, 0x342a], "candle": 0x10, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2b2c, 0x3466], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2b40, 0x3416], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2c12, 0x3538], "candle": 0x20, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2d54, 0x3788], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2c14, 0x36ca], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2cdc, 0x3670], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x29bc, 0x3422], "candle": 0x50, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2a84, 0x340e], "candle": 0x50, },
            {"zones": constants.ZONE["RARE"], "entities": [0x22ac, 0x2888], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2338, 0x28d8], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2360, 0x28ce], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x21d0, 0x278e], "candle": 0x10, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x279e, 0x32ae], "candle": 0x10, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x276c, 0x3290], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2636, 0x31d2], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2910, 0x33ee], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x292e, 0x3452], "candle": 0x20, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x19a6, 0x1dc0], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x21ca, 0x2b40], "candle": 0x10, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1df8, 0x23b6], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1e98, 0x2438], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3b04, 0x4bb4], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x42b6, 0x5302], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4338, 0x5398], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x400e, 0x4ff6], "candle": 0x10, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x2274, 0x294c], "candle": 0x60, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x23fa, 0x2bcc], "candle": 0x50, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x27d6, 0x30aa], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2a56, 0x3244], "candle": 0x60, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2b0a, 0x32d0], "candle": 0x60, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x3264, 0x38f4], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3006, 0x3f74], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x36a0, 0x4622], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x393e, 0x48b6], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2354, 0x2c52], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x273c, 0x3030], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x27c8, 0x308a], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x23ea, 0x2cc0], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2b80, 0x3424], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2ca2, 0x347e], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2ab8, 0x332a], "candle": 0x50, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2b1c, 0x333e], "candle": 0x50, },
            {"addresses": [0x043c3610, 0x044917e0, 0x0455cc60, 0x045e99b8, 0x04677558, 0x048fb154, 0x049d3a24,
                           0x04aa1a40, 0x04b68ae8, 0x04c328ec, 0x04cfbd2c, 0x04da5734, 0x04e327d0, 0x04ee32fc,
                           0x04f86070, 0x05050944, 0x050f8e70, 0x051ade84, 0x0526c720, 0x053f6464, 0x054b290c,
                           0x05573db0, 0x0560fbe0, 0x056be924, 0x05751978, 0x057e0778, 0x05883f48, 0x05903618,
                           0x059bca04, 0x05a6ee98, 0x05af32a4, 0x0606f0d8, 0x060fdd0c, 0x061a7790, 0x06247898,
                           0x06306188, 0x063aafe0, 0x06471a08, 0x065094bc, 0x065918b8, 0x06621d08, 0x066b4090,
                           0x06742ea8, 0x067d0d04, 0x06862054, 0x0692c45c, 0x069d21f0, 0x06a611d4, 0x047a3e74],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3616, 0x044917e6, 0x0455cc66, 0x045e99be, 0x0467755e, 0x048fb15a, 0x049d3a2a,
                           0x04aa1a46, 0x04b68aee, 0x04c328f2, 0x04cfbd32, 0x04da573a, 0x04e327d6, 0x04ee3302,
                           0x04f86076, 0x0505094a, 0x050f8e76, 0x051ade8a, 0x0526c726, 0x053f646a, 0x054b2912,
                           0x05573db6, 0x0560fbe6, 0x056be92a, 0x0575197e, 0x057e077e, 0x05883f4e, 0x0590361e,
                           0x059bca0a, 0x05a6ee9e, 0x05af32aa, 0x0606f0de, 0x060fdd12, 0x061a7796, 0x0624789e,
                           0x0630618e, 0x063aafe6, 0x06471a0e, 0x065094c2, 0x065918be, 0x06621d0e, 0x066b4096,
                           0x06742eae, 0x067d0d0a, 0x0686205a, 0x0692c462, 0x069d21f6, 0x06a611da, 0x047a3faa],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3618, 0x044917e8, 0x0455cc68, 0x045e99c0, 0x04677560, 0x048fb15c, 0x049d3a2c,
                           0x04aa1a48, 0x04b68af0, 0x04c328f4, 0x04cfbd34, 0x04da573c, 0x04e327d8, 0x04ee3304,
                           0x04f86078, 0x0505094c, 0x050f8e78, 0x051ade8c, 0x0526c728, 0x053f646c, 0x054b2914,
                           0x05573db8, 0x0560fbe8, 0x056be92c, 0x05751980, 0x057e0780, 0x05883f50, 0x05903620,
                           0x059bca0c, 0x05a6eea0, 0x05af32ac, 0x0606f0e0, 0x060fdd14, 0x061a7798, 0x062478a0,
                           0x06306190, 0x063aafe8, 0x06471a10, 0x065094c4, 0x065918c0, 0x06621d10, 0x066b4098,
                           0x06742eb0, 0x067d0d0c, 0x0686205c, 0x0692c464, 0x069d21f8, 0x06a611dc, 0x047a3fac],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c361a, 0x044917ea, 0x0455cc6a, 0x045e99c2, 0x04677562, 0x048fb15e, 0x049d3a2e,
                           0x04aa1a4a, 0x04b68af2, 0x04c328f6, 0x04cfbd36, 0x04da573e, 0x04e327da, 0x04ee3306,
                           0x04f8607a, 0x0505094e, 0x050f8e7a, 0x051ade8e, 0x0526c72a, 0x053f646e, 0x054b2916,
                           0x05573dba, 0x0560fbea, 0x056be92e, 0x05751982, 0x057e0782, 0x05883f52, 0x05903622,
                           0x059bca0e, 0x05a6eea2, 0x05af32ae, 0x0606f0e2, 0x060fdd16, 0x061a779a, 0x062478a2,
                           0x06306192, 0x063aafea, 0x06471a12, 0x065094c6, 0x065918c2, 0x06621d12, 0x066b409a,
                           0x06742eb2, 0x067d0d0e, 0x0686205e, 0x0692c466, 0x069d21fa, 0x06a611de, 0x047a3fae],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c361c, 0x044917ec, 0x0455cc6c, 0x045e99c4, 0x04677564, 0x048fb160, 0x049d3a30,
                           0x04aa1a4c, 0x04b68af4, 0x04c328f8, 0x04cfbd38, 0x04da5740, 0x04e327dc, 0x04ee3308,
                           0x04f8607c, 0x05050950, 0x050f8e7c, 0x051ade90, 0x0526c72c, 0x053f6470, 0x054b2918,
                           0x05573dbc, 0x0560fbec, 0x056be930, 0x05751984, 0x057e0784, 0x05883f54, 0x05903624,
                           0x059bca10, 0x05a6eea4, 0x05af32b0, 0x0606f0e4, 0x060fdd18, 0x061a779c, 0x062478a4,
                           0x06306194, 0x063aafec, 0x06471a14, 0x065094c8, 0x065918c4, 0x06621d14, 0x066b409c,
                           0x06742eb4, 0x067d0d10, 0x06862060, 0x0692c468, 0x069d21fc, 0x06a611e0, 0x047a3fb0],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c361e, 0x044917ee, 0x0455cc6e, 0x045e99c6, 0x04677566, 0x048fb162, 0x049d3a32,
                           0x04aa1a4e, 0x04b68af6, 0x04c328fa, 0x04cfbd3a, 0x04da5742, 0x04e327de, 0x04ee330a,
                           0x04f8607e, 0x05050952, 0x050f8e7e, 0x051ade92, 0x0526c72e, 0x053f6472, 0x054b291a,
                           0x05573dbe, 0x0560fbee, 0x056be932, 0x05751986, 0x057e0786, 0x05883f56, 0x05903626,
                           0x059bca12, 0x05a6eea6, 0x05af32b2, 0x0606f0e6, 0x060fdd1a, 0x061a779e, 0x062478a6,
                           0x06306196, 0x063aafee, 0x06471a16, 0x065094ca, 0x065918c6, 0x06621d16, 0x066b409e,
                           0x06742eb6, 0x067d0d12, 0x06862062, 0x0692c46a, 0x069d21fe, 0x06a611e2, 0x047a3fb2],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3620, 0x044917f0, 0x0455cc70, 0x045e99c8, 0x04677568, 0x048fb164, 0x049d3a34,
                           0x04aa1a50, 0x04b68af8, 0x04c328fc, 0x04cfbd3c, 0x04da5744, 0x04e327e0, 0x04ee330c,
                           0x04f86080, 0x05050954, 0x050f8e80, 0x051ade94, 0x0526c730, 0x053f6474, 0x054b291c,
                           0x05573dc0, 0x0560fbf0, 0x056be934, 0x05751988, 0x057e0788, 0x05883f58, 0x05903628,
                           0x059bca14, 0x05a6eea8, 0x05af32b4, 0x0606f0e8, 0x060fdd1c, 0x061a77a0, 0x062478a8,
                           0x06306198, 0x063aaff0, 0x06471a18, 0x065094cc, 0x065918c8, 0x06621d18, 0x066b40a0,
                           0x06742eb8, 0x067d0d14, 0x06862064, 0x0692c46c, 0x069d2200, 0x06a611e4, 0x047a3fb4],
             "enemy": constants.GLOBAL_DROP, }
        ]
    }, {
        "name": "$50",
        "type": constants.TYPE["GOLD"],
        "id": 4,
        "tiles": [
            {"zones": constants.ZONE["ARE"], "entities": [0x2f50, 0x35e2], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3522, 0x3baa], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x309a, 0x36f0], "candle": 0x10, },
            {"zones": constants.ZONE["CAT"], "entities": [0x304e, 0x3942], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3300, 0x3bc2], "candle": 0x20, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1b56, 0x1ea8], "candle": 0x00, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2f4a, 0x3904], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x31d4, 0x4072], "candle": 0x10, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3968, 0x411c], "candle": 0x50, },
            {"zones": constants.ZONE["NO2"], "entities": [0x39c0, 0x40d4], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3510, 0x3c4c], "candle": 0x40, },
            {"zones": constants.ZONE["NO2"], "entities": [0x38da, 0x3fbc], "candle": 0x10, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3902, 0x3efe], "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3de6, 0x4572, 0x3b86, 0x42c2],
             "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x32d0, 0x4330], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3398, 0x442a], "candle": 0x60, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3b0e, 0x4b14], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2f82, 0x38c6], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x28e8, 0x320e], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2a5a, 0x3376], "candle": 0x10, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2ba4, 0x34d4], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x30cc, 0x3a10], "candle": 0x20, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2c32, 0x35c6], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2c6e, 0x36a2], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2994, 0x34fe], "candle": 0x50, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2478, 0x2a2c], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2090, 0x2630], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x1fdc, 0x254a], "candle": 0x10, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2ad2, 0x35ec], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x262c, 0x3268], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2d8e, 0x38bc], "candle": 0x20, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x196a, 0x1e1a], "candle": 0x00, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x1a6e, 0x1ee2], "candle": 0x00, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x209e, 0x29f6], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x1f7c, 0x2816], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1ab0, 0x2046], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x380c, 0x47a4], "candle": 0x00, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x259e, 0x2ae6], "candle": 0x50, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x24a2, 0x2c68], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2632, 0x2df8], "candle": 0x40, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x283a, 0x30b4], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2bdc, 0x32f8], "candle": 0x60, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2c42, 0x330e], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3b46, 0x4aaa], "candle": 0x50, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2da4, 0x3cfe], "candle": 0x60, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x32f4, 0x4230], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x261a, 0x2ebe], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x219c, 0x2a72], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x223c, 0x2b08], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2336, 0x2bee], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2570, 0x2e50], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x23a4, 0x2c8e], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x23b8, 0x2cde], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x24bc, 0x2da6], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2840, 0x3120], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2c3e, 0x3456], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2c70, 0x3514], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2b26, 0x32da], "candle": 0x50, },
            {"addresses": [0x043c3622, 0x044917f2, 0x0455cc72, 0x045e99ca, 0x0467756a, 0x048fb166, 0x049d3a36,
                           0x04aa1a52, 0x04b68afa, 0x04c328fe, 0x04cfbd3e, 0x04da5746, 0x04e327e2, 0x04ee330e,
                           0x04f86082, 0x05050956, 0x050f8e82, 0x051ade96, 0x0526c732, 0x053f6476, 0x054b291e,
                           0x05573dc2, 0x0560fbf2, 0x056be936, 0x0575198a, 0x057e078a, 0x05883f5a, 0x0590362a,
                           0x059bca16, 0x05a6eeaa, 0x05af32b6, 0x0606f0ea, 0x060fdd1e, 0x061a77a2, 0x062478aa,
                           0x0630619a, 0x063aaff2, 0x06471a1a, 0x065094ce, 0x065918ca, 0x06621d1a, 0x066b40a2,
                           0x06742eba, 0x067d0d16, 0x06862066, 0x0692c46e, 0x069d2202, 0x06a611e6, 0x047a3fb6],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3624, 0x044917f4, 0x0455cc74, 0x045e99cc, 0x0467756c, 0x048fb168, 0x049d3a38,
                           0x04aa1a54, 0x04b68afc, 0x04c32900, 0x04cfbd40, 0x04da5748, 0x04e327e4, 0x04ee3310,
                           0x04f86084, 0x05050958, 0x050f8e84, 0x051ade98, 0x0526c734, 0x053f6478, 0x054b2920,
                           0x05573dc4, 0x0560fbf4, 0x056be938, 0x0575198c, 0x057e078c, 0x05883f5c, 0x0590362c,
                           0x059bca18, 0x05a6eeac, 0x05af32b8, 0x0606f0ec, 0x060fdd20, 0x061a77a4, 0x062478ac,
                           0x0630619c, 0x063aaff4, 0x06471a1c, 0x065094d0, 0x065918cc, 0x06621d1c, 0x066b40a4,
                           0x06742ebc, 0x067d0d18, 0x06862068, 0x0692c470, 0x069d2204, 0x06a611e8, 0x047a3fb8],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3626, 0x044917f6, 0x0455cc76, 0x045e99ce, 0x0467756e, 0x048fb16a, 0x049d3a3a,
                           0x04aa1a56, 0x04b68afe, 0x04c32902, 0x04cfbd42, 0x04da574a, 0x04e327e6, 0x04ee3312,
                           0x04f86086, 0x0505095a, 0x050f8e86, 0x051ade9a, 0x0526c736, 0x053f647a, 0x054b2922,
                           0x05573dc6, 0x0560fbf6, 0x056be93a, 0x0575198e, 0x057e078e, 0x05883f5e, 0x0590362e,
                           0x059bca1a, 0x05a6eeae, 0x05af32ba, 0x0606f0ee, 0x060fdd22, 0x061a77a6, 0x062478ae,
                           0x0630619e, 0x063aaff6, 0x06471a1e, 0x065094d2, 0x065918ce, 0x06621d1e, 0x066b40a6,
                           0x06742ebe, 0x067d0d1a, 0x0686206a, 0x0692c472, 0x069d2206, 0x06a611ea, 0x047a3fba],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c3628, 0x044917f8, 0x0455cc78, 0x045e99d0, 0x04677570, 0x048fb16c, 0x049d3a3c,
                           0x04aa1a58, 0x04b68b00, 0x04c32904, 0x04cfbd44, 0x04da574c, 0x04e327e8, 0x04ee3314,
                           0x04f86088, 0x0505095c, 0x050f8e88, 0x051ade9c, 0x0526c738, 0x053f647c, 0x054b2924,
                           0x05573dc8, 0x0560fbf8, 0x056be93c, 0x05751990, 0x057e0790, 0x05883f60, 0x05903630,
                           0x059bca1c, 0x05a6eeb0, 0x05af32bc, 0x0606f0f0, 0x060fdd24, 0x061a77a8, 0x062478b0,
                           0x063061a0, 0x063aaff8, 0x06471a20, 0x065094d4, 0x065918d0, 0x06621d20, 0x066b40a8,
                           0x06742ec0, 0x067d0d1c, 0x0686206c, 0x0692c474, 0x069d2208, 0x06a611ec, 0x047a3fbc],
             "enemy": constants.GLOBAL_DROP, }
        ]
    }, {
        "name": "$100",
        "type": constants.TYPE["GOLD"],
        "id": 5,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["ARE"], "entities": [0x3374, 0x3a56], "candle": 0x10, },
            {"zones": constants.ZONE["ARE"], "entities": [0x328e, 0x395c], "candle": 0x10, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2d38, 0x3622], "candle": 0x10, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2cd4, 0x356e], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x33d2, 0x3c80], "candle": 0x20, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1c14, 0x1f7a], "candle": 0x00, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2e32, 0x3800], "candle": 0x10, },
            {"zones": constants.ZONE["LIB"], "entities": [0x372c, 0x3dda], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x34b6, 0x3a56], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x301c, 0x3e7e], "candle": 0x10, },
            {"zones": constants.ZONE["NO1"], "entities": [0x386e, 0x4072], "candle": 0x50, },
            {"zones": constants.ZONE["NO1"], "entities": [0x3a76, 0x42d4], "candle": 0x50, },
            {"zones": constants.ZONE["NO2"], "entities": [0x365a, 0x3d82], "candle": 0x30, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3858, 0x3f26], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x386c, 0x4016], "candle": 0x10, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3280, 0x436c], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3b36, 0x4af6], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2fe6, 0x3916], "candle": 0x20, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2b90, 0x3542], "candle": 0x20, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2c78, 0x35f8], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2cd2, 0x35bc], "candle": 0x10, },
            {"zones": constants.ZONE["TOP"], "entities": [0x221e, 0x28f6], "candle": 0x60, },
            {"zones": constants.ZONE["RARE"], "entities": [0x24a0, 0x2a18], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x22a2, 0x27e8], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x21da, 0x2716], "candle": 0x10, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2e1a, 0x3916], "candle": 0x20, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x1bb8, 0x1fb4], "candle": 0x00, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x2486, 0x2db6], "candle": 0x10, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1c72, 0x2208], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1d62, 0x23de], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3910, 0x4916], "candle": 0x00, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x2120, 0x282a], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x204e, 0x271c], "candle": 0x50, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x258a, 0x2bf4], "candle": 0x50, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x259c, 0x2d58], "candle": 0x30, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2722, 0x30c8], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x3192, 0x37fa], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x30a2, 0x3728], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3b6e, 0x4a8c], "candle": 0x50, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x32c2, 0x423a], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2552, 0x2e00], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2458, 0x2d4c], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2d6a, 0x35b4], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2b94, 0x3532], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2c2a, 0x34f6], "candle": 0x10, },
            {"addresses": [0x0b6c04], "enemy": 5, },
            {"addresses": [0x043c362a, 0x044917fa, 0x0455cc7a, 0x045e99d2, 0x04677572, 0x048fb16e, 0x049d3a3e,
                           0x04aa1a5a, 0x04b68b02, 0x04c32906, 0x04cfbd46, 0x04da574e, 0x04e327ea, 0x04ee3316,
                           0x04f8608a, 0x0505095e, 0x050f8e8a, 0x051ade9e, 0x0526c73a, 0x053f647e, 0x054b2926,
                           0x05573dca, 0x0560fbfa, 0x056be93e, 0x05751992, 0x057e0792, 0x05883f62, 0x05903632,
                           0x059bca1e, 0x05a6eeb2, 0x05af32be, 0x0606f0f2, 0x060fdd26, 0x061a77aa, 0x062478b2,
                           0x063061a2, 0x063aaffa, 0x06471a22, 0x065094d6, 0x065918d2, 0x06621d22, 0x066b40aa,
                           0x06742ec2, 0x067d0d1e, 0x0686206e, 0x0692c476, 0x069d220a, 0x06a611ee, 0x047a3fbe],
             "enemy": constants.GLOBAL_DROP, },
            {"addresses": [0x043c362c, 0x044917fc, 0x0455cc7c, 0x045e99d4, 0x04677574, 0x048fb170, 0x049d3a40,
                           0x04aa1a5c, 0x04b68b04, 0x04c32908, 0x04cfbd48, 0x04da5750, 0x04e327ec, 0x04ee3318,
                           0x04f8608c, 0x05050960, 0x050f8e8c, 0x051adea0, 0x0526c73c, 0x053f6480, 0x054b2928,
                           0x05573dcc, 0x0560fbfc, 0x056be940, 0x05751994, 0x057e0794, 0x05883f64, 0x05903634,
                           0x059bca20, 0x05a6eeb4, 0x05af32c0, 0x0606f0f4, 0x060fdd28, 0x061a77ac, 0x062478b4,
                           0x063061a4, 0x063aaffc, 0x06471a24, 0x065094d8, 0x065918d4, 0x06621d24, 0x066b40ac,
                           0x06742ec4, 0x067d0d20, 0x06862070, 0x0692c478, 0x069d220c, 0x06a611f0, 0x047a3fc0],
             "enemy": constants.GLOBAL_DROP, }
        ]
    }, {
        "name": "$250",
        "type": constants.TYPE["GOLD"],
        "id": 6,
        "tiles": [
            {"zones": constants.ZONE["CAT"], "entities": [0x309e, 0x399c], "candle": 0x10, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2e46, 0x377e], "candle": 0x10, },
            {"zones": constants.ZONE["LIB"], "entities": [0x381c, 0x3ede], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2f0e, 0x3d3e], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3486, 0x428e], "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x358c, 0x4592], "candle": 0x50, },
            {"zones": constants.ZONE["NO4"], "entities": [0x392e, 0x48b2], "candle": 0x00, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2822, 0x31f2], "candle": 0x40, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x294c, 0x345c], "candle": 0x10, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x2346, 0x2c44], "candle": 0x10, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1ba0, 0x2118], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3834, 0x48bc], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3640, 0x46aa], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x364a, 0x46a0], "candle": 0x10, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x252e, 0x2d08], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2f3e, 0x3ee8], "candle": 0x50, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3592, 0x45a0], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x27aa, 0x3094], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2964, 0x31e0], "candle": 0x40, },
            {"addresses": [0x043c364a, 0x0449181a, 0x0455cc9a, 0x045e99f2, 0x04677592, 0x048fb18e, 0x049d3a5e,
                           0x04aa1a7a, 0x04b68b22, 0x04c32926, 0x04cfbd66, 0x04da576e, 0x04e3280a, 0x04ee3336,
                           0x04f860aa, 0x0505097e, 0x050f8eaa, 0x051adebe, 0x0526c75a, 0x053f649e, 0x054b2946,
                           0x05573dea, 0x0560fc1a, 0x056be95e, 0x057519b2, 0x057e07b2, 0x05883f82, 0x05903652,
                           0x059bca3e, 0x05a6eed2, 0x05af32de, 0x0606f112, 0x060fdd46, 0x061a77ca, 0x062478d2,
                           0x063061c2, 0x063ab01a, 0x06471a42, 0x065094f6, 0x065918f2, 0x06621d42, 0x066b40ca,
                           0x06742ee2, 0x067d0d3e, 0x0686208e, 0x0692c496, 0x069d222a, 0x06a6120e, 0x047a3fde],
             "enemy": constants.GLOBAL_DROP, }
        ]
    }, {
        "name": "$400",
        "type": constants.TYPE["GOLD"],
        "id": 7,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NO4"], "entities": [0x328a, 0x4376], "candle": 0x50, },
            {"zones": constants.ZONE["TOP"], "entities": [0x230e, 0x269e], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x239a, 0x27c0], "candle": 0x60, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x235a, 0x2ce4], "candle": 0x10, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2fe4, 0x36b0], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x3b78, 0x4a82], "candle": 0x50, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x24a8, 0x2d2e], "candle": 0x20, },
            {"addresses": [0x0b7464], "enemy": 19, },
            {"addresses": [0x0b6e34], "enemy": 25, },
            {"addresses": [0x0b6bb4], "enemy": 32, },
            {"addresses": [0x043c364c, 0x0449181c, 0x0455cc9c, 0x045e99f4, 0x04677594, 0x048fb190, 0x049d3a60,
                           0x04aa1a7c, 0x04b68b24, 0x04c32928, 0x04cfbd68, 0x04da5770, 0x04e3280c, 0x04ee3338,
                           0x04f860ac, 0x05050980, 0x050f8eac, 0x051adec0, 0x0526c75c, 0x053f64a0, 0x054b2948,
                           0x05573dec, 0x0560fc1c, 0x056be960, 0x057519b4, 0x057e07b4, 0x05883f84, 0x05903654,
                           0x059bca40, 0x05a6eed4, 0x05af32e0, 0x0606f114, 0x060fdd48, 0x061a77cc, 0x062478d4,
                           0x063061c4, 0x063ab01c, 0x06471a44, 0x065094f8, 0x065918f4, 0x06621d44, 0x066b40cc,
                           0x06742ee4, 0x067d0d40, 0x06862090, 0x0692c498, 0x069d222c, 0x06a61210, 0x047a3fe0],
             "enemy": constants.GLOBAL_DROP, }
        ]
    }, {
        "name": "$1000",
        "type": constants.TYPE["GOLD"],
        "id": 9,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["ARE"], "entities": [0x318a, 0x3844], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2130, 0x26b2], "candle": 0x10, },
            {"addresses": [0x0b83cc], "enemy": 40, }
        ]
    }, {
        "name": "$2000",
        "type": constants.TYPE["GOLD"],
        "id": 10,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NO4"], "entities": [0x38de, 0x48e4], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x35e2, 0x455a], "candle": 0x00, },
            {"addresses": [0x0b859c], "enemy": 50, }
        ]
    }, {
        "name": "Dagger",
        "type": constants.TYPE["SUBWEAPON"],
        "id": 14,
        "tiles": [
            {"zones": constants.ZONE["RNZ0"], "addresses": [0x04f883c4], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3158, 0x3790], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2fb8, 0x3d98], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x327e, 0x40fe], "candle": 0x10, },
            {"zones": constants.ZONE["NO1"], "entities": [0x37ec, 0x4018], "candle": 0x50, },
            {"zones": constants.ZONE["NO2"], "entities": [0x34f2, 0x3c60], "candle": 0x40, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3eae, 0x463a, 0x3c4e, 0x438a],
             "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3424, 0x44ca], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x29f6, 0x331c], "candle": 0x20, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2c96, 0x368e], "candle": 0x10, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2714, 0x30f8], "candle": 0x40, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2040, 0x25ea], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3730, 0x4812], "candle": 0x00, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x20e4, 0x2762], "candle": 0x50, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x265a, 0x2e0c], "candle": 0x40, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2d32, 0x33ea], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2ec6, 0x3dee], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x22b4, 0x2b62], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2be4, 0x3442], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2914, 0x31a4], "candle": 0x40, }
        ]
    }, {
        "name": "Axe",
        "type": constants.TYPE["SUBWEAPON"],
        "id": 15,
        "tiles": [
            {"zones": constants.ZONE["NZ0"], "addresses": [0x054b372c], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["RNZ0"], "addresses": [0x04f883d0], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["ARE"], "entities": [0x30e0, 0x3772], "candle": 0x10, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3490, 0x3d84], "candle": 0x10, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1c0a, 0x1f5c], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x34ea, 0x4342], "candle": 0x00, },
            {"zones": constants.ZONE["NO2"], "entities": [0x389e, 0x4020], "candle": 0x10, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3528, 0x45ba], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x28d4, 0x31f0], "candle": 0x20, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x28cc, 0x359e], "candle": 0x50, },
            {"zones": constants.ZONE["TOP"], "entities": [0x232c, 0x2676], "candle": 0x60, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2072, 0x25cc], "candle": 0x10, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2cb2, 0x37d6], "candle": 0x10, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x1ab4, 0x2004], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x43f6, 0x537a], "candle": 0x00, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2812, 0x2ee8], "candle": 0x10, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x308e, 0x370a], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2f98, 0x3eca], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2188, 0x2a90], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2a5e, 0x3398], "candle": 0x50, },
            {"addresses": [0x0b83a4], "enemy": 12, },
            {"addresses": [0x0b5964], "enemy": 30, }
        ]
    }, {
        "name": "Cross",
        "type": constants.TYPE["SUBWEAPON"],
        "id": 16,
        "tiles": [
            {"zones": constants.ZONE["NZ0"], "addresses": [0x054b371c], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["RNZ0"], "addresses": [0x04f883c0], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["ST0"], "entities": [0x2762, 0x28a2], "candle": 0x30, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2b92, 0x33be], "candle": 0x00, },
            {"zones": constants.ZONE["TOP"], "entities": [0x22c8, 0x273e], "candle": 0x30, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2f80, 0x36ba], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2ef8, 0x3e3e], "candle": 0x00, },
            {"zones": constants.ZONE["RNO4"], "entities": [0x2de0, 0x3ce0], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1b18, 0x20cc], "candle": 0x30, }
        ]
    }, {
        "name": "Holy Water",
        "type": constants.TYPE["SUBWEAPON"],
        "id": 17,
        "tiles": [
            {"zones": constants.ZONE["RNZ0"], "addresses": [0x04f883d4], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["ST0"], "entities": [0x26d6, 0x28d4], "candle": 0x20, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3130, 0x3786], "candle": 0x10, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1b38, 0x1ec6], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x2e3c, 0x3e2e], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x35e4, 0x4464], "candle": 0x10, },
            {"zones": constants.ZONE["NO2"], "entities": [0x370e, 0x3dfa], "candle": 0x40, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x3ed6, 0x4662, 0x3c76, 0x43b2],
             "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x3474, 0x44f2], "candle": 0x00, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2f6e, 0x38d0], "candle": 0x20, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2520, 0x2e82], "candle": 0x60, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x25d4, 0x3062], "candle": 0x60, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x26b0, 0x303a], "candle": 0x60, },
            {"zones": constants.ZONE["TOP"], "entities": [0x2192, 0x2752], "candle": 0x20, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2054, 0x25e0], "candle": 0x10, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x19c4, 0x1dde], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x3988, 0x47f4], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4464, 0x54b0], "candle": 0x10, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2b82, 0x3320], "candle": 0x40, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x3296, 0x38fe], "candle": 0x00, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2750, 0x3012], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x26d0, 0x2fa6], "candle": 0x60, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x278e, 0x308c], "candle": 0x60, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2860, 0x3050], "candle": 0x60, },
            {"zones": constants.ZONE["RTOP"], "entities": [0x1c26, 0x205e], "candle": 0x20, }
        ]
    }, {
        "name": "Stopwatch",
        "type": constants.TYPE["SUBWEAPON"],
        "id": 18,
        "tiles": [
            {"zones": constants.ZONE["RNZ0"], "addresses": [0x04f883d8], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2cb6, 0x35aa], "candle": 0x20, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3736, 0x3ef2], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x333c, 0x41bc], "candle": 0x10, },
            {"zones": constants.ZONE["NO2"], "entities": [0x39f2, 0x4160], "candle": 0x00, },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "entities": [0x4340, 0x4a72, 0x4112, 0x4808],
             "candle": 0x00, },
            {"zones": constants.ZONE["NO4"], "entities": [0x337a, 0x440c], "candle": 0x60, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2686, 0x31c8], "candle": 0x20, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1c5e, 0x20fa], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x414e, 0x514a], "candle": 0x10, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x2510, 0x2ccc], "candle": 0x00, },
            {"zones": constants.ZONE["RNO3"], "entities": [0x2f12, 0x35f2], "candle": 0x00, }
        ]
    }, {
        "name": "Bible",
        "type": constants.TYPE["SUBWEAPON"],
        "id": 19,
        "tiles": [
            {"zones": constants.ZONE["NZ0"], "addresses": [0x054b3724], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["RNZ0"], "addresses": [0x04f883c8], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2c66, 0x3546], "candle": 0x20, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2b1c, 0x3486], "candle": 0x10, },
            {"zones": constants.ZONE["NO0"], "entities": [0x3350, 0x41da], "candle": 0x20, },
            {"zones": constants.ZONE["NO1"], "entities": [0x39ea, 0x41b2], "candle": 0x50, },
            {"zones": constants.ZONE["NO2"], "entities": [0x3808, 0x3f30], "candle": 0x00, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x25fa, 0x3128], "candle": 0x20, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x208a, 0x2a00], "candle": 0x10, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4112, 0x5136], "candle": 0x20, },
            {"zones": constants.ZONE["RNO1"], "entities": [0x1fae, 0x2686], "candle": 0x50, },
            {"zones": constants.ZONE["RNO2"], "entities": [0x28c6, 0x30be], "candle": 0x00, }
        ]
    }, {
        "name": "Rebound Stone",
        "type": constants.TYPE["SUBWEAPON"],
        "id": 20,
        "tiles": [
            {"zones": constants.ZONE["NZ0"], "addresses": [0x054b3718], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["RNZ0"], "addresses": [0x04f883bc], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3108, 0x377c], "candle": 0x10, },
            {"zones": constants.ZONE["CAT"], "entities": [0x2c5c, 0x353c], "candle": 0x20, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3332, 0x3bd6], "candle": 0x20, },
            {"zones": constants.ZONE["CHI"], "entities": [0x1bd8, 0x1f8e], "candle": 0x00, },
            {"zones": constants.ZONE["NO0"], "entities": [0x31c0, 0x40ae], "candle": 0x10, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x3018, 0x3920], "candle": 0x20, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x28e0, 0x331e], "candle": 0x50, },
            {"zones": constants.ZONE["TOP"], "entities": [0x21ba, 0x28d8], "candle": 0x60, },
            {"zones": constants.ZONE["RARE"], "entities": [0x2068, 0x25d6], "candle": 0x10, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2604, 0x311e], "candle": 0x20, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x2d52, 0x38b2], "candle": 0x20, },
            {"zones": constants.ZONE["RCHI"], "entities": [0x1bae, 0x1f0a], "candle": 0x00, },
            {"zones": constants.ZONE["RNO0"], "entities": [0x4252, 0x51e0], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2782, 0x309e], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2a68, 0x32f8], "candle": 0x50, }
        ]
    }, {
        "name": "Vibhuti",
        "type": constants.TYPE["SUBWEAPON"],
        "id": 21,
        "tiles": [
            {"zones": constants.ZONE["RNZ0"], "addresses": [0x04f883cc], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["CAT"], "entities": [0x3170, 0x39ec], "candle": 0x00, },
            {"zones": constants.ZONE["DAI"], "entities": [0x2fa4, 0x3954], "candle": 0x10, },
            {"zones": constants.ZONE["NZ0"], "entities": [0x2c1c, 0x354c], "candle": 0x20, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x2494, 0x2f0e], "candle": 0x60, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x25de, 0x306c], "candle": 0x60, },
            {"zones": constants.ZONE["NZ1"], "entities": [0x26a6, 0x3012], "candle": 0x60, },
            {"zones": constants.ZONE["RCAT"], "entities": [0x28ac, 0x340c], "candle": 0x00, },
            {"zones": constants.ZONE["RDAI"], "entities": [0x2454, 0x2d84], "candle": 0x10, },
            {"zones": constants.ZONE["RNZ0"], "entities": [0x2462, 0x2d38], "candle": 0x20, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2720, 0x2f10], "candle": 0x60, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x2784, 0x30aa], "candle": 0x60, },
            {"zones": constants.ZONE["RNZ1"], "entities": [0x286a, 0x303c], "candle": 0x60, }
        ]
    }, {
        "name": "Agunea",
        "type": constants.TYPE["SUBWEAPON"],
        "id": 22,
        "tiles": [
            {"zones": constants.ZONE["NZ0"], "addresses": [0x054b3714], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["RNZ0"], "addresses": [0x04f883b8], "noOffset": True, "tank": True, },
            {"zones": constants.ZONE["ARE"], "entities": [0x3504, 0x3b82], "candle": 0x10, },
            {"zones": constants.ZONE["RARE"], "entities": [0x20cc, 0x263a], "candle": 0x10, }
        ]
    }, {
        "name": "Heart Vessel",
        "type": constants.TYPE["POWERUP"],
        "id": 12,
        "blacklist": [0x049d3674, 0x049d3676],
        "tiles": [
            {"zones": constants.ZONE["NO2"], "index": 1, "entities": [0x3718, 0x3e7c], },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "index": 0, "entities": [0x3e68, 0x45f4,
                                                                                               0x3c08, 0x4344], },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "index": 7, "entities": [0x4066, 0x47f2, 0x3e1a,
                                                                                               0x4556], },
            {"zones": constants.ZONE["NZ0"], "index": 1, "entities": [0x2eec, 0x3844], },
            {"zones": constants.ZONE["TOP"], "index": 15, "entities": [0x25f2, 0x2b8a], },
            {"zones": constants.ZONE["TOP"], "index": 16, "entities": [0x25de, 0x2b9e], },
            {"zones": constants.ZONE["TOP"], "index": 18, "entities": [0x2250, 0x2748], },
            {"zones": constants.ZONE["NZ1"], "index": 11, "entities": [0x2458, 0x2e64], },
            {"zones": constants.ZONE["NO1"], "index": 2, "entities": [0x3b34, 0x4220], },
            {"zones": constants.ZONE["NO0"], "index": 2, "entities": [0x367a, 0x44fa], },
            {"zones": constants.ZONE["NO0"], "index": 9, "entities": [0x36ca, 0x454a], },
            {"zones": [constants.ZONE["NO4"], constants.ZONE["NO4"]], "index": 0, "entities": [0x3316, 0x439e,
                                                                                               0x380c, 0x4ace], },
            {"zones": constants.ZONE["NO4"], "index": 29, "entities": [0x4176, 0x5208], },
            {"zones": constants.ZONE["CAT"], "index": 6, "entities": [0x2ea0, 0x3730], },
            {"zones": constants.ZONE["CAT"], "index": 10, "entities": [0x31a2, 0x3a82], },
            {"zones": constants.ZONE["ARE"], "index": 0, "entities": [0x3162, 0x3768], },
            {"zones": constants.ZONE["RTOP"], "index": 6, "entities": [0x1d52, 0x2176], },
            {"zones": constants.ZONE["RTOP"], "index": 8, "entities": [0x1d34, 0x218a], },
            {"zones": constants.ZONE["RTOP"], "index": 10, "entities": [0x1d20, 0x219e], },
            {"zones": constants.ZONE["RNZ1"], "index": 10, "entities": [0x25e0, 0x2e2a], },
            {"zones": constants.ZONE["RNO1"], "index": 0, "entities": [0x2058, 0x26fe], },
            {"zones": constants.ZONE["RNO0"], "index": 4, "entities": [0x3bb8, 0x4c18], },
            {"zones": constants.ZONE["RNO4"], "index": 7, "entities": [0x31dc, 0x4154], },
            {"zones": constants.ZONE["RNO4"], "index": 15, "entities": [0x2e12, 0x3dc6], },
            {"zones": constants.ZONE["RCAT"], "index": 10, "entities": [0x2974, 0x348e], },
            {"zones": constants.ZONE["RCAT"], "index": 15, "entities": [0x2816, 0x333a], },
            {"zones": constants.ZONE["RNO3"], "index": 3, "entities": [0x2e5e, 0x3566], },
            {"zones": constants.ZONE["RNZ0"], "index": 1, "entities": [0x26b0, 0x2f7c], },
            {"zones": constants.ZONE["RDAI"], "index": 5, "entities": [0x1fae, 0x27e4], },
            {"zones": constants.ZONE["RDAI"], "index": 17, "entities": [0x25a8, 0x2f00], },
            {"zones": constants.ZONE["RARE"], "index": 5, "entities": [0x219e, 0x27ac], },
            {"zones": constants.ZONE["RARE"], "index": 7, "entities": [0x21b2, 0x27c0], },
            {"zones": constants.ZONE["RNO2"], "index": 11, "entities": [0x2aa6, 0x329e], }
        ]
    }, {
        "name": "Life Vessel",
        "type": constants.TYPE["POWERUP"],
        "id": 23,
        "blacklist": [0x049d3674, 0x049d3676],
        "tiles": [
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "index": 1, "entities": [0x3e86, 0x4612,
                                                                                               0x3c26, 0x4362], },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "index": 6, "entities": [0x4228, 0x49b4,
                                                                                               0x400e, 0x474a], },
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "index": 8, "entities": [0x41ec, 0x491e,
                                                                                               0x3fd2, 0x4696], },
            {"zones": constants.ZONE["NZ0"], "index": 3, "entities": [0x2a28, 0x338a], },
            {"zones": constants.ZONE["DAI"], "index": 12, "entities": [0x2d9c, 0x36ca], },
            {"zones": constants.ZONE["TOP"], "index": 13, "entities": [0x25d4, 0x2b80], },
            {"zones": constants.ZONE["TOP"], "index": 14, "entities": [0x25e8, 0x2b94], },
            {"zones": constants.ZONE["NZ1"], "index": 10, "entities": [0x243a, 0x2e5a], },
            {"zones": constants.ZONE["NO1"], "index": 5, "entities": [0x3bc0, 0x4450], },
            {"zones": constants.ZONE["NO0"], "index": 0, "entities": [0x3652, 0x44d2], },
            {"zones": constants.ZONE["NO0"], "index": 8, "entities": [0x36c0, 0x4540], },
            {"zones": constants.ZONE["NO4"], "index": 1, "entities": [0x3334, 0x43bc], },
            {"zones": constants.ZONE["NO4"], "index": 28, "entities": [0x4130, 0x51fe], },
            {"zones": constants.ZONE["NO4"], "index": 6, "entities": [0x3f6e, 0x5000], },
            {"zones": constants.ZONE["NO4"], "index": 5, "entities": [0x3a64, 0x4cea], },
            {"zones": constants.ZONE["NO4"], "index": 24, "entities": [0x3cee, 0x4e70], },
            {"zones": constants.ZONE["CAT"], "index": 9, "entities": [0x3198, 0x3a78], },
            {"zones": constants.ZONE["RTOP"], "index": 9, "entities": [0x1d2a, 0x2194], },
            {"zones": constants.ZONE["RTOP"], "index": 7, "entities": [0x1d48, 0x2180], },
            {"zones": constants.ZONE["RTOP"], "index": 5, "entities": [0x1d5c, 0x216c], },
            {"zones": constants.ZONE["RNZ1"], "index": 9, "entities": [0x25c2, 0x2e34], },
            {"zones": constants.ZONE["RNO1"], "index": 3, "entities": [0x21de, 0x28d4], },
            {"zones": constants.ZONE["RNO0"], "index": 3, "entities": [0x3c1c, 0x4c22], },
            {"zones": constants.ZONE["RNO4"], "index": 12, "entities": [0x3b96, 0x4af0], },
            {"zones": constants.ZONE["RNO4"], "index": 6, "entities": [0x336c, 0x4122], },
            {"zones": constants.ZONE["RCAT"], "index": 16, "entities": [0x2820, 0x3344], },
            {"zones": constants.ZONE["RCAT"], "index": 9, "entities": [0x296a, 0x3498], },
            {"zones": constants.ZONE["RNO3"], "index": 8, "entities": [0x2ce2, 0x33ae], },
            {"zones": constants.ZONE["RNZ0"], "index": 2, "entities": [0x26f6, 0x2fc2], },
            {"zones": constants.ZONE["RDAI"], "index": 12, "entities": [0x23be, 0x2d52], },
            {"zones": constants.ZONE["RNO2"], "index": 8, "entities": [0x2b78, 0x33c0], },
            {"zones": constants.ZONE["RARE"], "index": 6, "entities": [0x21a8, 0x27b6], }
        ]
    }, {
        "name": "Monster vial 1",
        "type": constants.TYPE["USABLE"],
        "id": 1,
        "tiles": [
            {"addresses": [0x0b5caa], "enemy": 6, },
            {"addresses": [0x0b5cfa], "enemy": 10, }
        ]
    }, {
        "name": "Monster vial 2",
        "type": constants.TYPE["USABLE"],
        "id": 2,
        "tiles": [
            {"addresses": [0x0b63a2], "enemy": 3, }
        ]
    }, {
        "name": "Monster vial 3",
        "type": constants.TYPE["USABLE"],
        "id": 3,
        "tiles": [
            {"zones": constants.ZONE["CAT"], "index": 17, "entities": [0x3206, 0x3ae6], },
            {"zones": constants.ZONE["CAT"], "index": 18, "entities": [0x321a, 0x3afa], },
            {"zones": constants.ZONE["CAT"], "index": 19, "entities": [0x3224, 0x3b04], },
            {"zones": constants.ZONE["CAT"], "index": 20, "entities": [0x3238, 0x3b18], },
            {"addresses": [0x0b655a], "enemy": 7, },
            {"addresses": [0x0b60ac], "enemy": 76, },
            {"addresses": [0x0b6d94], "enemy": 102, },
            {"addresses": [0x0b6e84], "enemy": 113, }
        ]
    }, {
        "name": "Shield rod",
        "type": constants.TYPE["WEAPON1"],
        "id": 4,
        "tiles": [
            {"zones": constants.ZONE["ARE"], "index": 1, "entities": [0x3180, 0x3808], },
            {"zones": constants.ZONE["ST0"], "entities": [0x2816, 0x29b0], "candle": 0x80, }
        ]
    }, {
        "name": "Leather shield",
        "type": constants.TYPE["SHIELD"],
        "id": 5,
        "tiles": [
            {"zones": constants.ZONE["NZ0"], "index": 8, "entities": [0x2cf8, 0x36b4], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a3164], "shop": True, },
            {"addresses": [0x0b77d4], "enemy": 14, },
            {"addresses": [0x0b66ec], "enemy": 29, }
        ]
    }, {
        "name": "Knight shield",
        "type": constants.TYPE["SHIELD"],
        "id": 6,
        "tiles": [
            {"zones": constants.ZONE["ARE"], "index": 4, "entities": [0x34e6, 0x3ba0], },
            {"addresses": [0x0b77d2], "enemy": 14, },
            {"addresses": [0x0b70b4], "enemy": 149, }
        ]
    }, {
        "name": "Iron shield",
        "type": constants.TYPE["SHIELD"],
        "id": 7,
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a316c], "shop": True, },
            {"addresses": [0x0b6ed4], "enemy": 41, }
        ]
    }, {
        "name": "AxeLord shield",
        "type": constants.TYPE["SHIELD"],
        "id": 8,
        "tiles": [
            {"addresses": [0x0b5962], "enemy": 30, }
        ]
    }, {
        "name": "Herald shield",
        "type": constants.TYPE["SHIELD"],
        "id": 9,
        "tiles": [
            {"zones": constants.ZONE["NO4"], "index": 7, "entities": [0x3fa0, 0x503c], }
        ]
    }, {
        "name": "Dark shield",
        "type": constants.TYPE["SHIELD"],
        "id": 10,
        "tiles": [
            {"zones": constants.ZONE["ST0"], "entities": [0x27f8, 0x2992], "candle": 0x80, },
            {"addresses": [0x0b8214], "enemy": 126, }
        ]
    }, {
        "name": "Goddess shield",
        "type": constants.TYPE["SHIELD"],
        "id": 11,
        "tiles": [
            {"zones": constants.ZONE["RNZ0"], "index": 3, "entities": [0x289a, 0x3166], }
        ]
    }, {
        "name": "Shaman shield",
        "type": constants.TYPE["SHIELD"],
        "id": 12,
        "tiles": [
            {"zones": constants.ZONE["NZ1"], "index": 8, "entities": [0x29c6, 0x33d2], }
        ]
    }, {
        "name": "Medusa shield",
        "type": constants.TYPE["SHIELD"],
        "id": 13,
        "tiles": [
            {"addresses": [0x0b8eea], "enemy": 24, },
            {"addresses": [0x0b8f12], "enemy": 27, }
        ]
    }, {
        "name": "Skull shield",
        "type": constants.TYPE["SHIELD"],
        "id": 14,
        "tiles": [
            {"addresses": [0x0b872a], "enemy": 51, },
            {"addresses": [0x0b60aa], "enemy": 76, },
            {"addresses": [0x0b6d92], "enemy": 102, }
        ]
    }, {
        "name": "Fire shield",
        "type": constants.TYPE["SHIELD"],
        "id": 15,
        "tiles": [
            {"addresses": [0x0b65fc], "enemy": 124, }
        ]
    }, {
        "name": "Alucard shield",
        "type": constants.TYPE["SHIELD"],
        "id": 16,
        "tiles": [
            {"zones": constants.ZONE["RNO4"], "index": 0, "entities": [0x3880, 0x47da], }
        ]
    }, {
        "name": "Sword of Dawn",
        "type": constants.TYPE["WEAPON2"],
        "id": 17,
        "tiles": [
            {"zones": constants.ZONE["RTOP"], "index": 0, "entities": [0x1c76, 0x2040], }
        ]
    }, {
        "name": "Basilard",
        "type": constants.TYPE["WEAPON1"],
        "id": 18,
        "tiles": [
            {"zones": constants.ZONE["NZ0"], "index": 9, "entities": [0x2ca8, 0x360a], },
            {"addresses": [0x0b5a7a], "enemy": 13, }
        ]
    }, {
        "name": "Short sword",
        "type": constants.TYPE["WEAPON1"],
        "id": 19,
        "tiles": [
            {"addresses": [0x0b6b3c], "enemy": 9, },
            {"addresses": [0x04bc9324], "enemy": 9, "noOffset": True, }
        ]
    }, {
        "name": "Combat knife",
        "type": constants.TYPE["WEAPON1"],
        "id": 20,
        "tiles": [
            {"zones": constants.ZONE["CHI"], "index": 5, "entities": [0x1a84, 0x1df4], },
            {"addresses": [0x0b7964], "enemy": 84, }
        ]
    }, {
        "name": "Nunchaku",
        "type": constants.TYPE["WEAPON2"],
        "id": 21,
        "tiles": [
            {"zones": constants.ZONE["NO4"], "index": 36, "entities": [0x3c4e, 0x4c72], }
        ]
    }, {
        "name": "Were Bane",
        "type": constants.TYPE["WEAPON1"],
        "id": 22,
        "tiles": [
            {"addresses": [0x0b80ac], "enemy": 60, }
        ]
    }, {
        "name": "Rapier",
        "type": constants.TYPE["WEAPON1"],
        "id": 23,
        "tiles": [
            {"addresses": [0x0b5dc4], "enemy": 45, },
            {"addresses": [0x0b71a2], "enemy": 47, }
        ]
    }, {
        "name": "Karma Coin",
        "type": constants.TYPE["USABLE"],
        "id": 24,
        "tiles": [
            {"zones": constants.ZONE["CHI"], "index": 1, "entities": [0x1a8e, 0x1dfe], },
            {"zones": constants.ZONE["CAT"], "index": 14, "entities": [0x3346, 0x3c3a], },
            {"zones": constants.ZONE["CAT"], "index": 13, "entities": [0x335a, 0x3c30], },
            {"zones": constants.ZONE["RNZ1"], "index": 1, "entities": [0x2aea, 0x3316], },
            {"zones": constants.ZONE["RCAT"], "index": 4, "entities": [0x2d2a, 0x389e], },
            {"zones": constants.ZONE["RCAT"], "index": 5, "entities": [0x2d3e, 0x38a8], },
            {"addresses": [0x0b70dc], "enemy": 114, },
            {"addresses": [0x0b7322], "enemy": 116, }
        ]
    }, {
        "name": "Magic Missile",
        "type": constants.TYPE["USABLE"],
        "id": 25,
        "tiles": [
            {"zones": constants.ZONE["DAI"], "index": 5, "entities": [0x28f6, 0x32d8], },
            {"zones": constants.ZONE["NZ1"], "index": 0, "entities": [0x2a52, 0x34ea], },
            {"zones": constants.ZONE["RNZ1"], "index": 0, "entities": [0x2ad6, 0x32ee], },
            {"zones": constants.ZONE["RCAT"], "index": 0, "entities": [0x285c, 0x338a], },
            {"zones": constants.ZONE["RDAI"], "index": 15, "entities": [0x2562, 0x2ece], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a30d4], "shop": True, },
            {"addresses": [0x0b6ac4], "enemy": 26, },
            {"addresses": [0x0b6bb2], "enemy": 32, },
            {"addresses": [0x0b7a7c], "enemy": 118, }
        ]
    }, {
        "name": "Red Rust",
        "type": constants.TYPE["WEAPON2"],
        "id": 26,
        "tiles": [
            {"addresses": [0x0b6b3a], "enemy": 9, },
            {"addresses": [0x04bc9328], "enemy": 9, "noOffset": True, }
        ]
    }, {
        "name": "Takemitsu",
        "type": constants.TYPE["WEAPON2"],
        "id": 27,
        "tiles": [
            {"zones": constants.ZONE["LIB"], "index": 5, "entities": [0x377c, 0x3f10], },
            {"addresses": [0x0b5eb4], "enemy": 23, },
            {"addresses": [0x0b703c], "enemy": 148, }
        ]
    }, {
        "name": "Shotel",
        "type": constants.TYPE["WEAPON1"],
        "id": 28,
        "tiles": [
            {"zones": constants.ZONE["RNO1"], "index": 1, "entities": [0x215c, 0x2852], },
            {"addresses": [0x0b6de4], "enemy": 69, }
        ]
    }, {
        "name": "Orange",
        "type": constants.TYPE["USABLE"],
        "id": 29,
        "food": True,
    }, {
        "name": "Apple",
        "type": constants.TYPE["USABLE"],
        "id": 30,
        "food": True,
        "tiles": [
            {"addresses": [0x0b828c], "enemy": 73, }
        ]
    }, {
        "name": "Banana",
        "type": constants.TYPE["USABLE"],
        "id": 31,
        "food": True,
        "tiles": [
            {"addresses": [0x0b669c], "enemy": 38, }
        ]
    }, {
        "name": "Grapes",
        "type": constants.TYPE["USABLE"],
        "id": 32,
        "food": True,
        "tiles": [
            {"addresses": [0x0b748c], "enemy": 17, }
        ]
    }, {
        "name": "Strawberry",
        "type": constants.TYPE["USABLE"],
        "id": 33,
        "food": True,
        "tiles": [
            {"addresses": [0x0b748a], "enemy": 17, }
        ]
    }, {
        "name": "Pineapple",
        "type": constants.TYPE["USABLE"],
        "id": 34,
        "food": True,
    }, {
        "name": "Peanuts",
        "type": constants.TYPE["USABLE"],
        "id": 35,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["CHI"], "index": 9, "entities": [0x1a48, 0x1dc2], },
            {"zones": constants.ZONE["CHI"], "index": 10, "entities": [0x1a52, 0x1da4], },
            {"zones": constants.ZONE["CHI"], "index": 11, "entities": [0x1a5c, 0x1dae], },
            {"zones": constants.ZONE["CHI"], "index": 12, "entities": [0x1a66, 0x1db8], }
        ]
    }, {
        "name": "Toadstool",
        "type": constants.TYPE["USABLE"],
        "id": 36,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["NO4"], "index": 26, "entities": [0x3c58, 0x4b3c], },
            {"zones": constants.ZONE["NO4"], "index": 33, "entities": [0x36d6, 0x4876], },
            {"zones": constants.ZONE["RNO4"], "index": 2, "entities": [0x31aa, 0x4078], }
        ]
    }, {
        "name": "Shiitake",
        "type": constants.TYPE["USABLE"],
        "id": 37,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["NO4"], "index": 12, "entities": [0x3550, 0x461e], },
            {"zones": constants.ZONE["NO4"], "index": 35, "entities": [0x36ae, 0x4736], },
            {"zones": constants.ZONE["NO4"], "index": 27, "entities": [0x3bea, 0x4b0a], },
            {"zones": constants.ZONE["NO4"], "index": 32, "entities": [0x36cc, 0x47ea], },
            {"zones": constants.ZONE["CHI"], "index": 7, "entities": [0x1c46, 0x1fc0], },
            {"zones": constants.ZONE["CHI"], "index": 6, "entities": [0x1c6e, 0x1fca], },
            {"zones": constants.ZONE["RNO4"], "index": 1, "entities": [0x3bfa, 0x4b68], },
            {"zones": constants.ZONE["RNO4"], "index": 10, "entities": [0x31d2, 0x42a8], },
            {"zones": constants.ZONE["RNO4"], "index": 9, "entities": [0x3236, 0x42b2], },
            {"zones": constants.ZONE["RNO4"], "index": 3, "entities": [0x31b4, 0x4082], },
            {"zones": constants.ZONE["RCHI"], "index": 6, "entities": [0x1bd6, 0x204a], },
            {"zones": constants.ZONE["RCHI"], "index": 7, "entities": [0x1c30, 0x207c], }
        ]
    }, {
        "name": "Cheesecake",
        "type": constants.TYPE["USABLE"],
        "id": 38,
        "food": True,
        "tiles": [
            {"addresses": [0x0b80aa], "enemy": 60, }
        ]
    }, {
        "name": "Shortcake",
        "type": constants.TYPE["USABLE"],
        "id": 39,
        "food": True,
        "tiles": [
            {"addresses": [0x0b7fba], "enemy": 82, }
        ]
    }, {
        "name": "Tart",
        "type": constants.TYPE["USABLE"],
        "id": 40,
        "food": True,
        "tiles": [
            {"addresses": [0x0b5af2], "enemy": 22, }
        ]
    }, {
        "name": "Parfait",
        "type": constants.TYPE["USABLE"],
        "id": 41,
        "food": True,
    }, {
        "name": "Pudding",
        "type": constants.TYPE["USABLE"],
        "id": 42,
        "food": True,
    }, {
        "name": "Ice cream",
        "type": constants.TYPE["USABLE"],
        "id": 43,
        "food": True,
        "tiles": [
            {"addresses": [0x0b6a4a], "enemy": 49, }
        ]
    }, {
        "name": "Frankfurter",
        "type": constants.TYPE["USABLE"],
        "id": 44,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["TOP"], "index": 7, "entities": [0x241c, 0x29dc], },
            {"zones": constants.ZONE["LIB"], "index": 7, "entities": [0x379a, 0x3f24], },
            {"addresses": [0x0b5aa2], "enemy": 104, }
        ]
    }, {
        "name": "Hamburger",
        "type": constants.TYPE["USABLE"],
        "id": 45,
        "food": True,
    }, {
        "name": "Pizza",
        "type": constants.TYPE["USABLE"],
        "id": 46,
        "food": True,
        "tiles": [
            {"addresses": [0x0b6b62], "enemy": 44, },
            {"addresses": [0x0b6b8a], "enemy": 48, }
        ]
    }, {
        "name": "Cheese",
        "type": constants.TYPE["USABLE"],
        "id": 47,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["NO2"], "index": 6, "entities": [0x34ac, 0x3be8], },
            {"addresses": [0x0b5eb2], "enemy": 23, }
        ]
    }, {
        "name": "Ham and eggs",
        "type": constants.TYPE["USABLE"],
        "id": 48,
        "food": True,
        "tiles": [
            {"addresses": [0x0b6122], "enemy": 56, },
            {"addresses": [0x0b6d42], "enemy": 58, }
        ]
    }, {
        "name": "Omelette",
        "type": constants.TYPE["USABLE"],
        "id": 49,
        "food": True,
    }, {
        "name": "Morning set",
        "type": constants.TYPE["USABLE"],
        "id": 50,
        "food": True,
        "tiles": [
            {"addresses": [0x0b7a2a], "enemy": 15, }
        ]
    }, {
        "name": "Lunch A",
        "type": constants.TYPE["USABLE"],
        "id": 51,
        "food": True,
        "tiles": [
            {"addresses": [0x0b87a4], "enemy": 100, }
        ]
    }, {
        "name": "Lunch B",
        "type": constants.TYPE["USABLE"],
        "id": 52,
        "food": True,
    }, {
        "name": "Curry rice",
        "type": constants.TYPE["USABLE"],
        "id": 53,
        "food": True,
    }, {
        "name": "Gyros plate",
        "type": constants.TYPE["USABLE"],
        "id": 54,
        "food": True,
    }, {
        "name": "Spaghetti",
        "type": constants.TYPE["USABLE"],
        "id": 55,
        "food": True,
    }, {
        "name": "Grape juice",
        "type": constants.TYPE["USABLE"],
        "id": 56,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["DAI"], "addresses": [0x046c2658], "despawn": True, "noOffset": True, }
        ]
    }, {
        "name": "Barley tea",
        "type": constants.TYPE["USABLE"],
        "id": 57,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["CHI"], "index": 8, "entities": [0x1a3e, 0x1dd6], },
            {"addresses": [0x0b7a2c], "enemy": 15, }
        ]
    }, {
        "name": "Green tea",
        "type": constants.TYPE["USABLE"],
        "id": 58,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["ARE"], "index": 6, "entities": [0x3482, 0x3b0a], },
            {"zones": [constants.ZONE["RCHI"], constants.ZONE["RCHI"]], "index": 3, "entities": [0x1938, 0x1d98,
                                                                                                 0x1a8c, 0x1ece], },
            {"addresses": [0x0b6c7a], "enemy": 94, },
            {"addresses": [0x0b5e62], "enemy": 123, }
        ]
    }, {
        "name": "Natou",
        "type": constants.TYPE["USABLE"],
        "id": 59,
        "food": True,
        "tiles": [
            {"addresses": [0x0b6c2a], "enemy": 71, }
        ]
    }, {
        "name": "Ramen",
        "type": constants.TYPE["USABLE"],
        "id": 60,
        "food": True,
        "tiles": [
            {"addresses": [0x0b920c], "enemy": 99, }
        ]
    }, {
        "name": "Miso soup",
        "type": constants.TYPE["USABLE"],
        "id": 61,
        "food": True,
        "tiles": [
            {"addresses": [0x0b6c2c], "enemy": 71, }
        ]
    }, {
        "name": "Sushi",
        "type": constants.TYPE["USABLE"],
        "id": 62,
        "food": True,
        "tiles": [
            {"addresses": [0x0b9642], "enemy": 91, },
            {"addresses": [0x0b5e64], "enemy": 123, }
        ]
    }, {
        "name": "Pork bun",
        "type": constants.TYPE["USABLE"],
        "id": 63,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["CAT"], "index": 15, "entities": [0x3404, 0x3ce4], },
            {"addresses": [0x0b6ca2], "enemy": 53, }
        ]
    }, {
        "name": "Red bean bun",
        "type": constants.TYPE["USABLE"],
        "id": 64,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["RCAT"], "index": 6, "entities": [0x2dde, 0x3902], },
            {"addresses": [0x0b6cca], "enemy": 52, }
        ]
    }, {
        "name": "Chinese bun",
        "type": constants.TYPE["USABLE"],
        "id": 65,
        "food": True,
    }, {
        "name": "Dim Sum set",
        "type": constants.TYPE["USABLE"],
        "id": 66,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["RNO1"], "addresses": [0x0507d08c], "despawn": True, "noOffset": True, }
        ]
    }, {
        "name": "Pot roast",
        "type": constants.TYPE["USABLE"],
        "id": 67,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["NO3"], "addresses": [0x04ba9774, 0x05431554], "despawn": True,
             "noOffset": True, },
            {"zones": constants.ZONE["NO1"], "addresses": [0x04a197d8], "despawn": True, "noOffset": True, },
            {"zones": constants.ZONE["NZ1"], "addresses": [0x0557379c], "despawn": True, "noOffset": True, },
            {"zones": constants.ZONE["RNZ1"], "addresses": [0x059bc34c], "despawn": True, "noOffset": True, },
            {"zones": constants.ZONE["RNO3"], "addresses": [0x051e6e4c], "despawn": True, "noOffset": True, },
            {"zones": constants.ZONE["TOP"], "index": 6, "entities": [0x2412, 0x29d2], "despawn": True, },
            {"zones": [constants.ZONE["NO4"], constants.ZONE["BO3"]], "index": 21, "entities": [0x41da, 0x5262,
                                                                                                0x1d5c, 0x1f20], },
            {"zones": constants.ZONE["RNO4"], "index": 22, "entities": [0x39c0, 0x4910], },
            {"addresses": [0x0b6442], "enemy": 55, }
        ]
    }, {
        "name": "Sirloin",
        "type": constants.TYPE["USABLE"],
        "id": 68,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["TOP"], "index": 4, "entities": [0x23fe, 0x29be], },
            {"addresses": [0x0b6f4c], "enemy": 81, },
            {"addresses": [0x0b9d14], "enemy": 112, }
        ]
    }, {
        "name": "Turkey",
        "type": constants.TYPE["USABLE"],
        "id": 69,
        "food": True,
        "tiles": [
            {"zones": constants.ZONE["NO3"], "addresses": [0x04baa2b0, 0x05431f60], "despawn": True,
             "noOffset": True, },
            {"zones": constants.ZONE["TOP"], "index": 1, "entities": [0x2124, 0x282e], "despawn": True, },
            {"zones": constants.ZONE["TOP"], "index": 5, "entities": [0x2408, 0x29c8], },
            {"zones": constants.ZONE["CHI"], "addresses": [0x045e9602], "despawn": True, },
            {"addresses": [0x0b6124], "enemy": 56, }
        ]
    }, {
        "name": "Meal ticket",
        "type": constants.TYPE["USABLE"],
        "id": 70,
        "tiles": [
            {"zones": constants.ZONE["NO4"], "index": 14, "entities": [0x3640, 0x46b4], },
            {"zones": constants.ZONE["NO4"], "index": 15, "entities": [0x364a, 0x46be], },
            {"zones": constants.ZONE["NO4"], "index": 16, "entities": [0x362c, 0x46c8], },
            {"zones": constants.ZONE["NO4"], "index": 17, "entities": [0x3636, 0x46d2], },
            {"zones": constants.ZONE["RNO0"], "index": 9, "entities": [0x407c, 0x510e], },
            {"zones": constants.ZONE["RNO4"], "index": 16, "entities": [0x3056, 0x3fce], },
            {"zones": constants.ZONE["RNO4"], "index": 17, "entities": [0x3060, 0x3fba], },
            {"zones": constants.ZONE["RNO4"], "index": 18, "entities": [0x3074, 0x3fc4], },
            {"zones": constants.ZONE["RNO4"], "index": 19, "entities": [0x307e, 0x3fa6], },
            {"zones": constants.ZONE["RNO4"], "index": 20, "entities": [0x306a, 0x3fb0], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a3124], "shop": True, },
            {"addresses": [0x0b66ea], "enemy": 29, },
            {"addresses": [0x0b5e3c], "enemy": 109, },
            {"addresses": [0x043c364e, 0x0449181e, 0x0455cc9e, 0x045e99f6, 0x04677596, 0x048fb192, 0x049d3a62,
                           0x04aa1a7e, 0x04b68b26, 0x04c3292a, 0x04cfbd6a, 0x04da5772, 0x04e3280e, 0x04ee333a,
                           0x04f860ae, 0x05050982, 0x050f8eae, 0x051adec2, 0x0526c75e, 0x053f64a2, 0x054b294a,
                           0x05573dee, 0x0560fc1e, 0x056be962, 0x057519b6, 0x057e07b6, 0x05883f86, 0x05903656,
                           0x059bca42, 0x05a6eed6, 0x05af32e2, 0x0606f116, 0x060fdd4a, 0x061a77ce, 0x062478d6,
                           0x063061c6, 0x063ab01e, 0x06471a46, 0x065094fa, 0x065918f6, 0x06621d46, 0x066b40ce,
                           0x06742ee6, 0x067d0d42, 0x06862092, 0x0692c49a, 0x069d222e, 0x06a61212, 0x047a3fe2],
             "enemy": constants.GLOBAL_DROP, }
        ]
    }, {
        "name": "Neutron bomb",
        "type": constants.TYPE["USABLE"],
        "id": 71,
        "tiles": [
            {"zones": constants.ZONE["RLIB"], "index": 6, "entities": [0x1ccc, 0x226c], },
            {"zones": constants.ZONE["ST0"], "addresses": [0x119d00], "noOffset": True, "reward": True, },
            {"addresses": [0x0b69fa], "enemy": 28, },
            {"addresses": [0x0b73ec], "enemy": 122, }
        ]
    }, {
        "name": "Power of Sire",
        "type": constants.TYPE["USABLE"],
        "id": 72,
        "tiles": [
            {"zones": constants.ZONE["CHI"], "index": 0, "entities": [0x1a34, 0x1dcc], },
            {"zones": constants.ZONE["RCHI"], "index": 0, "entities": [0x1910, 0x1d7a], },
            {"zones": constants.ZONE["RCHI"], "index": 4, "entities": [0x1942, 0x1da2], },
            {"zones": constants.ZONE["ST0"], "entities": [0x282a, 0x29c4], "candle": 0x90, }
        ]
    }, {
        "name": "Pentagram",
        "type": constants.TYPE["USABLE"],
        "id": 73,
        "tiles": [
            {"zones": constants.ZONE["NZ1"], "index": 1, "entities": [0x2a0c, 0x34f4], },
            {"zones": constants.ZONE["NO4"], "index": 30, "entities": [0x3f28, 0x4fb0], },
            {"addresses": [0x0b5af4], "enemy": 22, },
            {"addresses": [0x0b819c], "enemy": 31, },
            {"addresses": [0x0b83ca], "enemy": 40, }
        ]
    }, {
        "name": "Bat Pentagram",
        "type": constants.TYPE["USABLE"],
        "id": 74,
        "tiles": [
            {"zones": constants.ZONE["RNO4"], "index": 5, "entities": [0x3754, 0x46a4], },
            {"addresses": [0x0b819a], "enemy": 31, }
        ]
    }, {
        "name": "Shuriken",
        "type": constants.TYPE["USABLE"],
        "id": 75,
        "tiles": [
            {"zones": constants.ZONE["DAI"], "index": 6, "entities": [0x291e, 0x32b0], },
            {"zones": constants.ZONE["RDAI"], "index": 6, "entities": [0x1f9a, 0x27f8], },
            {"zones": constants.ZONE["RNO2"], "index": 10, "entities": [0x29ac, 0x3190], },
            {"zones": constants.ZONE["NZ1"], "addresses": [0x055737a0], "despawn": True, "noOffset": True, },
            {"zones": constants.ZONE["RNZ1"], "addresses": [0x059bc350], "despawn": True, "noOffset": True, },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a30fc], "shop": True, },
            {"addresses": [0x0b5aa4], "enemy": 104, },
            {"addresses": [0x0b6cf4], "enemy": 106, }
        ]
    }, {
        "name": "Cross shuriken",
        "type": constants.TYPE["USABLE"],
        "id": 76,
        "tiles": [
            {"zones": constants.ZONE["CAT"], "index": 12, "entities": [0x333c, 0x3bea], },
            {"zones": constants.ZONE["CAT"], "index": 11, "entities": [0x3350, 0x3be0], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a3104], "shop": True, },
            {"addresses": [0x0b6de2], "enemy": 69, }
        ]
    }, {
        "name": "Buffalo star",
        "type": constants.TYPE["USABLE"],
        "id": 77,
        "tiles": [
            {"zones": constants.ZONE["RCAT"], "index": 1, "entities": [0x2866, 0x3380], },
            {"zones": constants.ZONE["RARE"], "index": 2, "entities": [0x2400, 0x29aa], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a310c], "shop": True, },
            {"addresses": [0x0b7ef4], "enemy": 120, }
        ]
    }, {
        "name": "Flame star",
        "type": constants.TYPE["USABLE"],
        "id": 78,
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a3114], "shop": True, },
            {"addresses": [0x0b6cf2], "enemy": 106, }
        ]
    }, {
        "name": "TNT",
        "type": constants.TYPE["USABLE"],
        "id": 79,
        "tiles": [
            {"zones": constants.ZONE["DAI"], "index": 7, "entities": [0x2946, 0x3292], },
            {"zones": constants.ZONE["RDAI"], "index": 7, "entities": [0x1f4a, 0x283e], },
            {"zones": constants.ZONE["NZ1"], "addresses": [0x055737a8], "despawn": True, "noOffset": True, },
            {"zones": constants.ZONE["RNZ1"], "addresses": [0x059bc358], "despawn": True, "noOffset": True, },
            {"addresses": [0x0b669a], "enemy": 38, },
            {"addresses": [0x0b75cc], "enemy": 103, }
        ]
    }, {
        "name": "Bwaka knife",
        "type": constants.TYPE["USABLE"],
        "id": 80,
        "tiles": [
            {"zones": constants.ZONE["RDAI"], "index": 14, "entities": [0x254e, 0x2ed8], },
            {"zones": constants.ZONE["NZ1"], "addresses": [0x055737a4], "despawn": True, "noOffset": True, },
            {"zones": constants.ZONE["RNZ1"], "addresses": [0x059bc354], "despawn": True, "noOffset": True, },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a30dc], "shop": True, },
            {"addresses": [0x0b6f24], "enemy": 147, }
        ]
    }, {
        "name": "Boomerang",
        "type": constants.TYPE["USABLE"],
        "id": 81,
        "tiles": [
            {"zones": constants.ZONE["DAI"], "index": 8, "entities": [0x2964, 0x326a], },
            {"zones": constants.ZONE["RDAI"], "index": 8, "entities": [0x1efa, 0x288e], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a30e4], "shop": True, },
            {"addresses": [0x0b5a2c], "enemy": 16, }
        ]
    }, {
        "name": "Javelin",
        "type": constants.TYPE["USABLE"],
        "id": 82,
        "tiles": [
            {"zones": constants.ZONE["RDAI"], "index": 9, "entities": [0x1ed2, 0x28c0], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a30ec], "shop": True, },
            {"addresses": [0x0b682c], "enemy": 39, },
            {"addresses": [0x0b6ed2], "enemy": 41, },
            {"addresses": [0x0b6d44], "enemy": 58, },
            {"addresses": [0x0b91e4], "enemy": 97, },
            {"addresses": [0x0b708c], "enemy": 150, }
        ]
    }, {
        "name": "Tyrfing",
        "type": constants.TYPE["WEAPON1"],
        "id": 83,
        "tiles": [
            {"zones": constants.ZONE["TOP"], "index": 3, "entities": [0x23b8, 0x2964], }
        ]
    }, {
        "name": "Namakura",
        "type": constants.TYPE["WEAPON2"],
        "id": 84,
        "tiles": [
            {"addresses": [0x0b6e32], "enemy": 25, }
        ]
    }, {
        "name": "Knuckle duster",
        "type": constants.TYPE["WEAPON1"],
        "id": 85,
        "tiles": [
            {"zones": constants.ZONE["NO4"], "index": 23, "entities": [0x3c80, 0x4e66], },
            {"addresses": [0x0b6b8c], "enemy": 48, }
        ]
    }, {
        "name": "Gladius",
        "type": constants.TYPE["WEAPON1"],
        "id": 86,
        "tiles": [
            {"zones": constants.ZONE["NO1"], "index": 4, "entities": [0x363e, 0x3e24], }
        ]
    }, {
        "name": "Scimitar",
        "type": constants.TYPE["WEAPON1"],
        "id": 87,
        "tiles": [
            {"zones": [constants.ZONE["NO4"], constants.ZONE["BO3"]], "index": 19, "entities": [0x423e, 0x52bc,
                                                                                                0x1e24, 0x1fde], },
            {"addresses": [0x0b872c], "enemy": 51, }
        ]
    }, {
        "name": "Cutlass",
        "type": constants.TYPE["WEAPON1"],
        "id": 88,
        "tiles": [
            {"zones": constants.ZONE["DAI"], "index": 14, "entities": [0x3026, 0x3972], },
            {"addresses": [0x0b59dc], "enemy": 43, },
            {"addresses": [0x0b7824], "enemy": 46, },
            {"addresses": [0x0b5b94], "enemy": 62, }
        ]
    }, {
        "name": "Saber",
        "type": constants.TYPE["WEAPON1"],
        "id": 89,
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a312c], "shop": True, },
            {"addresses": [0x0b5dc2], "enemy": 45, },
            {"addresses": [0x0b859a], "enemy": 50, }
        ]
    }, {
        "name": "Falchion",
        "type": constants.TYPE["WEAPON1"],
        "id": 90,
        "tiles": [
            {"zones": constants.ZONE["TOP"], "index": 12, "entities": [0x2476, 0x2a22], }
        ]
    }, {
        "name": "Broadsword",
        "type": constants.TYPE["WEAPON1"],
        "id": 91,
        "tiles": [
            {"zones": constants.ZONE["NO2"], "index": 4, "entities": [0x34c0, 0x3bd4], },
            {"addresses": [0x0b6efc], "enemy": 57, },
            {"addresses": [0x0b7014], "enemy": 63, }
        ]
    }, {
        "name": "Bekatowa",
        "type": constants.TYPE["WEAPON1"],
        "id": 92,
        "tiles": [
            {"zones": constants.ZONE["NZ1"], "index": 7, "entities": [0x29e4, 0x33c8], },
            {"addresses": [0x0b59da], "enemy": 43, }
        ]
    }, {
        "name": "Damascus sword",
        "type": constants.TYPE["WEAPON1"],
        "id": 93,
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a313c], "shop": True, },
            {"addresses": [0x0b7822], "enemy": 46, }
        ]
    }, {
        "name": "Hunter sword",
        "type": constants.TYPE["WEAPON1"],
        "id": 94,
        "tiles": [
            {"addresses": [0x0b79b4], "enemy": 83, }
        ]
    }, {
        "name": "Estoc",
        "type": constants.TYPE["WEAPON2"],
        "id": 95,
        "thrustSword": False,
        "tiles": [
            {"zones": constants.ZONE["NO2"], "index": 10, "entities": [0x34e8, 0x3c06], },
            {"addresses": [0x0b6f9c], "enemy": 77, }
        ]
    }, {
        "name": "Bastard sword",
        "type": constants.TYPE["WEAPON1"],
        "id": 96,
        "tiles": [
            {"zones": constants.ZONE["RTOP"], "index": 4, "entities": [0x1d66, 0x2162], },
            {"addresses": [0x0b6efa], "enemy": 57, },
            {"addresses": [0x0b7012], "enemy": 63, }
        ]
    }, {
        "name": "Jewel knuckles",
        "type": constants.TYPE["WEAPON1"],
        "id": 97,
        "tiles": [
            {"zones": constants.ZONE["NO1"], "index": 0, "entities": [0x36d4, 0x3eba], },
            {"addresses": [0x0b761c], "enemy": 117, }
        ]
    }, {
        "name": "Claymore",
        "type": constants.TYPE["WEAPON2"],
        "id": 98,
        "thrustSword": True,
        "tiles": [
            {"zones": constants.ZONE["NO4"], "index": 13, "entities": [0x3406, 0x4448], },
            {"addresses": [0x0b6f9a], "enemy": 77, }
        ]
    }, {
        "name": "Talwar",
        "type": constants.TYPE["WEAPON1"],
        "id": 99,
        "tiles": [
            {"zones": constants.ZONE["RDAI"], "index": 13, "entities": [0x2472, 0x2e06], }
        ]
    }, {
        "name": "Katana",
        "id": 100,
        "type": constants.TYPE["WEAPON2"],
        "tiles": [
            {"zones": constants.ZONE["RNZ0"], "index": 5, "entities": [0x2322, 0x2be4], },
            {"addresses": [0x0b6c7c], "enemy": 94, }
        ]
    }, {
        "name": "Flamberge",
        "type": constants.TYPE["WEAPON2"],
        "id": 101,
        "thrustSword": True,
        "tiles": [
            {"addresses": [0x0b88bc], "enemy": 78, }
        ]
    }, {
        "name": "Iron Fist",
        "type": constants.TYPE["WEAPON1"],
        "id": 102,
        "tiles": [
            {"addresses": [0x0b9d8c], "enemy": 108, }
        ]
    }, {
        "name": "Zwei hander",
        "type": constants.TYPE["WEAPON2"],
        "id": 103,
        "thrustSword": True,
        "tiles": [
            {"addresses": [0x0b9e04, 0x0b9e2c], "enemy": 128, }
        ]
    }, {
        "name": "Sword of Hador",
        "type": constants.TYPE["WEAPON1"],
        "id": 104,
        "tiles": [
            {"zones": constants.ZONE["RNO2"], "index": 1, "entities": [0x29fc, 0x31e0], }
        ]
    }, {
        "name": "Luminus",
        "type": constants.TYPE["WEAPON1"],
        "id": 105,
        "tiles": [
            {"zones": constants.ZONE["RNZ1"], "index": 3, "entities": [0x2afe, 0x335c], }
        ]
    }, {
        "name": "Harper",
        "type": constants.TYPE["WEAPON1"],
        "id": 106,
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a315c], "shop": True, }
        ]
    }, {
        "name": "Obsidian sword",
        "type": constants.TYPE["WEAPON2"],
        "id": 107,
        "thrustSword": True,
        "tiles": [
            {"addresses": [0x0b5c0c], "enemy": 80, }
        ]
    }, {
        "name": "Gram",
        "type": constants.TYPE["WEAPON1"],
        "id": 108,
        "tiles": [
            {"zones": constants.ZONE["RARE"], "index": 3, "entities": [0x2428, 0x29c8], }
        ]
    }, {
        "name": "Jewel sword",
        "type": constants.TYPE["WEAPON1"],
        "id": 109,
        "tiles": [
            {"zones": constants.ZONE["NP3"], "index": 9, "entities": [0x3e56, 0x459c], },
            {"addresses": [0x0b65aa], "enemy": 86, }
        ]
    }, {
        "name": "Mormegil",
        "type": constants.TYPE["WEAPON1"],
        "id": 110,
        "tiles": [
            {"zones": constants.ZONE["CAT"], "index": 3, "entities": [0x2c02, 0x34e2], }
        ]
    }, {
        "name": "Firebrand",
        "type": constants.TYPE["WEAPON1"],
        "id": 111,
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a3144], "shop": True, },
            {"zones": constants.ZONE["ST0"], "entities": [0x2802, 0x299c], "candle": 0x80, },
            {"addresses": [0x0b6f4a], "enemy": 81, }
        ]
    }, {
        "name": "Thunderbrand",
        "type": constants.TYPE["WEAPON1"],
        "id": 112,
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a3154], "shop": True, }
        ]
    }, {
        "name": "Icebrand",
        "type": constants.TYPE["WEAPON1"],
        "id": 113,
        "tiles": [
            {"zones": constants.ZONE["CAT"], "index": 1, "entities": [0x2c3e, 0x351e], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a314c], "shop": True, },
            {"addresses": [0x0b89aa], "enemy": 79, }
        ]
    }, {
        "name": "Stone sword",
        "type": constants.TYPE["WEAPON1"],
        "id": 114,
        "tiles": [
            {"addresses": [0x0b5d4a], "enemy": 125, }
        ]
    }, {
        "name": "Holy sword",
        "type": constants.TYPE["WEAPON1"],
        "id": 115,
        "tiles": [
            {"zones": constants.ZONE["ARE"], "index": 7, "entities": [0x34be, 0x3b46], },
            {"addresses": [0x0b80d4], "enemy": 64, }
        ]
    }, {
        "name": "Terminus Est",
        "type": constants.TYPE["WEAPON1"],
        "id": 116,
        "tiles": [
            {"addresses": [0x0b6e82], "enemy": 113, }
        ]
    }, {
        "name": "Marsil",
        "type": constants.TYPE["WEAPON1"],
        "id": 117,
        "tiles": [
            {"addresses": [0x0b65fa], "enemy": 124, }
        ]
    }, {
        "name": "Dark Blade",
        "type": constants.TYPE["WEAPON1"],
        "id": 118,
        "tiles": [
            {"zones": constants.ZONE["RNO4"], "index": 23, "entities": [0x309c, 0x3fec], }
        ]
    }, {
        "name": "Heaven sword",
        "type": constants.TYPE["WEAPON1"],
        "id": 119,
        "tiles": [
            {"addresses": [0x0b88ba], "enemy": 78, }
        ]
    }, {
        "name": "Fist of Tulkas",
        "type": constants.TYPE["WEAPON1"],
        "id": 120,
        "tiles": [
            {"addresses": [0x0b8752], "enemy": 96, }
        ]
    }, {
        "name": "Gurthang",
        "type": constants.TYPE["WEAPON1"],
        "id": 121,
        "tiles": [
            {"addresses": [0x0b7064], "enemy": 119, }
        ]
    }, {
        "name": "Mourneblade",
        "type": constants.TYPE["WEAPON1"],
        "id": 122,
        "tiles": [
            {"addresses": [0x0b8032], "enemy": 137, }
        ]
    }, {
        "name": "Alucard sword",
        "type": constants.TYPE["WEAPON1"],
        "id": 123,
        "tiles": [
            {"zones": constants.ZONE["RCHI"], "index": 2, "entities": [0x1cda, 0x213a], }
        ]
    }, {
        "name": "Mablung Sword",
        "type": constants.TYPE["WEAPON1"],
        "id": 124,
        "tiles": [
            {"addresses": [0x0b7062], "enemy": 119, }
        ]
    }, {
        "name": "Badelaire",
        "type": constants.TYPE["WEAPON1"],
        "id": 125,
        "tiles": [
            {"zones": constants.ZONE["RLIB"], "index": 7, "entities": [0x1b00, 0x20a0], },
            {"zones": constants.ZONE["ST0"], "entities": [0x27ee, 0x2988], "candle": 0x90, }
        ]
    }, {
        "name": "Sword Familiar",
        "type": constants.TYPE["WEAPON1"],
        "id": 126,
    }, {
        "name": "Great Sword",
        "type": constants.TYPE["WEAPON2"],
        "id": 127,
        "tiles": [
            {"addresses": [0x0b9ea4], "enemy": 143, }
        ]
    }, {
        "name": "Mace",
        "type": constants.TYPE["WEAPON1"],
        "id": 128,
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a3134], "shop": True, }
        ]
    }, {
        "name": "Morningstar",
        "type": constants.TYPE["WEAPON1"],
        "id": 129,
        "tiles": [
            {"zones": constants.ZONE["DAI"], "index": 1, "entities": [0x2982, 0x3242], },
            {"addresses": [0x0b6444], "enemy": 55, }
        ]
    }, {
        "name": "Holy rod",
        "type": constants.TYPE["WEAPON1"],
        "id": 130,
        "tiles": [
            {"zones": constants.ZONE["LIB"], "index": 2, "entities": [0x35b0, 0x3c5e], }
        ]
    }, {
        "name": "Star flail",
        "type": constants.TYPE["WEAPON1"],
        "id": 131,
        "tiles": [
            {"zones": constants.ZONE["NZ1"], "index": 3, "entities": [0x284a, 0x327e], }
        ]
    }, {
        "name": "Moon rod",
        "type": constants.TYPE["WEAPON1"],
        "id": 132,
        "tiles": [
            {"zones": constants.ZONE["RNZ1"], "index": 11, "entities": [0x2d06, 0x3578], },
            {"zones": constants.ZONE["ST0"], "entities": [0x27e4, 0x297e], "candle": 0x90, }
        ]
    }, {
        "name": "Chakram",
        "type": constants.TYPE["WEAPON1"],
        "id": 133,
        "tiles": [
            {"addresses": [0x0b65ac], "enemy": 86, }
        ]
    }, {
        "name": "Fire boomerang",
        "type": constants.TYPE["USABLE"],
        "id": 134,
        "tiles": [
            {"zones": constants.ZONE["RNO3"], "index": 7, "entities": [0x2d28, 0x33fe], },
            {"zones": constants.ZONE["RDAI"], "index": 2, "entities": [0x1e78, 0x2924], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a30f4], "shop": True, },
            {"addresses": [0x0b5a2a], "enemy": 16, }
        ]
    }, {
        "name": "Iron ball",
        "type": constants.TYPE["USABLE"],
        "id": 135,
        "tiles": [
            {"zones": constants.ZONE["NO2"], "index": 11, "entities": [0x3470, 0x3b98], },
            {"zones": constants.ZONE["RTOP"], "index": 1, "entities": [0x1c80, 0x2004], },
            {"zones": constants.ZONE["RNO0"], "index": 10, "entities": [0x4568, 0x55be], },
            {"addresses": [0x0b69fc], "enemy": 28, },
            {"addresses": [0x0b6dbc], "enemy": 151, }
        ]
    }, {
        "name": "Holbein dagger",
        "type": constants.TYPE["WEAPON1"],
        "id": 136,
        "tiles": [
            {"addresses": [0x0b5c0a], "enemy": 80, }
        ]
    }, {
        "name": "Blue knuckles",
        "type": constants.TYPE["WEAPON1"],
        "id": 137,
        "tiles": [
            {"addresses": [0x0b6b64], "enemy": 44, }
        ]
    }, {
        "name": "Dynamite",
        "type": constants.TYPE["USABLE"],
        "id": 138,
        "tiles": [
            {"addresses": [0x0b75ca], "enemy": 103, }
        ]
    }, {
        "name": "Osafune katana",
        "type": constants.TYPE["WEAPON2"],
        "id": 139,
        "tiles": [
            {"zones": constants.ZONE["RNO4"], "index": 26, "entities": [0x37c2, 0x473a], }
        ]
    }, {
        "name": "Masamune",
        "type": constants.TYPE["WEAPON2"],
        "id": 140,
        "tiles": [
            {"addresses": [0x0b5e3a], "enemy": 109, }
        ]
    }, {
        "name": "Muramasa",
        "type": constants.TYPE["WEAPON2"],
        "id": 141,
        "tiles": [
            {"addresses": [0x0b80d2], "enemy": 64, },
            {"addresses": [0x0b91e2], "enemy": 97, }
        ]
    }, {
        "name": "Heart Refresh",
        "type": constants.TYPE["USABLE"],
        "id": 142,
        "tiles": [
            {"zones": constants.ZONE["RNO0"], "index": 11, "entities": [0x44fa, 0x555a], },
            {"zones": constants.ZONE["RNO2"], "index": 9, "entities": [0x2970, 0x3154], },
            {"zones": constants.ZONE["ST0"], "addresses": [0x119ca4], "noOffset": True, "reward": True, },
            {"zones": constants.ZONE["ST0"], "entities": [0x280c, 0x29a6], "candle": 0x80, },
            {"addresses": [0x0b752a], "enemy": 95, },
            {"addresses": [0x0b8f3c], "enemy": 107, },
            {"addresses": [0x0b9e02, 0x0b9e2a], "enemy": 128, }
        ]
    }, {
        "name": "Runesword",
        "type": constants.TYPE["WEAPON1"],
        "id": 143,
        "tiles": [
            {"addresses": [0x0b6b12], "enemy": 141, }
        ]
    }, {
        "name": "Antivenom",
        "type": constants.TYPE["USABLE"],
        "id": 144,
        "tiles": [
            {"zones": constants.ZONE["LIB"], "index": 9, "entities": [0x3588, 0x3c40], },
            {"zones": constants.ZONE["NO4"], "index": 4, "entities": [0x3a6e, 0x4ca4], },
            {"zones": constants.ZONE["RNO0"], "index": 2, "entities": [0x3abe, 0x4a92], },
            {"zones": constants.ZONE["RNO3"], "index": 1, "entities": [0x2fda, 0x36ce], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a30bc], "shop": True, },
            {"addresses": [0x0b7462], "enemy": 19, },
            {"addresses": [0x0b789c], "enemy": 33, },
            {"addresses": [0x0b74b4], "enemy": 54, }
        ]
    }, {
        "name": "Uncurse",
        "type": constants.TYPE["USABLE"],
        "id": 145,
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a30c4], "shop": True, },
            {"zones": constants.ZONE["LIB"], "entities": [0x3448, 0x3b6e], "candle": 0x00, },
            {"zones": constants.ZONE["LIB"], "entities": [0x36b4, 0x3d58], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1dc6, 0x2302], "candle": 0x00, },
            {"zones": constants.ZONE["RLIB"], "entities": [0x1e84, 0x242e], "candle": 0x00, },
            {"addresses": [0x0b6764], "enemy": 42, }
        ]
    }, {
        "name": "Life apple",
        "type": constants.TYPE["USABLE"],
        "id": 146,
        "tiles": [
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "index": 2, "entities": [0x40a2, 0x4824,
                                                                                               0x3e60, 0x4588], },
            {"zones": constants.ZONE["NO0"], "index": 3, "entities": [0x296c, 0x37f6], },
            {"zones": constants.ZONE["RNZ1"], "index": 7, "entities": [0x2a0e, 0x3276], },
            {"zones": constants.ZONE["RCHI"], "index": 1, "entities": [0x191a, 0x1d70], },
            {"addresses": [0x0b828a], "enemy": 73, }
        ]
    }, {
        "name": "Hammer",
        "type": constants.TYPE["USABLE"],
        "id": 147,
        "tiles": [
            {"zones": constants.ZONE["NO0"], "index": 12, "entities": [0x3134, 0x3fa0], },
            {"zones": constants.ZONE["NO0"], "index": 4, "entities": [0x2976, 0x3800], },
            {"zones": constants.ZONE["RNO1"], "index": 2, "entities": [0x2170, 0x285c], },
            {"zones": constants.ZONE["RNO3"], "index": 0, "entities": [0x2f94, 0x36c4], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a30cc], "shop": True, },
            {"addresses": [0x0b7914], "enemy": 85, },
            {"addresses": [0x0b5d4c], "enemy": 125, }
        ]
    }, {
        "name": "Str. potion",
        "type": constants.TYPE["USABLE"],
        "id": 148,
        "tiles": [
            {"zones": constants.ZONE["NO0"], "index": 13, "entities": [0x3170, 0x3f14], },
            {"zones": constants.ZONE["DAI"], "index": 11, "entities": [0x2e82, 0x36c0], },
            {"zones": constants.ZONE["RNZ1"], "index": 2, "entities": [0x2af4, 0x3352], },
            {"addresses": [0x0b632c], "enemy": 70, }
        ]
    }, {
        "name": "Luck potion",
        "type": constants.TYPE["USABLE"],
        "id": 149,
        "tiles": [
            {"zones": constants.ZONE["NO2"], "index": 9, "entities": [0x3984, 0x4098], },
            {"zones": constants.ZONE["RNO1"], "index": 4, "entities": [0x221a, 0x291a], },
            {"zones": constants.ZONE["RNO2"], "index": 4, "entities": [0x2948, 0x312c], },
            {"addresses": [0x0b7874], "enemy": 105, },
            {"addresses": [0x0b8ac4], "enemy": 134, }
        ]
    }, {
        "name": "Smart potion",
        "type": constants.TYPE["USABLE"],
        "id": 150,
        "tiles": [
            {"zones": constants.ZONE["RNZ1"], "index": 4, "entities": [0x2b12, 0x3348], },
            {"zones": constants.ZONE["RDAI"], "index": 11, "entities": [0x2288, 0x2d5c], },
            {"addresses": [0x0b614c], "enemy": 20, }
        ]
    }, {
        "name": "Attack potion",
        "type": constants.TYPE["USABLE"],
        "id": 151,
        "tiles": [
            {"zones": constants.ZONE["NO0"], "index": 11, "entities": [0x372e, 0x45c2], },
            {"zones": constants.ZONE["RCAT"], "index": 12, "entities": [0x2b2c, 0x36b4], }
        ]
    }, {
        "name": "Shield potion",
        "type": constants.TYPE["USABLE"],
        "id": 152,
        "tiles": [
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "index": 4, "entities": [0x4156, 0x48ba,
                                                                                               0x3f1e, 0x4632], },
            {"zones": constants.ZONE["RNO1"], "index": 5, "entities": [0x2350, 0x2a46], },
            {"zones": constants.ZONE["RCAT"], "index": 11, "entities": [0x2b36, 0x366e], },
            {"zones": constants.ZONE["RNO2"], "index": 3, "entities": [0x293e, 0x3122], },
            {"addresses": [0x0b655c], "enemy": 7, }
        ]
    }, {
        "name": "Resist fire",
        "type": constants.TYPE["USABLE"],
        "id": 153,
        "tiles": [
            {"zones": constants.ZONE["NO2"], "index": 8, "entities": [0x397a, 0x40a2], },
            {"zones": constants.ZONE["RTOP"], "index": 17, "entities": [0x1e06, 0x2248], },
            {"zones": constants.ZONE["RLIB"], "index": 3, "entities": [0x1ace, 0x206e], },
            {"zones": constants.ZONE["RNO0"], "index": 8, "entities": [0x44b4, 0x5514], },
            {"zones": constants.ZONE["RCAT"], "index": 3, "entities": [0x2d48, 0x3858], },
            {"addresses": [0x0b805c], "enemy": 72, }
        ]
    }, {
        "name": "Resist thunder",
        "type": constants.TYPE["USABLE"],
        "id": 154,
        "tiles": [
            {"zones": constants.ZONE["NZ0"], "index": 7, "entities": [0x2956, 0x32c2], },
            {"zones": constants.ZONE["RTOP"], "index": 19, "entities": [0x1dfc, 0x222a], },
            {"zones": constants.ZONE["RNO0"], "index": 7, "entities": [0x44aa, 0x550a], },
            {"zones": constants.ZONE["RCAT"], "index": 2, "entities": [0x2d34, 0x384e], }
        ]
    }, {
        "name": "Resist ice",
        "type": constants.TYPE["USABLE"],
        "id": 155,
        "tiles": [
            {"zones": [constants.ZONE["NO4"], constants.ZONE["BO3"]], "index": 20, "entities": [0x4216, 0x52c6,
                                                                                                0x1df2, 0x1fe8], },
            {"zones": constants.ZONE["RTOP"], "index": 18, "entities": [0x1de8, 0x223e], },
            {"zones": constants.ZONE["RLIB"], "index": 4, "entities": [0x1ad8, 0x2078], },
            {"addresses": [0x0b89ac], "enemy": 79, }
        ]
    }, {
        "name": "Resist stone",
        "type": constants.TYPE["USABLE"],
        "id": 156,
        "tiles": [
            {"zones": constants.ZONE["TOP"], "index": 8, "entities": [0x2430, 0x29e6], },
            {"zones": constants.ZONE["RTOP"], "index": 20, "entities": [0x1df2, 0x2234], },
            {"zones": constants.ZONE["RLIB"], "index": 5, "entities": [0x1ae2, 0x2082], },
            {"addresses": [0x0b8eec], "enemy": 24, },
            {"addresses": [0x0b8f14], "enemy": 27, }
        ]
    }, {
        "name": "Resist holy",
        "type": constants.TYPE["USABLE"],
        "id": 157,
        "tiles": [
            {"zones": constants.ZONE["TOP"], "index": 10, "entities": [0x2444, 0x29fa], },
            {"zones": constants.ZONE["RNO0"], "index": 6, "entities": [0x44dc, 0x553c], }
        ]
    }, {
        "name": "Resist dark",
        "type": constants.TYPE["USABLE"],
        "id": 158,
        "tiles": [
            {"zones": constants.ZONE["TOP"], "index": 9, "entities": [0x243a, 0x29f0], },
            {"zones": constants.ZONE["RNO0"], "index": 5, "entities": [0x44d2, 0x5532], },
            {"zones": constants.ZONE["RNZ0"], "index": 9, "entities": [0x262e, 0x2edc], },
            {"addresses": [0x0b641a], "enemy": 36, },
            {"addresses": [0x0b8a24], "enemy": 87, }
        ]
    }, {
        "name": "Potion",
        "type": constants.TYPE["USABLE"],
        "id": 159,
        "tiles": [
            {"zones": constants.ZONE["NZ0"], "index": 10, "entities": [0x2b72, 0x3556], },
            {"zones": constants.ZONE["DAI"], "index": 15, "entities": [0x3008, 0x397c], },
            {"zones": constants.ZONE["LIB"], "index": 8, "entities": [0x357e, 0x3c36], },
            {"zones": constants.ZONE["NO0"], "index": 5, "entities": [0x2980, 0x380a], },
            {"zones": constants.ZONE["RNO0"], "index": 1, "entities": [0x3ab4, 0x4a2e], },
            {"zones": constants.ZONE["RNO4"], "index": 8, "entities": [0x3362, 0x414a], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a309c], "shop": True, },
            {"zones": constants.ZONE["ST0"], "addresses": [0x119bb8], "noOffset": True, "reward": True, },
            {"addresses": [0x0b63a4], "enemy": 3, },
            {"addresses": [0x0b74b2], "enemy": 54, }
        ]
    }, {
        "name": "High potion",
        "type": constants.TYPE["USABLE"],
        "id": 160,
        "tiles": [
            {"zones": constants.ZONE["RTOP"], "index": 21, "entities": [0x1dde, 0x225c], },
            {"zones": constants.ZONE["RNO1"], "index": 6, "entities": [0x242c, 0x2a8c], },
            {"zones": constants.ZONE["RNO3"], "index": 2, "entities": [0x302a, 0x3700], },
            {"zones": constants.ZONE["RNZ0"], "index": 6, "entities": [0x2804, 0x30e4], },
            {"zones": constants.ZONE["RNO2"], "index": 2, "entities": [0x2a06, 0x31ea], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a30a4], "shop": True, },
            {"addresses": [0x0b5edc], "enemy": 65, }
        ]
    }, {
        "name": "Elixir",
        "type": constants.TYPE["USABLE"],
        "id": 161,
        "tiles": [
            {"zones": constants.ZONE["NO4"], "index": 25, "entities": [0x3dd4, 0x4e7a], },
            {"zones": constants.ZONE["RNO4"], "index": 25, "entities": [0x3416, 0x43de], },
            {"zones": constants.ZONE["RCAT"], "index": 7, "entities": [0x3036, 0x3b64], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a30ac], "shop": True, }
        ]
    }, {
        "name": "Manna prism",
        "type": constants.TYPE["USABLE"],
        "id": 162,
        "tiles": [
            {"zones": constants.ZONE["NO2"], "index": 7, "entities": [0x3970, 0x40ac], },
            {"zones": constants.ZONE["RNO4"], "index": 24, "entities": [0x342a, 0x42da], },
            {"zones": constants.ZONE["RNZ0"], "index": 4, "entities": [0x2598, 0x2dec], },
            {"zones": constants.ZONE["RDAI"], "index": 10, "entities": [0x2364, 0x2d66], },
            {"zones": constants.ZONE["RNO2"], "index": 5, "entities": [0x2952, 0x3136], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a30b4], "shop": True, },
            {"addresses": [0x0b6762], "enemy": 42, },
            {"addresses": [0x0b80fa], "enemy": 139, }
        ]
    }, {
        "name": "Library card",
        "type": constants.TYPE["USABLE"],
        "id": 166,
        "tiles": [
            {"zones": constants.ZONE["NO0"], "index": 10, "entities": [0x3742, 0x45b8], },
            {"zones": constants.ZONE["CAT"], "index": 4, "entities": [0x3422, 0x3d02], },
            {"zones": constants.ZONE["ARE"], "index": 5, "entities": [0x352c, 0x3b78], },
            {"zones": constants.ZONE["RTOP"], "index": 24, "entities": [0x1e4c, 0x22a2], },
            {"zones": constants.ZONE["RLIB"], "index": 2, "entities": [0x1a56, 0x2000], },
            {"zones": constants.ZONE["RNO0"], "index": 0, "entities": [0x373a, 0x4a10], },
            {"zones": constants.ZONE["RCAT"], "index": 8, "entities": [0x3040, 0x3b5a], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a311c], "shop": True, }
        ]
    }, {
        "name": "Vorpal blade",
        "type": constants.TYPE["WEAPON1"],
        "id": 163,
        "tiles": [
            {"addresses": [0x0b8f3a], "enemy": 107, }
        ]
    }, {
        "name": "Crissaegrim",
        "type": constants.TYPE["WEAPON1"],
        "id": 164,
        "tiles": [
            {"addresses": [0x0b920a], "enemy": 99, }
        ]
    }, {
        "name": "Yasutsuna",
        "type": constants.TYPE["WEAPON2"],
        "id": 165,
        "tiles": [
            {"addresses": [0x0b9d8a], "enemy": 108, }
        ]
    }, {
        "name": "Alucart shield",
        "type": constants.TYPE["SHIELD"],
        "id": 167,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NO0"], "index": 1, "entities": [0x3670, 0x44f0], }
        ]
    }, {
        "name": "Alucart sword",
        "type": constants.TYPE["WEAPON1"],
        "id": 168,
        "tiles": [
            {"zones": constants.ZONE["NO0"], "index": 7, "entities": [0x36a2, 0x4522], }
        ]
    }, {
        "name": "Cloth tunic",
        "type": constants.TYPE["ARMOR"],
        "id": 170,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b6c02], "enemy": 5, },
            {"addresses": [0x0b5a7c], "enemy": 13, }
        ]
    }, {
        "name": "Hide cuirass",
        "type": constants.TYPE["ARMOR"],
        "id": 171,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NZ0"], "index": 0, "entities": [0x2df2, 0x377c], },
            {"addresses": [0x0b71a4], "enemy": 47, }
        ]
    }, {
        "name": "Bronze cuirass",
        "type": constants.TYPE["ARMOR"],
        "id": 172,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "index": 4, "entities": [0x3286, 0x398e], },
            {"addresses": [0x0b83a2], "enemy": 12, }
        ]
    }, {
        "name": "Iron cuirass",
        "type": constants.TYPE["ARMOR"],
        "id": 173,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a3194], "shop": True, },
            {"addresses": [0x0b682a], "enemy": 39, },
            {"addresses": [0x0b5eda], "enemy": 65, }
        ]
    }, {
        "name": "Steel cuirass",
        "type": constants.TYPE["ARMOR"],
        "id": 174,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a319c], "shop": True, }
        ]
    }, {
        "name": "Silver plate",
        "type": constants.TYPE["ARMOR"],
        "id": 175,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["DAI"], "index": 10, "entities": [0x2da6, 0x36b6], }
        ]
    }, {
        "name": "Gold plate",
        "type": constants.TYPE["ARMOR"],
        "id": 176,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NZ1"], "index": 4, "entities": [0x287c, 0x3288], },
            {"addresses": [0x0b79b2], "enemy": 83, },
            {"addresses": [0x0b7962], "enemy": 84, },
            {"addresses": [0x0b7912], "enemy": 85, }
        ]
    }, {
        "name": "Platinum mail",
        "type": constants.TYPE["ARMOR"],
        "id": 177,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["TOP"], "index": 11, "entities": [0x244e, 0x29b4], },
            {"addresses": [0x0b761a], "enemy": 117, }
        ]
    }, {
        "name": "Diamond plate",
        "type": constants.TYPE["ARMOR"],
        "id": 178,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a31a4], "shop": True, }
        ]
    }, {
        "name": "Fire mail",
        "type": constants.TYPE["ARMOR"],
        "id": 179,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["TOP"], "index": 2, "entities": [0x211a, 0x27a2], },
            {"addresses": [0x0b805a], "enemy": 72, },
            {"addresses": [0x0b64ba], "enemy": 89, }
        ]
    }, {
        "name": "Lightning mail",
        "type": constants.TYPE["ARMOR"],
        "id": 180,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RTOP"], "index": 23, "entities": [0x1e2e, 0x227a], },
            {"addresses": [0x0b64bc], "enemy": 89, }
        ]
    }, {
        "name": "Ice mail",
        "type": constants.TYPE["ARMOR"],
        "id": 181,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NZ1"], "index": 9, "entities": [0x2a02, 0x33dc], },
            {"addresses": [0x0b6a4c], "enemy": 49, }
        ]
    }, {
        "name": "Mirror cuirass",
        "type": constants.TYPE["ARMOR"],
        "id": 182,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NO1"], "index": 1, "entities": [0x36e8, 0x3ec4], }
        ]
    }, {
        "name": "Spike Breaker",
        "type": constants.TYPE["ARMOR"],
        "id": 183,
        "progression": True,
        "tiles": [
            {"zones": constants.ZONE["CAT"], "index": 16, "entities": [0x342c, 0x3d2a], }
        ]
    }, {
        "name": "Alucard mail",
        "type": constants.TYPE["ARMOR"],
        "id": 184,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RNO2"], "index": 7, "entities": [0x298e, 0x3172], }
        ]
    }, {
        "name": "Dark armor",
        "type": constants.TYPE["ARMOR"],
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "id": 185,
        "tiles": [
            {"addresses": [0x0b8212], "enemy": 126, }
        ]
    }, {
        "name": "Healing mail",
        "type": constants.TYPE["ARMOR"],
        "id": 186,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NZ1"], "index": 6, "entities": [0x2d18, 0x372e], }
        ]
    }, {
        "name": "Holy mail",
        "type": constants.TYPE["ARMOR"],
        "id": 187,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": [constants.ZONE["NO3"], constants.ZONE["NP3"]], "index": 5, "entities": [0x3ea4, 0x4630,
                                                                                               0x3c44, 0x4380], }
        ]
    }, {
        "name": "Walk armor",
        "type": constants.TYPE["ARMOR"],
        "id": 188,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["CAT"], "index": 2, "entities": [0x2c20, 0x3500], }
        ]
    }, {
        "name": "Brilliant mail",
        "type": constants.TYPE["ARMOR"],
        "id": 189,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b7a7a], "enemy": 118, }
        ]
    }, {
        "name": "Mojo mail",
        "type": constants.TYPE["ARMOR"],
        "id": 190,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b87a2], "enemy": 100, }
        ]
    }, {
        "name": "Fury plate",
        "type": constants.TYPE["ARMOR"],
        "id": 191,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RARE"], "index": 0, "entities": [0x2446, 0x29e6], },
            {"addresses": [0x0b9d12], "enemy": 112, }
        ]
    }, {
        "name": "Dracula tunic",
        "type": constants.TYPE["ARMOR"],
        "id": 192,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047d9370], "noOffset": True, "librarian": True, }
        ]
    }, {
        "name": "God\'s Garb",
        "type": constants.TYPE["ARMOR"],
        "id": 193,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b9ea2], "enemy": 143, }
        ]
    }, {
        "name": "Axe Lord armor",
        "type": constants.TYPE["ARMOR"],
        "id": 194,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047d9284], "noOffset": True, "librarian": True, }
        ]
    }, {
        "name": "Sunglasses",
        "type": constants.TYPE["HELMET"],
        "id": 196,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NZ0"], "index": 6, "entities": [0x3108, 0x3a60], },
            {"zones": constants.ZONE["ST0"], "entities": [0x2820, 0x29ba], "candle": 0x90, }
        ]
    }, {
        "name": "Ballroom mask",
        "type": constants.TYPE["HELMET"],
        "id": 197,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["CAT"], "index": 7, "entities": [0x2eaa, 0x3762], },
            {"addresses": [0x0b789a], "enemy": 33, }
        ]
    }, {
        "name": "Bandanna",
        "type": constants.TYPE["HELMET"],
        "id": 198,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NO4"], "index": 11, "entities": [0x3262, 0x42ea], }
        ]
    }, {
        "name": "Felt hat",
        "type": constants.TYPE["HELMET"],
        "id": 199,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b641c], "enemy": 36, }
        ]
    }, {
        "name": "Velvet hat",
        "type": constants.TYPE["HELMET"],
        "id": 200,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a3174], "shop": True, }
        ]
    }, {
        "name": "Goggles",
        "type": constants.TYPE["HELMET"],
        "id": 201,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["DAI"], "index": 9, "entities": [0x289c, 0x31f2], }
        ]
    }, {
        "name": "Leather hat",
        "type": constants.TYPE["HELMET"],
        "id": 202,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a317c], "shop": True, }
        ]
    }, {
        "name": "Holy glasses",
        "type": constants.TYPE["HELMET"],
        "id": 203,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "progression": True,
    }, {
        "name": "Steel helm",
        "type": constants.TYPE["HELMET"],
        "id": 204,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NZ1"], "index": 5, "entities": [0x2886, 0x3292], }
        ]
    }, {
        "name": "Stone mask",
        "type": constants.TYPE["HELMET"],
        "id": 205,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "index": 1, "entities": [0x3312, 0x39ac], },
            {"addresses": [0x0b7ef2], "enemy": 120, }
        ]
    }, {
        "name": "Circlet",
        "type": constants.TYPE["HELMET"],
        "id": 206,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a3184], "shop": True, },
            {"addresses": [0x0b614a], "enemy": 20, }
        ]
    }, {
        "name": "Gold circlet",
        "type": constants.TYPE["HELMET"],
        "id": 207,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b7fbc], "enemy": 82, }
        ]
    }, {
        "name": "Ruby circlet",
        "type": constants.TYPE["HELMET"],
        "id": 208,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RCAT"], "index": 17, "entities": [0x25a0, 0x30c4], }
        ]
    }, {
        "name": "Opal circlet",
        "type": constants.TYPE["HELMET"],
        "id": 209,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b7f1a], "enemy": 138, }
        ]
    }, {
        "name": "Topaz circlet",
        "type": constants.TYPE["HELMET"],
        "id": 210,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "index": 10, "entities": [0x35a6, 0x3c68], }
        ]
    }, {
        "name": "Beryl circlet",
        "type": constants.TYPE["HELMET"],
        "id": 211,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RNO3"], "index": 6, "entities": [0x2daa, 0x3462], }
        ]
    }, {
        "name": "Cat-eye circl.",
        "type": constants.TYPE["HELMET"],
        "id": 212,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["CAT"], "index": 0, "entities": [0x2e28, 0x3708], }
        ]
    }, {
        "name": "Coral circlet",
        "type": constants.TYPE["HELMET"],
        "id": 213,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b752c], "enemy": 95, }
        ]
    }, {
        "name": "Dragon helm",
        "type": constants.TYPE["HELMET"],
        "id": 214,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RNZ1"], "index": 5, "entities": [0x2a36, 0x329e], }
        ]
    }, {
        "name": "Silver crown",
        "type": constants.TYPE["HELMET"],
        "id": 215,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a318c], "shop": True, }
        ]
    }, {
        "name": "Wizard hat",
        "type": constants.TYPE["HELMET"],
        "id": 216,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b80fc], "enemy": 139, }
        ]
    }, {
        "name": "Cloth cape",
        "type": constants.TYPE["CLOAK"],
        "id": 218,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NZ0"], "index": 2, "entities": [0x2f32, 0x388a], }
        ]
    }, {
        "name": "Reverse cloak",
        "type": constants.TYPE["CLOAK"],
        "id": 219,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a31ac], "shop": True, }
        ]
    }, {
        "name": "Elven cloak",
        "type": constants.TYPE["CLOAK"],
        "id": 220,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a31b4], "shop": True, }
        ]
    }, {
        "name": "Crystal cloak",
        "type": constants.TYPE["CLOAK"],
        "id": 221,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": [constants.ZONE["NO4"], constants.ZONE["BO3"]], "index": 2, "entities": [0x3352, 0x43da,
                                                                                               0x1e42, 0x2006], }
        ]
    }, {
        "name": "Royal cloak",
        "type": constants.TYPE["CLOAK"],
        "id": 222,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RTOP"], "index": 11, "entities": [0x1d16, 0x21a8], }
        ]
    }, {
        "name": "Blood cloak",
        "type": constants.TYPE["CLOAK"],
        "id": 223,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["ARE"], "index": 3, "entities": [0x34a0, 0x3b28], }
        ]
    }, {
        "name": "Joseph\'s cloak",
        "type": constants.TYPE["CLOAK"],
        "id": 224,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a31bc], "shop": True, }
        ]
    }, {
        "name": "Twilight cloak",
        "type": constants.TYPE["CLOAK"],
        "id": 225,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RDAI"], "index": 16, "entities": [0x1d7e, 0x26d6], }
        ]
    }, {
        "name": "Moonstone",
        "type": constants.TYPE["ACCESSORY"],
        "id": 227,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NO4"], "index": 18, "entities": [0x3654, 0x46dc], }
        ]
    }, {
        "name": "Sunstone",
        "type": constants.TYPE["ACCESSORY"],
        "id": 228,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RNZ1"], "index": 8, "entities": [0x2a18, 0x326c], }
        ]
    }, {
        "name": "Bloodstone",
        "type": constants.TYPE["ACCESSORY"],
        "id": 229,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["CAT"], "index": 8, "entities": [0x2e32, 0x3712], }
        ]
    }, {
        "name": "Staurolite",
        "type": constants.TYPE["ACCESSORY"],
        "id": 230,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RLIB"], "index": 8, "entities": [0x1b82, 0x2122], }
        ]
    }, {
        "name": "Ring of Pales",
        "type": constants.TYPE["ACCESSORY"],
        "id": 231,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a31cc], "shop": True, }
        ]
    }, {
        "name": "Zircon",
        "type": constants.TYPE["ACCESSORY"],
        "id": 232,
        "salable": True,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["DAI"], "index": 13, "entities": [0x2f5e, 0x38aa], },
            {"zones": constants.ZONE["RDAI"], "index": 4, "entities": [0x1fd6, 0x27b2], },
            {"zones": constants.ZONE["NO1"], "index": 6, "entities": [0x3774, 0x3f3c], },
            {"zones": constants.ZONE["NO4"], "index": 9, "entities": [0x329e, 0x4308], },
            {"zones": constants.ZONE["RTOP"], "index": 2, "entities": [0x1b9a, 0x209a], },
            {"zones": constants.ZONE["RNO4"], "index": 14, "entities": [0x3b5a, 0x4ac8], },
            {"zones": constants.ZONE["RNO4"], "index": 21, "entities": [0x3af6, 0x4a28], },
            {"zones": constants.ZONE["RNO3"], "index": 4, "entities": [0x2d96, 0x3476], },
            {"zones": constants.ZONE["RARE"], "index": 1, "entities": [0x213a, 0x26e4], },
            {"addresses": [0x0b5cac], "enemy": 6, },
            {"addresses": [0x0b5cfc], "enemy": 10, },
            {"addresses": [0x0b6ca4], "enemy": 53, }
        ]
    }, {
        "name": "Aquamarine",
        "type": constants.TYPE["ACCESSORY"],
        "id": 233,
        "salable": True,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["DAI"], "index": 3, "entities": [0x28ba, 0x3328], },
            {"zones": constants.ZONE["RNO2"], "index": 6, "entities": [0x2664, 0x2e34], },
            {"zones": constants.ZONE["RARE"], "index": 4, "entities": [0x2036, 0x2612], },
            {"addresses": [0x0b6ccc], "enemy": 52, },
            {"addresses": [0x0b9644], "enemy": 91, }
        ]
    }, {
        "name": "Turquoise",
        "type": constants.TYPE["ACCESSORY"],
        "id": 234,
        "salable": True,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["TOP"], "index": 0, "entities": [0x212e, 0x2842], },
            {"zones": constants.ZONE["RLIB"], "index": 0, "entities": [0x1a42, 0x1fec], },
            {"zones": constants.ZONE["RNZ0"], "index": 7, "entities": [0x24d0, 0x2d10], },
            {"addresses": [0x0b7324], "enemy": 116, },
            {"addresses": [0x0b6dba], "enemy": 151, }
        ]
    }, {
        "name": "Onyx",
        "type": constants.TYPE["ACCESSORY"],
        "id": 235,
        "salable": True,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "index": 6, "entities": [0x3786, 0x3f1a], },
            {"zones": constants.ZONE["NO4"], "index": 22, "entities": [0x3d16, 0x4d6c], },
            {"zones": constants.ZONE["NO2"], "index": 5, "entities": [0x34b6, 0x3bde], }
        ]
    }, {
        "name": "Garnet",
        "type": constants.TYPE["ACCESSORY"],
        "id": 236,
        "salable": True,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NO1"], "index": 3, "entities": [0x37ba, 0x3f6e], },
            {"zones": constants.ZONE["NO2"], "index": 12, "entities": [0x3434, 0x3b5c], },
            {"zones": constants.ZONE["RTOP"], "index": 22, "entities": [0x1c6c, 0x1ffa], },
            {"zones": constants.ZONE["RNO1"], "index": 7, "entities": [0x2544, 0x2c8a], },
            {"zones": constants.ZONE["RNO4"], "index": 4, "entities": [0x381c, 0x476c], },
            {"addresses": [0x0b632a], "enemy": 70, }
        ]
    }, {
        "name": "Opal",
        "type": constants.TYPE["ACCESSORY"],
        "id": 237,
        "salable": True,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RLIB"], "index": 1, "entities": [0x1a4c, 0x1ff6], },
            {"zones": constants.ZONE["RNO4"], "index": 11, "entities": [0x3bbe, 0x4b0e], },
            {"zones": constants.ZONE["RNO3"], "index": 5, "entities": [0x2da0, 0x346c], },
            {"zones": constants.ZONE["RNO2"], "index": 0, "entities": [0x29f2, 0x31d6], }
        ]
    }, {
        "name": "Diamond",
        "type": constants.TYPE["ACCESSORY"],
        "id": 238,
        "salable": True,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RNZ1"], "index": 6, "entities": [0x29dc, 0x3280], },
            {"zones": constants.ZONE["RNO4"], "index": 13, "entities": [0x2d72, 0x3cc2], },
            {"zones": constants.ZONE["RCAT"], "index": 14, "entities": [0x25be, 0x30e2], },
            {"zones": constants.ZONE["RDAI"], "index": 3, "entities": [0x1f36, 0x2852], }
        ]
    }, {
        "name": "Lapis lazuli",
        "type": constants.TYPE["ACCESSORY"],
        "id": 239,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b70da], "enemy": 114, }
        ]
    }, {
        "name": "Ring of Ares",
        "type": constants.TYPE["ACCESSORY"],
        "id": 240,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["CHI"], "index": 4, "entities": [0x1d0e, 0x207e], }
        ]
    }, {
        "name": "Gold Ring",
        "type": constants.TYPE["ACCESSORY"],
        "id": 241,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "progression": True,
        "tiles": [
            {"zones": constants.ZONE["NO4"], "entities": [0x4270, 0x52ee], }
        ]
    }, {
        "name": "Silver Ring",
        "type": constants.TYPE["ACCESSORY"],
        "id": 242,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "progression": True,
        "tiles": [
            {"zones": constants.ZONE["DAI"], "index": 2, "entities": [0x281a, 0x31c0], }
        ]
    }, {
        "name": "Ring of Varda",
        "type": constants.TYPE["ACCESSORY"],
        "id": 243,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b7e2a], "enemy": 67, }
        ]
    }, {
        "name": "Ring of Arcana",
        "type": constants.TYPE["ACCESSORY"],
        "id": 244,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RNZ0"], "index": 8, "entities": [0x2368, 0x2c48], },
            {"zones": constants.ZONE["LIB"], "addresses": [0x047d92f0], "noOffset": True, "librarian": True, }
        ]
    }, {
        "name": "Mystic pendant",
        "type": constants.TYPE["ACCESSORY"],
        "id": 245,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["DAI"], "index": 4, "entities": [0x28e2, 0x32f6], },
            {"addresses": [0x0b7872], "enemy": 105, }
        ]
    }, {
        "name": "Heart broach",
        "type": constants.TYPE["ACCESSORY"],
        "id": 246,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b6b14], "enemy": 141, }
        ]
    }, {
        "name": "Necklace of J",
        "type": constants.TYPE["ACCESSORY"],
        "id": 247,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RCAT"], "index": 13, "entities": [0x25dc, 0x3100], },
            {"addresses": [0x0b7f1c], "enemy": 138, }
        ]
    }, {
        "name": "Gauntlet",
        "type": constants.TYPE["ACCESSORY"],
        "id": 248,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a31d4], "shop": True, },
            {"addresses": [0x0b7e2c], "enemy": 67, },
            {"addresses": [0x0b8754], "enemy": 96, }
        ]
    }, {
        "name": "Ankh of Life",
        "type": constants.TYPE["ACCESSORY"],
        "id": 249,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["DAI"], "index": 0, "entities": [0x2928, 0x32a6], }
        ]
    }, {
        "name": "Ring of Feanor",
        "type": constants.TYPE["ACCESSORY"],
        "id": 250,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b8a22], "enemy": 87, }
        ]
    }, {
        "name": "Medal",
        "type": constants.TYPE["ACCESSORY"],
        "id": 251,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a31c4], "shop": True, },
            {"addresses": [0x0b5b92], "enemy": 62, }
        ]
    }, {
        "name": "Talisman",
        "type": constants.TYPE["ACCESSORY"],
        "id": 252,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["RNO3"], "index": 9, "entities": [0x2d00, 0x33cc], },
            {"addresses": [0x0b6ac2], "enemy": 26, }
        ]
    }, {
        "name": "Duplicator",
        "type": constants.TYPE["ACCESSORY"],
        "id": 253,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["LIB"], "addresses": [0x047a31dc], "shop": True, }
        ]
    }, {
        "name": "King\'s stone",
        "type": constants.TYPE["ACCESSORY"],
        "id": 254,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b8ac2], "enemy": 134,}
        ]
    }, {
        "name": "Covenant stone",
        "type": constants.TYPE["ACCESSORY"],
        "id": 255,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b8034], "enemy": 137, }
        ]
    }, {
        "name": "Nauglamir",
        "type": constants.TYPE["ACCESSORY"],
        "id": 256,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"addresses": [0x0b73ea], "enemy": 122, }
        ]
    }, {
        "name": "Secret boots",
        "type": constants.TYPE["ACCESSORY"],
        "id": 257,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NO4"], "index": 31, "entities": [0x37da, 0x47e0], }
        ]
    }, {
        "name": "Alucart mail",
        "type": constants.TYPE["ARMOR"],
        "id": 258,
        "blacklist": [0x0b6b3c, 0x0b6b3a],
        "tiles": [
            {"zones": constants.ZONE["NO0"], "index": 6, "entities": [0x3698, 0x4518], }
        ]
    }, {
        "name": "$5000",
        "type": constants.TYPE["GOLD"],
        "id": 259,
        "blacklist": [0x0b6b3c, 0x0b6b3a]
    }
]

#get_item_type = {key: (constants.typeNames[value["type"]], value["type"]) for key, value in items_dict.items()}
get_item = {item["name"]: item for item in items_list}
get_item_by_id = {item["id"]: item for item in items_list}


if __name__ == "__main__":
    pass



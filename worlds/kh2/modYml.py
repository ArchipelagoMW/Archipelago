class modYml:
    def getDefaultMod():
        return {
            "title": "Randomizer Seed",
            "assets": [
                {
                    "name": "msg/jp/sys.bar",
                    "multi": [
                        {
                            "name": "msg/us/sys.bar"
                        },
                        {
                            "name": "msg/uk/sys.bar"
                        }
                    ],
                    "method": "binarc",
                    "source": [
                        {
                            "name": "sys",
                            "type": "list",
                            "method": "kh2msg",
                            "source": [
                                {
                                    "name": "sys.yml",
                                    "language": "en"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "msg/jp/jm.bar",
                    "multi": [
                        {
                            "name": "msg/us/jm.bar"
                        },
                        {
                            "name": "msg/uk/jm.bar"
                        }
                    ],
                    "method": "binarc",
                    "source": [
                        {
                            "name": "jm",
                            "type": "list",
                            "method": "kh2msg",
                            "source": [
                                {
                                    "name": "jm.yml",
                                    "language": "en"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "00battle.bin",
                    "method": "binarc",
                    "source": [
                        {
                            "name": "fmlv",
                            "method": "listpatch",
                            "type": "List",
                            "source": [
                                {
                                    "name": "FmlvList.yml",
                                    "type": "fmlv"
                                }
                            ]
                        },
                        {
                            "name": "lvup",
                            "method": "listpatch",
                            "type": "List",
                            "source": [
                                {
                                    "name": "LvupList.yml",
                                    "type": "lvup"
                                }
                            ]
                        },
                        {
                            "name": "bons",
                            "method": "listpatch",
                            "type": "List",
                            "source": [
                                {
                                    "name": "BonsList.yml",
                                    "type": "bons"
                                }
                            ]
                        },
                        {
                            "name": "plrp",
                            "method": "listpatch",
                            "type": "List",
                            "source": [
                                {
                                    "name": "PlrpList.yml",
                                    "type": "plrp"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "03system.bin",
                    "method": "binarc",
                    "source": [
                        {
                            "name": "trsr",
                            "method": "listpatch",
                            "type": "List",
                            "source": [
                                {
                                    "name": "TrsrList.yml",
                                    "type": "trsr"
                                }
                            ]
                        },
                        {
                            "name": "item",
                            "method": "listpatch",
                            "type": "List",
                            "source": [
                                {
                                    "name": "ItemList.yml",
                                    "type": "item"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def getJMYAML():
        return [
            {
                "id": 20279,
                "en": "Defeat Xemnas at the top of the Castle"
            },
            {
                "id": 20280,
                "en": "Defeat Storm Rider"
            },
            {
                "id": 20281,
                "en": "Defeat Xaldin in the Courtyard"
            },
            {
                "id": 20282,
                "en": "Defeat Dr. Finkelstein's Experiment"
            },
            {
                "id": 20283,
                "en": "Defeat Genie Jafar"
            },
            {
                "id": 20284,
                "en": "Defeat Hades"
            },
            {
                "id": 20285,
                "en": "Defeat Groundshaker"
            },
            {
                "id": 20286,
                "en": "Fight alongside Axel in the world Between"
            },
            {
                "id": 20287,
                "en": "Defend Hollow Bastion from the Heartless Army"
            },
            {
                "id": 20288,
                "en": "Defeat Grim Reaper II"
            },
            {
                "id": 20289,
                "en": "Protect the Cornerstone of Light from Pete"
            },
            {
                "id": 20290,
                "en": "Defeat the Master Control Program"
            },
            {
                "id": 20291,
                "en": "Confront DiZ in the Mansion's Pod Room"
            }
        ]

    def getSysYAML(seedHashIcons):
        seedHashString = " ".join(["{:icon " + icon + "}" for icon in seedHashIcons])
        sys = [{"id": 17198, "en":seedHashString}]
        sys.append({"id": 19482, "en": "Important Checks Found"})
        return sys

    def getPuzzleMod():
        return {
                    "name": "menu/jp/jiminy.bar",
                    "multi": [
                        {
                            "name": "menu/us/jiminy.bar"
                        },
                        {
                            "name": "menu/uk/jiminy.bar"
                        },
                        {
                            "name": "menu/fm/jiminy.bar"
                        }
                    ],
                    "method": "copy",
                    "source": [
                        {
                            "name" : "modified_jiminy.bar"
                        }
                    ]
                }
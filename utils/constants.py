import numpy as np

dmgTypes=["Standard","Strike","Slash","Pierce","Magic","Fire","Lightning","Holy"]
baseInfusions=["Heavy","Fire","Keen","Lightning","Magic","Cold","Sacred","Flame Art","Blood","Poison","Occult","Standard"]
infusionOrder=["Heavy","Hvy+Gse","Fire","Fire+FS","Keen","Keen+Gse","Lightning","Ltng+LS","Magic","Cold","Sacred","Scrd+SB","Flame Art","F.Art+FS","Blood","Poison","Occult","Quality","Qty+Gse","Standard","Std+Gse"] # for the table column names

idWeaponClass={ # refers to "wepType" in EquipParamWeapon
    29: "Halberds",
    25: "Spears",
    3: "Straight Swords",
    1: "Daggers",
    9: "Curved Swords",
    5: "Greatswords",
    7: "Colossal Swords",
    15: "Thrusting Swords",
    16: "Heavy Thrusting Swords",
    11: "Curved Greatswords",
    13: "Katanas",
    14: "Twinblades",
    21: "Hammers",
    23: "Greathammers",
    24: "Flails",
    17: "Axes",
    19: "Greataxes",
    28: "Great Spears",
    31: "Scythes",
    39: "Whips",
    35: "Fists",
    37: "Claws",
    41: "Colossal Weapons",
}

weaponClasses=idWeaponClass.values() # Halberds, Spears etc...

infusionOffset={ # offset to get "ID" from EquipParamWeapon with standard weapon ID
    "Standard":0,
    "Heavy":100,
    "Keen":200,
    "Quality":300, # lmao
    "Fire":400,
    "Flame Art":500,
    "Lightning":600,
    "Sacred":700,
    "Magic":800,
    "Cold":900,
    "Poison":1000,
    "Blood":1100,
    "Occult":1200,
}

forbiddenAshBuff={ # weapon classes incompatible with flaming strike, lightning slash and sacred blade
    "Fire":["Whips","Colossal Swords","Colossal Weapons"],
    "Flame Art":["Whips","Colossal Swords","Colossal Weapons"],
    "Lightning":["Halberds","Spears","Great Spears","Scythes","Whips","Fists","Claws"],
    "Sacred":["Whips","Fists","Claws"]
}

ashBuff={ # ash of war buff to apply depending on the infusion
    "Fire":["Fire+FS",np.array([0,0,0,0,0,90,0,0])],
    "Lightning":["Ltng+LS",np.array([0,0,0,0,0,0,90,0])],
    "Sacred":["Scrd+SB",np.array([0,0,0,0,0,0,0,90])],
    "Flame Art":["F.Art+FS",np.array([0,0,0,0,0,90,0,0])],
}

greaseBuff={ # grease to apply depending on the infusion
    "Heavy":["Hvy+Gse",np.array([0,0,0,0,0,0,110,0])],
    "Keen":["Keen+Gse",np.array([0,0,0,0,0,0,110,0])],
    "Standard":["Std+Gse",np.array([0,0,0,0,0,0,110,0])],
    "Quality":["Qty+Gse",np.array([0,0,0,0,0,0,110,0])],
}

claymanBuff={ # fuck clayman
    "Heavy":["Hvy+Gse",np.array([0,0,0,0,110,0,0,0])],
    "Keen":["Keen+Gse",np.array([0,0,0,0,110,0,0,0])],
    "Standard":["Std+Gse",np.array([0,0,0,0,110,0,0,0])],
    "Quality":["Qty+Gse",np.array([0,0,0,0,110,0,0,0])],
}

rareBuff={ # exceptions from the general rule
    "Treespear":["Std+Gse",np.array([0,0,0,0,0,0,0,110])],
    "Great Club":["Std+Gse",np.array([0,0,0,0,0,110,0,0])],
    "Troll's Hammer":["Std+Gse",np.array([0,0,0,0,0,110,0,0])],
}

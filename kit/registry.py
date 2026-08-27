"""The kit's family list. build_kit.py walks this in order.

CONTRACT -- every module in kit/pieces/ must define:

    FAMILY      = "stone_walls"              # matches the key below
    COLLECTION  = "01_Walls_Stone"           # one of spec.COLLECTIONS
    def build() -> list[bpy.types.Object]    # all pieces, built at the origin
    def demo()  -> list[bpy.types.Object]    # OPTIONAL: pieces snapped together
                                             # into a small arrangement, to prove
                                             # they actually fit. Built AFTER
                                             # build(), may reuse those objects.
"""
FAMILIES = {
    #  key              module                        collection           budget
    "stone_walls":  ("kit.pieces.stone_walls",   "01_Walls_Stone",     "wall"),
    "timber_walls": ("kit.pieces.timber_walls",  "02_Walls_Timber",    "wall"),
    "corners":      ("kit.pieces.corners",       "03_Corners_Posts",   "corner"),
    "roofs":        ("kit.pieces.roofs",         "04_Roof",            "roof"),
    "gables":       ("kit.pieces.gables",        "05_Gables",          "gable"),
    "dormers":      ("kit.pieces.dormers",       "06_Dormers",         "dormer"),
    "chimneys":     ("kit.pieces.chimneys",      "07_Chimneys",        "chimney"),
    "doors":        ("kit.pieces.doors",         "08_Doors",           "door"),
    "windows":      ("kit.pieces.windows",       "09_Windows",         "window"),
    "beams":        ("kit.pieces.beams",         "10_Beams_Corbels",   "beam"),
    "signage":      ("kit.pieces.signage",       "11_Signage_Lights",  "sign"),
    "props":        ("kit.pieces.props",         "12_Props",           "prop"),
    "ground":       ("kit.pieces.ground",        "13_Ground_Stairs",   "ground"),
    "foundations":  ("kit.pieces.foundations",   "14_Foundations",     "found"),
}
ORDER = list(FAMILIES)

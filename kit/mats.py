"""Shared materials. One material per palette entry, built on demand.

Every material multiplies its base tone by the mesh's "Col" vertex-colour
attribute, so util.Part's per-primitive tint jitter gives free variation with
no textures at all. Exports cleanly to glTF (COLOR_0 + PBR factors).
"""
import bpy
from . import spec as S

ROUGH = {
    "oak_dark": .74, "oak_mid": .72, "oak_pale": .70, "plaster": .86,
    "plaster_dim": .88, "stone": .80, "stone_dark": .82, "stone_pale": .78, "stone_warm": .80,
    "shingle": .78, "shingle_moss": .84, "moss": .90, "iron": .42,
    "glass": .18, "glass_dark": .11, "terracotta": .68, "flower_red": .74, "flower_gold": .74,
    "rope": .92, "thatch": .90,
}
METAL = {"iron": .75}
EMIT  = {"glass": 3.2}


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_lin(h):
    h = h.lstrip("#")
    return tuple(srgb_to_linear(int(h[i:i + 2], 16) / 255.0) for i in (0, 2, 4)) + (1.0,)


def get(name):
    """Return (creating if needed) the material for a palette key."""
    mat_name = "M_" + name
    m = bpy.data.materials.get(mat_name)
    if m:
        return m
    if name not in S.PALETTE:
        raise KeyError(f"{name!r} is not a palette key. Choose from: {sorted(S.PALETTE)}")
    m = bpy.data.materials.new(mat_name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (520, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (200, 0)
    col = nt.nodes.new("ShaderNodeVertexColor"); col.location = (-320, 120)
    col.layer_name = "Col"
    mix = nt.nodes.new("ShaderNodeMix"); mix.location = (-80, 60)
    mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
    mix.inputs["Factor"].default_value = 1.0
    mix.inputs[6].default_value = hex_lin(S.PALETTE[name])   # A
    nt.links.new(col.outputs["Color"], mix.inputs[7])        # B
    nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = ROUGH.get(name, .8)
    bsdf.inputs["Metallic"].default_value = METAL.get(name, 0.0)
    if name in EMIT:
        bsdf.inputs["Emission Color"].default_value = hex_lin(S.PALETTE[name])
        bsdf.inputs["Emission Strength"].default_value = EMIT[name]
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    m.diffuse_color = hex_lin(S.PALETTE[name])   # viewport/solid-mode colour
    return m


def build_all():
    for k in S.PALETTE:
        get(k)

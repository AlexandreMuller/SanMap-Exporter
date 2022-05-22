# ##### BEGIN LICENSE BLOCK #####
#
#  Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
#
#  This work is licensed under the Creative Commons
#  Attribution-NonCommercial 4.0 International License
#
#  To view a copy of this license,
#  visit https://creativecommons.org/licenses/by-nc/4.0/
#
# ##### END LICENSE BLOCK #####

import bpy
                    
#Criar textura de imagem com o nome da textura principal
node_image_texture = nodes.new(type='ShaderNodeTexImage')
node_image_texture.label = str(node_main_texture_label)
node_image_texture.image = bpy.data.images[str(main_texture)]
node_image_texture.location = -500, 0

#Criar o sombreador difuso
node_diffuse_bsdf = nodes.new(type='ShaderNodeBsdfDiffuse')
node_diffuse_bsdf.inputs['Roughness'].default_value = 1
node_diffuse_bsdf.location = -200, 0

#Criar saida do material
node_output  = nodes.new(type='ShaderNodeOutputMaterial')
node_output.location = 0, 0

#Linkar nodes
links = material.node_tree.links

#Linkar cor da textura com o sombreador difuso
links.new(node_image_texture.outputs['Color'], node_diffuse_bsdf.inputs['Color'])

#Linkar a saida do sombreador difuso com a saida do material
links.new(node_diffuse_bsdf.outputs['BSDF'], node_output.inputs['Surface'])

#-----------------------------------
#Modificar configuracoes do material
#-----------------------------------

#Alternar Blend Mode e Shadow Mode para Alpha Hashed nas configuracoes do material
material.blend_method = 'OPAQUE'
material.shadow_method = 'HASHED'
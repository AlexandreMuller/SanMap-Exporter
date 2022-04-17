# by Pommersch

import bpy

#Criar textura de imagem com o nome da textura principal
node_image_texture = nodes.new(type='ShaderNodeTexImage')
node_image_texture.label = str(node_main_texture_label)
node_image_texture.image = bpy.data.images[str(main_texture)]
node_image_texture.location = -700, 0

#Criar o sombreador difuso
node_diffuse_bsdf = nodes.new(type='ShaderNodeBsdfDiffuse')
node_diffuse_bsdf.inputs['Roughness'].default_value = 1
node_diffuse_bsdf.location = -400, -100

#Criar o sombreador transparente
node_transp_bsdf = nodes.new(type='ShaderNodeBsdfTransparent')
node_transp_bsdf.location = -390, 0

#Criar misturador de sombreador
node_mix_shader = nodes.new(type='ShaderNodeMixShader')
node_mix_shader.location = -190, 0

#Criar saida do material
node_output  = nodes.new(type='ShaderNodeOutputMaterial')
node_output.location = 0, 0

#Linkar nodes
links = blenderMat.node_tree.links

#Linkar cor da textura com o sombreador difuso
links.new(node_image_texture.outputs['Color'], node_diffuse_bsdf.inputs['Color'])

#Linkar o alpha da textura com o fator do misturador de sombreador
links.new(node_image_texture.outputs['Alpha'], node_mix_shader.inputs['Fac'])

#Linkar a saida do sombreador transparente com a segunda entrada do misturador de sombreador
links.new(node_transp_bsdf.outputs['BSDF'], node_mix_shader.inputs[1])

#Linkar a saida do sombreador difuso com a terceira entrada do misturador de sombreador
links.new(node_diffuse_bsdf.outputs['BSDF'], node_mix_shader.inputs[2])

#Linkar a saida do misturador de sombreador com a saida do material
links.new(node_mix_shader.outputs['Shader'], node_output.inputs['Surface'])

#--------------------------------------------------
#Modificar configuracoes do material e renderizacao
#--------------------------------------------------

#Alternar Blend Mode e Shadow Mode para Alpha Hashed nas configuracoes do material
blenderMat.blend_method = 'CLIP'
blenderMat.shadow_method = 'HASHED'

#Ativar/Desativar o Screen Space Refraction nas configuracoes do material
blenderMat.use_screen_refraction = False
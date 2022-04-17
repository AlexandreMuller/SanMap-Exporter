# by Pommersch

import bpy

# Pegar os objetos selecionados
objs = bpy.context.view_layer.objects.selected

# Objetos com erros
obj_error = []

# Modificar cada objeto que foi selecionado
for obj in objs:
    try:
        # Ativar os angulos das arestas
        obj.modifiers["EdgeSplit"].use_edge_angle = True
    except:
        # Adicionar objetos que nao foram possiveis de converter numa lista
        obj_error.append(obj.name)
        
print(f'\nObjetos com problemas:\n {obj_error}')
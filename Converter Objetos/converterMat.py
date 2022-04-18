# by Pommersch

import bpy
from PIL import Image

# Objetos selecionados
objects = bpy.context.selected_objects

matCount = 0        # Quantidade de materiais
file_errors = []    # Lista com materiais nao convertidos

folderPath = bpy.context.scene.my_tool.folderPath
folderPath = folderPath.replace('\\', '/')
folderPath = folderPath + '/'

# Indice dos objetos selecionados
index = 0

# Mostrar progresso da conversao
wm = bpy.context.window_manager
wm.progress_begin(0, len(objects))
step = 100/len(objects)
progress = 0

# Mostrar pequena janela de conclusao
def ShowMessageBox(message = "", title = "Concluido!", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    
for i in objects:
    material_slot = objects[index].material_slots
    for m in material_slot:
        material = m.material
        blenderMat = material
        blenderMat.use_nodes = True
        nodes = blenderMat.node_tree.nodes
        
        #Pegar o nome da textura principal do material
        try:
            node_main_texture = blenderMat.node_tree.nodes['Textura de imagem']
            main_texture = node_main_texture.image.name
            #Pegar rotulo do node
            node_main_texture_label = node_main_texture.label
            
            # Caminho da textura para checar se a imagem possui canal alpha
            check_alpha = Image.open(folderPath + main_texture)
        except:
            file_errors.append(m.name + ': ' + main_texture)
        
        # Verifique se a textura possui alpha
        if check_alpha.mode == 'RGBA':
            isAlpha = True
        else:
            isAlpha = False
            
        #APAGAR TODOS OS NOS
        nodes.clear()
        
        if isAlpha:
            # Material opaco com transparencia
            diffuseAlpha = bpy.data.texts["diffuseAlpha.py"]
            exec(diffuseAlpha.as_string())
        else:
            # Material apenas opaco
            diffuse = bpy.data.texts["diffuse.py"]
            exec(diffuse.as_string())
            
        matCount +=1
    index += 1
    
    # Atualizar o progresso
    progress += step
    wm.progress_update(progress)

# Finalizar progresso
wm.progress_end()

#Ativar/Desativar o Screen Space Reflections e a refracao dos materiais
bpy.context.scene.eevee.use_ssr = False
bpy.context.scene.eevee.use_ssr_refraction = False

# Mostrar mensagem ao concluir
ShowMessageBox(f'Objetos: {index}  Materiais convertidos: {matCount}  Erros: {len(file_errors)}')

# Erros
print(f"Não existe tal arquivo ou diretório\n{file_errors}")
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
import os

from bpy_extras.io_utils import ImportHelper
from bpy.types import Panel, Operator
from bpy.props import StringProperty

class ObjectPanel(Panel):
    bl_label = "Find Object ID"
    bl_idname = "Object_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "GTA SA Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.label(text = "Encontrar ID dos objetos selecionados")
        
        row = layout.row()
        row.label(text = "Abrir arquivo IDE")
        layout.operator("abrir_ide.open_filebrowser", icon="ZOOM_ALL")

# Abrir o File Browser para abrir o arquivo
class OpenIDEFile(Operator, ImportHelper):
    bl_label = "Buscar"
    bl_idname = "abrir_ide.open_filebrowser"

    # Mostrar arquivos com determinada extensao
    filter_glob: StringProperty(
        default = '*.ide;*.txt',
        options = {'HIDDEN'}
    )

    def execute(self, context):
        # Caminho e extensao do arquivo
        filename, extension = os.path.splitext(self.filepath)

        # Pegar os objetos selecionados
        objs = bpy.context.view_layer.objects.selected
        
        # Ler o arquivo
        objetos_desejados = open(self.filepath, "r")
        read_ide = objetos_desejados.readlines()

        obj_dff = []
        obj_error = []

        # Adicionar cada linha do arquivo em uma lista
        for i in read_ide:
            obj_dff.append(i.split('\n')[0].lower())

        # Modificar cada objeto que foi selecionado
        for obj in objs:
            try:
                # Procurar o nome do objeto na lista
                matching = [s for s in obj_dff if obj.name.lower() in s]
        
                # Adicionar a ID encontrada no objeto
                id = matching[0].split(',', 2)[0]
                obj["OBJ"] = str(id)
            except:
                # Adicionar objetos que nao foram possiveis de converter numa lista
                obj_error.append(obj.name)
        
        # Mostrar mensagem ao concluir
        if len(obj_error) < len(objs):
            ShowMessageBox(f"ID adicionadas: {len(objs) - len(obj_error)} Erros: {len(obj_error)}")
        else:
            ShowMessageBox(f"Nao foi possivel adicionar os ID", "Erro!", 'ERROR')
        
        print(f'\nObjetos com problemas:\n {obj_error}')
        
        return {'FINISHED'}

# Mostrar pequena janela de conclusao
def ShowMessageBox(message = "", title = "Concluido!", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

# Lista contendo as classes
classes = [ObjectPanel, OpenIDEFile]

# Registrar as classes
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
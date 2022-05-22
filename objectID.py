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

# Painel principal
class FIND_PT_IDPainelPrincipal(Panel):
    bl_label = "Find Object ID"
    bl_idname = "FIND_PT_IDPainelPrincipal"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "GTA SA Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text = "Abrir arquivo de busca")
        layout.operator("abrir_idfile.open_filebrowser", icon="ZOOM_ALL")

# Abrir o File Browser para abrir o arquivo
class OPEN_OP_IDFile(Operator, ImportHelper):
    bl_label = "Buscar"
    bl_idname = "abrir_idfile.open_filebrowser"

    # Mostrar arquivos com determinada extensao
    filter_glob: StringProperty(
        default = '*.txt;*.ide',
        options = {'HIDDEN'}
    )

    def execute(self, context):
        items = []
        erros = []
        
        # Caminho e extensao do arquivo
        filename, extension = os.path.splitext(self.filepath)
        
        try:
            # Ler o arquivo
            objetos_desejados = open(self.filepath, "r")
            for i in objetos_desejados:
                x = i.split(',')
                try:
                    items.append({'ID': x[0].split()[0], 'Nome': x[1].split()[0]})
                except:
                    pass
        except:
            self.report({'ERROR'}, 'A formateção do arquivo está incorreta ou possui problemas')
            
            return {'CANCELLED'}
        
        # Pegar os objetos selecionados
        objects = bpy.context.selected_objects
        
        if len(objects) != 0:
            # Procurar o nome do objeto na lista
            for obj in objects:
                notFound = True
                objName = obj.name.split('.')[0].lower()
                for i in items:
                    itemName = i['Nome']
                    if itemName.lower() == objName:
                        obj["INST"] = str(i['ID'])
                        notFound = False
                        break
                if notFound:
                    erros.append(obj.name)
        
            # Mostrar mensagem ao concluir
            if len(erros) < len(objects):
                self.report({'INFO'}, f"ID adicionadas: {len(objects) - len(erros)} Não encontrados: {len(erros)}")
            else:
                self.report({'WARNING'}, 'Nenhum objeto foi encontrado!')
            
        else:
            self.report({'WARNING'}, 'Selecione ao menos um objeto!')
        
        return {'FINISHED'}

# Lista das classes
classes = (
    FIND_PT_IDPainelPrincipal,
    OPEN_OP_IDFile
)

#Registrar as classes
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
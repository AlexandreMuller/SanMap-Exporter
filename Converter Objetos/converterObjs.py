# by Pommersch

import bpy
import os

from bpy_extras.io_utils import ImportHelper
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, PointerProperty

class MyProperties(PropertyGroup):
    folderPath: StringProperty(name = "", default = "")

class PainelPrincipal(Panel):
    bl_label = "Converter Objetos"
    bl_idname = "ADDONNAME_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GTA SA Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        #layout.prop(mytool, "folderPath")
        layout.operator("folder_path.open_folderbrowser", icon="FILEBROWSER")
        layout.operator("convert_mat.button_operator")
        layout.operator("modify_obj.button_operator")
        
# Abrir o Folder Browser para definir o diretorio
class FolderPath(Operator, ImportHelper):
    bl_label = "Abrir pasta"
    bl_idname = "folder_path.open_folderbrowser"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        folderPath = mytool.folderPath
        
        MyProperties.folderPath = os.path.dirname(self.filepath)
  
        return {'FINISHED'}

class ConverterMat_Button(Operator):
    bl_label = "Converter Materiais"
    bl_idname = "convert_mat.button_operator"

    def execute(self, context):
        conv_mat = bpy.data.texts["converterMat.py"]
        exec(conv_mat.as_string())
        return {'FINISHED'}


class ModificarObj_Button(Operator):
    bl_label = "Modificar Objetos"
    bl_idname = "modify_obj.button_operator"

    def execute(self, context):
        conv_obj = bpy.data.texts["modificarObj.py"]
        exec(conv_obj.as_string())
        return {'FINISHED'}

classes = [MyProperties, PainelPrincipal, FolderPath, ConverterMat_Button, ModificarObj_Button]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.my_tool = PointerProperty(type = MyProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()
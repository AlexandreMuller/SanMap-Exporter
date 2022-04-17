# by Pommersch

import bpy

from bpy.types import Operator, Panel


class PainelPrincipal(Panel):

    bl_label = "Converter Objetos"
    bl_idname = "ADDONNAME_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GTA SA Tools'

    def draw(self, context):
        layout = self.layout
        layout.operator("convert_mat.button_operator")
        layout.operator("modify_obj.button_operator")

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

classes = [PainelPrincipal, ConverterMat_Button, ModificarObj_Button]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
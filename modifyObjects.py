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

from bpy.types import Panel, PropertyGroup
from bpy.props import PointerProperty, BoolProperty, FloatVectorProperty, EnumProperty

# Pegar os objetos selecionados
objs = bpy.context.selected_objects

# Viewport Display
def showName(self, context):
    scene = context.scene
    modobjs = scene.modobjs
    
    for obj in objs:
        try:
            if modobjs.showName:
                obj.show_name = True
            else:
                obj.show_name = False
        except:
            pass
        
def shadow(self, context):
    scene = context.scene
    modobjs = scene.modobjs

    for obj in objs:
        try:
            if modobjs.shadow:
                obj.display.show_shadows = True
            else:
                obj.display.show_shadows = False
        except:
            pass
        
def inFront(self, context):
    scene = context.scene
    modobjs = scene.modobjs

    for obj in objs:
        try:
            if modobjs.inFront:
                obj.show_in_front = True
            else:
                obj.show_in_front = False
        except:
            pass
        
def newColor(self, context):
    scene = context.scene
    modobjs = scene.modobjs

    for obj in objs:
        try:
            obj.color = modobjs.newColor
        except:
            pass
        
def displayAs(self, context):
    scene = context.scene
    modobjs = scene.modobjs
    displayAs = modobjs.displayAs

    for obj in objs:
        try:
            if displayAs == "0":
                obj.display_type = 'TEXTURED'
            elif displayAs == "1":
                obj.display_type = 'SOLID'
            elif displayAs == "2":
                obj.display_type = 'WIRE'
            elif displayAs == "3":
                obj.display_type = 'BOUNDS'
        except:
            pass
                
class MODOBJS_Propriedades(PropertyGroup):
    # Propriedades da Viewport Display
    showName: BoolProperty(
        name = "Show Name",
        default = False,
        update = showName
    )
    shadow: BoolProperty(
        name = "Shadow",
        default = True,
        update = shadow
    )
    inFront: BoolProperty(
        name = "In Front",
        default = False,
        update = inFront
    )
    newColor: FloatVectorProperty(
        name = "Color",
        subtype = "COLOR",
        size = 4,
        min = 0.0,
        max = 1.0,
        default = [1,1,1,1],
        update = newColor
    )
    displayAs: EnumProperty(
        name = "Display As",
        update = displayAs,
        items = [("0", "Textured", ""),
                 ("1", "Solid", ""),
                 ("2", "Wire", ""),
                 ("3", "Bounds", "")]
    )

# Criar o painel principal
class MainPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GTA SA Tools'
    bl_options = {"DEFAULT_CLOSED"}

class MODOBJS_PT_PainelPrincipal(MainPanel, Panel):
    bl_idname = "MODIFY_PT_ObjsPanel"
    bl_label = "Modificar Objetos"

    def draw(self, context):
        pass

# Painel com as configuracoes da Viewport Display
class VIEWDISPLAY_PT_Panel(MainPanel, Panel):
    bl_parent_id = "MODIFY_PT_ObjsPanel"
    bl_label = "Viewport Display"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        modobjs = scene.modobjs

        layout.prop(modobjs, "showName")
        layout.prop(modobjs, "shadow")
        layout.prop(modobjs, "inFront")
        layout.prop(modobjs, "newColor")
        layout.prop(modobjs, "displayAs")

# Nome das classes
classes = [MODOBJS_Propriedades, MODOBJS_PT_PainelPrincipal, VIEWDISPLAY_PT_Panel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.modobjs = PointerProperty(type = MODOBJS_Propriedades)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.modobjs

if __name__ == "__main__":
    register()
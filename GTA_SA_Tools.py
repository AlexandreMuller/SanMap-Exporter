# Script parcialmente baseado no GTARW-BlenderMapExport - https://github.com/ajanhallinta/GTARW-BlenderMapExport

# by Pommersch

import bpy
import os
import math

from bpy_extras.io_utils import ImportHelper
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, PointerProperty, IntProperty, BoolProperty, EnumProperty
from math import pi

bl_info = {
    "name": "GTA SA Tools",
    "location": "View3D > Tools > GTA SA Tools",
    "support": "NONE",
    "category": "Tool"
}

# Carregar o script para encontrar ID dos objetos
findObjectScript = bpy.data.texts["objectID.py"]
exec(findObjectScript.as_string())

class MyProperties(PropertyGroup):
    # Alternar entre selecionados e todos da cena
    selectObjsToggle: BoolProperty(name = "Selecionados apenas", default = False)
    
    # Propriedades COL
    applyLightSettings: BoolProperty(default = True)
    matBrightness: IntProperty(default = 235)
    matLight: IntProperty(default = 235)
    
    # Propriedades IPL
    lod: IntProperty(name = "LOD", min = -1, max = 1, default = -1)
    interior: IntProperty(name = "Interior", min = 0, max = 1, default = 0)
    modelName: BoolProperty(name = "Usar nome do dff", default = False)
    modelDummy: StringProperty(name = "Nome", default = "dummy")

    # Propriedades IDE
    my_list = []
    id: IntProperty(name = "ID", min=0, default=14000)
    distancia: IntProperty(min = 0, default = 200)
    flags: IntProperty(min = 0, default = 0)
    dffBool: BoolProperty(default = True)
    txdName: StringProperty()

    toDFF: EnumProperty(
        name = "COL or DFF",
        description = "converter para",
        items = [('OP1', "COL", ""),
                 ('OP2', "DFF", "")]
    )

class COLPanel(Panel):
    bl_label = "GTA SA COL"
    bl_idname = "COL_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "GTA SA Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.label(text = "Converter para COL ou DFF")

        row = layout.row()
        layout.prop(mytool, "toDFF", expand = True)
        layout.prop(mytool, "applyLightSettings", text = "Aplicar configurações de luz")
        layout.prop(mytool, "matBrightness", text = "Brilho do Material")
        layout.prop(mytool, "matLight", text = "Luz do Material")
        layout.operator("wm.template_operator", icon = "UV_SYNC_SELECT")

# Nomes das texturas do modelo que representam a superfície de colisão específica.
gramaCurta = ['grass2']
gramaLonga = ['forestground1', 'forestground', 'desgreengrass']
gramaFina = ['finegrass', 'finegrass1']
cascalho = ['gravel2', 'gravel1', 'gravel', 'desertgravelgrassroad', 'dirttracksgrass256']
vidro = ['windows', 'windows2', 'wwindow', 'storewindow']
asfalto = ['road1', 'concrete3', 'Tar_1line256HV', 'dt_road_stoplinea', 'roadnew4_512']

class COLConvert(Operator):
    bl_label = "Converter"
    bl_idname = "wm.template_operator"

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        toDFF = mytool.toDFF
        applyLightSettings = mytool.applyLightSettings
        matBrightness = mytool.matBrightness
        matLight = mytool.matLight

        if toDFF == 'OP1':
            toDFF = 0
        else:
            toDFF = 1

        def setColSurface(mat, ob):
            for slot in ob.material_slots:
                thatMaterial = slot.material
                mat = thatMaterial
                mat.dff.col_mat_index = 0
                thatTexture = thatMaterial.node_tree.nodes["Textura de imagem"]
                if thatTexture.image:
                    matname = thatTexture.image.name.replace(
                        ".bmp", "").replace(".png", "").replace(".PNG", "")
                    if any(matname in s for s in gramaLonga):
                        mat.dff.col_mat_index = 14
                        print("long grass col set to ", ob.name)
                    if any(matname in s for s in gramaCurta):
                        mat.dff.col_mat_index = 9
                        print("short grass col set to ", ob.name)
                    if any(matname in s for s in gramaFina):
                        mat.dff.col_mat_index = 16
                        print("fine grass col set to ", ob.name)
                    if any(matname in s for s in cascalho):
                        mat.dff.col_mat_index = 6
                        print("gravel col set to ", ob.name)
                    if any(matname in s for s in vidro):
                        mat.dff.col_mat_index = 45
                        print("glass col set to ", ob.name)
                    if any(matname in s for s in asfalto):
                        mat.dff.col_mat_index = 1
                        print("asphalt col set to ", ob.name)

        def convertToVisualObjects():
            for collection in bpy.data.collections:
                collection.name = collection.name.replace(".dff", "") + ".dff"
                print(collection.name)

            for ob in scene.objects:
                if ob.type == 'MESH':
                    ob.dff.type = "OBJ"
                    print(ob.name + ": " + ob.dff.type)

        def convertToCollisionObjects():
            for collection in bpy.data.collections:
                collection.name = collection.name.replace(".dff", "")
                print(collection.name)

            for ob in scene.objects:
                if ob.type == 'MESH':
                    ob.dff.type = "COL"
                    for mat in ob.data.materials:
                        if applyLightSettings == 1:
                            mat.dff.col_brightness = matBrightness
                            mat.dff.col_light = matLight
                    setColSurface(mat, ob)

        scene = bpy.context.scene

        if toDFF is 1:
            convertToVisualObjects()
        else:
            convertToCollisionObjects()

        return {'FINISHED'}


# ------------------------------------------------------------------------
# -------------------------------GTA SA IPL-------------------------------
# ------------------------------------------------------------------------

class IPLPanel(Panel):
    bl_label = "GTA SA IPL"
    bl_idname = "IPL_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "GTA SA Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        modelName = mytool.modelName

        row = layout.row()
        row.label(text = "Converter transformações para IPL")
        row = layout.row()
        row.label(text = "apenas objetos com a propriedade 'OBJ'")

        row = layout.row()
        layout.prop(mytool, "lod")
        layout.prop(mytool, "interior")
        layout.prop(mytool, "modelName")
        
        if modelName == False:
            layout.prop(mytool, "modelDummy")
        
        row = layout.row()
        layout.prop(mytool, "selectObjsToggle")
        layout.operator("salvar_ipl.open_filebrowser", icon="CURRENT_FILE")

# Abrir o File Browser para salvar o arquivo
class SaveIPLFile(Operator, ImportHelper):
    bl_label = "Salvar"
    bl_idname = "salvar_ipl.open_filebrowser"
    
    # Arredondar valores
    roundDec: IntProperty(name = "Casas decimais", min = 0, max = 10, default = 5)

    # Mostrar arquivos com determinada extensao
    filter_glob: StringProperty(
        default = '*.ipl;*.txt',
        options = {'HIDDEN'}
    )

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        lod = mytool.lod
        interior = mytool.interior
        modelName = mytool.modelName
        modelDummy = mytool.modelDummy
        roundDec = self.roundDec
        selectObjsToggle = mytool.selectObjsToggle

        # Caminho e extensao do arquivo
        filename, extension = os.path.splitext(self.filepath)

        # Escrever o arquvio .IPL
        with open(self.filepath, "w") as file:
            file.write("inst\n")

            # Pegar apenas objetos selecionados que possuem a propriedade 'OBJ'
            if selectObjsToggle:
                objects = [obj for obj in bpy.context.view_layer.objects.selected if "OBJ" in obj]
            # Pegar todos os objetos que possuem a propriedade 'OBJ'
            else:
                objects = [obj for obj in bpy.data.objects if "OBJ" in obj]

            for obj in objects:
                # ID do objeto
                dffID = obj['OBJ']
                
                # Nome do objeto
                nome = ''

                # Verifique o nome do objeto
                if modelName:
                    nome = obj.name.split('.')[0]
                else:
                    nome = modelDummy
                
                # Posicoes globais do objeto
                posX = obj.location.x
                posY = obj.location.y
                posZ = obj.location.z
                
                # Modo de rotacao atual do objeto
                currentRot = obj.rotation_mode
                
                # Alterar modo de rotacao para quaternion
                obj.rotation_mode = 'QUATERNION'
                
                # Rotacao em quaternion do objeto
                rotW = obj.rotation_quaternion[0]
                rotX = obj.rotation_quaternion[1]
                rotY = obj.rotation_quaternion[2]
                rotZ = obj.rotation_quaternion[3]
                
                # Inverter rotacao em W
                rotW = -rotW
                
                # Retornar para o modo de rotacao
                obj.rotation_mode = currentRot
                
                # Arredondar posicoes
                posX = ("%." + str(roundDec) + "f") % posX
                posY = ("%." + str(roundDec) + "f") % posY
                posZ = ("%." + str(roundDec) + "f") % posZ
                    
                # Arredondar rotacoes
                rotW = ("%." + str(roundDec) + "f") % rotW
                rotX = ("%." + str(roundDec) + "f") % rotX
                rotY = ("%." + str(roundDec) + "f") % rotY
                rotZ = ("%." + str(roundDec) + "f") % rotZ
                
                iplString = "%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s,\t%s" % (dffID, nome, interior, posX, posY, posZ, rotX, rotY, rotZ, rotW, lod)

                # Escrever as informacoes no arquivo selecionado
                file.write(iplString)
                file.write("\n")
            file.write("end\n")
        
        # Mostrar mensagem ao concluir
        ShowMessageBox("IPL salvo com sucesso!", "Concluido!", 'DISK_DRIVE')
        
        return {'FINISHED'}


# ------------------------------------------------------------------------
# -------------------------------GTA SA PAWN------------------------------
# ------------------------------------------------------------------------

class PWNPanel(Panel):
    bl_label = "GTA SA PAWN"
    bl_idname = "PWN_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "GTA SA Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        selectObjsToggle = mytool.selectObjsToggle

        row = layout.row()
        row.label(text = "Converter transformações para PAWN")
        row = layout.row()
        row.label(text = "apenas objetos com a propriedade 'OBJ'")
        
        row = layout.row()
        layout.prop(mytool, "selectObjsToggle")
        layout.operator("salvar_pwn.open_filebrowser", icon = "CURRENT_FILE")

# Abrir o File Browser para salvar o arquivo
class SavePWNFile(Operator, ImportHelper):
    bl_label = "Salvar"
    bl_idname = "salvar_pwn.open_filebrowser"
    
    # Arredondar valores
    roundDec: IntProperty(name = "Casas decimais", min = 0, max = 10, default = 5)

    # Mostrar arquivos com determinada extensao
    filter_glob: StringProperty(
        default = '*.pwn;*.txt',
        options = {'HIDDEN'}
    )

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        selectObjsToggle = mytool.selectObjsToggle
        roundDec = self.roundDec

        # Caminho e extensao do arquivo
        filename, extension = os.path.splitext(self.filepath)

        print('Arquivo selecionado: ', self.filepath)
        # Escrever o arquvio .PWN
        with open(self.filepath, "w") as file:
            file.write("inst\n")

            # Pegar apenas objetos selecionados que possuem a propriedade 'OBJ'
            if selectObjsToggle:
                objects = [obj for obj in bpy.context.view_layer.objects.selected if "OBJ" in obj]
            # Pegar todos os objetos que possuem a propriedade 'OBJ'
            else:
                objects = [obj for obj in bpy.data.objects if "OBJ" in obj]
                
            for obj in objects:

                # ID do objeto
                dffID = obj['OBJ']

                # Posicoes globais do objeto
                posX = obj.location.x
                posY = obj.location.y
                posZ = obj.location.z
                
                # Modo de rotacao atual do objeto
                currentRot = obj.rotation_mode
                
                # Alterar modo de rotacao para quaternion
                obj.rotation_mode = 'XYZ'

                # Rotacao em graus do objeto
                rotX = math.degrees(obj.rotation_euler.x)
                rotY = math.degrees(obj.rotation_euler.y)
                rotZ = math.degrees(obj.rotation_euler.z)
                
                # Retornar para o modo de rotacao
                obj.rotation_mode = currentRot
                
                # Arredondar posicoes
                posX = ("%." + str(roundDec) + "f") % posX
                posY = ("%." + str(roundDec) + "f") % posY
                posZ = ("%." + str(roundDec) + "f") % posZ
                    
                # Arredondar rotacoes
                rotX = ("%." + str(roundDec) + "f") % rotX
                rotY = ("%." + str(roundDec) + "f") % rotY
                rotZ = ("%." + str(roundDec) + "f") % rotZ

                iplString = "%s%s, \t%s, \t%s, \t%s, \t%s, \t%s, \t%s%s" % ("CreateObject(", dffID, posX, posY, posZ, rotX, rotY, rotZ, ");")

                # Escrever as informacoes no arquivo selecionado
                file.write(iplString)
                file.write("\n")
            file.write("end\n")
            
        # Mostrar mensagem ao concluir
        ShowMessageBox("PAWN salvo com sucesso!", "Concluido!", 'DISK_DRIVE')
        
        return {'FINISHED'}


# ------------------------------------------------------------------------
# -------------------------------GTA SA IDE-------------------------------
# ------------------------------------------------------------------------

class IDEPanel(Panel):
    bl_label = "GTA SA IDE"
    bl_idname = "IDE_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GTA SA Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        dffBool = mytool.dffBool

        row = layout.row()
        layout.prop(mytool, "distancia", text = 'Distance')

        row = layout.row()
        layout.prop(mytool, "flags", text = 'Flags ')

        row = layout.row()
        row.label(text = "Nome do TXD:")
        myBool = layout.prop(mytool, "dffBool", text = "Igual ao DFF")
        
        if dffBool == False:
            layout.prop(mytool, "txdName", text = "Nome")

        row = layout.row()
        layout.prop(mytool, "selectObjsToggle")
        layout.prop(mytool, "id", text = 'ID ')
        layout.operator("add.obj")
        layout.operator("remove.obj")

        row = layout.row()
        layout.operator("ide_save.export", icon = "CURRENT_FILE")

class ADD_BUTTON(Operator):
    bl_label = "Add"
    bl_idname = "add.obj"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        id = mytool.id
        distancia = mytool.distancia
        flags = mytool.flags
        txdName = mytool.txdName
        my_list = mytool.my_list
        dffBool = mytool.dffBool
        selectObjsToggle = mytool.selectObjsToggle
        
        # Pegar apenas objetos selecionados que possuem a propriedade 'OBJ'
        if selectObjsToggle:
            objects = [obj for obj in bpy.context.view_layer.objects.selected if "OBJ" in obj]
        # Pegar todos os objetos que possuem a propriedade 'OBJ'
        else:
            objects = [obj for obj in bpy.data.objects if "OBJ" in obj]
                
        for obj in objects:
            name = obj.name.split('.')[0]

            if dffBool == True:
                txdName = name
            
            # ID do objeto
            # ID = obj['ID']

            objs = "%s, %s, %s, %s, %s" % (id, name, txdName, distancia, flags)

            if objs != "":
                if objs not in my_list:
                    my_list.append(objs)
            else:
                my_list.clear()
            print(my_list)

        return {'FINISHED'}

class REMOVE_BUTTON(Operator):
    bl_label = "Remove"
    bl_idname = "remove.obj"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        id = mytool.id
        distancia = mytool.distancia
        flags = mytool.flags
        txdName = mytool.txdName
        my_list = mytool.my_list
        dffBool = mytool.dffBool
        selectObjsToggle = mytool.selectObjsToggle
        
        # Pegar apenas objetos selecionados que possuem a propriedade 'OBJ'
        if selectObjsToggle:
            objects = [obj for obj in bpy.context.view_layer.objects.selected if "OBJ" in obj]
        # Pegar todos os objetos que possuem a propriedade 'OBJ'
        else:
            objects = [obj for obj in bpy.data.objects if "OBJ" in obj]
                
        for obj in objects:
            name = obj.name.split('.')[0]

            if dffBool == True:
                txdName = name
                
            # ID do objeto
            # ID = obj['ID']

            objs = "%s, %s, %s, %s, %s" % (id, name, txdName, distancia, flags)

            if objs in my_list:
                my_list.remove(objs)
            print(my_list)

        return {'FINISHED'}

class SaveIDEFile(Operator, ImportHelper):
    bl_label = "Save"
    bl_idname = "ide_save.export"

    # Mostrar apenas arquivos com a determinada extensao
    filter_glob: StringProperty(
        default = '*.ide;*.txt',
        options = {'HIDDEN'}
    )

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        my_list = mytool.my_list

        # Caminho e extensao do arquivo
        filename, extension = os.path.splitext(self.filepath)

        with open(self.filepath, "w") as file:

            file.write("objs\n")
            x = ('\n'.join(map(str, my_list)))
            file.write(x)
            file.write("\n")
            file.write("end\n")
        
        # Mostrar mensagem ao concluir
        ShowMessageBox("IDE salvo com sucesso!", "Concluido!", 'DISK_DRIVE')

        return {'FINISHED'}

# Mostrar pequena janela de conclusao
def ShowMessageBox(message = "", title = "Concluido!", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

# Lista contendo as classes
#classes = [MyProperties, COLPanel, COLConvert, IPLPanel, SaveIPLFile, PWNPanel, SavePWNFile, IDEPanel, ADD_BUTTON, REMOVE_BUTTON, SaveIDEFile]
classes = [MyProperties, IPLPanel, SaveIPLFile, PWNPanel, SavePWNFile, IDEPanel, ADD_BUTTON, REMOVE_BUTTON, SaveIDEFile]

# Registrar as classes
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
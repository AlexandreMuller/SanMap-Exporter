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
import math
import os

from bpy_extras.io_utils import ExportHelper
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, PointerProperty, IntProperty, BoolProperty, EnumProperty

# Items
assaultRifles = ('26, AK-47', "AK-47", ''),('27, M4', "M4", '')
gifts = ('33, Large_Purple_Dildo', "Large Purple Dildo", ''),('34, Small_White_Dildo', "Small White Dildo", ''),('35, Large_White_Vibrator', "Large White Vibrator", ''),('36, Small_Black_Vibrator', "Small Black Vibrator", ''),('37, Flowers', "Flowers", ''),('38, Cane', "Cane", '')
handguns = ('18, Colt_45', "Colt 45", ''),('19, Colt_45_Silenced', "Colt 45 Silenced", ''),('20, Deagle', "Deagle", '')
heavyWeapons = ('31, Flamethrower', "Flamethrower", ''),('32, Minigun', "Minigun", ''),('46, Rocket_Launcher', "Rocket Launcher", ''),('47, Rocket_Launcher_HS', "Rocket Launcher HS", '')
melee = ('10, Bat', "Bat", ''),('4, Brassknuckle', "Brassknuckle", ''),('14, Chainsaw', "Chainsaw", ''),('9, Golfclub', "Golfclub", ''),('13, Katana', "Katana", ''),('6, Knife', "Knife", ''),('5, Nightstick', "Nightstick", ''),('12, Poolstick', "Poolstick", ''),('11, Shovel', "Shovel", '')
projectiles = ('16, Grenade', "Grenade", ''),('15, Molotov', "Molotov", ''),('17, Satchel', "Satchel", ''),('43, Teargas', "Teargas", '')
rifles = ('28, Country_Rifle', "Country Rifle", ''),('29, Sniper_Rifle', "Sniper Rifle", '')
special = ('51, Camera', "Camera", ''),('41, Cellphone', "Cellphone", ''),('48, Detonator', "Detonator", ''),('50, Fire_Extinguisher', "Fire Extinguisher", ''),('53, Infrared', "Infrared Goggles", ''),('52, Nightvision', "Nightvision Goggles", ''),('54, Jetpack', "Jetpack", ''),('55, Parachute', "Parachute", ''),('49, Spraycan', "Spraycan", '')
subMachine = ('25, MP5', "MP5", ''),('23, Tec-9', "Tec-9", ''),('24, Uzi', "Uzi", '')
shotguns = ('22, Combat_Shotgun', "Combat Shotgun", ''),('21, Shotgun', "Shotgun", '')

beta = assaultRifles, gifts, handguns, heavyWeapons, melee, projectiles, rifles, shotguns, special, subMachine

# Atualizar e selecionar o dropdown correspondente
def selectEnum(self, context):
    # Indice das categorias
    index = int(context.scene.gunCategory)
    
    # Selecionar o dropdown de acordo com a categoria da arma
    enum_items = beta[index]

    return enum_items

# Propriedades
class Propriedades(PropertyGroup):
    # Verifique objetos selecionados
    selectObjsToggle: BoolProperty(name = "Selecionados apenas", default = False)

# Painel principal
class PICKPanel(Panel):
    bl_label = "Adicionar Pickup"
    bl_idname = "PICK_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "GTA SA Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        picktool = scene.picktool
        selectObjsToggle = picktool.selectObjsToggle
        
        # Selecionar arma
        row = layout.row()
        layout.prop(scene, "gunCategory")
        layout.prop(scene, "weapons")

        # Botao para adicionar
        row = layout.row()
        layout.operator("adicionar.veh")
        
        # Toggle para objetos selecionados
        row = layout.row()
        layout.prop(picktool, "selectObjsToggle")

        # Salvar arquivo
        layout.operator("pick_save.export", icon = "CURRENT_FILE")

# Operador para adicionar pickup
class ADDPickup(Operator):
    bl_label = "Adicionar"
    bl_idname = "adicionar.veh"

    def draw(self, context):
        layout = self.layout

    def execute(self, context):
        scene = context.scene
        picktool = scene.picktool
        gunCategory = scene.gunCategory
        weapons = scene.weapons
        
        # Lista para os nomes do material e cores do pickup
        materiais = ["assaultRiflesMat", "giftsMat", "handgunsMat", "heavyWeaponsMat", "meleeMat", "projectilesMat", "riflesMat", "shotgunsMat", "specialMat", "subMachineMat"]
        cores = (1, 0.05, 0, 1),(1, 0, 1, 1),(0, 1, 1, 1),(1, 0, 0, 1),(1, 1, 1, 1),(0.7, 0.5, 0.6, 1),(0, 0, 1, 1),(1, 1, 0, 1),(0.01, 0.01, 0.03, 1),(0, 1, 0, 1)
        
        # ID do pickup
        pickID = weapons.split()[0]
        pickID = pickID.replace(',', '')
        
        # Nome do pickup
        pickName = weapons.split()[1]
        
        # Nome do material e cor do pickup
        materialName = materiais[int(gunCategory)]
        pickupColor = cores[int(gunCategory)]
        
        # Adicionar cubo
        newPickup = bpy.ops.mesh.primitive_cube_add(scale = (0.25, 0.25, 0.25))
    
        # Objeto ativo
        pickup = bpy.context.object
        
        # Incrementar localizacao em Z
        pickup.location.z += 1
        
        # Mostrar aramado
        pickup.show_wire = True
        
        # Desativar sombras
        pickup.display.show_shadows = False
        
        # Mostrar como solido
        pickup.display_type = 'SOLID'

        # Alterar cor
        pickup.color = pickupColor

        # Verificar se o material do pickup ja existe
        newMaterial = True
        for mat in bpy.data.materials:
            if mat.name == materialName:
                # Adicionar material no pickup
                pickup.data.materials.append(bpy.data.materials[materialName])
                newMaterial = False
                break

        if newMaterial:
            # Criar novo material
            pickupMaterial = bpy.data.materials.new(name = materialName)
            
            # Ativar nodes
            pickupMaterial.use_nodes = True
            
            # Nodes do material
            nodes = pickupMaterial.node_tree.nodes
            
            # Apagar todos os nodes
            nodes.clear()
            
            #Criar o sombreador emissivo
            node_emissive = nodes.new(type="ShaderNodeEmission")
            node_emissive.inputs[1].default_value = 5
            node_emissive.inputs[0].default_value = pickupColor
            node_emissive.location = -200, 0

            #Criar saida do material
            node_output  = nodes.new(type='ShaderNodeOutputMaterial')
            node_output.location = 0, 0

            #Linkar nodes
            links = pickupMaterial.node_tree.links

            #Linkar a saida do sombreador emissivo com a saida do material
            links.new(node_emissive.outputs['Emission'], node_output.inputs['Surface'])

            # Adicionar material no pickup
            pickup.data.materials.append(pickupMaterial)

        # Nome do pickup
        pickup.name = pickName

        # ID do pickup
        pickup["PICK"] = pickID

        # Mostrar mensagem ao adicionar
        self.report({'INFO'}, f"Adicionado!  Nome: {pickName}   ID: {pickID}")

        return {'FINISHED'}

# Salvar arquivo
class SavePICKFile(Operator, ExportHelper):
    bl_label = "Salvar"
    bl_idname = "pick_save.export"

    # Arredondar valores
    roundDec: IntProperty(name = "Casas decimais", min = 0, max = 10, default = 5)
    
    filename_ext = ".ipl"

    # Mostrar apenas arquivos com a determinada extensao
    filter_glob: StringProperty(
        default = "*.ipl;*.txt",
        options = {"HIDDEN"}
    )

    def execute(self, context):
        scene = context.scene
        picktool = scene.picktool
        selectObjsToggle = picktool.selectObjsToggle
        roundDec = self.roundDec
    
        # Caminho e extensao do arquivo
        filename, extension = os.path.splitext(self.filepath)

        # Pegar apenas objetos selecionados que possuem a propriedade 'PICK'
        if selectObjsToggle:
            pickups = [obj for obj in bpy.context.view_layer.objects.selected if "PICK" in obj]

            if len(pickups) == 0:
                self.report({'ERROR'}, "Nenhum pickup selecionado!")

        # Pegar todos os objetos que possuem a propriedade 'PICK'
        else:
            pickups = [obj for obj in bpy.data.objects if "PICK" in obj]

            if len(pickups) == 0:
                self.report({'ERROR'}, "Nenhum pickup em sua cena!")

        if len(pickups) >= 1:
            with open(self.filepath, "w") as file:
                file.write("pick\n")

                for obj in pickups:
                    # ID do objeto
                    pickID = obj['PICK']

                    # Posicoes globais do objeto
                    posX = obj.location.x
                    posY = obj.location.y
                    posZ = obj.location.z

                    # Arredondar posicoes
                    posX = ("%." + str(roundDec) + "f") % posX
                    posY = ("%." + str(roundDec) + "f") % posY
                    posZ = ("%." + str(roundDec) + "f") % posZ

                    # Informacoes do pickup
                    pickString = "%s,\t%s,\t%s,\t%s" % (pickID, posX, posY, posZ)

                    # Escrever as informacoes no arquivo selecionado
                    file.write(pickString)
                    file.write("\n")
                file.write("end\n")

                # Mostrar mensagem ao concluir
                ShowMessageBox("Arquivo salvo com sucesso!", "Concluido!", 'DISK_DRIVE')

        return {'FINISHED'}

# Mostrar pequena janela de conclusao
def ShowMessageBox(message = "", title = "Concluido!", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

classes = [Propriedades, PICKPanel, ADDPickup, SavePICKFile]

# Registrar as classes
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.picktool = PointerProperty(type = Propriedades)

    # Categoria das armas
    bpy.types.Scene.gunCategory = EnumProperty(
        name = "",
        description = "Categoria das armas",
        items = [('0', "Assault Rifles", ''),
                 ('1', "Gifts", ''),
                 ('2', "Handguns", ''),
                 ('3', "Heavy Weapons", ''),
                 ('4', "Melee", ''),
                 ('5', "Projectiles", ''),
                 ('6', "Rifles", ''),
                 ('7', "Shotguns", ''),
                 ('8', "Special", ''),
                 ('9', "Sub-Machine", '')],
        update = selectEnum
    )

    bpy.types.Scene.weapons = EnumProperty(
        name = "",
        description = "",
        items = selectEnum,
        default = None
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.picktool
    del bpy.types.Scene.weapons
    del bpy.types.Scene.gunCategory

if __name__ == "__main__":
    register()
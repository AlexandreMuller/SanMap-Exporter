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

from bpy_extras.io_utils import ImportHelper
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, PointerProperty, IntProperty, BoolProperty, EnumProperty

class MyProperties(PropertyGroup):
    # Selecionados apenas
    selectObjsToggle: BoolProperty(name = "Selecionados apenas", default = False)
    
    # Arredondar valores
    roundValues: BoolProperty(name = "Arredondar valores", default = True)
    roundDec: IntProperty(name = "Casas decimais", min = 0, max = 8, default = 6)

    # Categoria das armas
    gunCategory: EnumProperty(
        name = "",
        description = "Categoria das armas",
        items = [('1', "Assault Rifles", ''),
                 ('2', "Gifts", ''),
                 ('3', "Handguns", ''),
                 ('4', "Heavy Weapons", ''),
                 ('5', "Melee", ''),
                 ('6', "Projectiles", ''),
                 ('7', "Rifles", ''),
                 ('8', "Shotguns", ''),
                 ('9', "Special", ''),
                 ('10', "Sub-Machine", '')]
    )

    # Armas corpo a corpo
    melee: EnumProperty(
        name = "",
        description = "Armas corpo a corpo",
        items = [('10, Bat', "Bat", ''),
                 ('4, Brassknuckle', "Brassknuckle", ''),
                 ('14, Chainsaw', "Chainsaw", ''),
                 ('9, Golfclub', "Golfclub", ''),
                 ('13, Katana', "Katana", ''),
                 ('6, Knife', "Knife", ''),
                 ('5, Nightstick', "Nightstick", ''),
                 ('12, Poolstick', "Poolstick", ''),
                 ('11, Shovel', "Shovel", '')]
    )
    
    # Pistolas
    handguns: EnumProperty(
        name = "",
        description = "Pistolas",
        items = [('18, Colt_45', "Colt 45", ''),
                 ('19, Colt_45_Silenced', "Colt 45 Silenced", ''),
                 ('20, Deagle', "Deagle", '')]
    )
    
    # Shotguns
    shotguns: EnumProperty(
        name = "",
        description = "Shotguns",
        items = [('22, Combat_Shotgun', "Combat Shotgun", ''),
                 ('21, Shotgun', "Shotgun", '')]
    )
    
    # Sub-Metralhadoras
    subMachine: EnumProperty(
        name = "",
        description = "Sub-Metralhadoras",
        items = [('25, MP5', "MP5", ''),
                 ('23, Tec-9', "Tec-9", ''),
                 ('24, Uzi', "Uzi", '')]
    )
    
    # Fuzil de assalto
    assaultRifles: EnumProperty(
        name = "",
        description = "Fuzil de assalto",
        items = [('26, AK-47', "AK-47", ''),
                 ('27, M4', "M4", '')]
    )
    
    # Rifles
    rifles: EnumProperty(
        name = "",
        description = "Rifles",
        items = [('28, Country_Rifle', "Country Rifle", ''),
                 ('29, Sniper_Rifle', "Sniper Rifle", '')]
    )
    
    # Armas pesadas
    heavyWeapons: EnumProperty(
        name = "",
        description = "Armas pesadas",
        items = [('31, Flamethrower', "Flamethrower", ''),
                 ('32, Minigun', "Minigun", ''),
                 ('46, Rocket_Launcher', "Rocket Launcher", ''),
                 ('47, Rocket_Launcher_HS', "Rocket Launcher HS", '')]
    )
    
    # Arremessiveis
    projectiles: EnumProperty(
        name = "",
        description = "Arremessiveis",
        items = [('16, Grenade', "Grenade", ''),
                 ('15, Molotov', "Molotov", ''),
                 ('17, Satchel', "Satchel", ''),
                 ('43, Teargas', "Teargas", '')]
    )
    
    # Presentes
    gifts: EnumProperty(
        name = "",
        description = "Presentes",
        items = [('33, Large_Purple_Dildo', "Large Purple Dildo", ''),
                 ('34, Small_White_Dildo', "Small White Dildo", ''),
                 ('35, Large_White_Vibrator', "Large White Vibrator", ''),
                 ('36, Small_Black_Vibrator', "Small Black Vibrator", ''),
                 ('37, Flowers', "Flowers", ''),
                 ('38, Cane', "Cane", '')]
    )
    
    # Especial
    special: EnumProperty(
        name = "",
        description = "Especial",
        items = [('51, Camera', "Camera", ''),
                 ('41, Cellphone', "Cellphone", ''),
                 ('48, Detonator', "Detonator", ''),
                 ('50, Fire_Extinguisher', "Fire Extinguisher", ''),
                 ('53, Infrared', "Infrared Goggles", ''),
                 ('52, Nightvision', "Nightvision Goggles", ''),
                 ('54, Jetpack', "Jetpack", ''),
                 ('55, Parachute', "Parachute", ''),
                 ('49, Spraycan', "Spraycan", '')]
    )

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
        roundValues = picktool.roundValues
        gunCategory = picktool.gunCategory
        
        # Selecionar arma
        row = layout.row()
        layout.prop(picktool, "gunCategory")
        
        if gunCategory == '1':
            layout.prop(picktool, "assaultRifles")
        elif gunCategory == '2':
            layout.prop(picktool, "gifts")
        elif gunCategory == '3':
            layout.prop(picktool, "handguns")
        elif gunCategory == '4':
            layout.prop(picktool, "heavyWeapons")
        elif gunCategory == '5':
            layout.prop(picktool, "melee")
        elif gunCategory == '6':
            layout.prop(picktool, "projectiles")
        elif gunCategory == '7':
            layout.prop(picktool, "rifles")
        elif gunCategory == '8':
            layout.prop(picktool, "shotguns")
        elif gunCategory == '9':
            layout.prop(picktool, "special")
        elif gunCategory == '10':
            layout.prop(picktool, "subMachine")

        # Botao para adicionar
        row = layout.row()
        layout.operator("adicionar.veh")

        # Arredondar valores
        row = layout.row()
        layout.prop(picktool, "roundValues")
        if roundValues:
            layout.prop(picktool, "roundDec")
        
        # Selecionados apenas
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
        roundValues = picktool.roundValues
        roundDec = picktool.roundDec
        
        gunCategory = picktool.gunCategory
        assaultRifles = picktool.assaultRifles
        gifts = picktool.gifts
        handguns = picktool.handguns
        heavyWeapons = picktool.heavyWeapons
        melee = picktool.melee
        projectiles = picktool.projectiles
        rifles = picktool.rifles
        shotguns = picktool.shotguns
        special = picktool.special
        subMachine = picktool.subMachine

        if gunCategory == '1':
            pickID = assaultRifles.split()[0]
            pickID = pickID.replace(',', '')
            pickName = assaultRifles.split()[1]
            materialName = "assaultRiflesMat"
            pickupColor = (1, 0.05, 0, 1)
            
        elif gunCategory == '2':
            pickID = gifts.split()[0]
            pickID = pickID.replace(',', '')
            pickName = gifts.split()[1]
            materialName = "giftsMat"
            pickupColor = (1, 0, 1, 1)
            
        elif gunCategory == '3':
            pickID = handguns.split()[0]
            pickID = pickID.replace(',', '')
            pickName = handguns.split()[1]
            materialName = "handgunsMat"
            pickupColor = (0, 1, 1, 1)
            
        elif gunCategory == '4':
            pickID = heavyWeapons.split()[0]
            pickID = pickID.replace(',', '')
            pickName = heavyWeapons.split()[1]
            materialName = "heavyWeaponsMat"
            pickupColor = (1, 0, 0, 1)
            
        elif gunCategory == '5':
            pickID = melee.split()[0]
            pickID = pickID.replace(',', '')
            pickName = melee.split()[1]
            materialName = "meleeMat"
            pickupColor = (1, 1, 1, 1)
            
        elif gunCategory == '6':
            pickID = projectiles.split()[0]
            pickID = pickID.replace(',', '')
            pickName = projectiles.split()[1]
            materialName = "projectilesMat"
            pickupColor = (0.7, 0.5, 0.6, 1)
            
        elif gunCategory == '7':
            pickID = rifles.split()[0]
            pickID = pickID.replace(',', '')
            pickName = rifles.split()[1]
            materialName = "riflesMat"
            pickupColor = (0, 0, 1, 1)
            
        elif gunCategory == '8':
            pickID = shotguns.split()[0]
            pickID = pickID.replace(',', '')
            pickName = shotguns.split()[1]
            materialName = "shotgunsMat"
            pickupColor = (1, 1, 0, 1)
            
        elif gunCategory == '9':
            pickID = special.split()[0]
            pickID = pickID.replace(',', '')
            pickName = special.split()[1]
            materialName = "specialMat"
            pickupColor = (0.01, 0.01, 0.03, 1)
            
        elif gunCategory == '10':
            pickID = subMachine.split()[0]
            pickID = pickID.replace(',', '')
            pickName = subMachine.split()[1]
            materialName = "subMachineMat"
            pickupColor = (0, 1, 0, 1)
        
        # Adicionar cubo
        newPickup = bpy.ops.mesh.primitive_cube_add(scale = (0.25, 0.25, 0.25))
    
        # Objeto ativo
        pickup = bpy.context.object
        
        # Aumentar localizacao em Z
        pickup.location.z += 1
        
        # Mostrar aramado
        pickup.show_wire = True
        
        # Desativar sombras
        pickup.display.show_shadows = False
        
        # Mostrar como solido
        pickup.display_type = 'SOLID'
        
        # Alterar cor
        pickup.color = pickupColor
        
        # Verificar material
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
class SavePICKFile(Operator, ImportHelper):
    bl_label = "Salvar"
    bl_idname = "pick_save.export"

    # Mostrar apenas arquivos com a determinada extensao
    filter_glob: StringProperty(
        default = "*.ipl;*.txt",
        options = {"HIDDEN"}
    )

    def execute(self, context):
        scene = context.scene
        picktool = scene.picktool
        selectObjsToggle = picktool.selectObjsToggle
        roundValues = picktool.roundValues
        roundDec = picktool.roundDec

        # Caminho e extensao do arquivo
        filename, extension = os.path.splitext(self.filepath)

        with open(self.filepath, "w") as file:
            file.write("pick\n")

            # Pegar apenas objetos selecionados que possuem a propriedade 'PICK'
            if selectObjsToggle:
                pickups = [obj for obj in bpy.context.view_layer.objects.selected if "PICK" in obj]
            # Pegar todos os objetos que possuem a propriedade 'PICK'
            else:
                pickups = [obj for obj in bpy.data.objects if "PICK" in obj]
            
            for obj in pickups:
                # ID do objeto
                pickID = obj['PICK']
                
                # Posicoes globais do objeto
                posX = obj.location.x
                posY = obj.location.y
                posZ = obj.location.z
                
                # Arredondar posicoes
                if roundValues:
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

classes = [MyProperties, PICKPanel, ADDPickup, SavePICKFile]

# Registrar as classes
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.picktool = PointerProperty(type = MyProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.picktool

if __name__ == "__main__":
    register()
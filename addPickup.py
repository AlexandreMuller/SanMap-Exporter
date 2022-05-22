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
assaultRifles = ('26, 355, AK-47', "AK-47", ''),('27, 356, M4', "M4", '')
gifts = ('33, 321, Large_Purple_Dildo', "Large Purple Dildo", ''),('34, 322, Small_White_Dildo', "Small White Dildo", ''),('35, 323, Large_White_Vibrator', "Large White Vibrator", ''),('36, 324, Small_Black_Vibrator', "Small Black Vibrator", ''),('37, 325, Flowers', "Flowers", ''),('38, 326, Cane', "Cane", '')
handguns = ('18, 346, Colt_45', "Colt 45", ''),('19, 347, Colt_45_Silenced', "Colt 45 Silenced", ''),('20, 348, Deagle', "Deagle", '')
heavyWeapons = ('31, 361, Flamethrower', "Flamethrower", ''),('32, 362, Minigun', "Minigun", ''),('46, 359, Rocket_Launcher', "Rocket Launcher", ''),('47, 360, Rocket_Launcher_HS', "Rocket Launcher HS", '')
melee = ('10, 336, Bat', "Bat", ''),('4, 331, Brassknuckle', "Brassknuckle", ''),('14, 341, Chainsaw', "Chainsaw", ''),('9, 333, Golfclub', "Golfclub", ''),('13, 339, Katana', "Katana", ''),('6, 335, Knife', "Knife", ''),('5, 334, Nightstick', "Nightstick", ''),('12, 338, Poolstick', "Poolstick", ''),('11, 337, Shovel', "Shovel", '')
projectiles = ('16, 342, Grenade', "Grenade", ''),('15, 344, Molotov', "Molotov", ''),('17, 363, Satchel', "Satchel", ''),('43, 343, Teargas', "Teargas", '')
rifles = ('28, 357, Country_Rifle', "Country Rifle", ''),('29, 358, Sniper_Rifle', "Sniper Rifle", '')
special = ('51, 367, Camera', "Camera", ''),('41, -1, Cellphone', "Cellphone", ''),('48, 364, Detonator', "Detonator", ''),('50, 366, Fire_Extinguisher', "Fire Extinguisher", ''),('53, 369, Infrared', "Infrared Goggles", ''),('52, 368, Nightvision', "Nightvision Goggles", ''),('54, 370, Jetpack', "Jetpack", ''),('55, 371, Parachute', "Parachute", ''),('49, 365, Spraycan', "Spraycan", '')
subMachine = ('25, 353, MP5', "MP5", ''),('23, 372, Tec-9', "Tec-9", ''),('24, 352, Uzi', "Uzi", '')
shotguns = ('22, 351, Combat_Shotgun', "Combat Shotgun", ''),('21, 349, Shotgun', "Shotgun", '')

weaponCategoryList = assaultRifles, gifts, handguns, heavyWeapons, melee, projectiles, rifles, shotguns, special, subMachine

# Atualizar e selecionar o dropdown correspondente
def selectEnum(self, context):
    # Indice das categorias
    index = int(context.scene.gunCategory)
    
    # Selecionar o dropdown de acordo com a categoria da arma
    enum_items = weaponCategoryList[index]

    return enum_items

# Painel principal
class PICK_PT_PainelPrincipal(Panel):
    bl_label = "Adicionar Pickup"
    bl_idname = "PICK_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "GTA SA Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Selecionar arma
        row = layout.row()
        layout.prop(scene, "gunCategory")
        layout.prop(scene, "weapons")

        # Botao para adicionar
        row = layout.row()
        layout.operator("adicionar.veh", icon = "ADD")

        # Salvar arquivo
        layout.operator("pick_save.export", icon = "CURRENT_FILE")

# Operador para adicionar pickup
class ADD_OP_Pickup(Operator):
    bl_label = "Add"
    bl_idname = "adicionar.veh"
    bl_description = "Adicionar o pickup selecionado"

    def execute(self, context):
        scene = context.scene
        gunCategory = scene.gunCategory
        weapons = scene.weapons
        
        # Lista para os nomes do material e cores do pickup
        materiais = ["assaultRiflesMat", "giftsMat", "handgunsMat", "heavyWeaponsMat", "meleeMat", "projectilesMat", "riflesMat", "shotgunsMat", "specialMat", "subMachineMat"]
        cores = (1, 0.05, 0, 1),(1, 0, 1, 1),(0, 1, 1, 1),(1, 0, 0, 1),(1, 1, 1, 1),(0.7, 0.5, 0.6, 1),(0, 0, 1, 1),(1, 1, 0, 1),(0.01, 0.01, 0.03, 1),(0, 1, 0, 1)
        
        # ID do pickup
        pickID = weapons.split()[0]
        pickID = pickID.replace(',', '')
        
        # ID do modelo
        modelID = weapons.split()[1]
        modelID = modelID.replace(',', '')
        
        # Nome do pickup
        pickName = weapons.split()[2]
        
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
            
            # Criar o sombreador emissivo
            node_emissive = nodes.new(type="ShaderNodeEmission")
            node_emissive.inputs[1].default_value = 5
            node_emissive.inputs[0].default_value = pickupColor
            node_emissive.location = -200, 0

            # Criar saida do material
            node_output  = nodes.new(type='ShaderNodeOutputMaterial')
            node_output.location = 0, 0

            # Linkar nodes
            links = pickupMaterial.node_tree.links

            # Linkar a saida do sombreador emissivo com a saida do material
            links.new(node_emissive.outputs['Emission'], node_output.inputs['Surface'])

            # Adicionar material no pickup
            pickup.data.materials.append(pickupMaterial)

        # Nome do pickup
        pickup.name = pickName

        # ID do pickup
        pickup["PICK"] = pickID
        
        # ID do modelo
        if modelID != '-1':
            pickup["MODEL"] = modelID

        # Mostrar mensagem ao adicionar
        self.report({'INFO'}, f"Adicionado!  Nome: {pickName}   ID: {pickID}")

        return {'FINISHED'}

# Salvar arquivo
class SAVE_OP_PickFile(Operator, ExportHelper):
    bl_label = "Save"
    bl_idname = "pick_save.export"
    bl_description = "Exportar arquivo"
    
    # Organizar o arquivo
    orgArquivo: BoolProperty(
        name = "",
        default = True
    )
    
    # Toggle dos objetos selecionados
    selectObjsToggle: BoolProperty(
        name = "",
        description = "Serão exportados apenas os objetos selecionados",
        default = False
    )

    # Arredondar valores
    roundDec: IntProperty(
        name = "",
        description = "Número de casas decimais para os valores de localização do objeto",
        min = 0,
        max = 10,
        default = 5
    )
    
    # Mostrar apenas arquivos com a determinada extensao
    filter_glob: StringProperty(
        default = "*.ipl;*.txt",
        options = {"HIDDEN"}
    )
    
    # Extensao do arquivo
    filename_ext = ".ipl"
    
    def draw(self, context):
        layout = self.layout
        
        # Toggle para organizar o arquivo
        grid = layout.grid_flow(columns=2, align=True)
        grid.prop(self, "orgArquivo")
        grid.label(text = "Arquivo organizado")
        
        # Toggle dos objetos selecionados
        grid = layout.grid_flow(columns=2, align=True)
        grid.prop(self, "selectObjsToggle")
        grid.label(text = "Selected Objects")
        
        # Numero de casas decimais
        grid = layout.grid_flow(columns=2, align=True)
        grid.label(text = "Casas decimais:")
        grid.prop(self, "roundDec")

    def execute(self, context):
        scene = context.scene
        roundDec = self.roundDec
        orgArquivo = self.orgArquivo
    
        # Caminho e extensao do arquivo
        filename, extension = os.path.splitext(self.filepath)

        # Pegar apenas objetos selecionados que possuem a propriedade 'PICK'
        if self.selectObjsToggle:
            pickups = [obj for obj in bpy.context.selected_objects if "PICK" in obj]

            if len(pickups) == 0:
                self.report({'ERROR'}, "Nenhum pickup selecionado!")

        # Pegar todos os objetos que possuem a propriedade 'PICK'
        else:
            pickups = [obj for obj in bpy.data.objects if "PICK" in obj]

            if len(pickups) == 0:
                self.report({'ERROR'}, "Nenhum pickup em sua cena!")

        if len(pickups) > 0:
            with open(self.filepath, "w") as file:
                file.write("pick\n")

                # Estrutura contendo informacoes dos pickups
                estrutura = {'ID': [], 'PosX': [], 'PosY': [], 'PosZ': []}

                # Adicionar as propriedades do objeto na estrutura
                for obj in pickups:
                    # ID do objeto
                    pickID = obj['PICK']
                    estrutura['ID'].append(pickID)

                    # Posicoes globais do objeto
                    posX = obj.location.x
                    posY = obj.location.y
                    posZ = obj.location.z

                    # Arredondar posicoes
                    estrutura['PosX'].append(("%." + str(roundDec) + "f") % posX)
                    estrutura['PosY'].append(("%." + str(roundDec) + "f") % posY)
                    estrutura['PosZ'].append(("%." + str(roundDec) + "f") % posZ)

                # Colunas da estrutura
                columns = ('ID', 'PosX', 'PosY', 'PosZ')

                # Lista contendo o tamanho dos itens
                itemLengthList = []

                # Pegar o tamanho de cada item para organizar o arquivo
                def organizeFile(self, context):
                    for column in range(len(estrutura)):
                        maxValue = None
                        items = estrutura[columns[column]]
                        for i in items:
                            item = len(str(i))
                            if (maxValue is None or item > maxValue):
                                maxValue = item
                        itemLengthList.append(maxValue)

                if orgArquivo:
                    organizeFile(self, context)

                # Escrever arquivo
                def escreverArquivo(self, context):
                    for i in range(len(pickups)):
                        item = ''
                        for column in range(len(columns)):
                            y = estrutura[columns[column]]

                            if orgArquivo:
                                x = itemLengthList[column]

                                if column == 0:
                                    f = "{0:<" + str(x) + "}"
                                else:
                                    f = "{0:>" + str(x) + "}"

                                item += f.format(y[i]) + ', '

                                if column == len(columns) - 1:
                                    item = item[:-2]
                            else:
                                item += str(y[i]) + ','
                                if column == len(columns) - 1:
                                    item = item[:-1]
                        file.write(item)
                        file.write("\n")
                    file.write("end\n")

                try:
                    escreverArquivo(self, context)
                    self.report({'INFO'}, 'Arquivo salvo com sucesso!')
                except Exception as e:
                    self.report({'ERROR'}, f'{e}')

        return {'FINISHED'}

# Lista das classes
classes = (
    PICK_PT_PainelPrincipal,
    ADD_OP_Pickup,
    SAVE_OP_PickFile
)

# Registrar as classes
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Categoria das armas
    bpy.types.Scene.gunCategory = EnumProperty(
        name = "",
        description = "Categoria selecionada",
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
        description = "Pickup selecionado",
        items = selectEnum,
        default = None
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.weapons
    del bpy.types.Scene.gunCategory

if __name__ == "__main__":
    register()
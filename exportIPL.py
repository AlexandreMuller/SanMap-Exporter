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

from bpy_extras.io_utils import ExportHelper
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, PointerProperty, IntProperty, BoolProperty

# Propriedades do script
class IPL_Propriedades(PropertyGroup):
    lod: IntProperty(
        name = "LOD",
        min = -1,
        default = -1
    )
    
    interior: IntProperty(
        name = "Interior",
        min = 0,
        default = 0
    )
    
    modelName: BoolProperty(
        name = "Usar nome fictício",
        description = "Usar nome fictício ao invés do objeto",
        default = False
    )
    
    modelDummy: StringProperty(
        name = "Nome",
        default = "dummy"
    )

# Painel Principal
class IPL_PT_PainelPrincipal(Panel):
    bl_label = "Exportar para IPL"
    bl_idname = "IPL_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "GTA SA Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ipltool = scene.ipltool

        layout.prop(ipltool, "lod")
        layout.prop(ipltool, "interior")
        
        box = layout.box()
        box.prop(ipltool, "modelName")
        if ipltool.modelName:
            box.prop(ipltool, "modelDummy")
        
        layout.operator("salvar_ipl.open_filebrowser", icon="CURRENT_FILE")

# Abrir o File Browser para salvar o arquivo
class SAVE_OP_IPLFile(Operator, ExportHelper):
    bl_label = "Save"
    bl_idname = "salvar_ipl.open_filebrowser"
    
    # Toggle dos objetos selecionados
    selectObjsToggle: BoolProperty(
        name = "",
        description = "Serão exportados apenas os objetos selecionados",
        default = False
    )
    
    # Organizar o arquivo
    orgArquivo: BoolProperty(
        name = "",
        default = True
    )

    # Arredondar valores
    roundDec: IntProperty(
        name = "",
        description = "Número de casas decimais para os valores de localização e rotação do objeto",
        min = 0,
        max = 10,
        default = 5
    )
    
    # Mostrar arquivos com determinada extensao
    filter_glob: StringProperty(
        default = '*.ipl;*.txt',
        options = {'HIDDEN'}
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
        ipltool = scene.ipltool
        roundDec = self.roundDec
        orgArquivo = self.orgArquivo

        # Caminho e extensao do arquivo
        filename, extension = os.path.splitext(self.filepath)
        
        # Pegar apenas objetos selecionados que possuem a propriedade 'INST'
        if self.selectObjsToggle:
            objects = [obj for obj in bpy.context.selected_objects if "INST" in obj]
            
            if len(objects) == 0:
                self.report({'ERROR'}, "Selecione ao menos um objeto!")
                
        # Pegar todos os objetos que possuem a propriedade 'INST'
        else:
            objects = [obj for obj in bpy.data.objects if "INST" in obj]
            
            if len(objects) == 0:
                self.report({'ERROR'}, 'Sua cena não possui objetos com a propriedade "INST"!')
        
        if len(objects) > 0:
            # Escrever o arquvio IPL
            with open(self.filepath, "w") as file:
                file.write("inst\n")

                # Estrutura contendo informacoes dos objetos
                estrutura = {'ID': [], 'Nome': [], 'Interior': [], 'PosX': [], 'PosY': [], 'PosZ': [],  'RotX': [], 'RotY': [], 'RotZ': [], 'RotW': [], 'LOD': []}

                # Adicionar as propriedades do objeto na estrutura
                for obj in objects:
                    # Adicionar as propriedades interior e lod
                    estrutura['Interior'].append(ipltool.interior)
                    estrutura['LOD'].append(ipltool.lod)

                    # ID do objeto
                    dffID = obj['INST']
                    estrutura['ID'].append(dffID)

                    # Verifique o nome do objeto
                    nome = ''
                    if ipltool.modelName:
                        nome = ipltool.modelDummy
                    else:
                        nome = obj.name.split('.')[0]
                    estrutura['Nome'].append(nome)

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
                    estrutura['PosX'].append(("%." + str(roundDec) + "f") % posX)
                    estrutura['PosY'].append(("%." + str(roundDec) + "f") % posY)
                    estrutura['PosZ'].append(("%." + str(roundDec) + "f") % posZ)

                    # Arredondar rotacoes
                    estrutura['RotW'].append(("%." + str(roundDec) + "f") % rotW)
                    estrutura['RotX'].append(("%." + str(roundDec) + "f") % rotX)
                    estrutura['RotY'].append(("%." + str(roundDec) + "f") % rotY)
                    estrutura['RotZ'].append(("%." + str(roundDec) + "f") % rotZ)

                # Colunas da estrutura
                columns = ('ID', 'Nome', 'Interior', 'PosX', 'PosY', 'PosZ', 'RotX', 'RotY', 'RotZ', 'RotW', 'LOD')

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
                    for i in range(len(objects)):
                        item = ''
                        for column in range(len(columns)):
                            y = estrutura[columns[column]]

                            if orgArquivo:
                                x = itemLengthList[column]

                                if column == 0 or column == 1:
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
                except:
                    self.report({'ERROR'}, 'Não foi possível salvar o arquivo!')
        
        return {'FINISHED'}

# Lista das classes
classes = (
    IPL_Propriedades,
    IPL_PT_PainelPrincipal,
    SAVE_OP_IPLFile
)

# Registrar as classes
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.ipltool = PointerProperty(type = IPL_Propriedades)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.ipltool

if __name__ == "__main__":
    register()
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
from bpy.types import Context, Panel, Operator, PropertyGroup
from bpy.props import StringProperty, PointerProperty, IntProperty, BoolProperty

bl_info = {
    'name': 'SanMap Exporter',
    'description': 'Exportar mapas IPL para o GTA San Andreas',
    'author': 'Alexandre A. Muller',
    'version': (1, 1, 0),
    'blender': (4, 1, 1),
    'category': 'Development',
}

def preferences():
    return bpy.context.preferences.addons[__name__].preferences

def criar_estrutura(preferencias, object):
    estrutura = {'ID': [], 'Nome': [], 'Interior': [], 'PosX': [], 'PosY': [], 'PosZ': [], 'RotX': [], 'RotY': [], 'RotZ': [], 'RotW': [], 'LOD': []}
    
    # ID do objeto
    estrutura['ID'].append(object['INST'])
    
    # Nome do objeto
    nome = preferencias.objeto_nome if preferencias.nome_ficticio else object.name.split('.')[0]
    estrutura['Nome'].append(nome)
    
    # Interior
    estrutura['Interior'].append(preferencias.interior)
    
    # Posicoes globais do objeto
    posX, posY, posZ = object.location.x, object.location.y, object.location.z
    
    # Rotacao em quaternion do objeto
    matrix = object.matrix_world.to_quaternion()
    rotX, rotY, rotZ, rotW = matrix.x, matrix.y, matrix.z, matrix.w
    
    # Arredondar posicoes
    estrutura['PosX'].append(f'%.{preferencias.casas_decimais}f' % posX)
    estrutura['PosY'].append(f'%.{preferencias.casas_decimais}f' % posY)
    estrutura['PosZ'].append(f'%.{preferencias.casas_decimais}f' % posZ)
    
    # Arredondar rotacoes
    estrutura['RotX'].append(f'%.{preferencias.casas_decimais}f' %  rotX)
    estrutura['RotY'].append(f'%.{preferencias.casas_decimais}f' %  rotY)
    estrutura['RotZ'].append(f'%.{preferencias.casas_decimais}f' %  rotZ)
    estrutura['RotW'].append(f'%.{preferencias.casas_decimais}f' % -rotW)
    
    # LOD
    estrutura['LOD'].append(preferencias.lod)
    
    return estrutura

def criar_arquivo(preferencias, filepath, estrutura, size):
    with open(filepath, 'w') as file:
        file.write('inst\n')
        
        largura_coluna = []
        for coluna in estrutura: largura_coluna.append(max(len(str(item)) for item in estrutura[coluna]))
        
        for i in range(size):
            for index, coluna in enumerate(estrutura):
                valor = str(estrutura[coluna][i])
                
                if preferencias.organizar_arquivo:
                    formatacao = f'{{0:<{largura_coluna[index]}}}' if index <= 1 else f'{{0:>{largura_coluna[index]}}}'
                    item = formatacao.format(valor) + ', '
                    if coluna == 'LOD': item = item[:-2]
                else:
                    item = valor + ','
                    if coluna == 'LOD': item = item[:-1]
        
                file.write(item)
            file.write('\n')
        file.write('end')
        file.close()

# Propriedades do script
class Preferencias(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    diretorio: StringProperty(
        name = 'Diretorio do GTA',
        default = ''
    )# type: ignore
    
    lod: IntProperty(
        name = 'LOD',
        min = -1,
        default = -1
    )# type: ignore
    
    interior: IntProperty(
        name = 'Interior',
        min = 0,
        default = 0
    )# type: ignore
    
    nome_ficticio: BoolProperty(
        name = 'Usar nome ficticio',
        description = 'Usar nome ficticio ao invés do objeto',
        default = False
    )# type: ignore
    
    objeto_nome: StringProperty(
        name = 'Nome',
        default = 'dummy'
    )# type: ignore
    
    # Alternar selecao dos objetos
    selecionar_objetos: BoolProperty(
        name = 'Objetos selecionados',
        description = 'Serao exportados apenas os objetos selecionados',
        default = False
    )# type: ignore
    
    # Organizar o arquivo
    organizar_arquivo: BoolProperty(
        name = 'Arquivo organizado',
        description = 'Organizar o arquivo em colunas para facilitar sua leitura',
        default = True
    )# type: ignore

    # Arredondar valores
    casas_decimais: IntProperty(
        name = '',
        description = 'Numero de casas decimais para os valores de localizacao e rotacao do objeto',
        min = 0,
        max = 10,
        default = 5
    )# type: ignore
    
    def draw(self, context):
        layout = self.layout

        layout.prop(self, 'diretorio')

# Painel Principal
class _PT_PainelPrincipal(Panel):
    bl_label = 'Exportar para IPL'
    bl_idname = 'PT_Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SanMap Exporter'

    def draw(self, context):
        layout = self.layout
        preferencias = preferences()

        layout.prop(preferencias, 'lod')
        layout.prop(preferencias, 'interior')
        
        box = layout.box()
        box.prop(preferencias, 'nome_ficticio')
        if preferencias.nome_ficticio:
            box.prop(preferencias, 'objeto_nome')

        # Toggle para organizar o arquivo
        row = layout.row()
        row.prop(preferencias, 'organizar_arquivo')

        # Toggle dos objetos selecionados
        row = layout.row()
        row.prop(preferencias, 'selecionar_objetos')

        # Numero de casas decimais
        grid = layout.grid_flow(columns=2, align=True)
        grid.label(text = 'Casas decimais:')
        grid.prop(preferencias, 'casas_decimais')
        
        layout.operator('salvar_ipl.open_filebrowser', icon='CURRENT_FILE')
        layout.operator('salvar_ipls.operator', icon='CURRENT_FILE')
        
class SAVE_OP_IPLFiles(Operator):
    bl_label = 'Salvar Tudo'
    bl_idname = 'salvar_ipls.operator'
    bl_description = 'Salvar todos os objetos separados em arquivos por cada colecao no modloader(isso apagara todos os arquivos existentes!)'
    
    def execute(self, context):
        preferencias = preferences()
        
        diretorio = r'%s\modloader\SanMap Exporter' % preferencias.diretorio
        
        if preferencias.diretorio == '':
            self.report({'ERROR'}, 'Forneca um diretorio nas configuracoes do addon antes de salvar!')
            return {'FINISHED'}
        else:
            if not os.path.exists(diretorio): os.mkdir(diretorio)
            
            try:
                for file in os.listdir(diretorio):
                    os.remove(r'%s\%s' % (diretorio, file))
            except:
                pass
        
        # Apenas objetos selecionados ou fazer busca completa
        select_objects = bpy.context.selected_objects if preferencias.selecionar_objetos else bpy.data.objects

        collections = {}

        for obj in select_objects:
            if 'INST' in obj:
                if not obj.users_collection[0].name in collections: collections[obj.users_collection[0].name] = []
                collections[obj.users_collection[0].name].append(obj)
        
        estrutura = {}
        loader = ''
        for collection in collections:
            estrutura[collection] = {'ID': [], 'Nome': [], 'Interior': [], 'PosX': [], 'PosY': [], 'PosZ': [], 'RotX': [], 'RotY': [], 'RotZ': [], 'RotW': [], 'LOD': []}
            
            size = 0
            for obj in collections[collection]:
                items = criar_estrutura(preferencias, obj)
                for item in items:
                    estrutura[collection][item].append(items[item][0])
                size += 1
            
            if size == 0:
                self.report({'ERROR'}, 'Sua cena nao possui objetos com a propriedade "INST"!')
                return {'FINISHED'}
            
            path = r'%s\%s.ipl' % (diretorio, collection)
            
            try:
                criar_arquivo(preferencias, path, estrutura[collection], size)
                loader += f'IPL data\maps\{collection}.ipl\n'
                
                self.report({'INFO'}, f'Arquivos salvos com sucesso em: {diretorio}')
            except Exception as e:
                print(e)
                self.report({'ERROR'}, 'Nao foi possivel salvar o arquivo!')
        
        # criar loader
        with open(rf'{diretorio}\loader.txt', 'w') as file:
            file.write(loader)
            file.close()
            
        return {'FINISHED'}

# Abrir o File Browser para salvar o arquivo
class SAVE_OP_IPLFile(Operator, ExportHelper):
    bl_label = 'Salvar'
    bl_idname = 'salvar_ipl.open_filebrowser'

    # Mostrar arquivos com determinada extensao
    filter_glob: StringProperty(
        default = '*.ipl;*.txt',
        options = {'HIDDEN'}
    )# type: ignore
    
    # Extensao do arquivo
    filename_ext = '.ipl'
    
    def execute(self, context):
        preferencias = preferences()

        # Caminho e extensao do arquivo
        filename, extension = os.path.splitext(self.filepath)
        
        # Apenas objetos selecionados ou fazer busca completa
        select_objects = bpy.context.selected_objects if preferencias.selecionar_objetos else bpy.data.objects
        
        # Verificar se objetos foram selecionados
        if select_objects == [] and preferencias.selecionar_objetos:
            self.report({'ERROR'}, 'Selecione ao menos um objeto!')
            return {'FINISHED'}

        # Dicionario do arquivo(estrutura do IPL)
        estrutura = {'ID': [], 'Nome': [], 'Interior': [], 'PosX': [], 'PosY': [], 'PosZ': [],  'RotX': [], 'RotY': [], 'RotZ': [], 'RotW': [], 'LOD': []}
        size = 0

        # Adicionar as propriedades do objeto na estrutura
        for obj in select_objects:
            if 'INST' in obj:
                items = criar_estrutura(preferencias, obj)
                for item in items:
                    estrutura[item].append(items[item][0])
                
                size += 1
        if size == 0:
            self.report({'ERROR'}, 'Sua cena nao possui objetos com a propriedade "INST"!')
            return {'FINISHED'}
        try:
            criar_arquivo(preferencias, self.filepath, estrutura, size)
            
            self.report({'INFO'}, 'Arquivo salvo com sucesso!')
        except Exception as e:
            print(e)
            self.report({'ERROR'}, 'Nao foi possivel salvar o arquivo!')
        
        return {'FINISHED'}

# Lista das classes
classes = (
    Preferencias,
    _PT_PainelPrincipal,
    SAVE_OP_IPLFile,
    SAVE_OP_IPLFiles
)

# Registrar as classes
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
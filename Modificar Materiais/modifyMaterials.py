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

from bpy.types import Panel, Operator, PropertyGroup, UIList
from bpy.props import PointerProperty, BoolProperty, CollectionProperty, EnumProperty, FloatProperty, IntProperty

class MODMAT_Propriedades(PropertyGroup):
    # Indice do material
    matIndex: IntProperty()
    
    materialList: BoolProperty(
        name = "Utilizar Lista",
        description = "Converter os materiais que estão na lista",
        default = False
    )
    
    backfaceCulling: BoolProperty(
        name = "Backface Culling",
        description = "Usa o abate das faces oclusas de maneira a ocultar o lado de trás das faces (em geral, as partes internas do objeto)",
        default = False
    )
    
    blendMode: EnumProperty(
        name = "Blend Mode",
        description = "Modo de mesclagem para faces transparentes",
        items = [("0", "Opaque", "Renderizar superfície sem transparência"),
                 ("1", "Alpha Clip", "Usa o limite alfa para cortar a visibilidade (visibilidade binária)"),
                 ("2", "Alpha Hashed", "Usa ruído para pontilhar a visibilidade binária (funciona bem com várias amostras)"),
                 ("3", "Alpha Blend", "Renderiza os polígonos transparentes, dependendo do canal alfa da textura")],
        default = 0
    )
    
    shadowMode: EnumProperty(
        name = "Shadow Mode",
        description = "Método para mapeamento de sombra",
        items = [("0", "None", "O material não vai criar sombra"),
                 ("1", "Opaque", "O material vai criar sombras sem transparência"),
                 ("2", "Alpha Clip", "Usa o limite alfa para cortar a visibilidade (visibilidade binária)"),
                 ("3", "Alpha Hashed", "Usa ruído para pontilhar a visibilidade binária e use filtragem para reduzir o ruído")],
        default = 3
    )
    
    showBackface: BoolProperty(
        name = "Show Backface",
        description = "Renderiza várias camadas transparentes (pode ocorrer problemas de classificação de transparência)",
        default = False
    )
    
    clipThreshold: FloatProperty(
        name = "Clip Threshold",
        description = "Um pixel é renderizado somente se seu valor alfa estiver acima desse limite",
        min = 0,
        max = 1,
        default = 0.5,
        precision = 3
    )
    
    ssr: BoolProperty(
        name = "Screen Space Refraction",
        description = "Usar refrações de espaço de tela com raytraced",
        default = False
    )
    
    refractionDepth: FloatProperty(
        name = "Refraction Depth",
        description = "Aproxime a espessura do objeto para calcular dois eventos de refração (0 está desabilitado)",
        min = 0,
        default = 0,
        precision = 2,
        unit = "LENGTH"
    )
    
    subsurfTransluc: BoolProperty(
        name = "Subsurface Translucency",
        description = "Adiciona efeito translucido na superfície",
        default = False
    )
    
    passIndex: IntProperty(
        name = "Pass Index",
        description = 'Número de índice para o "Índice de material" no passo de renderização',
        min = 0,
        default = 0
    )

# Criar o painel principal
class MainPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GTA SA Tools'
    bl_options = {"DEFAULT_CLOSED"}

class MODMAT_PT_PainelPrincipal(MainPanel, Panel):
    bl_idname = "PAINEL_PT_ModMaterial"
    bl_label = "Modificar Materiais"
    
    def draw(self, context):
        pass

# Painel de conversao do material
class CONV_PT_MaterialPanel(MainPanel, Panel):
    bl_parent_id = "PAINEL_PT_ModMaterial"
    bl_label = "Converter Materiais"
    
    def draw(self, context):
       layout = self.layout
       
       layout.operator("convert_mat.button_operator", icon = 'MATERIAL')

# Painel com as configuracoes do material
class MAT_PT_SettingsPanel(MainPanel, Panel):
    bl_parent_id = "PAINEL_PT_ModMaterial"
    bl_label = "Settings"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        convmat = scene.convmat
        blendMode = convmat.blendMode
        
        layout.prop(convmat, "backfaceCulling")
        layout.prop(convmat, "blendMode")
        layout.prop(convmat, "shadowMode")

        # Blend Mode
        showBack = layout.row()
        if blendMode == '3':
            showBack.enabled = True
        else:
            showBack.enabled = False
        showBack.prop(convmat, "showBackface")

        # Clip Threshold
        clipThr = layout.row()
        if blendMode == '1':
            clipThr.enabled = True
        else:
            clipThr.enabled = False
        clipThr.prop(convmat, "clipThreshold", slider=True, icon_only = False)

        layout.prop(convmat, "ssr")
        layout.prop(convmat, "refractionDepth")
        layout.prop(convmat, "subsurfTransluc")
        layout.prop(convmat, "passIndex")
        
        # Modificar apenas os materiais da lista
        layout.prop(convmat, "materialList")
        
        if convmat.materialList:
            rows = 2
            row = layout.row()
            row.template_list("MATERIAL_UL_List", "material_list", scene, "matCollection", convmat, "matIndex", rows = rows)
            col = row.column(align=True)
            col.operator("add_mat.button_operator", icon = 'ADD', text = "")
            col.operator("rem_mat.button_operator", icon = 'REMOVE', text = "")
            layout.operator("limpar_lista.button_operator", icon = 'TRASH')
        
        layout.operator("mat_settings.button_operator", icon = 'FILE_REFRESH')

# Botao para converter o material
class CONV_OP_MaterialButton(Operator):
    bl_label = "Converter Materiais"
    bl_idname = "convert_mat.button_operator"
    bl_description = "Converter os materiais dos objetos selecionados para opaco com ou sem transparência"
    
    def execute(self, context):
        # Verificar se os scripts necessarios estao na cena
        try:
            bpy.data.texts["diffuseAlpha.py"]
            bpy.data.texts["diffuse.py"]
        except:
            self.report({'ERROR'}, 'É necessário ter os scripts "diffuse.py" e "diffuseAlpha.py" em sua cena!')
            
            return {'CANCELLED'}
        
        # Converter materiais dos objetos selecionados
        if len(context.selected_objects) != 0:
            converterMaterial(self, context)
        else:
            self.report({'ERROR'}, "Selecione ao menos um objeto!")

        return {'FINISHED'}

# Botao para modificar as configuracoes definidas
class MAT_OP_SettingsButton(Operator):
    bl_label = "Atualizar"
    bl_idname = "mat_settings.button_operator"
    bl_description = "Atualizar os materiais dos objetos selecionados ou da lista com as configurações definidas"
    
    def execute(self, context):
        # Modificar materiais dos objetos selecionados ou materiais da lista
        if len(context.selected_objects) != 0:
            materialConfig(self, context)
        else:
            self.report({'ERROR'}, "Selecione ao menos um objeto ou material!")

        return {'FINISHED'}

# Botao para adicionar material ativo na lista
class ADD_OP_Material(Operator):
    bl_label = ""
    bl_idname = "add_mat.button_operator"
    
    def execute(self, context):
        scene = context.scene
        convmat = scene.convmat
        matIndex = convmat.matIndex
        
        # Pegar o objeto ativo
        obj = context.active_object
        
        # Checar se o material existe na lista
        def checkMaterialCollection():
            materials = []
            for mat in scene.matCollection:
                materials.append(mat.name)
                
            if obj.active_material.name in materials:
                self.report({'INFO'}, "Já está na lista!")
                return True
            else:
                return False
                
        # Adicionar o material na lista
        if not checkMaterialCollection():
            item = scene.matCollection.add()
            item.id = len(scene.matCollection)
            item.material = obj.active_material
            item.name = item.material.name
            matIndex = (len(scene.matCollection)-1)
            
        return {'FINISHED'}

# Botao para remover o material selecionado da lista    
class REMOVE_OP_Material(Operator):
    bl_label = ""
    bl_idname = "rem_mat.button_operator"
    
    def execute(self, context):
        scene = context.scene
        convmat = scene.convmat
        matIndex = convmat.matIndex
        
        # Verifique primeiro se a lista nao e vazia
        try:
            item = scene.matCollection[matIndex]
        except IndexError:
            pass
        else:
            # Pegar o material selecionado
            obj = context.active_object
            mat = obj.active_material

            # Remover o material selecionado da lista
            item = scene.matCollection[matIndex]
            mat = item.material
            scene.matCollection.remove(matIndex)
            if matIndex == 0:
                matIndex = 0
            else:
                matIndex -= 1
        
        return {'FINISHED'}

# Botao para remover todos os materiais da lista   
class CLEAN_OP_List(Operator):
    bl_idname = "limpar_lista.button_operator"
    bl_label = "Limpar Lista"
    bl_description = "Limpar lista dos materiais"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.matCollection)

    def execute(self, context):
        # Verifique se a lista nao esta vazia
        if bool(context.scene.matCollection):
            context.scene.matCollection.clear()
        else:
            self.report({'INFO'}, "Nada para remover")
            
        return{'FINISHED'}

# Lista dos materiais adicionados
class MATERIAL_UL_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        mat = item.material
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            row.prop(mat, "name", text = "", emboss = False, icon_value = layout.icon(mat))

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text = "", icon_value = layout.icon(mat))

# Ponteiro do material
class MODMAT_MaterialCollection(PropertyGroup):
    material: PointerProperty(
        name="Material",
        type=bpy.types.Material
    )

# Funcao para modificar as configuracoes do material
def materialConfig(self, context):
    scene = context.scene
    convmat = scene.convmat
    
    # Propriedades
    blendMode = convmat.blendMode
    shadowMode = convmat.shadowMode

    # Modificar configuracoes
    def modSettings(material):
        # Abate das faces oclusas
        material.use_backface_culling = convmat.backfaceCulling
        
        # Modo de mesclagem
        if blendMode == '0':
            material.blend_method = 'OPAQUE'
        elif blendMode == '1':
            material.blend_method = 'CLIP'
            # Clip Threshold
            material.alpha_threshold = convmat.clipThreshold
        elif blendMode == '2':
            material.blend_method = 'HASHED'
        elif blendMode == '3':
            material.blend_method = 'BLEND'
            # Show Backface
            material.show_transparent_back = convmat.showBackface
            
        # Shadow Mode
        if shadowMode == '0':
            material.shadow_method = 'NONE'
        elif shadowMode == '1':
            material.shadow_method = 'OPAQUE'
        elif shadowMode == '2':
            material.shadow_method = 'CLIP'
        elif shadowMode == '3':
            material.shadow_method = 'HASHED'
        
        # Screen Space Refraction
        material.use_screen_refraction = convmat.ssr
        
        # Refraction Depth
        material.refraction_depth = convmat.refractionDepth
        
        # Subsurface Translucency
        material.use_sss_translucency = convmat.subsurfTransluc
        
        # Pass index
        material.pass_index = convmat.passIndex
    
    # Objetos selecionados
    objects = bpy.context.selected_objects
    
    # Progresso atual
    progresso = 0
    
    # Verifique se esta usando lista de materiais
    if convmat.materialList:
        stepProgress = 100/len(scene.matCollection)
        for mat in scene.matCollection:
            material = mat.material

            # Chamar funcao para modificar configuracoes
            modSettings(material)
            
            # Chamar funcao para atualizar progresso
            progresso += stepProgress
            progressUpdate(progresso, False)

        # Finalizar progresso
        progressUpdate(progresso, True)
    else:
        stepProgress = 100/len(objects)
        for i in objects:
            for mat in i.material_slots:
                # Chamar funcao para modificar configuracoes
                modSettings(mat.material)
            
            # Chamar funcao para atualizar progresso
            progresso += stepProgress
            progressUpdate(progresso, False)
            
        # Finalizar progresso
        progressUpdate(progresso, True)
    
    self.report({'INFO'}, "Materiais atualizados")
    
    return {'FINISHED'}

# Funcao para converter material
def converterMaterial(self, context):
    # Objetos selecionados
    objects = bpy.context.selected_objects
    
    matCount = 0  # Quantidade de materiais
    erros = []    # Lista com materiais nao convertidos

    # Progresso atual
    stepProgress = 100/len(objects)
    progresso = 0
    
    # Percorrer objetos
    for i in objects:
        # Percorrer materiais do objeto
        for m in i.material_slots:
            material = m.material
            material.use_nodes = True
            nodes = material.node_tree.nodes
            image = None
            
            try:
                # Pegar a textura de imagem
                for mat_node in nodes:
                    if mat_node.type == 'TEX_IMAGE':
                        image = mat_node.image
                        main_texture = image.name
                        node_main_texture_label = mat_node.label
                
                # Checar se a imagem possui canal alpha
                def checkAlpha(img):
                    b = 32 if img.is_float else 8
                    return (img.depth == 2*b or img.depth == 4*b)

                if image != None:
                    # APAGAR TODOS OS NODES
                    nodes.clear()

                    # Verifique para modificar o material do objeto
                    if checkAlpha(image):
                        # Material opaco com transparencia
                        diffuseAlpha = bpy.data.texts["diffuseAlpha.py"]
                        exec(diffuseAlpha.as_string())
                    else:
                        # Material apenas opaco
                        diffuse = bpy.data.texts["diffuse.py"]
                        exec(diffuse.as_string())
                else:
                    erros.append(m.name)
            except Exception as e:
                self.report({'ERROR'}, f"{e}")
                
                return {'CANCELLED'}

            matCount +=1

        # Chamar funcao para atualizar progresso
        progresso += stepProgress
        progressUpdate(progresso, False)
        
    # Finalizar progresso
    progressUpdate(progresso, True)
    
    # Mostrar mensagem ao concluir ou reportar possiveis erros
    if len(erros) == 0:
        ShowMessageBox(f'Objetos: {len(objects)}  Materiais convertidos: {matCount}')
    elif len(erros) < matCount:
        ShowMessageBox(f'Objetos: {len(objects)}  Materiais convertidos: {matCount - len(erros)}  Erros: {len(erros)}')
        self.report({'WARNING'}, f'Materiais com problemas: {len(erros)}')
        self.report({'WARNING'}, f"{', '.join(map(str, erros))}")
    else:
        self.report({'ERROR'}, f'Não foi possível converter os materiais! Erros: {len(erros)}')
        self.report({'WARNING'}, f"{', '.join(map(str, erros))}")
        
    return {'FINISHED'}

# Mostrar progresso da funcao em execucao
def progressUpdate(progress, finalizar):
    wm = bpy.context.window_manager
    wm.progress_begin(0, 100)
    wm.progress_update(progress)
    
    # Finalizar progresso
    if finalizar:
        wm.progress_end()

# Mostrar pequena janela de conclusao
def ShowMessageBox(message = "", title = "Concluido!", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)  

# Lista das classes
classes = (
    MODMAT_Propriedades,
    MODMAT_PT_PainelPrincipal,
    CONV_PT_MaterialPanel,
    MAT_PT_SettingsPanel,
    CONV_OP_MaterialButton,
    MAT_OP_SettingsButton,
    ADD_OP_Material,
    REMOVE_OP_Material,
    CLEAN_OP_List,
    MATERIAL_UL_List,
    MODMAT_MaterialCollection
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.convmat = PointerProperty(type = MODMAT_Propriedades)
    bpy.types.Scene.matCollection = CollectionProperty(type = MODMAT_MaterialCollection)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.convmat
    del bpy.types.Scene.matCollection

if __name__ == "__main__":
    register()
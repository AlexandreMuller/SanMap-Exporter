# GTA SA Tools

Ferramentas para auxiliar na exportação de arquivos para o GTA San Andreas. Como, por exemplo, .ipl, .pwn e .ide.

Ainda não é possível converter de forma satisfatória as rotações em quaternion dos objetos para o formato .ipl. Não sei como é feito a conversão. Enquanto .pwn funciona perfeitamente, sendo necessário apenas converter usando o [Conversor PAWN para IPL](https://www.mixmods.com.br/2016/10/samp-map-construction-map-editor-pawn-2-ipl-tuto/). 

### Find Object ID

Este formato de arquivo é suficiente para que a busca seja executada corretamente:

```
3626, dcKwRKhut
3169, trailER_largE2_01
9238, moRESfnSHIT28
```

Simplesmente o ID e o nome do dff...

### Converter Objetos

Para converter os materiais, será necessário selecionar o diretório que contém as texturas dos objetos importados. Pois, é feito uma busca do endereço da imagem, pelo menos por enquanto.

![Blender-Conv-Mat](./Imagens/readme/Blender_Conv_Mat.gif)

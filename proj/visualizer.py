import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys

def visualizer(grid):
    #Transforms the input into a grid for example, [["FC","VC"],["VC","FC"]]
    #grid = [line.strip().split('\t') for line in f] 
    
    
    
    path = 'C:/Users/franc/OneDrive/Documentos/IST/IA/IA/Visualizador/Visualizador/images/'

    
    fig, axs = plt.subplots(len(grid), len(grid[0]), figsize=(5, 5)) 

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    for ax in axs.flatten():
        ax.axis('off')

    for i, row in enumerate(grid):
        for j, img_code in enumerate(row):
            if not img_code[1]:
                img_path = f"{path}{img_code[0]}f.png"
            else:
                img_path = f"{path}{img_code[0]}.png" 
            img = mpimg.imread(img_path) 
            axs[i, j].imshow(img) 

    plt.savefig('output.png')

'''grid = [[['VB', False], ['VE', False], ['FB', False], ['VB', False], ['LH', False], ['VE', False], ['VB', False], ['LH', False], ['FE', False], ['FB', False]], [['LV', False], ['FC', False], ['LV', False], ['FC', False], ['FB', False], ['BD', False], ['BC', False], ['LH', False], ['LH', False], ['BE', False]], [['LV', False], ['FD', True], ['VB', True], ['BB', False], ['BC', True], ['BC', True], ['LV', True], ['LH', False], ['FE', False], ['FC', False]], [['BD', False], ['BE', True], ['LH', True], ['BB', True], ['BB', True], ['BB', True], ['LH', True], ['BB', False], ['BB', False], ['FE', False]], [['FC', False], ['FC', True], ['VD', True], ['BD', True], ['VE', True], ['LH', True], ['VB', True], ['LV', False], ['VE', True], ['FC', True]], [['FB', False], ['VB', True], ['BE', True], ['VC', True], ['BE', True], ['VD', True], ['FE', True], ['VC', True], ['BD', True], ['VE', False]], [['LV', False], ['VB', True], ['BD', True], ['FE', True], ['FD', True], ['BB', True], ['FB', True], ['FC', True], ['VD', True], ['LV', False]], [['LV', False], ['VE', True], ['VC', True], ['FE', True], ['LV', True], ['BE', True], ['LH', True], ['FE', True], ['VE', True], ['BE', False]], [['LV', False], ['VE', True], ['BB', True], ['BC', True], ['VD', True], ['FE', True], ['VB', True], ['VB', True], ['VE', True], ['LV', False]], [['VD', False], ['VC', False], ['FE', True], ['VE', True], ['VD', True], ['FE', True], ['VD', False], ['BC', False], ['FE', False], ['FC', False]]]
visualizer(grid)'''
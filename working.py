import oom_markdown
import os
import yaml
import shutil
import itertools

#process
#  locations set in working_parts.ods 
#  export to working_parts.csv
#  put components on the right side of the board
#  run this script

def main(**kwargs):
    
    make_readme(**kwargs)
    make_grid_file(**kwargs)


def make_grid_file(**kwargs):
    file_grid_source = "working_grid_source.yml"
    file_grid_output = "working_grid_output.yml"

    #load in source file
    print(f"loading in file: {file_grid_source}")
    with open(file_grid_source) as f:
        grid_source = yaml.load(f, Loader=yaml.FullLoader)

    seeds = []
    #seeds.append(12569868)
    start = 987600000
    number_of_seeds = 10
    for i in range(number_of_seeds):
        seeds.append(start + i)
    for seed in seeds:
        new = {}
        new['title'] = f"{seed}"
        new["params"] = {}
        new['params']["seed"] = f"{seed}"
        grid_source["axes"]['seed']["values"][seed] = new

    
    
    

    #all permutations
    #styles_raw = ["lowpoly","origami","analog film","anime","craft clay","isometric","ads food","grafitti","pop art","dystopian","kawaii","papercraft"]
    #styles_raw = ["lowpoly","origami","anime","craft clay","isometric","grafitti","pop art","kawaii"]
    #styles_raw = ["kawaii","craft clay","low_poly","pop art"]
    
    styles_raw = ["lowpoly kawaii", "kawaii craft clay","kawaii craft clay pop art"]
    permutations = False



    if permutations:
        #make an array with all permutations of styles_raw in it using itertools
        styles_tupple = []
        for r in range(1, len(styles_raw) + 1):
            styles_tupple.extend(list(itertools.combinations(styles_raw, r)))
        #turn into a list of streings seperated by space
        styles = []
        for style in styles_tupple:
            styles.append(" ".join(style))
    else:
        styles = styles_raw
    
    
    for style in styles:
        new = {}
        new['title'] = f"{str(style)}"
        new["params"] = {}
        new['params']["promptreplace"] = f"no style={str(style)}"
        grid_source["axes"]['style']["values"][style] = new

    pass
    
    # delete images
    print(f"deleting images")
    dir_images = rf"C:\sd2\webui\outputs\txt2img-grids\working_grid_output\default"
    #delete directory and all files in it
    if os.path.exists(dir_images):
        shutil.rmtree(dir_images)
    
    

    #write out file
    print(f"writing out file: {file_grid_output}")
    with open(file_grid_output, 'w') as f:
        #dump in the order it's in and no line length limit preserve quotes
        yaml.dump(grid_source, f, sort_keys=False)

    #copy to stable diffusion
    print(f"copying to stable diffusion folder")
    file_src = file_grid_output
    file_dst = rf"C:\sd2\webui\extensions\sd-infinity-grid-generator-script\assets\{file_grid_output}"
    shutil.copyfile(file_src, file_dst)

def make_readme(**kwargs):
    os.system("generate_resolution.bat")
    #oom_markdown.generate_readme_project(**kwargs)
    oom_markdown.generate_readme_teardown(**kwargs)
    

if __name__ == '__main__':
    main()
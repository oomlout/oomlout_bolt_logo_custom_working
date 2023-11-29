import oom_markdown
import os
import yaml
import shutil
import itertools
import oom_base

#process
#  locations set in working_parts.ods 
#  export to working_parts.csv
#  put components on the right side of the board
#  run this script

start = 123456789
seeds = []

def main(**kwargs):
    global seeds, start

    files_delete = False
    kwargs['files_delete'] = files_delete


    #se t seeds
    seeds = []
    #seeds.append(12569868)
    
    number_of_seeds = 500
    for i in range(number_of_seeds):
        seeds.append(start + i)

    #make_readme(**kwargs)
    #make_grid_file(**kwargs)
    copy_files(**kwargs)
    #make_yaml(**kwargs)
    #make_label(**kwargs)

def copy_files(**kwargs):   
    global seeds
    pass
    dir_image_base = f"C:/sd2/webui/outputs/txt2img-grids/working_grid_output"
    dir_image_prefix = f"default/"
    dir_image_suffix = "/euler_a/model_sdxl/10241024/steps_51/cfg_11/kawaii_craft_clay/no_artist/no_extra/logo_1/weight_1d5.png"

    for seed in seeds:
        #for keeping them not synced
        #dir_image_generated = f"generated/{seed}"
        #putting on github
        dir_image_generated = f"logos/{seed}"
        file_image_generated = f"{dir_image_generated}/logo.png"
        file_source = f"{dir_image_base}/{dir_image_prefix}{seed}{dir_image_suffix}"
        file_destination = file_image_generated
        
        os.makedirs(dir_image_generated, exist_ok=True)
        if os.path.exists(file_source):
            print(f"copying file: {file_source} to {file_destination}")
            shutil.copyfile(file_source, file_destination)
        else:
            print(f"file not found: {file_source}")


def make_grid_file(**kwargs):
    global seeds

    files_delete = kwargs.get('files_delete', False)
    
    file_grid_source = "working_grid_source.yml"
    file_grid_output = "working_grid_output.yml"

    #load in source file
    print(f"loading in file: {file_grid_source}")
    with open(file_grid_source) as f:
        grid_source = yaml.load(f, Loader=yaml.FullLoader)

    
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
    
    #styles_raw = ["lowpoly kawaii", "kawaii craft clay","kawaii craft clay pop art"]
    styles_raw = ["kawaii craft clay"]
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
        if grid_source["axes"]['style'] == None:
            grid_source["axes"]['style'] = {}
        if grid_source["axes"]['style'].get("values",None) == None:
            grid_source["axes"]['style']["values"] = {}
        grid_source["axes"]['style']["values"][style] = new

    pass
    
    if files_delete:
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

def make_label(**kwargs):
    global seeds
    for seed in seeds:
        dir_label = f"generated/{seed}"
        file_label = f"generated/{seed}/label.svg"
        file_template = f"templates/template_label_logo_150_mm_100_mm.svg"
        #load working.yaml from dir_label
        file_yaml = f"generated/{seed}/working.yaml"
        print(f"loading in file: {file_yaml}")
        with open(file_yaml) as f:
            yaml_deets = yaml.load(f, Loader=yaml.FullLoader)
        
        dict_data = yaml_deets
        file_template = file_template
        file_output = file_label
        oom_base.get_jinja2_template(dict_data=dict_data, file_template=file_template, file_output=file_output)
        file_input = file_label        
        oom_base.convert_svg_to_pdf(file_input=file_input)
        
        

def make_readme(**kwargs):
    os.system("generate_resolution.bat")
    #oom_markdown.generate_readme_project(**kwargs)
    oom_markdown.generate_readme_teardown(**kwargs)
    
def make_yaml(**kwargs):
    global seeds
    for seed in seeds:
        yaml_deets = {}
        yaml_deets['seed'] = seed
        yaml_deets['order_number'] = seed
        #dump to working.yaml in generated directory
        file_yaml = f"generated/{seed}/working.yaml"
        print(f"writing out file: {file_yaml}")
        with open(file_yaml, 'w') as f:            
            yaml.dump(yaml_deets, f, sort_keys=False)

if __name__ == '__main__':
    main()
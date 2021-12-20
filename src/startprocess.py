# main.py
import os
import sys
import copy
import random
import numpy as np
from datetime import datetime
from PIL import Image,ImageDraw

def drawSolution(newimage):
    global org_im
    new_im=Image.new('RGB', org_im.size)
    draw = ImageDraw.Draw(new_im)
    
    for prim in newimage["primitives"]:
        draw.polygon(prim["primitive"],prim["color"])
        
    newimage["image"]=new_im

def createSolution(num_of_primitives):
    global org_im
    
    newimage={"primitives":[]}
    for i in range(0,num_of_primitives):
        x1=random.randint(0,org_im.size[0])
        x2=random.randint(0,org_im.size[1])
        y1=random.randint(x1,org_im.size[0])
        y2=random.randint(x2,org_im.size[1])

        z1=random.randint(0,org_im.size[0])
        z2=random.randint(0,org_im.size[1])
        
        m1=(x1+y1+z1)/3
        n1=(x2+y2+z2)/3
        
        r, g, b = org_im.getpixel((m1, n1))
        
        newprim={"primitive":((x1,x2),(y1,y2),(z1,z2)),"type":2,"color":(r,g,b)}
        newimage["primitives"].append(newprim)
    drawSolution(newimage)
    return newimage

def costFunction(image):
    global org_data
    in_org_data=np.asarray(image)
    in_org_data2=np.reshape(in_org_data,-1)
    vec=abs(np.int32(org_data)-np.int32(in_org_data2))
    vec=vec**2
    return sum(vec)

def mutate_colors_2(solution,debug=False):
    if debug:
        drawSolution(solution)
        val=costFunction(solution["image"])
        if (val !=solution["value"]):
            print(f'SHIT IN {val} {solution["value"]}')
            solution["value"]=val
#            A/0
        
    cur_val=solution["value"]
    if debug:
        print(f"ORGL {cur_val}")

    for i in range(0,len(solution["primitives"])):
        if debug:
            print(solution["primitives"][i]["color"])
        orgcolor=solution["primitives"][i]["color"]
        newcolor=list(solution["primitives"][i]["color"])
        
        color_to_move=random.randint(1,5)
        for j in range(0,3):
            if newcolor[j]>=color_to_move:
                newcolor[j]-=color_to_move
                if debug:
                    print("Try:"+str(newcolor))
                solution["primitives"][i]["color"]=tuple(newcolor)
                drawSolution(solution)
                val=costFunction(solution["image"])
                if debug:
                    print(f"NVAL {val}")
                if val>cur_val:
                    if debug:                    
                        print("LOOSER")
                    solution["primitives"][i]["color"]=orgcolor
                    newcolor[j]+=color_to_move
                    if newcolor[j]<255-color_to_move:
                        newcolor[j]+=color_to_move
                        if debug:
                            print("Try2:"+str(newcolor))
                        solution["primitives"][i]["color"]=tuple(newcolor)
                        drawSolution(solution)
                        val=costFunction(solution["image"])
                        if debug:                        
                            print(f"NVAL2 {val}")


                        if val>cur_val:
                            if debug:
                                print("LOOSER2")
                            solution["primitives"][i]["color"]=orgcolor
                            newcolor[j]-=color_to_move
                        else:
                            if debug:
                                print("WINNER2")

                            orgcolor=solution["primitives"][i]["color"]
                            solution["value"]=val

                    
                    
                else:
                    if debug:
                        print("WINNER")

                    orgcolor=solution["primitives"][i]["color"]
                    solution["value"]=val
                    
        solution["primitives"][i]["color"]=tuple(newcolor)            
    
    if debug:
        print(f'ENDRGL {solution["value"]}')


    
    if debug:
        drawSolution(solution)
        val=costFunction(solution["image"])
        if (val !=solution["value"]):
            print(f'SHIT OUT {val} {solution["value"]}')
            solution["value"]=val

def mutate_permute(solution,debug=False):
    if debug:
        drawSolution(solution)
        val=costFunction(solution["image"])
        if (val !=solution["value"]):
            print(f'SHIT PERMUTE IN {val} {solution["value"]}')
            solution["value"]=val
#            A/0
    for i in range(0,1):
        src=random.randint(1,primitives-2)
        if random.randint(0,1)==0:
            trg=src+1
        else:
            trg=src-1
        cur_val=solution["value"]
#        print(src,trg)
        
        orgtrg=solution["primitives"][trg]["primitive"]
        orgsrc=solution["primitives"][src]["primitive"]
        solution["primitives"][trg]["primitive"]=orgsrc
        solution["primitives"][src]["primitive"]=orgtrg
        
        drawSolution(solution)
        val=costFunction(solution["image"])
#        print(val)
        if val>cur_val:        
#            print("Failure+")            
            solution["primitives"][src]["primitive"]=orgsrc
            solution["primitives"][trg]["primitive"]=orgtrg
            drawSolution(solution)
            val=costFunction(solution["image"])
        else:
#            print("Success+")            

            cur_val=val
            
    solution["value"]=cur_val
    if debug:
        drawSolution(solution)
        val=costFunction(solution["image"])
        if (val !=solution["value"]):
            print(f'SHIT PERMUTE OUT {val} {solution["value"]}')
            solution["value"]=val

def mutate_pt(solution,debug=False):
    if debug:
        drawSolution(solution)
        val=costFunction(solution["image"])
        if (val !=solution["value"]):
            print(f'SHIT PT IN {val} {solution["value"]}')
            solution["value"]=val
#            A/0
    prims_tocheck=random.randint(0,primitives-1)
#    print(prims_tocheck)
    
    bestprimitive=solution["primitives"][prims_tocheck]["primitive"]
    bestprimitivearr=[list(_) for _ in bestprimitive]
#    print(bestprimitivearr)
    tomove=random.randint(1,25)
    cur_val=solution["value"]
#    print(f"Start:{cur_val}")
    for i in range(0,len(bestprimitive)):
        for x in range(0,2):
#            print(f"Opt {i}=>x:{x}")
            # try +
            newprimitive=copy.deepcopy(bestprimitivearr)
            newprimitive[i][x]+=tomove
            solution["primitives"][prims_tocheck]["primitive"]=tuple(tuple(_) for _ in newprimitive)
#            print(solution)
            drawSolution(solution)
            val=costFunction(solution["image"])

            if val>cur_val:        
#                print("Failure+")            
#                print(val)
                solution["primitives"][prims_tocheck]["primitive"]=bestprimitive
                drawSolution(solution)
                val=costFunction(solution["image"])
#                print(val)            
            else:
#                print("Better+")
#                print(val)
                bestprimitive=solution["primitives"][prims_tocheck]["primitive"]
                bestprimitivearr=[list(_) for _ in bestprimitive]
                cur_val=val

            # try -
            newprimitive=copy.deepcopy(bestprimitivearr)
            newprimitive[i][x]-=tomove
            solution["primitives"][prims_tocheck]["primitive"]=tuple(tuple(_) for _ in newprimitive)
#            print(solution)
            drawSolution(solution)
            val=costFunction(solution["image"])

            if val>cur_val:        
#                print("Failure-")            
#                print(val)
                solution["primitives"][prims_tocheck]["primitive"]=bestprimitive
                drawSolution(solution)
                val=costFunction(solution["image"])
#                print(val)            
            else:
#                print("Better")
#                print(val)
                bestprimitive=solution["primitives"][prims_tocheck]["primitive"]
                bestprimitivearr=[list(_) for _ in bestprimitive]
                cur_val=val
            
    solution["value"]=cur_val
    if debug:
        drawSolution(solution)
        val=costFunction(solution["image"])
        if (val !=solution["value"]):
            print(f'SHIT PT OUT {val} {solution["value"]}')
            solution["value"]=val

def mutate_dead_primitives(solution):
    drawSolution(solution)
    val=costFunction(solution["image"])
    if (val !=solution["value"]):
        print(f'SHIT DEAD IN {val} {solution["value"]}')
        solution["value"]=val

    cur_val=solution["value"]
#    print(f"ORGL {cur_val}")

    found=True
    
    for i in range(0,len(solution["primitives"])):
#        print(i)
        orgprimitive=solution["primitives"][i]["primitive"]
        newprimitive=((0,0),(0,0),(0,0))
        solution["primitives"][i]["primitive"]=newprimitive
        
#        print(orgprimitive)
#        print(newprimitive)
        drawSolution(solution)
        val=costFunction(solution["image"])
#        print(f"NVAL {val}")
        if val>=cur_val:        
#            print("Failure+")            
            solution["primitives"][i]["primitive"]=orgprimitive
            drawSolution(solution)
            val=costFunction(solution["image"])
            #print(f"OVAL {val}")
        else:
            found=True
#            print(f"VICTORY {i}")
#        break
    #    print(bestprimitivearr)
#        tomove=random.randint(1,25)
#        cur_val=solution["value"]
    #    print(f"Start:{cur_val}")
#        for i in range(0,len(bestprimitive)):
    newprimitives=[]
    for prims in solution["primitives"]:
        prim=prims["primitive"]
        if prim[0][0]!=0 or prim[0][1]!=0 or prim[1][0]!=0 or prim[1][1]!=0 or prim[2][0]!=0 or prim[2][1]!=0:
            newprimitives.append(prims)
#    print(len(newprimitives))
    
    while(len(newprimitives)<primitives):
        x1=random.randint(0,org_im.size[0]-3)
        x2=random.randint(0,org_im.size[1]-3)
        
        y1=x1+2
        y2=x2

        z1=x1
        z2=x2+2
        
        m1=(x1+y1+z1)/3
        n1=(x2+y2+z2)/3
        
        r, g, b = org_im.getpixel((m1, n1))

        
        newprim={"primitive":((x1,x2),(y1,y2),(z1,z2)),"type":2,"color":(r,g,b)}
#        print(newprim)
        newprimitives.append(newprim)
    solution["primitives"]=newprimitives
    drawSolution(solution)
    solution["value"]=costFunction(solution["image"])

def check_population():
    for i,solution in enumerate(population):
        
        drawSolution(solution)
        val=costFunction(solution["image"])
#        print(f'{solution["value"]} <> {val}')
        if (val !=solution["value"]):
            print("Shit Check "*10)
            print(f'{solution["value"]} <> {val} => {i}')
            solution["value"]=val    

def cross(sol1,sol2):
    global primitives
    cut=random.randint(1,primitives-1)
    new_primitives=(copy.deepcopy(sol1["primitives"][0:cut])+copy.deepcopy(sol2["primitives"][cut:]))
    
    newimage={"primitives":new_primitives}
    drawSolution(newimage)

    newimage["value"]=costFunction(newimage["image"])
    return newimage

def cross2(sol1,sol2):
    global primitives
    newimage={"primitives":[]}
    for i in range(0,len(sol1["primitives"])):
        if random.randint(0,2)==0:
            newimage["primitives"].append(copy.deepcopy(sol1["primitives"][i]))
        else:
            newimage["primitives"].append(copy.deepcopy(sol2["primitives"][i]))
    drawSolution(newimage)

    newimage["value"]=costFunction(newimage["image"])
    return newimage

def create_generation():
    global population
    # add new solutions
    for i in range(len(population),population_size):
        print("Create New One")
        sol=createSolution(primitives)
        sol["value"]=costFunction(sol["image"])
        population.append(sol)
    
    for sol in population:
        if len(sol["primitives"])!=primitives:
            print("Fix primitives")
            while(len(sol["primitives"])<primitives):
                x1=random.randint(0,org_im.size[0])
                x2=random.randint(0,org_im.size[1])
                y1=random.randint(x1,org_im.size[0])
                y2=random.randint(x2,org_im.size[1])

                z1=random.randint(0,org_im.size[0])
                z2=random.randint(0,org_im.size[1])
                newprim={"primitive":((x1,x2),(y1,y2),(z1,z2)),"type":2,"color":(random.randint(0,255),random.randint(0,255),random.randint(0,255))}
                sol["primitives"].append(newprim)

            drawSolution(sol)
            sol["value"]=costFunction(sol["image"])


            
    check_population()
    
    print("- Cross")
    # cross solutions
    for i in range(0,int(population_size)):
#    for i in range(0,0):
        source=random.randint(0,population_size-1)
        target=random.randint(0,population_size-1)
        if source==target:
            continue
#        print(f"Cross {source} and {target}")
        to_do= random.randint(0,2)
        if to_do==0:    
            population.append(cross(population[source],population[target]))
        else:
            population.append(cross2(population[source],population[target]))

    check_population()
    
    print("- Mutate")
    # mutate solution
    for i in range(0,int(population_size/2)):
#        print(i)
        source=random.randint(0,len(population)-1)
        bef=population[source]["value"]
        #print("BEF:"+str(population[source]["value"]))
        
        for j in range(0,30): 
            
            to_do= random.randint(0,3)
            if to_do==0:
#                print("TATA")
                mutate_colors_2(population[source],debug=False) 
#                check_population()
            elif to_do==1:
                mutate_pt(population[source])        
            elif to_do==2:
                mutate_permute(population[source])        
            else:
                mutate_dead_primitives(population[source])        

        

        #print("AFTER:"+str(population[source]["value"]))
        
    check_population()
        
    pop_hash={}
    newpopulation=[]
    for pop in population:
        if pop["value"] not in pop_hash:
            pop_hash[pop["value"]]=True
            newpopulation.append(pop)
            
    #print(f"New pop length:{len(newpopulation)}")
    population=newpopulation
            
            
    population.sort(key=lambda x: x["value"], reverse=False)
    population=population[0:population_size]

def load_solution(filename):
    #type
    
    with open(filename, 'rb') as file:
        typ=int.from_bytes(file.read(2), byteorder='big', signed=True)
        prim=int.from_bytes(file.read(2), byteorder='big', signed=True)
        size=(int.from_bytes(file.read(2), byteorder='big', signed=True),int.from_bytes(file.read(2), byteorder='big', signed=True))
        print(f"Type:{typ} Primitives:{prim}")
        solution={"primitives":[]}
        
        for i in range(0,prim):
            primarr=[]
            for j in  range(0,9):
                primarr.append(int.from_bytes(file.read(2), byteorder='big', signed=True))
            newprim={"primitive":((primarr[0],primarr[1]),(primarr[2],primarr[3]),(primarr[4],primarr[5]))
                        ,"color":(primarr[6],primarr[7],primarr[8])}
            solution["primitives"].append(newprim)
        return solution

def save_solution(solution,filename):
    #type
    
    with open(filename, 'wb') as file:

#        print(solution)

        file.write((1).to_bytes(2, byteorder='big', signed=True))
        file.write((primitives).to_bytes(2, byteorder='big', signed=True))
        file.write((solution["image"].size[0]).to_bytes(2, byteorder='big', signed=True))
        file.write((solution["image"].size[1]).to_bytes(2, byteorder='big', signed=True))

        for pri in solution["primitives"]:
            print(pri["color"])
            for i in range(0,3):
                for j in range(0,2):
                    file.write((pri["primitive"][i][j]).to_bytes(2, byteorder='big', signed=True))
            for i in range(0,3):
                file.write((pri["color"][i]).to_bytes(2, byteorder='big', signed=True))
########################################

primitives=32
population_size=64
population=[]


if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")

    filename=sys.argv[1]
    print(f"File:"+filename)
    population_size=int(sys.argv[2])
    print(f"Pop Size:{population_size}")
    primitives=int(sys.argv[3])
    print(f"Primitives:{primitives}")

    path_to_folder=f"./solutions/{filename.replace('.jpg','')}-{primitives}"
    try:
        os.makedirs(path_to_folder)
    except:
        pass

    org_data=None
    with Image.open(filename) as org_im:
        org_data1 = np.asarray(org_im)
        org_data=np.reshape(org_data1,-1)

    if len(sys.argv)>4 and sys.argv[4]=="reload":
        print("Try to load previous solutions")
        for file in os.listdir(path_to_folder):
            if file.endswith(".eco"):
                print(os.path.join(path_to_folder, file))
                newsol=load_solution(os.path.join(path_to_folder, file))
                drawSolution(newsol)
                newsol["value"]=costFunction(newsol["image"])

                print(newsol["value"])
                population.append(newsol)
        
        population.sort(key=lambda x: x["value"], reverse=False)
        for pop in population:
            print(pop["value"])
        population=population[0:population_size]


    for i in range(len(population),population_size):
        sol=createSolution(primitives)
        sol["value"]=costFunction(sol["image"])
        population.append(sol)
    
    bestage=0
    for i in range(0,1000):
        
        bestvalue=population[0]["value"]
        create_generation()
        bestvalue2=population[0]["value"]
        if bestvalue==bestvalue2:
            bestage+=1
        else:
    #        population[0]["image"].show()
            population[0]["image"].save(path_to_folder+"/"+filename+"." + datetime.now().strftime("%d-%B-%Y_%H%M%S")+"-"+str(primitives)+".jpg", "JPEG", quality=100, subsampling=0)
            save_solution(population[0],path_to_folder+"/"+filename+"." + datetime.now().strftime("%d-%B-%Y_%H%M%S")+"-"+str(primitives)+".eco")
            bestage=0
        if bestage==20:
            population=population[0:10]
            primitives+=2
            print("Primitives:"+str(primitives))
        
        print(f'Best:{population[0]["value"]} age:{bestage} primitives:{primitives} pop:{len(population)}')


        
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

pa1=0
pa2=0
xx=0
yy=0
zo=0
gCamAng = 40
orxz=0
ory=0
check_lclick = 0
check_rclick = 0

deltaox=0
deltaoy=0
deltapx=0
deltapy=0

zkey = GL_FILL
znum = 0

seffect = True

gVertexArray = []

gVarrArray = []
gIndexArray = []
gNormArray = []

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([2.,0.,0.]))
    
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([-2.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,2.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,2.]))

    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,-2.]))
    
    glColor3ub(255, 255, 255)
    for i in range(6):
        for j in range(6):
            # ++영역(xz)
                glVertex3fv(np.array([0.4*j,0.,0.]))
                glVertex3fv(np.array([0.4*j,0.,2.]))

                glVertex3fv(np.array([0.,0.,0.4*j]))
                glVertex3fv(np.array([2.,0.,0.4*j]))
            # +-영역(xz)
                glVertex3fv(np.array([0.4*j,0.,0.]))
                glVertex3fv(np.array([0.4*j,0.,-2.]))
                    
                glVertex3fv(np.array([0.,0.,-0.4*j]))
                glVertex3fv(np.array([2.,0.,-0.4*j]))
            # -+영역(xz)
                glVertex3fv(np.array([-0.4*j,0.,0.]))
                glVertex3fv(np.array([-0.4*j,0.,2.]))
                
                glVertex3fv(np.array([0.,0.,0.4*j]))
                glVertex3fv(np.array([-2.,0.,0.4*j]))
            # --영역(xz)
                glVertex3fv(np.array([-0.4*j,0.,0.]))
                glVertex3fv(np.array([-0.4*j,0.,-2.]))
                
                glVertex3fv(np.array([0.,0.,-0.4*j]))
                glVertex3fv(np.array([-2.,0.,-0.4*j]))
    glEnd()


# • glNormalPointer( type, stride, pointer )
# • specifies the location and data format of an array of normals
# – type: The data type of each coordinate value in the array. GL_FLOAT, GL_SHORT, GL_INT or GL_DOUBLE.
# – stride: The number of bytes to offset to the next normal
# – pointer: The pointer to the first coordinate of the first normal in the array

# • glDrawElements( mode , count , type , indices )
# • : render primitives from vertex & index array data
# – mode: The primitive type to render. GL_POINTS, GL_TRIANGLES, ...
# – count: The number of indices to be rendered
# – type: The type of the values in indices. GL_UNSIGNED_BYTE, GL_UNSIGNED_SHORT, or GL_UNSIGNED_INT
# – indices: The pointer to the index array


def drawUnitCube_glDrawArray():
    global gVertexArray
    varr = np.array(gVertexArray)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_DOUBLE, 6 * varr.itemsize, varr)
    glVertexPointer(3, GL_DOUBLE, 6 * varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3 * varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size / 6))

def drawCube_glDrawElements():
    global gVarrArray, gIndexArray, gNormArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_DOUBLE, 3*gVarrArray.itemsize, gNormArray)
    glVertexPointer(3, GL_DOUBLE, 3*gVarrArray.itemsize, gVarrArray)
    glDrawElements(GL_TRIANGLES, gIndexArray.size, GL_UNSIGNED_INT, gIndexArray)


#마우스 스크롤(휠) 입력받기
def scroll_callback(window, xoffset, yoffset):
    global xx,yy,zo
    xx = xoffset
    yy = yoffset
    #zooming (x가 양수 y=0) 도형이 축소 // (x=0 y가 양수) 도형이 확대
    if xx>0 and yy==0:
        zo -= xx/3
    elif xx<0 and yy==0:
        zo += -(xx/3)
    elif xx==0 and yy>0:
        zo -= yy/3
    elif xx==0 and yy<0:
        zo += -(yy/3)

# zooming은 완성
def cursor_callback(window, xpos, ypos):
    global check_lclick, check_rclick
    global orxz,ory,deltaox,deltaoy
    global pa1, pa2, deltapx,deltapy
    global a,b
    if(check_lclick == 1):
        orxz += 0.01*(xpos - deltaox)
        deltaox = xpos
        ory += 0.03*(ypos - deltaoy)
        dletaoy = ypos

    if(check_rclick == 1):
        pa1 += 0.01*(xpos - deltapx)
        deltapx = xpos
        pa2 -= 0.01*(ypos - deltapy)
        deltapy = ypos

#orbit(mouse left drag),panning(mouse right drag)
def button_callback(window, button, action, mod):
    #panning을 위한 변수 pa1,2 orbit을 위한 변수 orx, ory
    global check_lclick, check_rclick, deltaox, deltaoy, deltapx, deltapy
    if button == glfw.MOUSE_BUTTON_LEFT:
       if  action == glfw.PRESS or action == glfw.REPEAT:
           check_lclick = 1
           deltaox, deltaoy = glfw.get_cursor_pos(window)
       
       elif action == glfw.RELEASE:
           check_lclick = 0

    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if  action == glfw.PRESS or action == glfw.REPEAT:
            check_rclick = 1
            deltapx, deltapy = glfw.get_cursor_pos(window)
        
        elif action == glfw.RELEASE:
            check_rclick = 0

########## glfw Set Drop Call back 구현하기 ##########
#obj 파일 구성은 어떻게 됐을까?
# v  ( x y z ) -> vertex의 좌표값이다
# vn ( x y z ) -> 각 면의 법선벡터(normal vector) 좌표값이다 정육면체이므로 6개가 생긴다
# f  ( v/vt/vn v/vt/vn v/vt/vn ) -> face를 나타내며 하나의 면을 구성하는 vertex와 texture coordinate, vertex normal을 나타낸 것이다
# vt ( u v d ) -> texture의 좌표계 값을 나타낸다
# 예를 들어서 f 1//1 2//1 3//1 이렇게 나와있다면 하나의 삼각형을 구성하는데  1,2,3 벌텍스가 사용되며 vt는 없고, 같은 1번 normal vector을 공유하고 있는 걸 알 수 있다
# 정육면체에서 한 면은 삼각형 2개로 이루어져있기 때문에 총 12개의 f가 존재한다

#split 문자열을 정해준 기준으로 잘라준다 밑에는 예시이다 :에 맞게 잘라준다
#>>> time_str = "10:34:17"
#>>> time_str.split(':')
#['10', '34', '17']

def drop_callback(window, paths):
    global gVertexArray
    global gVarrArray, gIndexArray, gNormArray
    
    vertex = []
    normal = []
    varr = []
    
    norm = []
    iarr = []
    adjacent = []

    face3 = 0
    face4 = 0
    face_more = 0
    face_total = 0
    
    vertex_count = 0

    objFile = open(" ".join(paths),'r')
    
    for line in objFile:
        #라인을 공백으로 자르고 그 잘려진 라인을 partition이라고 부른다
        partition = line.split()
        
        if line.startswith('#'):
            continue
        if not partition:
            continue
        
        # v 1.62505 -1.47645 0.882653 이런 식으로 되어 있으므로 처음 공백 위치에서 +1을 해서 x를 찾아준다
        if partition[0] == "v":
            line_vertex = (float(partition[1]),float(partition[2]),float(partition[3]))
            vertex.append(line_vertex)
            adjacent.append([0.0])
            vertex_count += 1
        
        if partition[0] == "vn":
            line_normal = (float(partition[1]),float(partition[2]),float(partition[3]))
            normal.append(line_normal)
        
            #f는 한글자이기 때문에 'f'을 해줘야 한다
        if partition[0] == 'f':
            #f가 나오면 그 줄을 face_count에 넣어준다
            face_count = np.array(partition[1:])
            #그리고 그 항목의 개수가 face를 이루는 개수이기 때문에 size를 이용해서 num에 넣어준다
            face_num = np.size(face_count)

            if face_num == 3:
                face3 += 1
            elif face_num == 4:
                face4 += 1
            elif face_num > 4:
                face_more += 1
            
            search = partition[1].split('/')
            one_iarr = int(search[0])
            oneVertex = vertex[int(search[0])-1]
            oneNormal = normal[int(search[2])-1]
            one_ver = np.array(oneVertex)
            varr.append(oneNormal)
            varr.append(oneVertex)
            
            search = partition[2].split('/')
            two_iarr = int(search[0])
            twoVertex = vertex[int(search[0])-1]
            twoNormal = normal[int(search[2])-1]
            two_ver = np.array(twoVertex)
            varr.append(twoNormal)
            varr.append(twoVertex)
            
            search = partition[3].split('/')
            three_iarr = int(search[0])
            threeVertex = vertex[int(search[0])-1]
            threeNormal = normal[int(search[2])-1]
            three_ver = np.array(threeVertex)
            varr.append(threeNormal)
            varr.append(threeVertex)

            Vtwo = two_ver - one_ver
            Vthree = three_ver - one_ver
            Vout = np.cross(Vtwo, Vthree)
            Vsize = np.sqrt(np.dot(Vout, Vout))
            V_fn = Vout / Vsize

            line_iarr = (one_iarr-1, two_iarr-1, three_iarr-1)
            iarr.append(line_iarr)

            line_vector = np.array([V_fn[0],V_fn[1],V_fn[2]])

            adjacent[one_iarr-1] += line_vector
            adjacent[two_iarr-1] += line_vector
            adjacent[three_iarr-1] += line_vector

            num = 3
            while (face_num > 3):
                search = partition[num].split('/')
                re_two_iarr = int(search[0])
                re_twoVertex = vertex[int(search[0])-1]
                re_twoNormal = normal[int(search[2])-1]
                re_two_ver = np.array(re_twoVertex)
                
                search = partition[num+1].split('/')
                re_three_iarr = int(search[0])
                re_threeVertex = vertex[int(search[0])-1]
                re_threeNormal = normal[int(search[2])-1]
                re_three_ver = np.array(re_threeVertex)

                twoVertex = re_twoVertex
                twoNormal = re_twoNormal
                two_iarr = re_two_iarr
                two_ver = re_two_ver
                
                threeVertex = re_threeVertex
                threeNormal = re_threeNormal
                three_iarr = re_three_iarr
                three_ver = re_three_ver
                
                Vtwo = two_ver - one_ver
                Vthree = three_ver - one_ver
                Vout = np.cross(Vtwo, Vthree)
                Vsize = np.sqrt(np.dot(Vout, Vout))
                V_fn = Vout / Vsize

                line_iarr = (one_iarr-1, two_iarr-1, three_iarr-1)
                iarr.append(line_iarr)

                line_vector = np.array([V_fn[0],V_fn[1],V_fn[2]])
                adjacent[one_iarr-1] += line_vector
                adjacent[two_iarr-1] += line_vector
                adjacent[three_iarr-1] += line_vector

                varr.append(oneNormal)
                varr.append(oneVertex)

                varr.append(re_twoNormal)
                varr.append(re_twoVertex)
                
                varr.append(re_threeNormal)
                varr.append(re_threeVertex)

                num += 1
                face_num -= 1
                    
    #한줄씩 다 읽어주고 나서 norm 배열을 완성시켜준다
    for i in range(0, vertex_count):
        final_n_v = adjacent[i]
        V_n_size = np.sqrt(np.dot(final_n_v,final_n_v))
        fnv = final_n_v/V_n_size

        line_norm = (float(fnv[0]),float(fnv[1]),float(fnv[2]))
        norm.append(line_norm)

    gVertexArray = varr
    gVarrArray = np.array(vertex)
    gIndexArray = np.array(iarr)
    gNormArray = np.array(norm)

    face_total = face3 + face4 + face_more
    
    #1. File name
    #2. Total number of faces
    #3. Number of faces with 3 vertices
    #4. Number of faces with 4 vertices
    #5. Number of faces with more than 4 vertices

    print("1. File name : " + str(paths))
    print("2. Total number of faces : %d" %(face_total))
    print("3. Number of faces with 3 vertices : %d" %(face3))
    print("4. Number of faces with 4 vertices : %d" %(face4))
    print("5. Number of faces with more than 4 vertices : %d" %(face_more))
    print(' ')

########## ########## ########## ########## ########


########## Toggle wireframe/solid mode by pressing Z key 구현하기 (완료) ##########

def key_callback(window, key, scancode, action, mods):
    global zkey, znum, seffect
    if action==glfw.PRESS or action==glfw.PRESS:
        if key==glfw.KEY_Z:
            if znum == 0:
                zkey = GL_LINE
                znum = 1
            elif znum == 1:
                zkey = GL_FILL
                znum = 0
        elif key==glfw.KEY_S:
                seffect = not seffect

########## ########## ########## ########## ########

def render():
    global pa1,pa2,zo,orxz,ory,a,seffect
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, zkey)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #Zooming 설정할때 사용하기
    gluPerspective(90+zo, 1, 1,10)
    
    eye = np.array([5*np.cos(gCamAng-(ory/500))*np.sin(gCamAng-(orxz/2)),5*np.sin(gCamAng-(ory/500)),5*np.cos(gCamAng-(ory/500))*np.cos(gCamAng-(orxz/2))])
    at = np.array([0,0,0])
    up = np.array([0,1,0])
    temp = (eye-at)
    w = temp / np.sqrt(np.dot(temp,temp))
    temp2 = np.cross(up,w)
    u = temp2 / np.sqrt(np.dot(temp2,temp2))
    v = np.cross(w,u)
    m=np.array([0.,0.,0.])
    m+=u*pa1+v*pa2
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(eye[0],eye[1],eye[2],0,0,0, 0,1,0)
    
    glTranslatef(m[0],m[1],m[2])
    
    #glTranslatef(v[0]*pa2,v[1]*pa2,v[2]*pa2)
    drawFrame()

########## LIGHTING 구현하기 ##########
# multiple light sources (not a single light) to better visualize the mesh -> lightpos 추가해주기
# Choose the number of light sources, light source types, light colors, material colors as you want.

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_RESCALE_NORMAL)
    
    #light1
    lightPos1 = (4.,5.,6.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos1)
    
    ambientLightColor1 = (.1,.1,.1,0.3)
    diffuseLightColor1 = (1.,1.,1.,0.3)
    specularLightColor1 = (1.,1.,1.,0.3)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor1)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor1)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specularLightColor1)
    
    #light2
    lightPos = (4.,5.,-6.,0.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    
    ambientLightColor = (.1,.1,.1,1.)
    diffuseLightColor = (1.,1.,1.,1.)
    specularLightColor = (1.,0.,0.,1.)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specularLightColor)
    
    # material reflectance for each color channel
    objectColor = (0.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glColor3ub(0, 0, 255)
    
    if seffect:
        drawUnitCube_glDrawArray()
    else:
        drawCube_glDrawElements()
    
    glDisable(GL_LIGHTING)

########## ########## ########## ####

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'Obj viewer', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.set_scroll_callback(window, scroll_callback)
        glfw.set_mouse_button_callback(window, button_callback)
        glfw.set_cursor_pos_callback(window, cursor_callback)
        ########## ##########
        glfw.set_key_callback(window, key_callback)
        ########## ##########
        glfw.set_drop_callback(window, drop_callback)
        ########## ##########
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()

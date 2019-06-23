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
spbar = 0
seffect = True

get_line_offset = []
get_gwalho = []
get_gwalho_cnt = 0

get_line_motion = []
get_st = 0 # 총 몇개의 column(기둥)으로 이루어졌는지 세어주는 변수
get_frame_cnt = 0 # 총 몇 줄의 motion으로 이루어졌는지 세어주는 변수
pl = 0 # motion을 위해 다음 줄로 내려주는 역할을 한다

Width = 600
Height = 600
near = 5
far = 1000.

zoom = 60.
resize = 0


def drawCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.3, 0.3,-0.3)
    glVertex3f(-0.3, 0.3,-0.3)
    glVertex3f(-0.3, 0.3, 0.3)
    glVertex3f( 0.3, 0.3, 0.3)
    
    glVertex3f( 0.3,-0.3, 0.3)
    glVertex3f(-0.3,-0.3, 0.3)
    glVertex3f(-0.3,-0.3,-0.3)
    glVertex3f( 0.3,-0.3,-0.3)
    
    glVertex3f( 0.3, 0.3, 0.3)
    glVertex3f(-0.3, 0.3, 0.3)
    glVertex3f(-0.3,-0.3, 0.3)
    glVertex3f( 0.3,-0.3, 0.3)
    
    glVertex3f(-0.3, 0.3, 0.3)
    glVertex3f(-0.3, 0.3,-0.3)
    glVertex3f(-0.3,-0.3,-0.3)
    glVertex3f(-0.3,-0.3, 0.3)
    
    glVertex3f( 0.3, 0.3,-0.3)
    glVertex3f( 0.3, 0.3, 0.3)
    glVertex3f( 0.3,-0.3, 0.3)
    glVertex3f( 0.3,-0.3,-0.3)
    glEnd()

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

#마우스 스크롤(휠) 입력받기
def scroll_callback(window, xoffset, yoffset):
    global zoom
    zoom -= yoffset

# zooming은 완성
def cursor_callback(window, xpos, ypos):
    global check_lclick, check_rclick
    global orxz,ory,deltaox,deltaoy
    global pa1, pa2, deltapx,deltapy
    global a,b
    if(check_lclick == 1):
        orxz += 0.07*(xpos - deltaox)
        deltaox = xpos
        ory += 0.07*(ypos - deltaoy)
        dletaoy = ypos

    if(check_rclick == 1):
        pa1 += 0.02*(xpos - deltapx)
        deltapx = xpos
        pa2 -= 0.02*(ypos - deltapy)
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

def size_callback(window, width, height):
    global Width, Height
    Width = width
    Height = height
    glViewport(0, 0, Width, Height)

def key_callback(window, key, scancode, action, mods):
    global zkey, znum, seffect, spbar
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
        elif key==glfw.KEY_SPACE:
            if spbar == 0:
                spbar = 1
            elif spbar == 1:
                spbar = 0

############### ############### ###############


def drawline(L1, L2):
    glBegin(GL_LINES)
    glColor3ub(255, 255, 0)
    glVertex3fv(L2)
    glVertex3fv(L1)

    glEnd()

def drawSkeleton():
    global get_line_offset, get_gwalho_cnt, get_gwalho, get_line_motion
    global get_st, pl, get_frame_cnt, spbar, resize
    s = 0
    u = 0
    
    for i in range(get_gwalho_cnt): # {{ }}을 확인해서 push pop을 해준다
        if get_gwalho[i] == 1000:
            glPushMatrix()
            n1 = np.array(get_line_offset[0])
            n2 = n1 + np.array(get_line_offset[s])
            
            if resize == 1:
                n2 = n2 / 15
                drawline(n1,n2)
                arr = np.array(get_line_offset[s]) / 15
                glTranslatef(arr[0],arr[1],arr[2])
            else:
                drawline(n1,n2)
                arr = np.array(get_line_offset[s])
                glTranslatef(arr[0],arr[1],arr[2])

            s += 1
            
            if get_gwalho[i+1] == -1000:
                continue
            elif i == 0:
                if int(get_line_motion[u][0]) == 1:
                    if int(get_line_motion[u+1][0]) == 2 and int(get_line_motion[u+2][0]) == 3:
                        glTranslatef(float(get_line_motion[u][pl]), float(get_line_motion[u+1][pl]), float(get_line_motion[u+2][pl]))
                            
                    elif int(get_line_motion[u+1][0]) == 3 and int(get_line_motion[u+2][0]) == 2:
                        glTranslatef(float(get_line_motion[u][pl]), float(get_line_motion[u+2][pl]), float(get_line_motion[u+1][pl]))

                if int(get_line_motion[u][0]) == 2:
                    if int(get_line_motion[u+1][0]) == 1 and int(get_line_motion[u+2][0]) == 3:
                        glTranslatef(float(get_line_motion[u+1][pl]), float(get_line_motion[u][pl]), float(get_line_motion[u+2][pl]))
            
                    elif int(get_line_motion[u+1][0]) == 3 and int(get_line_motion[u+2][0]) == 1:
                        glTranslatef(float(get_line_motion[u+2][pl]), float(get_line_motion[u][pl]), float(get_line_motion[u+1][pl]))
                
                if int(get_line_motion[u][0]) == 3:
                    if int(get_line_motion[u+1][0]) == 1 and int(get_line_motion[u+2][0]) == 2:
                        glTranslatef(float(get_line_motion[u+1][pl]), float(get_line_motion[u+2][pl]), float(get_line_motion[u][pl]))
                    
                    elif int(get_line_motion[u+1][0]) == 2 and int(get_line_motion[u+2][0]) == 1:
                        glTranslatef(float(get_line_motion[u+2][pl]), float(get_line_motion[u+1][pl]), float(get_line_motion[u][pl]))


                if int(get_line_motion[u+3][0]) == 4:
                    if int(get_line_motion[u+4][0]) == 5 and int(get_line_motion[u+5][0]) == 6:
                        glRotatef(float(get_line_motion[u+3][pl]), 0,0,1)
                        glRotatef(float(get_line_motion[u+4][pl]), 1,0,0)
                        glRotatef(float(get_line_motion[u+5][pl]), 0,1,0)
                                        
                    elif int(get_line_motion[u+4][0]) == 6 and int(get_line_motion[u+5][0]) == 5:
                        glRotatef(float(get_line_motion[u+3][pl]), 0,0,1)
                        glRotatef(float(get_line_motion[u+4][pl]), 0,1,0)
                        glRotatef(float(get_line_motion[u+5][pl]), 1,0,0)

                if int(get_line_motion[u+3][0]) == 5:
                    if int(get_line_motion[u+4][0]) == 4 and int(get_line_motion[u+5][0]) == 6:
                        glRotatef(float(get_line_motion[u+3][pl]), 1,0,0)
                        glRotatef(float(get_line_motion[u+4][pl]), 0,0,1)
                        glRotatef(float(get_line_motion[u+5][pl]), 0,1,0)
            
                    elif int(get_line_motion[u+4][0]) == 6 and int(get_line_motion[u+5][0]) == 4:
                        glRotatef(float(get_line_motion[u+3][pl]), 1,0,0)
                        glRotatef(float(get_line_motion[u+4][pl]), 0,1,0)
                        glRotatef(float(get_line_motion[u+5][pl]), 0,0,1)
                
                if int(get_line_motion[u+3][0]) == 6:
                    if int(get_line_motion[u+4][0]) == 4 and int(get_line_motion[u+5][0]) == 5:
                        glRotatef(float(get_line_motion[u+3][pl]), 0,1,0)
                        glRotatef(float(get_line_motion[u+4][pl]), 0,0,1)
                        glRotatef(float(get_line_motion[u+5][pl]), 1,0,0)
                    
                    elif int(get_line_motion[u+4][0]) == 5 and int(get_line_motion[u+5][0]) == 4:
                        glRotatef(float(get_line_motion[u+3][pl]), 0,1,0)
                        glRotatef(float(get_line_motion[u+4][pl]), 1,0,0)
                        glRotatef(float(get_line_motion[u+5][pl]), 0,0,1)
                
                u += 6

            else:
                if int(get_line_motion[u][0]) == 4:
                    if int(get_line_motion[u+1][0]) == 5 and int(get_line_motion[u+2][0]) == 6:
                        glRotatef(float(get_line_motion[u][pl]), 0,0,1)
                        glRotatef(float(get_line_motion[u+1][pl]), 1,0,0)
                        glRotatef(float(get_line_motion[u+2][pl]), 0,1,0)
                    
                    elif int(get_line_motion[u+1][0]) == 6 and int(get_line_motion[u+2][0]) == 5:
                        glRotatef(float(get_line_motion[u][pl]), 0,0,1)
                        glRotatef(float(get_line_motion[u+1][pl]), 0,1,0)
                        glRotatef(float(get_line_motion[u+2][pl]), 1,0,0)
                            
                            
                if int(get_line_motion[u][0]) == 5:
                    if int(get_line_motion[u+1][0]) == 4 and int(get_line_motion[u+2][0]) == 6:
                        glRotatef(float(get_line_motion[u][pl]), 1,0,0)
                        glRotatef(float(get_line_motion[u+1][pl]), 0,0,1)
                        glRotatef(float(get_line_motion[u+2][pl]), 0,1,0)

                    elif int(get_line_motion[u+1][0]) == 6 and int(get_line_motion[u+2][0]) == 4:
                        glRotatef(float(get_line_motion[u][pl]), 1,0,0)
                        glRotatef(float(get_line_motion[u+1][pl]), 0,1,0)
                        glRotatef(float(get_line_motion[u+2][pl]), 0,0,1)
        
                if int(get_line_motion[u][0]) == 6:
                    if int(get_line_motion[u+1][0]) == 4 and int(get_line_motion[u+2][0]) == 5:
                        glRotatef(float(get_line_motion[u][pl]), 0,1,0)
                        glRotatef(float(get_line_motion[u+1][pl]), 0,0,1)
                        glRotatef(float(get_line_motion[u+2][pl]), 1,0,0)
                    
                    elif int(get_line_motion[u+1][0]) == 5 and int(get_line_motion[u+2][0]) == 4:
                        glRotatef(float(get_line_motion[u][pl]), 0,1,0)
                        glRotatef(float(get_line_motion[u+1][pl]), 1,0,0)
                        glRotatef(float(get_line_motion[u+2][pl]), 0,0,1)

                u += 3
                    
        elif get_gwalho[i] == -1000:
            glPopMatrix()

    if spbar == 1:
        pl += 1
    if spbar == 0:
        pl = 1

    if pl == int(get_frame_cnt)+1:
        pl = 2

########## glfw Set Drop Call back 구현하기 ##########
#split 문자열을 정해준 기준으로 잘라준다 밑에는 예시이다 :에 맞게 잘라준다
#>>> time_str = "10:34:17"
#>>> time_str.split(':')
#['10', '34', '17']

def drop_callback(window, paths):
    global get_line_all, get_line_motion, get_line_offset, get_gwalho_cnt, get_gwalho
    global get_line_motion, get_st, get_frame_cnt, resize
    joint_cnt = 0
    frame_cnt = 0
    fps = 0
    joint_name = []
    ##### #####
    line_offset = [] # hierarchy 중 offset들을 저장한다
    gwalho = [] # hierarchy 중 { } 들을 저장하다
    gwalho_cnt = 0 # stack을 위해서 괄호의 개수를 저장한다
    line_motion = [] # 마지막 motion을 위해 필요한 배열이다
    ##### #####
    #channel이 몇개 총 들어가는지 확인하기 위해서 사용한 변수
    right_gwal = 0
    ch = 0
    t=0
    st = 0
    
    bvhFile = open(" ".join(paths),'r')
    
    resize = 0
    
    for line in bvhFile:
        #라인을 공백으로 자르고 그 잘려진 라인을 partition이라고 부른다
        # string = line.lstrip()
        # partition = string.split()
        partition = line.lstrip().split()
        
        if partition[0] == "HIERARCHY" or partition[0] == "MOTION":
            continue
        
        elif partition[0] == "End":
            continue
        
        elif partition[0] == "ROOT" or partition[0] == "JOINT":
            joint_name.append(partition[1])
            joint_cnt += 1
        
        elif partition[0] == '{':
            gwalho.append(1000)
            gwalho_cnt += 1
            right_gwal += 1
        
        elif partition[0] == "OFFSET":
            line_xyz = (float(partition[1]),float(partition[2]),float(partition[3]))
            line_resize = np.array(line_xyz)
            if np.sqrt(np.dot(line_resize,line_resize)) > 1:
                resize = 1
            line_offset.append(line_xyz)

        elif partition[0] == '}':
            gwalho.append(-1000)
            gwalho_cnt += 1

        elif partition[0] == "Frames:":
            frame_cnt = partition[1]
                
        elif partition[0] == "Frame" and partition[1] == "Time:":
            fps = 1.0 / float(partition[2])

        elif partition[0] == "CHANNELS":
            for i in range(int(partition[1])): #0부터 int(partition[1])-1 까지
                line_motion.append([]) # 6개, 3개에 맞추어 공백 만들어주기
                
                if partition[i+2].upper() == "XPOSITION":
                    line_motion[st].append(1.0)
                    line_motion[st].append(0.0)
                elif partition[i+2].upper() == "YPOSITION":
                    line_motion[st].append(2.0)
                    line_motion[st].append(0.0)
                elif partition[i+2].upper() == "ZPOSITION":
                    line_motion[st].append(3.0)
                    line_motion[st].append(0.0)
                elif partition[i+2].upper() == "ZROTATION":
                    line_motion[st].append(4.0)
                    line_motion[st].append(0.0)
                elif partition[i+2].upper() == "XROTATION":
                    line_motion[st].append(5.0)
                    line_motion[st].append(0.0)
                elif partition[i+2].upper() == "YROTATION":
                    line_motion[st].append(6.0)
                    line_motion[st].append(0.0)

                st += 1

            ch += 1
        
        else:
            if resize == 1:
                for i in range(st):
                    if int(line_motion[i][0]) == 1 or int(line_motion[i][0]) == 2 or int(line_motion[i][0]) == 3:
                        line_motion[i].append(float(partition[i]) / 15.0)
                    if int(line_motion[i][0]) == 4 or int(line_motion[i][0]) == 5 or int(line_motion[i][0]) == 6:
                        line_motion[i].append(float(partition[i]))
            else:
                #resize = 0
                for i in range(st):
                    line_motion[i].append(partition[i])
                
    get_line_offset = line_offset
    get_gwalho = np.array(gwalho)
    get_gwalho_cnt = gwalho_cnt
    get_line_motion = line_motion
    get_st = st
    get_frame_cnt = frame_cnt
    
    print("1. File name : " + str(paths))
    print("2. Number of frames : " + str(frame_cnt))
    print("3. FPS (which is 1/FrameTime) : " + str(fps))
    print("4. Number of joints (including root) : " + str(joint_cnt))
    print("5. List of all joint names : ")
    for i in range(joint_cnt):
        print(" " + str(joint_name[i]))
    print(" ")

def render():
    global pa1,pa2,zo,orxz,ory,a,seffect
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, zkey)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(zoom, float(Width)/float(Height), near, far)
    glTranslatef(0., 0., -15)
    
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
    
    drawFrame()
    
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
    
    glColor3ub(255, 255, 255)
    
    glDisable(GL_LIGHTING)

    drawSkeleton()

########## ########## ########## ####

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'Bvh viewer', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, size_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glfw.set_scroll_callback(window, scroll_callback)
        glfw.set_mouse_button_callback(window, button_callback)
        glfw.set_cursor_pos_callback(window, cursor_callback)
        ########## ##########
        glfw.set_key_callback(window, key_callback)
        ########## ##########
        glfw.set_drop_callback(window, drop_callback)
        render()
        ########## ##########
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()

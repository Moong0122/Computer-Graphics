import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

pa1=0
pa2=0
xx=0
yy=0
zo=0
gCamAng = 45
orxz=0
ory=0
check_lclick = 0
check_rclick = 0
deltaox=0
deltaoy=0
deltapx=0
deltapy=0
a = 1
b = 0

def drawCube():
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glEnd()

def drawSphere(numLats=12, numLongs=12):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        
        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
        
        # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP)
        
        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        
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
    #참고하기
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

def render():
    global pa1,pa2,zo,orxz,ory,a
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()

    gluPerspective(90+zo, 1, 1,10)
    
    eye = np.array([5*np.cos(gCamAng-(ory/500))*np.sin(gCamAng-(orxz/2)),5*np.sin(gCamAng-(ory/500)),5*np.cos(gCamAng-(ory/500))*np.cos(gCamAng-(orxz/2))])
    at = np.array([0,0,0])
    up = np.array([0,1,0])
    temp = (eye-at)
    w = temp / np.sqrt(np.dot(temp,temp))
    temp2 = np.cross(up,w)
    u = temp2 / np.sqrt(np.dot(temp2,temp2))
    v = np.cross(w,u)
    
    glTranslatef(u[0]*pa1,u[1]*pa1,0)
    glTranslatef(v[0]*pa2,v[1]*pa2,0)

    gluLookAt(5*np.cos(gCamAng-(ory/500))*np.sin(gCamAng-(orxz/2)),5*np.sin(gCamAng-(ory/500)),5*np.cos(gCamAng-(ory/500))*np.cos(gCamAng-(orxz/2)), 0,0,0, 0,a,0)
    
    glMatrixMode(GL_MODELVIEW)
    t = glfw.get_time()
    
    #사람의 시작부분 몸통 -> 얼굴,왼팔,오른팔,왼다리,오른다리
    #왼팔 - 왼팔밑팔, 왼팔주먹
    #오른팔 - 오른팔밑팔, 오른팔주먹
    #왼다리 - 왼밑다리, 발
    #오른다리 - 오른밑다리, 발
    #왼팔, 오른다리 쌍 <=>(서로반대) 오른팔, 왼다리 쌍
    
    glColor3ub(0, 255, 255)
    glScalef(0.6, 0.9, 0.7)
    glTranslatef(0.0, 0.5*np.sin(t*3), 0.0)
    drawCube() # 몸통
    
    glPushMatrix()
    glScalef(0.5, 0.5, 0.5)
    glTranslatef(0, 3.5, 0) #얼굴
    glColor3ub(255, 255, 0)
    drawSphere()
    glPopMatrix()
    
    glPushMatrix()
    glScalef(0.5, 0.7, 0.5)
    glTranslatef(-3.3, 0.5, 0.0)
    glRotatef(25*np.sin(t*3), 1, 0, 0)
    glColor3ub(255, 0, 0)
    drawCube() # 왼팔
    
    glPushMatrix()
    glScalef(1, 0.5, 2)
    glTranslatef(0, -2, 0.5)
    glColor3ub(255, 0, 0)
    drawCube() # 왼팔 밑팔
    
    glPushMatrix()
    glScalef(1, 1, 0.5)
    glTranslatef(0, 0, 2.8)
    glColor3ub(255, 0, 0)
    drawSphere() # 왼팔 밑팔 주먹
    
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    
    glPushMatrix()
    glScalef(0.5, 0.7, 0.5)
    glTranslatef(3.3, 0.5, 0.0)
    glRotatef(-25*np.sin(t*3), 1, 0, 0)
    glColor3ub(0, 0, 255)
    drawCube() #오른팔
    
    glPushMatrix()
    glScalef(1, 0.5, 2)
    glTranslatef(0, -2, 0.5)
    glColor3ub(0, 0, 255)
    drawCube() # 오른팔 밑팔
    
    glPushMatrix()
    glScalef(1, 1, 0.5)
    glTranslatef(0, 0, 2.8)
    glColor3ub(0, 0, 255)
    drawSphere() # 오른팔 밑팔 주먹
    
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    
    glPushMatrix()
    glRotatef(-10,1,0,0)
    glScalef(0.5, 0.7, 0.5)
    glTranslatef(-1.7, -2.2, 0.0)
    glRotatef(-25*np.sin(t*3), 1, 0, 0)
    glColor3ub(0, 255, 0)
    drawCube() #왼다리
    
    glPushMatrix()
    glRotatef(20,1,0,0)
    glTranslatef(0.0, -2.2, 0.4)
    glColor3ub(0, 255, 0)
    drawCube() #왼다리 밑다리
    
    glPushMatrix()
    glRotatef(-10,1,0,0)
    glScalef(1.2, 0.7, 2.2)
    glTranslatef(0.0, -2., 0.3)
    glColor3ub(0, 255, 0)
    drawSphere() #왼다리 발
    
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    
    glPushMatrix()
    glRotatef(-10,1,0,0)
    glScalef(0.5, 0.7, 0.5)
    glTranslatef(1.7, -2.2, 0.0)
    glRotatef(25*np.sin(t*3), 1, 0, 0)
    glColor3ub(0, 255, 0)
    drawCube() #오른다리
    
    glPushMatrix()
    glRotatef(20,1,0,0)
    glTranslatef(0.0, -2.2, 0.4)
    glColor3ub(0, 255, 0)
    drawCube() #오른다리 밑다리
    
    glPushMatrix()
    glRotatef(-10,1,0,0)
    glScalef(1.2, 0.7, 2.2)
    glTranslatef(0.0, -2., 0.3)
    glColor3ub(0, 255, 0)
    drawSphere() #왼다리 발
    
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

    drawFrame()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'Basic OpenGL viewer', None,None)
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
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()

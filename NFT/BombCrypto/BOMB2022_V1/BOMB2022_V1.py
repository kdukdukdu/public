import time
import cv2 as cv2
import numpy
from matplotlib import pyplot as plt
import pyautogui
from datetime import datetime
############
import mss
import yaml
import random

if __name__ == '__main__': 
    stream = open("config.yaml", 'r')# LÊ AS CONNFIGURAÇÕES O ARQUIVO
    config = yaml.safe_load(stream)
    c_time_loop = config['time_intervals']
    cont_log_bomb = config['cont_log_bomb'] #SERÁ UM VALOR FIXO DE FERENCIA DE CONTAS - LOGADAS
    
    go_conect = cv2.imread('targets/new50/login_assinar_meta/connect.png')#Botão para Iniciar o Jogo
    go_select_sign_meta1 = cv2.imread('targets/new50/login_assinar_meta/assina1.png')#Botao para Confirmar na Metamask
    go_select_sign_meta2 = cv2.imread('targets/new50/login_assinar_meta/assinar2.png')#Botao para Confirmar na Metamask

    go_map = cv2.imread('targets/new50/treasure-hunt-icon.png')#botão entrar no jogo
    go_back = cv2.imread('targets/new50/voltar.png')#botão voltar pagina
    x_button = cv2.imread('targets/new50/x.png')#botão fechar
    go_hero_work_ini = cv2.imread('targets/new50/heroes.png')#botão selecao hero

    tela_ini1 = cv2.imread('targets/new50/findbox/telaini1.png')#botão voltar pagina
    tela_ini2 = cv2.imread('targets/new50/findbox/telaini2.png')#botão voltar pagina
    tela_work1 = cv2.imread('targets/new50/findbox/telawork1.png')
    tela_work2 = cv2.imread('targets/new50/findbox/telawork2.png')


    hero_epic = cv2.imread('targets/new50/heroes/hero_epico.png')#botão voltar pagina
    hero_supr = cv2.imread('targets/new50/heroes/hero_supraro.png')#botão voltar pagina
    hero_raro = cv2.imread('targets/new50/heroes/raro.png')#botão voltar pagina
    hero_commum = cv2.imread('targets/new50/heroes/commun.png')#botão voltar pagina
    workgreen = cv2.imread('targets/new50/heroes/workgreen.png')#botão voltar pagina
    noworkred = cv2.imread('targets/new50/heroes/noworkred.png')#botão voltar pagina

    hero_rest = cv2.imread('targets/new50/heroes/rest_hero.png')#botão voltar pagina
    go_work = cv2.imread('targets/new50/heroes/work.png')#botao colocar pra trabalhar
    go_home = cv2.imread('targets/new50/heroes/home.png')#botao colocar pra trabalhar
    
    go_rest_nowork = cv2.imread('targets/new50/heroes/rest_hero.png')#botao colocar pra trabalhar
    go_all_work = cv2.imread('targets/new50/heroes/go_all_work.png')#botão selecao hero
    go_all_nowork = cv2.imread('targets/new50/heroes/go_all_nowork.png')#botão selecao hero
    
    go_new_map = cv2.imread('targets/new50/mapa/new-map.png')#botão ok
    go_select_hero1 = cv2.imread('targets/new50/mapa/select-hero1.png')#botão selecao hero
    go_select_hero11 = cv2.imread('targets/new50/mapa/select-hero2.png')#botão selecao hero   
    go_hero_work_map = cv2.imread('targets/new50/mapa/heroes.png')#botão selecao hero
    
    #go_moeda = cv2.imread('targets/moeda.png')#Botão da Moeda

    ok_bt = cv2.imread('targets/new50/erro/ok.png')#botão ok
###########################SCREEM TELA & BOX########################################
def printScreenTela():
    with mss.mss() as sct:
        # Não entendi o motivo deste comando
        monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        sct_img = numpy.array(sct.grab(sct.monitors[0]))
        return sct_img[:,:,:3]

def printScreenBox(x,y,w,h):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"top": y, "left": x, "width": w, "height": h}
        # Grab the data
        sct_img = numpy.array(sct.grab(monitor))
        #mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        return sct_img[:,:,:3]    

###################################################################
def Scroll(scroolnum = -100):#Padrão Baixo
    last = 1
    while last < 21:
        #carregando todos os usuarios
        pyautogui.scroll(scroolnum)
        if(last == 21):
            time.sleep(0.3)
            break

        last = last + 1
        time.sleep(0.1)
##########################################################################################
#################################VERSÃO 2022###########################################
def horarioexato():
    return datetime.today().strftime("%Hh%Mmin%Ss DO DIA %d/%m/%Y")

def findElementosScreen(screen,find_in_inscreen, threshold=0.8, debug_mode='rectangles'):
    result = cv2.matchTemplate(screen, find_in_inscreen, cv2.TM_CCOEFF_NORMED)
    #Pega os valores max_val -> % de acerto na Busca, Max_loc --> coordenada X,Y encontrada
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        locations = numpy.where(result >= threshold)
        
        #ALTURA E LARGURA DA IMG EM BUSCA
        find_img_h = find_in_inscreen.shape[0]
        find_img_w = find_in_inscreen.shape[1]
        
        locations = list(zip(*locations[::-1]))
        
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), find_img_w, find_img_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        
        points_ini = []
        points_end = []
        points_center = []
        if len(rectangles):
            #print('Found needle.')

            line_color = (0, 255, 0)
            line_type = cv2.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv2.MARKER_CROSS

            # Loop over all the rectangles
            for (x, y, w, h) in rectangles:
                points_ini.append((x, y))
                points_end.append((x + w, y + h))

                # Determine the center position
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                # Save the points
                points_center.append((center_x, center_y))
                
                if debug_mode == 'rectangles':
                    # Determine the box position
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    # Draw the box
                    cv2.rectangle(screen, top_left, bottom_right, color=line_color, 
                                lineType=line_type, thickness=2)
                elif debug_mode == 'points':
                    # Draw the center point
                    cv2.drawMarker(screen, (center_x, center_y), 
                                color=marker_color, markerType=marker_type, 
                                markerSize=40, thickness=2)

            #if debug_mode:
                #cv2.imshow('Matches', screen)
                #cv2.waitKey()
                #cv.imwrite('result.jpg', haystack_img)
        return points_ini, points_center,points_end
    else:
        #print('Elemento na Screeen - Não foi encontrado a Imagem Procurada :(')
        return [],[],[]

def coordTelaXY(find_in_inscreen):
    screen = printScreenTela()#printa a tela
    cv2.imwrite('resultados/PrintTelaOk.jpg',screen)#guarda a imagem 
    screen = cv2.imread('resultados/PrintTelaOk.jpg')#carrega a imagem
    return findElementosScreen(screen,find_in_inscreen)

def findTelaXY(find_in_inscreen,onclicked= False,doubleclick = False,addX = 0,addY = 0,f5Pag = False,listUn = False,workheroes = False):#BUSCA EM TODA A TELA A POSIÇÃO DAS IMAGENS
    screen = printScreenTela()#printa a tela
    cv2.imwrite('resultados/PrintTelaOk.jpg',screen)#guarda a imagem 
    screen = cv2.imread('resultados/PrintTelaOk.jpg')#carrega a imagem

    pini,pcenter,pend = findElementosScreen(screen,find_in_inscreen)

    if(len(pcenter)>0):
        cont = 1
        for (pini,pcenter) in zip(pini,pcenter):
            (xc,yc) = pcenter
            #print(' \n Ponto Inicial ==> ', cont,' -> X=',xc,', Y=',yc)
            
            if(onclicked):
                pyautogui.moveTo(xc+addX,yc+addY,0.2)
                pyautogui.click(xc+addX,yc+addY,interval=1)
                #time.sleep(0.5)
            if(doubleclick):
                pyautogui.doubleClick()
                time.sleep(1.0)
            
            if(f5Pag):
                #pyautogui.press("f5")
                time.sleep(1.0)
                pyautogui.hotkey('ctrl', 'f5')

            if(listUn and cont == 1):#SÓ QUERO QUE LIST O PRIMEIRO ELEMENTO
                break
            if(workheroes):
                if(cont % 5 == 0):
                    Scroll(workheroes)

            cont = cont + 1
        return True
    else:
        return False
    #SELEÇÃO DAS COORDENADAS PRINCIPAIS DE TODAS AS TELAS. #COORD_INI/#COORD_CENTRO/#COORD_FIM

def findGoHero(findpoint_img1,find_element,onclicked = False, listUn = False,gogreen = False,gored = False):#BUSCA TODOS AS BOX COM PONTOS CARACTERÍSTICOS
    #SELEÇÃO DAS COORDENADAS PRINCIPAIS DE TODAS AS TELAS.
    pini1,pcenter1,pend1 = coordTelaXY(findpoint_img1)#PEGA APENAS AS COORDENADAS TOP=LEFT X/Y
    
    #LOOP PRINCIPAL - BOMBCRYPTO A QUAL GERENCIA TODAS AS TELAS - BOX
    if(len(pini1)>0):
        cont1 = 1
        for (pini,pend) in zip(pini1,pend1):

            (xi,yi) = pini
            (xf,yf) = pend
            
            x = int(xi)
            y = int(yi-18)
            #yi = int(y)
            
            w = int(400)
            h = int(50)
            #TRABALHO DENTRO DA BOX - ACHO QUE É DESNECESSÁRIO
            screen = printScreenBox(x,y,w,h)
            cv2.imwrite('resultados/PrintBox'+str(cont1)+'.jpg',screen)#guarda a imagem 
            screen = cv2.imread('resultados/PrintBox'+str(cont1)+'.jpg')#carrega a imagem        

            p_work_ini,p_work_center,p_work_end = findElementosScreen(screen,find_element)

            print(' \n Quadro n° ', cont1,' --- ',p_work_center)
            #print('ij')
            #SE ENCONTROU ALGO - PERCORRE :) = OU SEJA, TAMANHO DA LISTA É MAIOR QUE 0
            if(len(p_work_center) > 0):
                
                cont2 = 1
                for (p_ini,p_center) in zip(p_work_ini,p_work_center):
                    if(cont2 == 1):
                        (returnX,returnY) = p_center
                        
                    (map_x,map_y) = p_center
                    #print('-> X=',map_x,', -> Y=',map_y)
                    
                    if(onclicked):
                        pyautogui.moveTo(xi+map_x,yi+map_y-18,0.3)
                        pyautogui.click(xi+map_x,yi+map_y-18,interval=0.4)
                        time.sleep(1)
                    else: 
                        pyautogui.moveTo(xi+map_x,yi+map_y-18,0.5)
                    
                    if(listUn and cont2 == 1):#SÓ QUERO QUE LIST O PRIMEIRO ELEMENTO
                        break

                    cont2 = cont2 + 1
        
            cont1 = cont1 + 1

        return True
    else:
        return False
##########################################################################################
def CheckLogin():
    #VERIFICA ALGUM ERRO NA TELA - DE BOTÃO OK CONECTION - PT/BR
    #checkXBack()
    while True: 
        ############################CHECK INICIAL################################
        if(findTelaXY(go_select_sign_meta1) or findTelaXY(ok_bt)):
            time.sleep(1)
            findTelaXY(go_select_sign_meta1,True,True,-50,-200)
            time.sleep(1)
            findTelaXY(go_select_sign_meta2,True)
            time.sleep(1)
            print('ENCONTRAMOS UM BOTÃO OK/CONEXAO ÀS {} '.format(horarioexato()))
            findTelaXY(ok_bt,True)
            sleepTime(12,'IREMOS ATUALIZAR CADA UMA DA(S) PAGINA(S) :)')   
        ############################################################
        ############################VERIFICAR SE TEM BOTÃO DE CONEXÃO WALET################################
        if (findTelaXY(go_conect)):
            print('BOTÃO CONECT ENCONTRADO NA TELA! IREMOS DAR F5 ÀS {} '.format(horarioexato()))
            contconta = 1
            while(findTelaXY(go_conect)): #CLICA SO NO PRIMEIRO ENTRAR - SERÁ VERIFICADO UM POR UM
                findTelaXY(go_conect,True,True,0,-100,True,True) #ATUALIZA A 1° PAGINA
                sleepTime(25,'INICIANDO O LOGIN NA(S) CONTA  '+str(contconta)) #TEMPO CONSIDERÁVEL PARA ATUALIZAR PAGINA
                findTelaXY(go_conect,True,True,0,0,False,True) #CLICA APENAS NA 1° PAGINA
                findTelaXY(go_conect,True,True,0,0,False,True) #CLICA APENAS NA 1° PAGINA
                
                #ENQUANTO TIVER A CAIXA DE CONFIRMAÇÃO METAMASK ELE FICA AQUI DENTRO TENTANDO CLICAR.
                contx = 0
                while(findTelaXY(go_select_sign_meta1)==False and contx < 2):
                    sleepTime(15,'Clicando no Conected - na Conta '+str(contconta)+'. Tentativa '+str(contx)+'°')#TEMPO CONSIDERÁVEL PARA ATUALIZAR PAGINA
                    findTelaXY(go_select_sign_meta1,True,True,-50,-200,False,True)
                    sleepTime(1)
                    findTelaXY(go_select_sign_meta2,True)
                    contx = contx + 1
                    if findTelaXY(ok_bt):
                        continue

                contconta = contconta + 1
        
                sleepTime(2,'Entrando na sua conta')
                findTelaXY(go_select_sign_meta2,True) 
                sleepTime(2,'Só Aguardar 100% :)')
        else:
            sleepTime(2,'NÃO FOI ENCONTRADO NENHUM BOTÃO CONECT NA TELA')#TEMPO CONSIDERÁVEL PARA ATUALIZAR PAGINA
    
        ret_error = findTelaXY(ok_bt)#AO ACHAR, VAMOS DAR UM SLEEP ATÉ RECARREGAR A PAGINA 
        if(ret_error):#SE ENCONTRAR O BOTÃO OK, É PQ DEU ERRO 
            print('ENCONTRAMOS UM BOTÃO OK/CONEXAO ÀS {} '.format(horarioexato()))
            findTelaXY(ok_bt,True)
            sleepTime(12,'Aguarde enquanto atualizamos a pagina')   

        if findTelaXY(go_conect) or findTelaXY(go_select_sign_meta1)  or  findTelaXY(go_select_sign_meta2):
            continue
        else:
            print('TODAS CONTAS DEVEM ESTAR CONECTADAS :)')
            sleepTime(2)
            break
##########################################################################################
def herosFullWorkIni():
    while True:
        checkXBack()
        print('INICIANDO O PROCESSO DE SELEÇÃO DOS HEROS- ÀS {} '.format(horarioexato()))
        sleepTime(5)
        ################APENAS SELEÇÃO ALL - HEROES#############
        findTelaXY(go_hero_work_ini,True)
        print('COLOCANDO OS HEROS PARA TRABALHAR')
        sleepTime(5)
        findTelaXY(go_all_work,True)
        time.sleep(1.5)
        
        findTelaXY(x_button,True)
        print('ENTRAREMOS EM TODOS OS MAPAS')
        sleepTime(5)
        findTelaXY(go_map,True)
        
        print('VERIFICANDO SE NÃO TEMOS TELA INICIAL')
        sleepTime(5)
        if findTelaXY(go_hero_work_ini) or findTelaXY(x_button):
            continue
        else:
            return False


def updateMapaHero():
    findTelaXY(go_back,True)
    time.sleep(1.5)
    findTelaXY(x_button,True)
    time.sleep(1.5)
    findTelaXY(go_map,True)

def newMap():
    checkXBack()
    findTelaXY(go_new_map,True)

def reloadContas():
    checkXBack()
    #sys.stdout.write('\n VAMOS REINICIAR TODAS AS CONTAS  - ÀS {} '.format(horarioexato()))
    
    findTelaXY(go_hero_work_ini,True)
    time.sleep(1.5)
    findTelaXY(go_all_nowork,True)
    time.sleep(1.5)
    #newMap()
    #time.sleep(1.5)
    checkXBack()
    findTelaXY(go_hero_work_ini,True,False,0,-100,True) # CLICA ACIMA E ATUALIZA
    #print('VAMOS AGUARDAR 20s')
    #time.sleep(20.0)#TEMPO CONSIDERÁVEL PARA ATUALIZAR PAGINA
    CheckLogin()
 ################FUNÇÕES AUXILIARES#############   
def checkXBack():
    while(findTelaXY(go_back) or findTelaXY(x_button)):
        findTelaXY(x_button,True)
        time.sleep(1.5)
        findTelaXY(go_back,True)
        time.sleep(1.5)

def sleepTime(qtdseg = 1, info_msg = ''):
    #sys.stdout.write('Será necessário aguardar '+str(y)+'s')
    for x in range((qtdseg), 0,-1):
        print(f'{"Aguarde: "+str(x)}seg para prosseguir {info_msg}:) \r', end="")
        time.sleep(1)
def main():
###########################AMBIENTE DE TESTE########################################
    #findTelaXY(go_select_sign_meta1,True,True,-50,-200)
    #while True:
    #goWorkIni2()

    #findGoHero(hero_supr,go_work,False,True,False,True)

    #CheckLogin()#100%
    #herosFullWorkIni()#100%
        #sleepTime(10)
    #updateMapaHero()100%
    
 ###########################AMBIENTE DE TESTE########################################
    contloop = 1
    while True:
        cont = 1
        print('SE GOSTOU DO BOOT DO BOMB - FIQUE A VONTADE PARA PAGAR UM CAFE/BCOINHA :)')
        print('CARTEIRA WALET: 0xAc8b000865BdBcD6C4eD4Ac85475Afd57DD2244D')
        print('BOT BOMBCRYPTO 2022 - INICIAL NO SISTEMA PELA ',contloop,'° vez. Aguarde 2s...')
        time.sleep(2)
        t_cont = {
            "check_bt_login" : 0,#ok CHEK ERRO - LOGIN ETC
            "time_refresh_position" : 0, #ok ATUALIZAR MAPA SAIR E VOLTAR
            "hero_comum_work" : 0,#ok
            "hero_raro_work" : 0,
            "hero_sraro_work" : 0,
            "hero_epico_work" : 0,
            "hero_full_work" : 0,
            "check_bt_map" : 0,#ok
            "time_reboot_bot": 0
        }

        cont = 1
        temporefresh = 0.05 # 0.1min = 6s
        now_loop = time.time() #INICIO DO PRIMEIRO LOOP PRINCIPAL

        t_cont['hero_comum_work'] = t_cont['hero_raro_work'] = t_cont['hero_sraro_work'] = t_cont['hero_epico_work'] = now_loop #PRA NÃO ENTRAR A PRIMEIRA VEZ UMA VEZ
        ###################################INICIADO O LOOP PRINCIPAL###################################
        while True:
            now = time.time()#DEFINE UM TIME AO ENTRAR. EX.: 101516
            
            random_number = 0.1*random.uniform(5, 10)   
            ###### CONDIÇÃO - VERIFICA LOGIN & LOGAR - METAMASK - BOMBER - VERIFICAR PAG ERRO
            if (now - t_cont['check_bt_login']) > (c_time_loop['check_bt_login'] * 60):
                t_cont['check_bt_login'] = now
                #sys.stdout.write('\n VERIFICANDO A PRESENÇA DO BOTÃO CONECT OU LOGIN - ÀS {} '.format(horarioexato()))
                CheckLogin()   
            ####################WORK TRABALHAR HEROS################################  

            ######COLOCANDO TODOS FULL A 1° VES###################
            if (now - t_cont['hero_full_work']) > (c_time_loop['hero_full_work'] * 60):
                t_cont['hero_full_work'] = now
                #sys.stdout.write('\n VERIFICANDO A PRESENÇA DO BOTÃO CONECT OU LOGIN - ÀS {} '.format(horarioexato()))
                print('INICIANDO COM TODOS OS HEROES - ÀS {} '.format(horarioexato()))
                herosFullWorkIni()
            ######COLOCANDO TODOS FULL A 1° VES###################

            ####################WORK TRABALHAR HEROS################################  
            
            ###### CONDIÇÃO - SAIR DO MAPA - VOLTAR E ENTRAR NO MAPA
            if (now - t_cont['time_refresh_position']) > (random_number*c_time_loop['time_refresh_position'] * 60):
                t_cont['time_refresh_position'] = now
                updateMapaHero()
                   
        ###################################INICIADO O LOOP PRINCIPAL###################################                
main()
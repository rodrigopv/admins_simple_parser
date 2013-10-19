#!/usr/bin/python

# Se buscara conseguir solamente SteamID, Flags e Inmunidad

class Admins_Simple:
#file = open('admins_simple.ini');

  def __init__(self, path):
    self.admins = []
    self.buffer_steamid = ""
    self.buffer_flags = ""
    self.buffer_immunity = 0
    # 0 = Esperando " o //
    self.estado = 0 
    self.file = open(path)
    self.cargarArchivo(self.file)

  def cargarArchivo(self, file):    
    for linea in file:
       self.buffer_steamid = ""
       self.buffer_flags = ""
       self.buffer_immunity = 0

       while len(linea) > 0:
         if self.estado == 0 or self.estado == 2:
            linea = linea.strip()
         if self.estado == 0: 
            if linea.find('//') == 0:
              #print 'Comentario: ', linea
              linea = ""	  
              continue
            elif linea.find('"') == 0:
              self.estado = 1
              linea = linea[1:]
         elif self.estado == 1: # Esperando " o strings
            if linea.find('"') != -1:
              # print 'STEAMID:', linea[:linea.find('"')]
              self.buffer_steamid = linea[:linea.find('"')]
              self.estado = 2
              linea = linea[linea.find('"')+1:]
              continue
            else:
              print 'Error de formato'
              self.estado = 0
              linea = ""
         elif self.estado == 2: # Esperando "
            if linea.find('"') != -1: 
              self.estado = 3
              linea = linea[1:]
              continue  
            else:
              print 'Error de formato'
              linea = ""
              self.estado = 0
         elif self.estado == 3: # Conseguir "<flags>[:int]"
            if linea.find('"') != -1:
               linea = linea[:linea.find('"')]
               if linea.find(':') != -1:
                  self.tmp = linea.split(':')
                  self.buffer_flags = self.tmp[0]
                  self.buffer_immunity = self.tmp[1]
                  #linea = ""
                  #self.estado = 0
                  #continue
               else:
                  self.buffer_flags = linea
               self.admins.append([self.buffer_steamid, self.buffer_flags, self.buffer_immunity])
               linea = ""
               self.estado = 0
               continue  

adminparser = Admins_Simple('admins_simple.ini')
admins = adminparser.admins
print '[PARSER] Se han encontrado %d admins' % (len(admins))
for admin in admins:
   print '====='
   print '  STEAMID:', admin[0]
   print '    FLAGS:', admin[1]
   print ' IMMUNITY:', admin[2]
print '====='

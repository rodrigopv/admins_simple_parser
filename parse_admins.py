#!/usr/bin/python
file = open('admins_simple.ini');
admins = []
buffer_steamid = ""
buffer_flags = ""
buffer_immunity = 0
# 0 = Esperando " o //
estado = 0 
for linea in file:
   buffer_steamid = ""
   buffer_flags = ""
   buffer_immunity = 0


   while len(linea) > 0:
     if estado == 0 or estado == 2:
        linea = linea.strip()
     if estado == 0: 
        if linea.find('//') == 0:
          # print 'Comentario: ', linea
	  linea = ""	  
          continue
        elif linea.find('"') == 0:
          estado = 1
          linea = linea[1:]
     elif estado == 1: # Esperando " o strings
        if linea.find('"') != -1:
          # print 'STEAMID:', linea[:linea.find('"')]
          buffer_steamid = linea[:linea.find('"')]
          estado = 2
          linea = linea[linea.find('"')+1:]
          continue
        else:
          print 'Error de formato'
          estado = 0
          linea = ""
     elif estado == 2: # Esperando "
        if linea.find('"') != -1: 
          estado = 3
          linea = linea[1:]
          continue  
        else:
          print 'Error de formato'
          linea = ""
          estado = 0
     elif estado == 3: # Conseguir "<flags>[:int]"
        if linea.find('"') != -1:
           linea = linea[:linea.find('"')]
           if linea.find(':') != -1:
              tmp = linea.split(':')
              buffer_flags = tmp[0]
              buffer_immunity = tmp[1]
              #linea = ""
              #estado = 0
              #continue
           else:
              buffer_flags = linea
           admins.append([buffer_steamid, buffer_flags, buffer_immunity])
           linea = ""
           estado = 0
           continue  
print '[PARSER] Se han encontrado %d admins' % (len(admins))
for admin in admins:
   print '====='
   print '  STEAMID:', admin[0]
   print '    FLAGS:', admin[1]
   print ' IMMUNITY:', admin[2]
print '====='

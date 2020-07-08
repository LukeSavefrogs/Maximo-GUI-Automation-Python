from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import maximo_gui_connector as MGC
import json

def getCredentials ():	
	"""
	Gets the credentials from a local json

	Returns:
		tuple: contains USERNAME and PASSWORD
	"""
	with open('maximo_credentials.json') as f:
		data = json.load(f)

	return (data["USERNAME"], data["PASSWORD"])


if __name__ == "__main__":
	try:
		# Get credentials
		USERNAME, PASSWORD = getCredentials()

		maximo = MGC.MaximoAutomation({ "debug": True, "headless": False })

		browser = maximo.driver
	
		maximo.login(USERNAME, PASSWORD)

		# maximo.goto_section("Activities and Tasks")
		maximo.goto_section("Changes")
		
		# maximo.quickSearch("CH1665157")

		# maximo.setFilters({ "Change Num.": "CH1670157" })

		maximo.setFilters({ "status": "=REVIEW", "owner group": "V-OST-IT-SYO-OPS-TRENITALIA_ICTSM" })
		records = maximo.getAllRecordsFromTable()

		# print(json.dumps(records, sort_keys=True, indent=4))

		changes = [ record["data"]["change"]["value"] for record in records ]

		for index, change in enumerate(changes):
			maximo.quickSearch(change)
			browser.find_element_by_link_text("Details & Closure").click()
			maximo.waitUntilReady()

			browser.find_element_by_id("m8e32699b-tb").send_keys("COMPLETE")
			browser.find_element_by_id("m8e32699b-tb").send_keys(Keys.TAB)
			
			maximo.waitUntilReady()

			browser.find_element_by_link_text("Change Status/Group/Owner (MP)").click()
			maximo.waitUntilReady()

			browser.find_element_by_id("m67b8314e-tb").send_keys("CLOSE")
			browser.find_element_by_id("m67b8314e-tb").send_keys(Keys.TAB)
			maximo.waitUntilReady()

			# Click on "Route Workflow"
			browser.find_element_by_id("m24bf0ed1-pb").click()
			maximo.waitUntilReady()
			
			# Click on "Close Window" to close the dialog
			browser.find_element_by_id("mbdb65f6b-pb").click()
			maximo.waitUntilReady()


			print(f"[DEBUG] - Chiuso change: {change} (" + str(index + 1) + " of " + str(len(changes)) + ")")
			break

		print(changes)
		
		if maximo.debug: input("Premi per eseguire il logout")

		maximo.logout()
	
	except Exception as e:
		print(e)

	finally:
		print()
		input("Premi un tasto per terminare il programma")

		maximo.close()
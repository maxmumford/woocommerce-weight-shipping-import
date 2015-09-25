import time
import urlparse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from RuleUploader import RuleUploader

class SeleniumUploader(RuleUploader):
	def __init__(self, domain, username, password):
		""" set up browser and login """
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(4)
		self.domain = domain

		self.driver.get(self.domain + "/wp-login.php")
		log = self.driver.find_element_by_name("log")
		log.send_keys(username)
		pwd = self.driver.find_element_by_name("pwd")
		pwd.send_keys(password)
		pwd.send_keys(Keys.RETURN)
		time.sleep(4)

	def upload(self, name, title, min_price, max_price, min_weight, max_weight, countries):
		""" Create a rule using selenium """
		# open new rule page
		self.driver.get(self.domain + "/wp-admin/admin.php?page=wc-settings&tab=shipping&section=WC_Weight_Based_Shipping")
		new_link = self.driver.find_element_by_css_selector('.add-new-h2')
		new_link.click()
		time.sleep(4)

		# get form fields
		parsed = urlparse.urlparse(self.driver.current_url)
		wbs_profile = urlparse.parse_qs(parsed.query)['wbs_profile'][0]

		fields = ['enabled', 'name', 'title', 'availability', 'tax_status', 'min_price', 'max_price', 'min_weight', 'max_weight']
		form_elements = {}
		for field in fields:
			form_elements[field] = self.driver.find_element_by_name('woocommerce_WC_Weight_Based_Shipping_%s_%s' % (wbs_profile, field))

		# fill in the form
		form_elements['enabled'].click()

		form_elements['name'].clear()
		form_elements['name'].send_keys(name)

		form_elements['title'].clear()
		form_elements['title'].send_keys(title)

		form_elements['min_price'].clear()
		form_elements['min_price'].send_keys(min_price)

		form_elements['max_price'].clear()
		form_elements['max_price'].send_keys(max_price)

		form_elements['min_weight'].clear()
		form_elements['min_weight'].send_keys(min_weight)

		form_elements['max_weight'].clear()
		form_elements['max_weight'].send_keys(max_weight)

		for option in form_elements['availability'].find_elements_by_tag_name('option'):
		    if option.text == 'Specific countries':
		        option.click()
		        break

		for option in form_elements['tax_status'].find_elements_by_tag_name('option'):
		    if option.text == 'None':
		        option.click()
		        break

		country_codes_serialized = '['
		for country_code in countries.values():
			country_codes_serialized = country_codes_serialized + "'%s', " % country_code
		country_codes_serialized = country_codes_serialized + ']'
		script = "jQuery('#woocommerce_WC_Weight_Based_Shipping_%s_countries').select2('val', %s)" % (wbs_profile, country_codes_serialized)
		self.driver.execute_script(script)

		# save rule
		save_button = self.driver.find_element_by_name('save')
		save_button.click()

	def done(self):
		self.driver.close()

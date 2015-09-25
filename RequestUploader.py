import sys
import time
import requests

from RuleUploader import RuleUploader

class RequestUploader(RuleUploader):
	"""
	Insert into db by posting admin form.
	This is a work in progress, currently not working, probably due to header issues
	"""
	def __init__(self, domain, username, password):
		raise Exception("This is a work in progress, please see the class comments...")
		self.domain = domain
		self.username = username
		self.password = password

		# login
		self.session = requests.self.session()
		login_respose = self.session.post(self.domain + '/wp-login.php', {'log': self.username, 'pwd': self.password}, verify=False)
		if 'The password you entered' in login_respose.content:
			raise Exception('Login failed')

	def upload(self, name, title, min_price, max_price, min_weight, max_weight, countries):
		timestamp = str(time.time()).split('.')[0]
		headers = {
			'Origin': self.domain,
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'en-GB,en;q=0.8,fr;q=0.6',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36',
			'Content-Type': 'multipart/form-data;',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Cache-Control': 'max-age=0',
			'Referer': self.domain + '/wp-admin/admin.php?page=wc-settings&tab=shipping&section=WC_Weight_Based_Shipping&wbs_profile=%s' % timestamp,
			'Connection': 'keep-alive',
			'DNT': '1'
		}

		# prepare
		prepare_response = self.session.post(self.domain + '/wp-admin/admin.php?page=wc-settings&tab=shipping&section=WC_Weight_Based_Shipping&wbs_profile=%s' % timestamp, verify=False)
		if 'Action failed' in prepare_response.content:
			raise Exception('Prepare failed')

		# make post data
		data = {
			"woocommerce_WC_Weight_Based_Shipping_%s_enabled" % timestamp: "1",
			"woocommerce_WC_Weight_Based_Shipping_%s_name" % timestamp: name,
			"woocommerce_WC_Weight_Based_Shipping_%s_title" % timestamp: title,
			"woocommerce_WC_Weight_Based_Shipping_%s_availability" % timestamp: "specific",
			"woocommerce_WC_Weight_Based_Shipping_%s_countries[ % timestamp]": "DZ", # TODO: won't work with dict
			"woocommerce_WC_Weight_Based_Shipping_%s_countries[ % timestamp]": "AD",
			"woocommerce_WC_Weight_Based_Shipping_%s_countries[ % timestamp]": "AI",
			"woocommerce_WC_Weight_Based_Shipping_%s_tax_status" % timestamp: "none",
			"woocommerce_WC_Weight_Based_Shipping_%s_fee" % timestamp: "0",
			"woocommerce_WC_Weight_Based_Shipping_%s_rate" % timestamp: "0",
			"woocommerce_WC_Weight_Based_Shipping_%s_min_price" % timestamp: min_price,
			"woocommerce_WC_Weight_Based_Shipping_%s_max_price" % timestamp: max_price,
			"woocommerce_WC_Weight_Based_Shipping_%s_extra_weight_only" % timestamp: "1",
			"woocommerce_WC_Weight_Based_Shipping_%s_weight_step" % timestamp: "0",
			"woocommerce_WC_Weight_Based_Shipping_%s_min_weight" % timestamp: min_weight,
			"woocommerce_WC_Weight_Based_Shipping_%s_max_weight" % timestamp: max_weight,
			"woocommerce_WC_Weight_Based_Shipping_%s_min_subtotal" % timestamp: "0",
			"woocommerce_WC_Weight_Based_Shipping_%s_max_subtotal" % timestamp: "0",
			"save": "Save changes",
			"subtab": "",
			"_wpnonce": "2ce7c80a2f",
			"_wp_http_referer": "/wp-admin/admin.php?page=wc-settings&tab=shipping&section=WC_Weight_Based_Shipping&wbs_profile=%s" % timestamp,
		}
		
		# insert
		insert_response = self.session.post(self.domain + "/wp-admin/admin.php?page=wc-settings&tab=shipping&section=WC_Weight_Based_Shipping&wbs_profile=%s" % timestamp, data, verify=False)
		if 'Action failed' in insert_response.content:
			raise Exception('Insert failed')

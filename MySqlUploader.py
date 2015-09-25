import MySQLdb

class MySqlUploader(RuleUploader):
	""" 
	Inserts rules directly into the wp_options table.
	This is a work in progress due to serialization issues. 
	The rules are created but when loaded by wp, all fields are blank.
	"""

	def __init__(self, host, database_name, username, password, table_prefix):
		raise Exception("This is a work in progress. See comments for the MySqlUploader class...")
		self.host = host
		self.database_name = database_name
		self.username = username
		self.password = password
		self.table_prefix = table_prefix

		# connect to db
        self.db = MySQLdb.connect(host=self.host, user=self.username, passwd=self.password, db=self.database_name) 
		self.cur = self.db.cursor()

	def upload(self, name, title, min_price, max_price, min_weight, max_weight, countries):
		# construct serialized list of country codes
        country_codes_serialized = '{'
        country_code_number = 0
        for country_code in countries.values():
            country_codes_serialized = country_codes_serialized + 'i:%(number)s;s:2:"%(code)s";' % \
                                                                        {'number': country_code_number, 'code': country_code}
            country_code_number = country_code_number + 1
        country_codes_serialized = country_codes_serialized + '}'

        shipping_rule_serialized_vars = {
            "name": name,
            "name_length": len(name),
            "title": title,
            "title_length": len(title),
            "min_price": min_price,
            "max_price": max_price,
            "min_weight": min_weight,
            "max_weight": max_weight,
            "country_count": len(countries),
            "country_codes_serialized": country_codes_serialized,
        }

        # create serialized rule
        shipping_rule_serialized = ("""
			a:18:{
			s:7:"enabled";s:3:"yes";
			s:4:"name";s:%(name_length)s:"%(name)s";
			s:5:"title";s:%(title_length)s:"%(title)s";
			s:12:"availability";s:8:"specific";
			s:9:"countries";a:%(country_count)s:%(country_codes_serialized)s
			s:10:"tax_status";s:4:"none";
			s:3:"fee";i:0;
			s:4:"rate";i:0;
			s:9:"min_price";d:%(price)s;
			s:9:"max_price";d:%(price)s;
			s:17:"extra_weight_only";s:2:"no";
			s:11:"weight_step";i:0;
			s:10:"min_weight";d:%(min_weight)s;
			s:10:"max_weight";d:%(max_weight)s;
			s:12:"min_subtotal";i:0;
			s:12:"max_subtotal";i:0;
			s:17:"subtotal_with_tax";s:2:"no";
			s:24:"shipping_class_overrides";O:31:"WBS_Shipping_Class_Override_Set":1:{s:42:"WBS_Shipping_Class_Override_Setoverrides";a:0:{}}
			}""" % shipping_rule_serialized_vars).strip().replace('\n', '').replace('\r', '')

        shipping_rule_name = "woocommerce_WC_Weight_Based_Shipping_%s_settings" % str(time.time()).split('.')[0]

        # insert into db
	    options_table_name = self.table_prefix + 'options'
		    query = "INSERT INTO %(options_table_name)s (option_name, option_value, autoload) VALUES ('%(rule_name)s', '%(rule_serialized)s', 'yes');" % \
		                    {'options_table_name': options_table_name, "rule_name": shipping_rule_name, "rule_serialized": shipping_rule_serialized}
		    cur.execute(query)

		db.commit()

	def done(self):
		pass

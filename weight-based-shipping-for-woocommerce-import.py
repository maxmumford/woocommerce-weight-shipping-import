import argparse
import csv
import random
import MySQLdb
import os

from fedex_country_codes import FEDEX_COUNTRY_CODES

from RuleGenerator import RuleGenerator
from SeleniumUploader import SeleniumUploader

################## arguments
parser = argparse.ArgumentParser()

# selenium details
parser.add_argument('domain', metavar='domain', type=str, help='Wordpress domain name')
parser.add_argument('username', metavar='username', type=str, help='Selenium username')
parser.add_argument('password', metavar='password', type=str, help='Selenium password')

# csvs
parser.add_argument('rates_csv', metavar='rates_csv', type=str, help='The path of the rates csv file')
parser.add_argument('zones_csv', metavar='zones_csv', type=str, help='The path of the zones csv file')

# shipping
parser.add_argument('shipping_type', metavar='shipping_type', type=str, help='The name of the postage type, for example "Fedex International Priority"')
parser.add_argument('title', metavar='title', type=str, help='The shipping method title that will be visible to the user on the checkout page')

parser.add_argument('--log_file', metavar='log_file', type=str, help='Log file for uploaded rule ids', default='uploaded_rule_ids.txt')

arguments = parser.parse_args()

################## make rules
# generate
rule_generator = RuleGenerator(arguments.zones_csv, arguments.rates_csv, arguments.shipping_type, arguments.title)
rules = rule_generator.generate()

# prepare log files
def append_uploaded_rule_ids(uploaded_rule_ids):
    if not isinstance(uploaded_rule_ids, list):
        raise TypeError()
    log = open(arguments.log_file, 'a')
    log.writelines([rule + '\n' for rule in uploaded_rule_ids])
    log.close()

def get_uploaded_rule_ids():
    log = open(arguments.log_file, 'r')
    return [line.replace('\n', '') for line in log.readlines()]

if not os.path.exists(arguments.log_file):
    log = open(arguments.log_file, 'w')
    log.write('')
    log.close()

# prepare uploader
selenium_uploader = SeleniumUploader(arguments.domain, arguments.username, arguments.password)

# start uploading
for rule_number in range(0, len(rules)):
    rule = rules[rule_number]
    rule_id = rule.pop('id')

    # skip rules whose ids are in previously_uploaded_rule_ids
    if rule_id in get_uploaded_rule_ids():
        print 'Skipping rule: ' + rule_id
        continue

    try:
        selenium_uploader.upload(**rule)
    except Exception as e:
        print 'Could not upload rule: ' + rule_id
        raise e
    else:
        append_uploaded_rule_ids([rule_id])
        print 'Imported rule %s of %s' % (rule_number, len(rules))

selenium_uploader.done()

# feedback
print "Imported %s rules" % rule_number

#!/usr/bin/python3
import sys
import re
import unicodedata
import string
import fcntl

trans ={
'\x85'	:	'...',	# HORIZONTAL ELLIPSIS
'\x88'	:	'^'	,# MODIFIER LETTER CIRCUMFLEX ACCENT
'\x8A'	:	'S'	,# LATIN CAPITAL LETTER S WITH CARON
'\x8C'	:	'OE',	# LATIN CAPITAL LIGATURE OE

'\x96':	'-',	# EN DASH
'\x97':		'-',	# EM DASH
'\x99':		'_tm_',	# TRADE MARK SIGN
'\x9A':		's',	# LATIN SMALL LETTER S WITH CARON
'\x9C':		'oe',	# LATIN SMALL LIGATURE OE
'\x9F':		'Y',	# LATIN CAPITAL LETTER Y WITH DIAERESIS
'\xA2':		'_cent_',
'\xA3':		'_pound_',
'\xA5':		'_yen_',
'\xA9':		'_copy_',
'\xAE':		'_reg_',

'\xB2':		'2',
'\xB3':		'3',
'\xB5':		'b',
'\xB6':		'_pp_',
'\xB9':		'1',
'\xC0':		'A',	# LATIN CAPITAL LETTER A WITH GRAVE
'\xC1':		'A',	# LATIN CAPITAL LETTER A WITH ACUTE
'\xC2':		'A',	# LATIN CAPITAL LETTER A WITH CIRCUMFLEX
'\xC3':		'A',	# LATIN CAPITAL LETTER A WITH TILDE
'\xC4':		'A',	# LATIN CAPITAL LETTER A WITH DIAERESIS
'\xC5':		'A',	# LATIN CAPITAL LETTER A WITH RING ABOVE
'\xC6':		'AE',	# LATIN CAPITAL LETTER AE
'\xC7':		'C',	# LATIN CAPITAL LETTER C WITH CEDILLA
'\xC8':		'E',	# LATIN CAPITAL LETTER E WITH GRAVE
'\xC9':		'E',	# LATIN CAPITAL LETTER E WITH ACUTE
'\xCA':		'E',	# LATIN CAPITAL LETTER E WITH CIRCUMFLEX
'\xCB':		'E',	# LATIN CAPITAL LETTER E WITH DIAERESIS
'\xCC':		'I',	# LATIN CAPITAL LETTER I WITH GRAVE
'\xCD':		'I',	# LATIN CAPITAL LETTER I WITH ACUTE
'\xCE':		'I',	# LATIN CAPITAL LETTER I WITH CIRCUMFLEX
'\xCF':		'I',	# LATIN CAPITAL LETTER I WITH DIAERESIS

'\xD0':		'TH',	# LATIN CAPITAL LETTER ETH (Icelandic)
'\xD1':		'N',	# LATIN CAPITAL LETTER N WITH TILDE
'\xD2':		'O',	# LATIN CAPITAL LETTER O WITH GRAVE
'\xD3':		'O',	# LATIN CAPITAL LETTER O WITH ACUTE
'\xD4':		'O',	# LATIN CAPITAL LETTER O WITH CIRCUMFLEX
'\xD5':		'O',	# LATIN CAPITAL LETTER O WITH TILDE
'\xD6':		'O',	# LATIN CAPITAL LETTER O WITH DIAERESIS
'\xD7':		'x',	# MULTIPLICATION SIGN
'\xD8':		'O',	# LATIN CAPITAL LETTER O WITH STROKE
'\xD9':		'U',	# LATIN CAPITAL LETTER U WITH GRAVE
'\xDA':		'U',	# LATIN CAPITAL LETTER U WITH ACUTE
'\xDB':		'U',	# LATIN CAPITAL LETTER U WITH CIRCUMFLEX
'\xDC':		'U',	# LATIN CAPITAL LETTER U WITH DIAERESIS
'\xDD':		'Y',	# LATIN CAPITAL LETTER Y WITH ACUTE
'\xDE':		'TH',	# LATIN CAPITAL LETTER THORN (Icelandic)
'\xDF':		'ss',	# LATIN SMALL LETTER SHARP S (German)

'\xE0'	:	'a'	,# LATIN SMALL LETTER A WITH GRAVE
'\xE1'	:	'a'	,# LATIN SMALL LETTER A WITH ACUTE
'\xE2'	:	'a'	,# LATIN SMALL LETTER A WITH CIRCUMFLEX
'\xE3'	:	'a'	,# LATIN SMALL LETTER A WITH TILDE
'\xE4'	:	'a'	,# LATIN SMALL LETTER A WITH DIAERESIS
'\xE5'	:	'a'	,# LATIN SMALL LETTER A WITH RING ABOVE
'\xE6'	:	'ae',	# LATIN SMALL LETTER AE
'\xE7'	:	'c'	,# LATIN SMALL LETTER C WITH CEDILLA
'\xE8'	:	'e'	,# LATIN SMALL LETTER E WITH GRAVE
'\xE9'	:	'e'	,# LATIN SMALL LETTER E WITH ACUTE
'\xEA'	:	'e'	,# LATIN SMALL LETTER E WITH CIRCUMFLEX
'\xEB'	:	'e'	,# LATIN SMALL LETTER E WITH DIAERESIS
'\xEC'	:	'i'	,# LATIN SMALL LETTER I WITH GRAVE
'\xED'	:	'i'	,# LATIN SMALL LETTER I WITH ACUTE
'\xEE'	:	'i'	,# LATIN SMALL LETTER I WITH CIRCUMFLEX
'\xEF'	:	'i'	,# LATIN SMALL LETTER I WITH DIAERESIS
'\xF0'	:		'th',	# LATIN SMALL LETTER ETH (Icelandic)
'\xF1'	:		'n'	,# LATIN SMALL LETTER N WITH TILDE
'\xF2'	:		'o'	,# LATIN SMALL LETTER O WITH GRAVE
'\xF3'	:		'o'	,# LATIN SMALL LETTER O WITH ACUTE
'\xF4'	:		'o'	,# LATIN SMALL LETTER O WITH CIRCUMFLEX
'\xF5'	:		'o'	,# LATIN SMALL LETTER O WITH TILDE
'\xF6'	:		'o'	,# LATIN SMALL LETTER O WITH DIAERESIS
'\xF8'	:		'o'	,# LATIN SMALL LETTER O WITH STROKE
'\xF9'	:		'u'	,# LATIN SMALL LETTER U WITH GRAVE
'\xFA'	:		'u'	,# LATIN SMALL LETTER U WITH ACUTE
'\xFB'	:		'u'	,# LATIN SMALL LETTER U WITH CIRCUMFLEX
'\xFC'	:		'u'	,# LATIN SMALL LETTER U WITH DIAERESIS
'\xFD'	:		'y'	,# LATIN SMALL LETTER Y WITH ACUTE
'\xFE'	:		'th',	# LATIN SMALL LETTER THORN (Icelandic)
'\xFF'	:		'y',	# LATIN SMALL LETTER Y WITH DIAERESIS
'\xC4'	:		'AE',	# LATIN CAPITAL LETTER A WITH UMLAUT
'\xD6'	:		'OE',	# LATIN CAPITAL LETTER O WITH UMLAUT
'\xDC'	:		'UE',	# LATIN CAPITAL LETTER U WITH UMLAUT

'\xE4'	:		'ae',	# LATIN SMALL LETTER A WITH UMLAUT
'\xF6'	:		'oe',	# LATIN SMALL LETTER O WITH UMLAUT
'\xFC'	:		'ue',	# LATIN SMALL LETTER U WITH UMLAUT
'\x26':		'_and_'	# &
}

def log_input(s):
    with open('/home/phil/dev/mung.log','a') as g:
        fcntl.flock(g,fcntl.LOCK_EX)
        g.write(s)
        fcntl.flock(g,fcntl.LOCK_UN)

def sub_to_ascii(s):
    """used LUT to translate as many characters to safe characters as possible ie é becomes e"""
    for key, val in trans.items():
        s = s.replace(key, val)
    #this replates part of above, I should perhaps trim the custom dict
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode()
    valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in s if c in valid_filename_chars)
    #remove spaces
    cleaned_filename=str(cleaned_filename).strip().replace(' ', '_')
    return cleaned_filename


in_string = sys.stdin.readline()
#log_input(in_string)
split_string = in_string.split(' ', 1)
disc_id = split_string[0]
dirty_name = split_string[1]
clean_name = sub_to_ascii(dirty_name)
#handle the unknown album problem by appending the disc id
clean_name = clean_name.replace('Unknown_Album', 'Unknown_Album_'+disc_id+"/")
print(clean_name)


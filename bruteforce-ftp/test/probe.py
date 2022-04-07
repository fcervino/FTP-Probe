from driver import Driver
import subprocess
import ftplib
		
validi = []
#L'array validi contiene le eventuali credenziali valide trovate, non sapevo bene però
#come e se aggiungerlo nel json di output, nel dubbio ho provato a dichiararlo come "globale"

RESULT_MAP = {
    0: {
        'Extradata': {
            'Key': 'Has vulnerable credentials',
            'Value': False,
	    'Credentials' : ''
        },
        'Result': True
    },
    1: {
        'Extradata': {
            'Key': 'ERROR',
            'Value': 'Check if the host is up and contact Moon Cloud admin',
	    'Credentials' : ''
        },
        'Result': False
    },
    2: {
        'Extradata': {
            'Key': 'Has vulnerable credentials',
            'Value': True,
	    'Credentials' : validi[]
        },
        'Result': False
    },
    3: {
        'Extradata': {
            'Key': 'Has fail2ban implemented',
            'Value': True,
	    'Credentials' : ''
        },
        'Result': False
    }
}


class Probe(Driver):

	def brute(host, user, passwd):
		debole = 0
		noban = True
		with open(user, 'r') as fu:
			with open(passwd, 'r') as fp:
				for uline in fu.read().splitlines():
					for pline in fp.read().splitlines():
						if noban:
							uname = uline.strip('\n')
							pwd = pline.strip('\n')
							try:
								ftp.connect(host)
								ftp.login(uname, pwd)
								validi.append(uname + ':' + pwd)
								debole = True
								ftp.quit()
							except ftplib.all_errors:
								noban = False
		if noban == False:
			return 3
		if debole == True:
			for item in validi:
				print (item)
		else:
			return 0
		return 2

	def raggiungi(host):
		try:
			ftp.connect(host)
			return 0
		except ftplib.all_errors:
			return 1

    def check_input(self, inputs=None):
        config = self.testinstances.get('config')
        assert config is not None
        host = config.get('host')
        return host

    @staticmethod
    def execute(inputs):
        assert isinstance(inputs, tuple)
        host = inputs[0]
        if(raggiungi(host)==0):
            return brute(host, 'usernames.txt', 'pwdlist.txt')
        else:
            return 1

    def parse(self, inputs=int):
        assert isinstance(inputs, int)
        return_code = inputs
        result_obj = RESULT_MAP.get(return_code)
        if result_obj is not None:
            self.result.put_value(result_obj['Extradata']['Key']['Credentials'], result_obj['Extradata']['Value']['Credentials'])
            return result_obj['Result']
        else:
            self.result.put_value('Error', 'Fail to get the result. Contact Moon Cloud admin')
            return False

    def rollback(self, inputs=None):
        self.result.put_value('ERROR', 'Contact Moon Cloud admin')
        return False

    def appendAtomics(self):
        self.appendAtomic(self.check_input, self.rollback)
        self.appendAtomic(self.execute, self.rollback)
        self.appendAtomic(self.parse, self.rollback)

from driver import Driver
import subprocess
import ftplib

RESULT_MAP = {
    0: {
        'Extradata': {
            'Key': 'Is vulnerable to anonymous login',
            'Value': False
        },
        'Result': True
    },
    1: {
        'Extradata': {
            'Key': 'ERROR',
            'Value': 'Check if the host is up and contact Moon Cloud admin'
        },
        'Result': False
    },
    2: {
        'Extradata': {
            'Key': 'Is vulnerable to anonymous login',
            'Value': True
        },
        'Result': False
    }
}


class Probe(Driver):

    def raggiungi(host):
        try:
            ftp.connect(host)
            return 0
        except ftplib.all_errors:
            return 1
        
    def login():
        try:
            ftp.login('ftp', 'anonymous')
            ftp.quit()
            return 2
        except ftplib.all_errors:
            return 0

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
            return login()
        else:
            return 1

    def parse(self, inputs=int):
        assert isinstance(inputs, int)
        return_code = inputs
        result_obj = RESULT_MAP.get(return_code)
        if result_obj is not None:
            self.result.put_value(result_obj['Extradata']['Key'], result_obj['Extradata']['Value'])
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

class helper():
    def __init__(self):
        self.commands = []
        self.parms = []
        self.descriptions = []
    
    def add(self, command, parm, description):
        self.commands.append(command)
        self.parms.append(parm)
        self.descriptions.append(description)

    def compose(self, command, parm, description):
        '''
        Compoose command, parm, and description to a readable format
        '''
        c1 = f'!{command}'
        c2 = f'`{parm}`'
        return f'{c1} {c2}' + '\n' + description
    
    def response(self):
        res = []
        for c, p, d in zip(self.commands, self.parms, self.descriptions):
            res.append(self.compose(c, p, d))
        return '\n\n'.join(res)
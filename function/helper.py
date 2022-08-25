class helper():
    def __init__(self):
        self.commands = []
        self.descriptions = []
    
    def add(self, command, description):
        self.commands.append(command)
        self.descriptions.append(description)

    def compose(self, command, description):
        '''
        Compoose command and description to a readable format
        '''
        return f'`!{command}`' + '\n' + description
    
    def response(self):
        res = []
        for c, d in zip(self.commands, self.descriptions):
            res.append(self.compose(c, d))
        return '\n\n'.join(res)
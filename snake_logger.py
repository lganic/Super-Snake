import time

class Log_Stream:
    def __init__(self):
        self.file_name = f'log-{str(int(time.time()))}.txt'
        self.file_obj = open(self.file_name, 'w')
    
    def close(self):
        self.file_obj.close()
    
    def log_new_apple_pos(self, position):
        log_out = f'APPLE: {position}'

        print(log_out)

        self.file_obj.write(log_out + '\n')  # Ensure proper line formatting in the log file
    
    def log_new_snake_pos(self, snake):
        log_out = f'SNAKE: {snake}'

        print(log_out)

        self.file_obj.write(log_out + '\n')
    
    def log_new_hamilton(self, hamilton):
        log_out = f'HAMIL: {hamilton}'

        print(log_out)

        self.file_obj.write(log_out + '\n')

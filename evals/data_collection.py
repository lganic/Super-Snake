class Length_Tracker:
    def __init__(self):
        self.records = []

    def add(self, current_path):
        self.records.append(len(current_path))

class All_Tracker:
    def __init__(self):
        self.all_records = []

    def add_record(self, record):
        self.all_records.append(record.copy())
    
    def avg_track(self):
        max_len = 0
        for record in self.all_records:
            if len(record) > max_len:
                max_len = len(record)
        
        k = [0] * max_len

        for index in range(max_len):
            sample_count = 0

            for record in self.all_records:
                
                if len(record) <= index:
                    continue

                sample_count += 1
                k[index] += record[index]
            
            if sample_count == 0:
                continue # Shouldn't be possible, but whatever

            k[index] /= sample_count
        
        return k

    def max_lengths(self):
        return [k[-1] for k in self.all_records]
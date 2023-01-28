import event

# read from file to load all data

class Board():
    def __init__(self) -> None:
        self.jobs = None
        self.investments = None
        self.events = None
        self.special_events = None
        self.misfortunes = None
        self.love_interests = None
        
    def match_jobs(self, education):
        matched_jobs = []
        for job in self.jobs:
            if job.is_qualified(education):
                matched_jobs.append(job)
        
        return matched_jobs
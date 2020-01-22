import pysubs2
import tinysegmenter

class Subtitles:

    def __init__(self, file):
        self.subs = pysubs2.load(file)
    
    def __len__(self):
        return len(self.subs)
    
    def __getitem__(self, i):
        return self.subs[i]

    def nextSubtitleAt(self, time):
        """ Finds the next appropriate subtitle to display along with its index if any, otherwise returns None """
        start,end=0,len(self.subs)-1
        while start <= end:
            midpt = (start + end)//2
            sub = self.subs[midpt]
            if time >= sub.start and time <= sub.end:
                return sub,midpt
            elif time < sub.start:
                start,end = start,midpt-1
            else:
                start,end = midpt+1,end
        return None,-1

    # def nextSubtitleAt(self, time, index):
    
    

    


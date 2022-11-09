import itertools as  its

class busyAnimations:
    dots = ["•...", ".•..", "..•.", "...•"]
    bar = ["=   ", " =  ", "  = ", "   ="]
    short_arrow = [">   ", " >  ", "  > ", "   >"]
    arrow = ["->  ", " -> ", "  ->", ">  -"]
    
    anim_dict = {
        "dots" : dots,
        "bar" : bar,
        "short_arrow" : short_arrow,
        "arrow" : arrow,
    }
    
    @staticmethod
    def get_iter_from_name(name):
        return its.cycle(busyAnimations.anim_dict[name])
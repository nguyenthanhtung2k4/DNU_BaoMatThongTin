import  hashlib 

def file(path_file):
    with open (path_file,'r+',  encoding='utf-8') as  f:
        for i  in f:
            return  i;
def  hash(path_file):
    f1=file(path_file);
    return hashlib.md5(f1.encode()).hexdigest()

def compare(f1,f2):
        return True if hash(f1) ==hash(f2) else False
    
    
if __name__=="__main__":
    file1='Class/Hash/f1.txt'
    file2='Class/Hash/f2.txt'
    print(compare(file1,file2))
    
    
    
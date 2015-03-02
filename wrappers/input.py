import sys

def print_output(filepath):
    f=open(filepath,'r')
    lines=f.readlines()
    f.close()
    print(lines[0].strip(),end='\n')
    lines=lines[1:]
    lines_out=[]
    #read input and print input
    for l in lines:
        inp,out=l.strip().split('=')
        print(inp)
        lines_out.append(out)
    #write output to a file for use lateron
    f=open('temp_output_file','w')
    f.writelines('\n'.join(lines_out))
    f.close()
if __name__=='__main__':
    test_file_path=sys.argv[1]
    print_output(test_file_path)

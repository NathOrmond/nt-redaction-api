import os, sys

def get_file_contents(filename): 
  fd = os.open(filename, os.O_RDWR)
  ret = os.read(fd, os.path.getsize(filename))
  rval = ret.decode("utf-8")
  os.close(fd)
  return ret

get_file_contents
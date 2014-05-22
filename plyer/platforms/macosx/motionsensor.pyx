# distutils: language = c
# distutils: sources = unimotion.c

cdef extern from "unimotion.h":
	int detect_sms()
	int read_sms_scaled(int, int*, int*, int*)

def is_available():
	hardware = detect_sms()
	
	if hardware > 0:
		return True
	else:
		return False

def get_coord():
	hardware = detect_sms()

	cdef int x, y, z
	cdef int *_x = &x, *_y = &y, *_z = &z
	result = read_sms_scaled(hardware, _x, _y, _z)

	if (result < 1):
		return 0
	else:
		return (x, y, z)

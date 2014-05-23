/*
 *  UniMotion - Unified Motion detection for Apple portables.
 *
 *  Copyright (c) 2006 Lincoln Ramsay. All rights reserved.
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public
 *  License version 2.1 as published by the Free Software Foundation.
 *
 *  This library is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public
 *  License along with this library; if not, write to the Free Software
 *  Foundation Inc. 59 Temple Place, Suite 330, Boston MA 02111-1307 USA
 */
#ifndef UNIMOTION_H
#define UNIMOTION_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// The various SMS hardware that unimotion supports
enum sms_hardware {
    unknown = 0,
    powerbook = 1,
    ibook = 2,
    highrespb = 3,
    macbookpro = 4
};

// prototypes for the functions in unimotion.c

// returns the value of SMS hardware present or unknown if no hardware is
// detected
int detect_sms();

// use the value returned from detect_sms as the type
// don't call read_sms(detect_sms()...) as this will do extra work
// if you can't save the type between calls pass 0 as type to avoid extra work

// all functions return 1 on success and 0 on failure
// they modify x, y and z if they are not 0


//
// 0.3 functions
//

// raw, unmodified values
int read_sms_raw(int type, int *x, int *y, int *z);

// "calibrated" values (same as raw if no calibration data exists)
int read_sms(int type, int *x, int *y, int *z);
// real (1.0 = 1G) values (requires calibration data)
// note that this is the preferred API as it need not change with new machines
// if no "scale" calibration data exists defaults will be used based on the
// machine type
int read_sms_real(int type, double *x, double *y, double *z);


//
// 0.4 functions
//

// raw SMS data (useful for debugging)
// note that endian issues make reading the raw bytes non-trivial
// returns 0 or a pointer that should be released with free() when you are
// finished with it
// sets *size to the size of the structure returned if size is not 0
uint8_t *read_sms_raw_bytes(int type, int *size);

// scaled values, like real but easier to handle
// this reverses the backwards polarity of x and increases the range of the
// older machines to match the MacBook [Pro] sensor
int read_sms_scaled(int type, int *x, int *y, int *z);

#ifdef __cplusplus
}
#endif

#endif


#import <Foundation/Foundation.h>
#define MB (1024*1024)
#define GB (MB*1024)


@interface SizeClass: NSObject {
}
- (int) get_bit_size;
@end


@implementation SizeClass

- (int) get_bit_size {
    if (sizeof(void*) == 4) {
        return 32;
    }
    else if (sizeof(void*) == 8){
        return 64;
    }
}
@end


@interface StorageClass: NSObject {
}
- (double) get_total_space;
@end


@implementation StorageClass

- (double)memoryFormatter:(long long)diskSpace {
    double bytes = 1.0 * diskSpace;
    double megabytes = bytes / MB;
    double gigabytes = bytes / GB;
    return gigabytes;
}

- (double) get_total_space {
    long long space = [[[[NSFileManager defaultManager]
                     attributesOfFileSystemForPath:NSHomeDirectory() error:nil]
                     objectForKey:NSFileSystemSize] longLongValue];
    return [self memoryFormatter:space];
  }

@end

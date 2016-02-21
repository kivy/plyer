#import <Foundation/Foundation.h>
#import <CoreBluetooth/CoreBluetooth.h>

@interface CBAdvertisementDataKeys : NSObject
@end

@implementation CBAdvertisementDataKeys

+ (NSString*) getLocalName {
    return CBAdvertisementDataLocalNameKey;
}

+ (NSString*) getServiceUUIDs {
    return CBAdvertisementDataServiceUUIDsKey;
}

+ (NSString*) getManufacturerData {
    return CBAdvertisementDataManufacturerDataKey;
}

@end
